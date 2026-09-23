"""Replace whole add(...) entries in lessons.py by title, after a review round.

Usage:
    from fix_entries import replace
    replace({"<lesson title>": '''add(0, "<lesson title>", "over", ...)'''})

The title must match exactly. Rebuild with build.py afterwards.
"""
import re

P = "lessons.py"


def replace(entries):
    s = open(P).read()
    for title, new in entries.items():
        m = re.search(r'add\(\d+, "%s", .*?\)\n(?=\n)' % re.escape(title), s, re.S)
        assert m, title
        s = s[:m.start()] + new.strip() + "\n" + s[m.end():]
    open(P, "w").write(s)
