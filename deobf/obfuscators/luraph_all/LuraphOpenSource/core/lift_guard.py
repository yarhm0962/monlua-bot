"""Fault-tolerance helpers shared by the Luraph lift drivers.

The lifters stop on the first thing they cannot prove (a walk that does not
converge, a state explosion, a constant that is not decoded yet).  On a big or
slightly unusual script that is often only a *limit* being too tight, not a
real dead end, so the drivers retry once with the limits relaxed before giving
up.  Nothing here changes what a successful lift produces.
"""
import contextlib
import sys

# module-level limits of the devirt engines and the factor each is relaxed by
_LIMITS = {
    "WALK_RESTARTS": 4,
    "WALK_MAX_ERRORS": 4,
    "STACK_WALK_MAX": 4,
    "WALK_LIMIT": 4,
    "WALK_STAGNANT": 3,
}


@contextlib.contextmanager
def relaxed(devirt, factors=None):
    """Temporarily raise the walk limits of `devirt` (restored on exit)."""
    saved = {}
    for name, factor in (factors or _LIMITS).items():
        cur = getattr(devirt, name, None)
        if isinstance(cur, int) and not isinstance(cur, bool):
            saved[name] = cur
            setattr(devirt, name, cur * factor)
    try:
        yield dict((n, getattr(devirt, n)) for n in saved)
    finally:
        for name, val in saved.items():
            setattr(devirt, name, val)


def attempt_lifts(devirtualize, dpath, devirt, label="devirtualization"):
    """Run `devirtualize()` (a zero-argument callable returning truthy when it
    wrote `dpath`); on an error or an empty result retry once with relaxed
    limits.  SystemExit counts as a failure too: several code paths used to
    call sys.exit from inside the lifter, which skipped every handler and
    killed the whole run (and with it the fallback output).  Returns True when
    a lift was written."""
    import os
    for attempt in (1, 2):
        ctx = relaxed(devirt) if attempt == 2 else contextlib.nullcontext()
        try:
            with ctx:
                if attempt == 2:
                    print("[*] retrying %s with relaxed walk limits" % label, file=sys.stderr)
                ok = devirtualize()
            if ok is not False and os.path.exists(dpath):
                return True
        except (Exception, SystemExit) as e:
            print("[!] %s failed: %s: %s" % (label, type(e).__name__, e), file=sys.stderr)
            if os.environ.get("DEVIRT_TB"):
                import traceback
                traceback.print_exc()
        if os.environ.get("DEVIRT_NO_RETRY"):
            break
    return False


# markers the lifters write where they could not recover code
UNRESOLVED_MARKERS = (
    "-- unresolved native/runtime closure",
    "unresolved Luraph runtime helper",
    "-- VM ",
)


def quality(text):
    """(code_lines, unresolved_markers, calls_of_nil) of a lifted text."""
    code = 0
    marks = 0
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("--"):
            if any(m in s for m in UNRESOLVED_MARKERS):
                marks += 1
            continue
        code += 1
    return code, marks, text.count("(nil)(")
