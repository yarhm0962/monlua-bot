import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEOB_DIR = ROOT / "deobf"
ENGINE_DIR = DEOB_DIR / "obfuscators" / "luraph_v143"
for extra in (str(DEOB_DIR), str(ENGINE_DIR)):
    if extra not in sys.path:
        sys.path.insert(0, extra)

from obfuscators.luraph_v143 import driver
from obfuscators.luraph_v143 import proto_deserializer as PD


def _uleb(value):
    out = bytearray()
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _make_blob(sp_bias, op_bias, n_insns=20, insn_val=None):
    """A minimal but genuine-shaped Luraph v14.3 blob: three constants, one
    proto with n_insns TYPE_RAW instructions and a one-entry jump table."""
    if insn_val is None:
        insn_val = 8 * 31 + 3  # 251: l/z/rp mod 8 == TYPE_RAW(3)
    pool = bytearray()
    pool += _uleb(3 + sp_bias)   # constant count (biased)
    pool.append(0)               # wrap byte
    text = b"return 1"
    pool += bytes([0x70]) + _uleb(len(text)) + text
    pool += bytes([0x0F]) + struct.pack("<d", 3.5)
    pool += bytes([0x22]) + struct.pack("<q", 42)
    body = bytearray()
    body += _uleb(1 + op_bias)   # upvalue count (biased)
    body += _uleb(0)             # numparams
    body += _uleb(1)             # head count
    body += _uleb(4)             # head id
    body += _uleb(n_insns + op_bias)
    for i in range(n_insns):
        # shape a real instruction: opcode varies between two values, and
        # insn 1 references pool constant 1 (rp_val = e*8 + TYPE_CONST)
        s_val = insn_val if i % 2 == 0 else (insn_val - 32)
        if insn_val == 1:
            l_val = s_val = z_val = rp_val = 1
        elif i == 1:
            l_val = s_val = z_val = 251
            rp_val = 1 * 8 + 4
        else:
            l_val = z_val = rp_val = 251
        body += _uleb(l_val) + _uleb(s_val) + _uleb(z_val) + _uleb(rp_val)
    body += _uleb(1)             # jump table count
    body += _uleb(0)             # entry: even word, op 0
    return bytes(pool) + bytes(body)


class LuraphV143BiasSearch(unittest.TestCase):
    def test_default_bias_blob_is_found(self):
        blob = _make_blob(PD.SP_BIAS, 10)
        found = driver._search_biases(blob)
        self.assertIsNotNone(found)
        self.assertEqual(found[0], PD.SP_BIAS)
        self.assertEqual(found[1], 10)
        self.assertEqual(found[3], 20)

    def test_alternate_sp_bias_is_autodetected(self):
        # a build whose constant-count bias changed but whose op bias matches
        # the known constant must still be recovered via the boundary probes
        blob = _make_blob(20000, PD.OP_BIAS)
        found = driver._search_biases(blob)
        self.assertIsNotNone(found)
        self.assertEqual(found[0], 20000)
        self.assertEqual(found[1], PD.OP_BIAS)

    def test_garbage_never_crashes(self):
        import random
        rng = random.Random(7)
        blobs = (b"", b"\x00" * 64, b"\xff" * 128,
                 bytes(rng.randrange(256) for _ in range(4096)))
        for blob in blobs:
            try:
                driver._search_biases(blob)
            except Exception as exc:
                self.fail(f"_search_biases raised on garbage: {exc!r}")

    def test_tiny_spurious_alignment_is_rejected(self):
        # tiny operand values let every short prefix "align"; the coverage
        # bar must reject them instead of returning wrong output
        blob = _make_blob(PD.SP_BIAS, 10, insn_val=1)
        self.assertIsNone(driver._search_biases(blob))


if __name__ == "__main__":
    unittest.main()
