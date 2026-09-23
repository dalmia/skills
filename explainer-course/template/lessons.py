# Course content. One add() call per lesson. build.py turns this into the page.
#
# Every lesson is ONE slide with a three-box visual (before / now / what it means for us).
# Fields, in order:
#   m       module index (0-based, into MODULES)
#   title   the change or the problem itself, said plainly. Shown in the sidebar.
#   kind    "over"  relevant, the default
#           "skip"  not relevant: a feature or provider the reader does not use at all.
#                   Red banner "Not relevant to us" on the slide, red row in the sidebar.
#           "avail" an improvement the reader could adopt but has not.
#                   Orange banner "Improvement available. Not used yet", orange row.
#   head    the headline: what happened / what is new, plus the verdict when it is not a red or orange slide
#           (Fixed by upgrading / Fixed in this PR / To fix after merge / Decided: ... / Nothing to do)
#   text    the body, under 110 words. HTML allowed. Class and setting names in <code>.
#   before  one line, under 20 words: how it was before
#   now     one line, under 20 words: how it is now
#   us      one line, under 20 words: what it means for the reader, with the verdict
#   why     required for "skip" and "avail", under 45 words:
#             skip  -> exactly why it does not apply (which feature is off, which provider is not used)
#             avail -> exactly what adopting it would take (which file, which setting, which decision)
#           None for "over".

import json


def js(v):
    return json.dumps(v, ensure_ascii=False)


COURSE = dict(
    title="{{Course title, 2 to 4 words}}",
    brand="{{Topic}} <em>{{before &rarr; after}}</em>",
    slug="{{course-slug}}",
    before_label="Before, {{old version or state}}",
    now_label="Now, {{new version or state}}",
    us_label="What it means for us",
)

MODULES = [
    # [name, one-line subtitle]. Group lessons by what the reader cares about, not by file or PR number.
    ["{{Module name}}", "{{What this group of lessons is about}}"],
]

L = []


def add(m, title, kind, head, text, before, now, us, why=None):
    assert kind in ("over", "skip", "avail"), kind
    assert (kind == "over") == (why is None), "skip/avail need a why box; over must not have one: " + title
    L.append(dict(m=m, title=title, kind=kind, head=head, text=text, before=before, now=now, us=us, why=why))


# ================================================================ MODULE 1
add(0, "{{The change or bug, plainly}}", "over",
    "{{Headline: what went wrong or what is new. Verdict at the end}}",
    "{{Body under 110 words: what the problem was on a real run, what changed, what it means for us.}}",
    "{{Before, one line}}",
    "{{Now, one line}}",
    "{{What it means for us, one line, with the verdict}}")

# ---------------------------------------------------------------- build the structures build.py expects
VIS = {}
LESSONS = []
for i, e in enumerate(L):
    key = "s%d" % (i + 1)
    VIS[key] = "simple3(" + js({"before": e["before"], "after": e["now"], "us": e["us"]}) + ")"
    slide = [e["kind"], e["head"], e["text"], key]
    if e["why"]:
        slide.append(e["why"])
    LESSONS.append({"m": e["m"], "title": e["title"], "slides": [slide]})
