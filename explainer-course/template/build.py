"""Build the course page from course.html (template) + lessons.py (content).

Usage, from the course working folder that holds course.html, lessons.py and this file:

    python3 build.py

Writes:
    <slug>.html   the page to publish as an artifact
    view.html     same page wrapped in a full document, for the local browser check

lessons.py must define:
    COURSE   dict: title, brand (HTML allowed), slug, before_label, now_label, us_label
    MODULES  list of [name, one-line subtitle]
    LESSONS  list of {m, title, slides}   (built by add() in lessons.py)
    VIS      dict visKey -> JS expression returning HTML (simple3(...) for the three boxes)
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def js(v):
    return json.dumps(v, ensure_ascii=False)


def load_lessons():
    spec = importlib.util.spec_from_file_location("lessons", os.path.join(HERE, "lessons.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fill(base, marker, body):
    start = "/* ===== GEN %s ===== */" % marker
    end = "/* ===== END GEN %s ===== */" % marker
    assert start in base and end in base, marker
    return base.replace(start + "\n" + end, start + "\n" + body + "\n" + end)


def main():
    src = load_lessons()
    c = src.COURSE
    base = open(os.path.join(HERE, "course.html")).read()
    for k, v in {"TITLE": c["title"], "BRAND": c["brand"], "STORAGE_KEY": "course-" + c["slug"] + "-v1",
                 "BEFORE_LABEL": c["before_label"], "NOW_LABEL": c["now_label"], "US_LABEL": c["us_label"]}.items():
        base = base.replace("{{%s}}" % k, v)

    mods = ",\n".join(" " + js(m) for m in src.MODULES)
    lessons = []
    for les in src.LESSONS:
        slides = ",\n ".join(js(s) for s in les["slides"])
        lessons.append("les(%d,%s,[\n %s\n]);" % (les["m"], js(les["title"]), slides))
    vis = ["VIS[%s]=function(){return %s;};" % (js(k), body) for k, body in src.VIS.items()]

    out = fill(base, "MODULES", mods)
    out = fill(out, "LESSONS", "\n".join(lessons))
    out = fill(out, "VIS", "\n".join(vis))

    page = os.path.join(HERE, c["slug"] + ".html")
    open(page, "w").write(out)
    head = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><style>html,body{margin:0;height:100%;'
            'color-scheme:dark}</style></head><body>\n')
    open(os.path.join(HERE, "view.html"), "w").write(head + out + "\n</body></html>")
    print("built %s: %d modules, %d lessons" % (page, len(src.MODULES), len(src.LESSONS)))


if __name__ == "__main__":
    main()
