"""Two jobs, run from the course working folder:

    python3 audit.py lengths     flag every lesson over the length limits (D5)
    python3 audit.py dump        write review_dump.txt: one block per lesson, plain text,
                                 for the review agents to read one lesson at a time

Limits: body under 110 words, each box line under 20 words, why box under 45 words.
"""
import html
import re
import sys

import lessons

TAG = re.compile(r"<[^>]+>")


def words(s):
    return len(html.unescape(TAG.sub("", s or "")).split())


def lengths():
    bad = 0
    for i, e in enumerate(lessons.L, 1):
        problems = []
        if words(e["text"]) >= 110:
            problems.append("body %d words" % words(e["text"]))
        for k in ("before", "now", "us"):
            if words(e[k]) >= 20:
                problems.append("%s line %d words" % (k, words(e[k])))
        if e["why"] and words(e["why"]) >= 45:
            problems.append("why box %d words" % words(e["why"]))
        if problems:
            bad += 1
            print("LESSON %d (%s): %s" % (i, e["title"], "; ".join(problems)))
    print("%d of %d lessons over a limit" % (bad, len(lessons.L)))


def dump():
    out = []
    for i, e in enumerate(lessons.L, 1):
        m = lessons.MODULES[e["m"]][0]
        out.append("=" * 70)
        out.append("LESSON %d | module: %s | kind: %s" % (i, m, e["kind"]))
        out.append("SIDEBAR TITLE: " + e["title"])
        out.append("HEADLINE: " + e["head"])
        out.append("BODY: " + html.unescape(TAG.sub("", e["text"])))
        out.append("BOX %s: %s" % (lessons.COURSE["before_label"], e["before"]))
        out.append("BOX %s: %s" % (lessons.COURSE["now_label"], e["now"]))
        out.append("BOX %s: %s" % (lessons.COURSE["us_label"], e["us"]))
        if e["why"]:
            label = "WHY NOT RELEVANT TO US" if e["kind"] == "skip" else "WHAT ADOPTING IT WOULD TAKE"
            out.append("%s: %s" % (label, e["why"]))
    open("review_dump.txt", "w").write("\n".join(out) + "\n")
    print("wrote review_dump.txt, %d lessons" % len(lessons.L))


if __name__ == "__main__":
    {"lengths": lengths, "dump": dump}[sys.argv[1]]()
