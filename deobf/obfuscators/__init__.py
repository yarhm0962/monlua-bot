"""Obfuscator registry and code-aware detection."""
from obfuscators.base import Obfuscator, Job
from obfuscators.luraph_v15 import LuraphV15
from obfuscators.luraph_v151 import LuraphV151
from obfuscators.ironbrew1 import Ironbrew1
from obfuscators.moonsec_v3 import MoonsecV3
from obfuscators.centurion import Centurion
from obfuscators.generic import Generic
from obfuscators import extra_families

PLUGINS = [
    LuraphV151(),
    LuraphV15(),
    Ironbrew1(),
    MoonsecV3(),
    Centurion(),
    Generic(),
]

MIN_CONFIDENCE = 0.5


def by_name(name):
    for plugin in PLUGINS:
        if plugin.name == name:
            return plugin
    raise KeyError("unknown obfuscator %r (known: %s)" % (name, ", ".join(p.name for p in PLUGINS)))


def scores(source, analysis=None):
    analysis = analysis or extra_families.LuaAnalysis(source)
    out = []
    for plugin in PLUGINS:
        try:
            confidence = plugin.detect(source, analysis)
        except Exception:
            confidence = 0.0
        out.append((confidence, plugin))
    return sorted(out, key=lambda item: -item[0])


def all_scores(source):
    analysis = extra_families.LuaAnalysis(source)
    candidates = []
    for confidence, plugin in scores(source, analysis):
        candidates.append((plugin.name, confidence, plugin.label, list(getattr(plugin, "last_evidence", []) or [])))
    candidates.extend(extra_families.family_scores(source, analysis))
    candidates.sort(key=lambda row: row[1], reverse=True)
    score, evidence = extra_families.obfuscation_score(source, analysis)
    if score >= 0.5:
        candidates.append(("obfuscated", score, "Obfuscated (unknown engine)", evidence))
    else:
        candidates.append(("plain", score, "No obfuscation detected", evidence))
    return candidates


def detect(source):
    analysis = extra_families.LuaAnalysis(source)
    best = scores(source, analysis)[0]
    if best[0] >= MIN_CONFIDENCE:
        return best[1], best[0]
    return by_name(Generic.name), best[0] if best[1].name == Generic.name else 0.0
