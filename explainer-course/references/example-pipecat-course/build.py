"""Assemble the course: lesson 1 (hand-written in course-base.html) plus lessons 2..48.

Rewritten modules come from lessons_*.py. Modules not yet rewritten keep their old
blocks from old_blocks.json, so the page always has all 48 lessons.

Every code panel is read from the real source files by line number, never typed.
"""
import glob, importlib.util, json, os, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = {"1.2.1": os.path.join(HERE, "src-1.2.1"), "1.8.1": os.path.join(HERE, "src-1.8.1"),
       "repo": "/private/tmp/pr181src", "client-before": os.path.join(HERE, "src-client-before"), "sp": HERE}


def lines(ver, path, start, end):
    with open(os.path.join(SRC[ver], path)) as f:
        return f.read().split("\n")[start - 1:end]


def code(ver, path, *ranges):
    """Exact source lines. Several ranges are joined by a '...' line."""
    parts = []
    for i, (a, b) in enumerate(ranges):
        if i:
            parts.append(["..."])
        parts.append(lines(ver, path, a, b))
    flat = [l for p in parts for l in p]
    body = textwrap.dedent("\n".join(l for l in flat if l != "..."))
    # re-insert the ellipsis markers after dedent
    out, it = [], iter(body.split("\n"))
    for p in parts:
        if p == ["..."]:
            out.append(None)          # filled below with the next line's indent
        else:
            for _ in p:
                out.append(next(it))
    for i, l in enumerate(out):
        if l is None:
            nxt = next((x for x in out[i + 1:] if x), "")
            out[i] = " " * (len(nxt) - len(nxt.lstrip())) + "..."
    return "\n".join(out).rstrip()


def js(v):
    return json.dumps(v, ensure_ascii=False)


def load_modules():
    mods = {}
    for f in sorted(glob.glob(os.path.join(HERE, "lessons_m*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        m.code, m.js = code, js
        spec.loader.exec_module(m)
        for mod_index in m.MODULES:
            mods[mod_index] = m
    return mods


def main():
    base = open(os.path.join(HERE, "course-base.html")).read()
    old = json.load(open(os.path.join(HERE, "old_blocks.json")))
    mods = load_modules()

    lesson_js, vis_js = [], []
    done = set()
    for blk in old:
        m = blk["m"]
        if m in mods:
            if m in done:
                continue
            done.add(m)
            src = mods[m]
            for les in src.LESSONS:
                if les["m"] != m:
                    continue
                slides = ",\n ".join(js(s) for s in les["slides"])
                lesson_js.append(f'les({m},{js(les["title"])},[\n {slides}\n]);')
        else:
            lesson_js.append(blk["raw"])
    for src in {id(v): v for v in mods.values()}.values():
        for name, body in src.VIS.items():
            vis_js.append(f"VIS[{js(name)}]=function(){{return {body};}};")

    # mark modules still carrying old text, so nothing unfinished passes as done
    import re
    mblock = re.search(r"var M=\[\n(.*?)\n\];", base, re.S)
    rows = mblock.group(1).split("\n")
    for i, r in enumerate(rows):
        if i not in mods and i != 0:
            rows[i] = re.sub(r'^(\s*\[")([^"]*)(")', r'\1\2, old text\3', r)
    base = base[:mblock.start(1)] + "\n".join(rows) + base[mblock.end(1):]
    out = base.replace("/* ===== GEN LESSONS ===== */\n/* ===== END GEN LESSONS ===== */",
                       "/* ===== GEN LESSONS ===== */\n" + "\n".join(lesson_js) + "\n/* ===== END GEN LESSONS ===== */")
    out = out.replace("/* ===== GEN VIS ===== */\n/* ===== END GEN VIS ===== */",
                      "/* ===== GEN VIS ===== */\n" + "\n".join(vis_js) + "\n/* ===== END GEN VIS ===== */")
    open(os.path.join(HERE, "pipecat-upgrade-course.html"), "w").write(out)
    head = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><style>html,body{margin:0;height:100%;'
            'color-scheme:dark}</style></head><body>\n')
    open(os.path.join(HERE, "view.html"), "w").write(head + out + "\n</body></html>")
    n = out.count("\nles(") + out.count("\nles(0,")  # rough
    print("built; rewritten modules:", sorted(m + 1 for m in mods))


if __name__ == "__main__":
    main()
