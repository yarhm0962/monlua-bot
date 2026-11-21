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


def _search_biases(data):
    """Find (op_bias, up_count, insn_count, end_pos, jt_entries) where the
    proto section parses plausibly. Cheap prefix scan first, guarded parse
    only on survivors."""
    import proto_deserializer as PD

    sp_bias = PD.SP_BIAS
    anchor = PD.Deserializer(data, sp_bias=sp_bias)
    anchor.read_constant_pool()
    p = anchor.cur.pos

    up_raw, p = _uleb(data, p)
    numparams, p = _uleb(data, p)
    hc, p = _uleb(data, p)
    for _ in range(hc):
        _, p = _uleb(data, p)
    insns_raw, p = _uleb(data, p)
    insns_start = p

    max_insns = max(1, (len(data) - insns_start) // 4)
    max_insns = min(max_insns, 200000)

    # one pass over the stream: values and the byte offset after each uleb
    limit = max_insns * 4
    vals = []
    positions = [insns_start]
    q = insns_start
    try:
        for _ in range(limit):
            v, q = _uleb(data, q)
            vals.append(v)
            positions.append(q)
    except IndexError:
        pass

    def jt_ok(ic):
        """Cheap jump-table plausibility at the position after ic*4 ulebs."""
        if ic <= 0 or ic * 4 > len(vals):
            return None
        jt_pos = positions[ic * 4]
        try:
            cnt, r = _uleb(data, jt_pos)
        except IndexError:
            return None
        if not (0 < cnt < 100000):
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

    best = None
    for insns in range(1, max_insns + 1):
        # quick opcode sanity on the candidate stream
        chunk = vals[insns * 4 - 4:insns * 4] if insns <= 256 else None
        if chunk is not None and any(v > 255 for v in chunk):
            continue
        found = jt_ok(insns)
        if not found:
            continue
        op_bias, _up, ic, _r, _n, entries = found
        try:
            parsed = _guarded_proto_parse(data, PD.Deserializer, op_bias, sp_bias, up_raw if up_raw <= 64 else 1)
        except Exception:
            continue
        if not parsed:
            continue
        proto, end_pos, entries2 = parsed
        best = (op_bias, 1, len(proto["opcodes"]), end_pos, len(entries2))
        break
    return best


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
            "Luraph v14.3: the blob decoded (%d bytes) and the constant pool "
            "parsed, but the bytecode section did not align under any bias "
            "yet. Recovery is still in research." % len(data)
        )
    op_bias, up_count, ic, end_pos, entry_count = found
    ds = PD.Deserializer(data, op_bias=op_bias, sp_bias=PD.SP_BIAS)
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
