import re

_IDENT_RX = re.compile(r"\b[A-Za-z_]\w*\b")
_ESC_RX = re.compile(r"\\x[0-9a-fA-F]{2}|\\\d{1,3}")
_BLOB_RX = re.compile(r'"[^"\\]{500,}"|\'[^\'\\]{500,}\'')
_DECODER_RX = re.compile(r"\b(?:string\.(?:byte|char|sub)|bit32\.(?:bxor|band|bor|rshift|lshift))\b")
_NUM_TABLE_RX = re.compile(r"\{\s*-?\d+\s*(?:,\s*-?\d+\s*){19,}")
_DISPATCH_RX = re.compile(r"\[\s*[A-Za-z_]\w*\s*\]\s*\(")
_FUNCTION_RX = re.compile(r"\\bfunction\\b")
_LOOP_RX = re.compile(r"\\b(?:while|repeat|for)\\b")
_BRANCH_RX = re.compile(r"\\b(?:if|elseif)\\b")
_KEYWORDS = {
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
    "if", "in", "local", "nil", "not", "or", "repeat", "return", "then",
    "true", "until", "while", "continue", "export", "type", "typeof"
}


def _mask(text):
    return "".join("\n" if c == "\n" else "\r" if c == "\r" else " " for c in text)


def _long_bracket_open(source, index):
    if index >= len(source) or source[index] != "[":
        return None
    cursor = index + 1
    while cursor < len(source) and source[cursor] == "=":
        cursor += 1
    if cursor < len(source) and source[cursor] == "[":
        return cursor - index - 1, cursor + 1
    return None


def _quoted_end(source, start):
    quote = source[start]
    cursor = start + 1
    while cursor < len(source):
        if source[cursor] == "\\":
            cursor += 2
            continue
        if source[cursor] == quote:
            return cursor + 1
        cursor += 1
    return len(source)


def _count(rx, text, cap=200000):
    total = 0
    for _ in rx.finditer(text):
        total += 1
        if total >= cap:
            break
    return total


class LuaAnalysis:
    __slots__ = (
        "source", "code", "structure", "comments", "header", "identifier_count",
        "short_identifier_count", "unique_identifier_count", "function_count",
        "loop_count", "branch_count", "string_count", "string_bytes",
        "max_string_length", "nonspace_size", "line_count", "escape_count",
        "numeric_table_count", "dispatch_call_count"
    )

    def __init__(self, source):
        self.source = source
        code_parts = []
        structure_parts = []
        comments = []
        header = []
        leading = True
        string_count = 0
        string_bytes = 0
        max_string_length = 0
        i = 0
        n = len(source)

        while i < n:
            c = source[i]

            if source.startswith("--", i):
                opened = _long_bracket_open(source, i + 2)
                if opened is not None:
                    level, after_open = opened
                    close = "]" + "=" * level + "]"
                    found = source.find(close, after_open)
                    end = n if found < 0 else found + len(close)
                else:
                    found = source.find("\n", i)
                    end = n if found < 0 else found
                comment = source[i:end]
                comments.append(comment)
                if leading:
                    header.append(comment)
                masked = _mask(comment)
                code_parts.append(masked)
                structure_parts.append(masked)
                i = end
                continue

            if c in ("'", '"', chr(96)):
                end = _quoted_end(source, i)
                literal = source[i:end]
                code_parts.append(literal)
                structure_parts.append(_mask(literal))
                string_count += 1
                string_bytes += len(literal)
                max_string_length = max(max_string_length, len(literal))
                leading = False
                i = end
                continue

            if c == "[":
                opened = _long_bracket_open(source, i)
                if opened is not None:
                    level, after_open = opened
                    close = "]" + "=" * level + "]"
                    found = source.find(close, after_open)
                    end = n if found < 0 else found + len(close)
                    literal = source[i:end]
                    code_parts.append(literal)
                    structure_parts.append(_mask(literal))
                    string_count += 1
                    string_bytes += len(literal)
                    max_string_length = max(max_string_length, len(literal))
                    leading = False
                    i = end
                    continue

            if c.isspace():
                code_parts.append(c)
                structure_parts.append(c)
                i += 1
                continue

            leading = False
            code_parts.append(c)
            structure_parts.append(c)
            i += 1

        self.code = "".join(code_parts)
        self.structure = "".join(structure_parts)
        self.comments = "\n".join(comments)
        self.header = "\n".join(header)
        self.string_count = string_count
        self.string_bytes = string_bytes
        self.max_string_length = max_string_length
        self.line_count = source.count("\n") + 1
        self.nonspace_size = sum(not c.isspace() for c in self.code)
        identifiers = set()
        identifier_count = 0
        short_identifier_count = 0
        for match in _IDENT_RX.finditer(self.structure):
            name = match.group(0)
            if name in _KEYWORDS:
                continue
            identifier_count += 1
            identifiers.add(name)
            if len(name) <= 2:
                short_identifier_count += 1
        self.identifier_count = identifier_count
        self.short_identifier_count = short_identifier_count
        self.unique_identifier_count = len(identifiers)
        self.function_count = _count(_FUNCTION_RX, self.structure)
        self.loop_count = _count(_LOOP_RX, self.structure)
        self.branch_count = _count(_BRANCH_RX, self.structure)
        self.escape_count = _count(_ESC_RX, self.code)
        self.numeric_table_count = _count(_NUM_TABLE_RX, self.structure)
        self.dispatch_call_count = _count(_DISPATCH_RX, self.structure)


def scan_lua_source(source):
    analysis = LuaAnalysis(source)
    return analysis.code, analysis.comments


def strip_lua_comments(source):
    return LuaAnalysis(source).code


def strip_lua_strings(source):
    out = []
    i = 0
    n = len(source)
    while i < n:
        c = source[i]
        if c in ("'", '"', chr(96)):
            end = _quoted_end(source, i)
            out.append(_mask(source[i:end]))
            i = end
            continue
        if c == "[":
            opened = _long_bracket_open(source, i)
            if opened is not None:
                level, after_open = opened
                close = "]" + "=" * level + "]"
                found = source.find(close, after_open)
                end = n if found < 0 else found + len(close)
                out.append(_mask(source[i:end]))
                i = end
                continue
        out.append(c)
        i += 1
    return "".join(out)


def leading_lua_comments(source):
    return LuaAnalysis(source).header


FAMILIES = [
    ("xen", "Synapse Xen",
     re.compile(r"generated by xen\b|obfuscated (?:by|using) xen\b", re.I),
     re.compile(r"SynapseXen_[A-Za-z_]\w+"), 5, 0.9, 0.65),
    ("moonsec_v2", "MoonSec V2",
     re.compile(r"(?:protected|obfuscated|generated|created)\s+(?:with|by|using)\s+moonsec\s*v2\b", re.I),
     None, 0, 0.9, 0.6),
    ("ironbrew2", "IronBrew2",
     re.compile(r"(?:protected|obfuscated|generated|created)\s+(?:with|by|using)\s+ironbrew\s*2\b", re.I),
     None, 0, 0.9, 0.6),
    ("psu", "PSU",
     re.compile(r"psu\.dev\b|protected by psu\b|obfuscated (?:by|using) psu\b", re.I),
     None, 0, 0.85, 0.55),
    ("boronide", "Boronide",
     re.compile(r"(?:obfuscated|protected|generated|created)\s+(?:by|with|using)\s+boronide\b", re.I),
     None, 0, 0.85, 0.55),
    ("prometheus", "PromethEus",
     re.compile(r"(?:obfuscated|protected|generated|created)\s+(?:by|with|using)\s+prometheus\b", re.I),
     None, 0, 0.85, 0.55),
    ("hierarchy", "Hierarchy",
     re.compile(r"obfuscated (?:by|using) hierarchy\b|protected (?:by|with) hierarchy\b|hierarchy\s*obfuscator", re.I),
     None, 0, 0.85, 0.55),
    ("luauguard", "LuauGuard",
     re.compile(r"(?:protected|obfuscated|generated|created)\s+(?:by|with|using)\s+luau\s*guard\b", re.I),
     None, 0, 0.85, 0.55),
]


def family_scores(source, analysis=None):
    analysis = analysis or (source if isinstance(source, LuaAnalysis) else LuaAnalysis(source))
    structure = analysis.structure
    header = analysis.header[:800]
    out = []
    for name, label, header_rx, shape_rx, min_hits, conf, weak in FAMILIES:
        if header_rx.search(header):
            out.append((name, conf, label, ["leading header comment matched"]))
            continue
        if shape_rx is None:
            continue
        hits = _count(shape_rx, structure)
        if hits >= min_hits * 3:
            out.append((name, conf, label, ["%d code-pattern hits (need %d)" % (hits, min_hits * 3)]))
        elif min_hits and hits >= min_hits:
            out.append((name, weak, label, ["%d code-pattern hits (need %d for a strong match)" % (hits, min_hits * 3)]))
    return out


def obfuscation_score(source, analysis=None):
    analysis = analysis or (source if isinstance(source, LuaAnalysis) else LuaAnalysis(source))
    code = analysis.code
    structure = analysis.structure
    size = max(1, analysis.nonspace_size)
    per_kb = 1000.0 / size
    score = 0.0
    evidence = []

    newlines = structure.count("\n")
    if size > 4000 and newlines < size / 2000.0:
        score += 0.2
        evidence.append("minified (%.0f newlines in %.0f KB)" % (newlines, size / 1000.0))

    escapes = analysis.escape_count
    if escapes * per_kb > 20:
        score += 0.2
        evidence.append("%.0f string escapes per KB" % (escapes * per_kb))

    total = analysis.identifier_count
    short = analysis.short_identifier_count
    if total >= 500 and short / total > 0.35:
        score += 0.2
        evidence.append("%.0f%% 1-2-character identifiers" % (100.0 * short / total))

    if analysis.numeric_table_count:
        score += 0.2
        evidence.append("large numeric constant tables (VM bytecode)")

    if re.search(r"\bwhile\s+true\s+do\b", structure) and analysis.dispatch_call_count:
        score += 0.15
        evidence.append("while-true dispatcher with table-index calls")

    blobs = _count(_BLOB_RX, code, cap=50)
    if blobs:
        score += 0.15
        evidence.append("%d opaque 500+ character string blobs" % blobs)

    if size >= 8000 and analysis.function_count >= 25 and analysis.branch_count >= 40:
        if total >= 250 and short / max(1, total) >= 0.25:
            score += 0.1
            evidence.append("dense function and branch structure with generated identifiers")

    decoder_ops = _count(_DECODER_RX, structure)
    if decoder_ops >= 12 and analysis.string_bytes >= size * 0.15:
        score += 0.1
        evidence.append("%d string/bitwise decoder operations around encoded data" % decoder_ops)

    return min(1.0, score), evidence
