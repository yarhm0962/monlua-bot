"""Luraph v14.3 recovery driver.

Chains the research pipeline: extract + decode the LPH blob, deserialize the
bytecode with bias auto-detection, then build per-proto structure and emit a
structured listing. Raises a clear diagnostic when a stage cannot validate,
so callers report exactly which recovery step is still open.
"""
import importlib.util
import io
import os
import sys
import types

_PKG_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_flat():
    """Load the toolkit's flat modules (they import each other by bare name)."""
    saved = list(sys.path)
    sys.path.insert(0, _PKG_DIR)
    try:
        for name in ("proto_deserializer", "vm_opcode_table", "cfg_builder",
                     "expr_table", "structure_cfg", "batch_structure",
                     "luraph_decoder"):
            if name in sys.modules:
                continue
            path = os.path.join(_PKG_DIR, name + ".py")
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
        return {name: sys.modules[name] for name in
                ("proto_deserializer", "vm_opcode_table", "cfg_builder",
                 "expr_table", "structure_cfg", "batch_structure",
                 "luraph_decoder")}
    finally:
        del sys.path[0]


def _uleb(data, pos):
    result = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if b < 0x80:
            return result, pos
        shift += 7
        if shift > 70:
            raise ValueError("varint too long")


def _decode_blob(source_text, luraph_decoder):
    blob = luraph_decoder.extract_blob(source_text)
    if not blob:
        raise ValueError("no Luraph v14.3 encoded blob found in the source")
    decoded = luraph_decoder.decode_payload(blob)
    if not decoded:
        raise ValueError("the encoded blob did not decode")
    return decoded


def _guarded_proto_parse(data, deserializer_cls, op_bias, sp_bias, up_count):
    """Deserialize with a guarded jump table; return the proto or None."""
    import proto_deserializer as PD  # flat module loaded by _load_flat

    orig = PD.Deserializer._read_jump_table
    entries = []

    def patched(self):
        cnt = self.qp()
        if not (0 <= cnt <= 100000):
            raise ValueError("jump-table count out of range")
        for _ in range(cnt):
            w = self.qp()
            op = w // 2
            if w % 2:
                s_val = self.qp()
                end_idx = self.qp()
                if op > 10 ** 7 or s_val > 10 ** 7 or end_idx > 10 ** 7:
                    raise ValueError("jump-table entry out of range")
                entries.append((op, s_val, end_idx))
            else:
                if op > 10 ** 7:
                    raise ValueError("jump-table entry out of range")
                entries.append((op, None, op))
            if self.cur.pos > len(data):
                raise ValueError("jump-table overruns the blob")
        return entries

    PD.Deserializer._read_jump_table = patched
    try:
        ds = deserializer_cls(data, op_bias=op_bias, sp_bias=sp_bias)
        ds.read_constant_pool()
        up_raw = ds.qp()
        if up_raw - up_count != 0:
            return None
        return ds.read_proto(), ds.cur.pos, entries
    finally:
        PD.Deserializer._read_jump_table = orig


def _pool_walk(data, pos, count):
    """Walk `count` constant-pool entries, mirroring
    Deserializer.read_constant_pool byte-for-byte, and bail only on layouts
    that cannot be a real pool: a string longer than 64 KB or a string that
    is nearly all control bytes. Real Luraph strings may contain binary
    bytes, so this stays a loose filter. Returns the position after the
    pool, or None."""
    q = pos
    try:
        q += 1  # wrap byte after the count varint
        strings = 0
        for _ in range(count):
            tag = data[q]
            q += 1
            if tag > 0x22:
                n, q = _uleb(data, q)
                if n > 65536:
                    return None
                chunk = data[q:q + n]
                q += n
                if len(chunk) >= 8:
                    controls = sum(1 for b in chunk if b < 0x20 and b not in (9, 10, 13))
                    if controls * 2 > len(chunk):
                        return None
                strings += 1
            elif tag > 0x15:
                q += 8
            elif tag == 0x15:
                q += 1
            else:
                q += 8
            if q > len(data):
                return None
        if strings == 0:
            return None
        return q
    except IndexError:
        return None


def _pool_end_map(data, pool_start):
    """One incremental pool walk from pool_start; maps every reached entry
    boundary to the number of entries consumed. Only boundaries with at
    least one string qualify, matching _pool_walk's plausibility rules."""
    ends = {}
    q = pool_start + 1  # wrap byte
    strings = 0
    idx = 0
    try:
        while q < len(data):
            tag = data[q]
            q += 1
            if tag > 0x22:
                n, q = _uleb(data, q)
                if n > 65536:
                    break
                chunk = data[q:q + n]
                q += n
                if len(chunk) >= 8:
                    controls = sum(1 for b in chunk if b < 0x20 and b not in (9, 10, 13))
                    if controls * 2 > len(chunk):
                        break
                strings += 1
            elif tag > 0x15:
                q += 8
            elif tag == 0x15:
                q += 1
            else:
                q += 8
            idx += 1
            if strings:
                ends[q] = idx
    except IndexError:
        pass
    return ends


def _anchor_candidate(data, sp_bias):
    """Walk the pool for one sp_bias candidate and read the proto fields
    that follow it. Returns (sp_bias, up_raw, numparams, hc, insns_raw,
    insns_start) or None when the layout does not fit."""
    try:
        raw_sp, pool_start = _uleb(data, 0)
    except (IndexError, ValueError):
        return None
    count = raw_sp - sp_bias
    if count < 1 or count > 200000:
        return None
    pool_end = _pool_walk(data, pool_start, count)
    if pool_end is None:
        return None
    try:
        up_raw, p2 = _uleb(data, pool_end)
        numparams, p2 = _uleb(data, p2)
        hc, p2 = _uleb(data, p2)
        for _ in range(hc):
            _, p2 = _uleb(data, p2)
        insns_raw, p2 = _uleb(data, p2)
    except (IndexError, ValueError):
        return None
    if not (0 <= up_raw < 10 ** 7 and 0 <= numparams <= 255
            and 0 <= hc <= 65536 and insns_raw < 10 ** 7):
        return None
    return (sp_bias, up_raw, numparams, hc, insns_raw, p2)


def _scan_candidate(data, entry, budget):
    """Run the jump-table scan for one anchored candidate. Returns
    (strong, best, best_insn_bytes): strong is the accepted tuple on a
    high-coverage alignment, best the best low-coverage one so far."""
    import proto_deserializer as PD

    sp_bias, up_raw, numparams, hc, insns_raw, insns_start = entry
    max_insns = max(1, (len(data) - insns_start) // 4)
    max_insns = min(max_insns, 200000)

    budget[0] -= (len(data) - insns_start) + max_insns
    if budget[0] < 0:
        return None, None, 0

    # one pass over the stream: values and the byte offset after each uleb
    vals = []
    positions = [insns_start]
    q = insns_start
    try:
        # +2: the jump-table count varint sits one value past the last
        # instruction uleb and must be readable for the largest ic
        for _ in range(max_insns * 4 + 2):
            v, q = _uleb(data, q)
            vals.append(v)
            positions.append(q)
    except IndexError:
        pass

    def jt_ok(ic):
        """Plausibility of a jump table at the position after ic*4 ulebs."""
        if ic <= 0 or ic * 4 > len(vals):
            return None
        jt_pos = positions[ic * 4]
        try:
            cnt, r = _uleb(data, jt_pos)
        except IndexError:
            return None
        if not (0 < cnt <= ic):  # a jump table never exceeds the instruction count
            return None
        entries = []
        try:
            for _ in range(cnt):
                w, r = _uleb(data, r)
                op = w // 2
                if w % 2:
                    s_val, r = _uleb(data, r)
                    end_idx, r = _uleb(data, r)
                    if op > ic or s_val > ic or end_idx > ic or end_idx < op:
                        return None
                    entries.append((op, s_val, end_idx))
                else:
                    if op > ic:
                        return None
                    entries.append((op, None, op))
        except IndexError:
            return None
        return (insns_raw - ic, 1, ic, r, len(entries), entries)

    local_best = None
    local_score = -1.0
    local_bytes = 0
    for insns in range(1, max_insns + 1):
        # cheap prefilter: the uleb at the candidate jump-table position
        # must itself read as a plausible jump count within this proto
        if insns * 4 >= len(vals):
            break
        budget[0] -= 4
        if budget[0] < 0:
            break
        cnt_hint = vals[insns * 4]
        if cnt_hint <= 0 or cnt_hint > min(insns, 20000):
            continue
        found = jt_ok(insns)
        if not found:
            continue
        op_bias, _up, ic, _r, _n, entries = found
        if op_bias <= 0 or ic <= 0:
            continue  # the real bias constant is positive; rejects spurious alignments
        budget[0] -= 4 * insns  # a parse reads the whole proto stream
        if budget[0] < 0:
            break
        try:
            parsed = _guarded_proto_parse(data, PD.Deserializer, op_bias, sp_bias, up_raw)
        except Exception:
            continue
        if not parsed:
            continue
        proto, end_pos, entries2 = parsed
        if len(proto["opcodes"]) != ic:
            continue  # the proto must decode exactly ic instructions
        # quality bar: a genuine alignment keeps opcodes in byte range,
        # varies them, and resolves every constant reference it makes
        # inside the pool; spurious alignments do none of that
        ops = proto["opcodes"]
        if any(o is None or o > 255 for o in ops) or len(set(ops)) < 2:
            continue
        has_const = False
        unresolved = False
        for arr in (proto["operand_G"], proto["operand_l"], proto["operand_Hp"]):
            for v in arr:
                if isinstance(v, tuple):
                    if v[0] == "unresolved_const":
                        unresolved = True
                    else:
                        has_const = True
        if unresolved or not has_const:
            continue
        insn_bytes = positions[ic * 4] - insns_start
        score = insn_bytes / max(1, len(data))
        if score > local_score:
            local_score = score
            local_best = (sp_bias, op_bias, 1, ic, end_pos, len(entries2))
            local_bytes = insn_bytes
        if ic >= 16 and insn_bytes >= len(data) * 0.2:
            return local_best, local_best, local_bytes  # strong: accept now

    return None, local_best, local_bytes


def _priority_entries(data, ends, op_bias, raw_sp):
    """Anchor candidates read straight off the pool boundary map: every
    boundary whose following varint reads as a plausible biased upvalue
    count (op_bias .. op_bias+512). Returns entry tuples sorted by how
    close the implied upvalue count is to zero, capped at 64."""
    out = []
    n = len(data)
    lo, hi = op_bias, op_bias + 512
    first_bytes = set()
    for v in range(lo, hi + 1):
        first_bytes.add(v & 0x7F if v < 128 else (v & 0x7F) | 0x80)
    i = 1
    while i < n - 1:
        if data[i] not in first_bytes:
            i += 1
            continue
        try:
            up_raw, p2 = _uleb(data, i)
        except (IndexError, ValueError):
            i += 1
            continue
        if not (lo <= up_raw <= hi):
            i += 1
            continue
        count = ends.get(i)
        if count is None:
            i += 1
            continue
        sp_bias = raw_sp - count
        if sp_bias < 0:
            i += 1
            continue
        try:
            numparams, p3 = _uleb(data, p2)
            hc, p3 = _uleb(data, p3)
            for _ in range(hc):
                _, p3 = _uleb(data, p3)
            insns_raw, p3 = _uleb(data, p3)
        except (IndexError, ValueError):
            i += 1
            continue
        if not (0 <= numparams <= 255 and 0 <= hc <= 65536 and insns_raw < 10 ** 7):
            i += 1
            continue
        out.append((up_raw - op_bias, (sp_bias, up_raw, numparams, hc, insns_raw, p3)))
        i = p2
    out.sort(key=lambda t: t[0])
    return [e for _gap, e in out[:64]]


def _search_biases(data):
    """Find (sp_bias, op_bias, up_count, insn_count, end_pos, jt_entries)
    where the constant pool and the proto section both parse plausibly.

    The stored SP_BIAS is tried first; if the pool does not fit it (a newer
    build with a different bias constant), the pool boundary map is probed
    at every position whose following varint looks like a biased upvalue
    count, so the engine keeps working across v14.3 builds instead of
    crashing on the first parse. A work budget keeps the worst case bounded.
    """
    import proto_deserializer as PD

    try:
        raw_sp, pool_start = _uleb(data, 0)
    except (IndexError, ValueError):
        return None

    budget = [3000000]  # work units: stream reads + jump-table probes
    best = None
    best_bytes = 0

    default_entry = _anchor_candidate(data, PD.SP_BIAS)
    if default_entry is not None:
        strong, cand, cand_bytes = _scan_candidate(data, default_entry, budget)
        if strong is not None:
            return strong
        if cand is not None and cand_bytes > best_bytes:
            best, best_bytes = cand, cand_bytes

    # brute force anchored on the known OP_BIAS constant: probe every pool
    # boundary whose next varint reads as a biased upvalue count
    ends = _pool_end_map(data, pool_start)
    op_bias = getattr(PD, "OP_BIAS", 0x3C3A)
    for entry in _priority_entries(data, ends, op_bias, raw_sp):
        if entry[0] == PD.SP_BIAS:
            continue  # already scanned in the default tier
        strong, cand, cand_bytes = _scan_candidate(data, entry, budget)
        if strong is not None:
            return strong
        if cand is not None and cand_bytes > best_bytes:
            best, best_bytes = cand, cand_bytes

    # accept the best candidate only when its instruction stream is
    # substantial; tiny spurious alignments inside the pool never are
    if best and best[3] >= 16 and best_bytes >= max(256, len(data) * 0.02):
        return best
    return None


def deobfuscate_file(input_path, output_path, job=None):
    mods = _load_flat()
    PD = mods["proto_deserializer"]
    luraph_decoder = mods["luraph_decoder"]

    with open(input_path, "r", encoding="latin-1") as f:
        source_text = f.read()
    data = _decode_blob(source_text, luraph_decoder)

    found = _search_biases(data)
    if not found:
        raise ValueError(
            "Luraph v14.3: the blob decoded (%d bytes), but no sp/op bias "
            "pair aligned the constant pool and bytecode section under any "
            "candidate layout. Recovery is still in research." % len(data)
        )
    sp_bias, op_bias, up_count, ic, end_pos, entry_count = found
    ds = PD.Deserializer(data, op_bias=op_bias, sp_bias=sp_bias)
    ds.read_constant_pool()
    ds.read_upvalue_section()
    proto = ds.read_proto()

    BS = mods["batch_structure"]
    text = BS.format_proto(proto, proto, op_bias) if hasattr(BS, "format_proto") else None
    if text is None:
        blocks = mods["cfg_builder"].build_basic_blocks(proto)
        edges = mods["cfg_builder"].build_cfg(proto, blocks)
        preds = mods["structure_cfg"].build_preds(len(blocks), edges)
        dom, reachable = mods["structure_cfg"].compute_dominators(len(blocks), preds, entry=0)
        loops = mods["structure_cfg"].find_natural_loop_headers(len(blocks), edges, dom, reachable)
        order = mods["structure_cfg"].linear_order(len(blocks), entry=0)
        lines = mods["structure_cfg"].emit_structured(proto, blocks, edges, loops, order)
        text = "\n".join(lines)
    header = (job.credit_header() if job else
              "-- [[ Deobfuscated by MonLua [discord.gg/EdrQjndmAW] ]]\n")
    body = header + text
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    return output_path
