---
name: explainer-course
description: Build an interactive one-slide-per-lesson course that explains any set of changes or concepts (a dependency upgrade, a PR, a migration, a system, a design) to a non-engineer reader, published as an artifact, then reviewed by five parallel agents on five dimensions until every slide passes. Use when the user says "explain this like the course", "make a course", "teach me the changes", "lesson by lesson", "explainer-course", or asks to understand a diff / upgrade / PR change by change.
---

# Explain as a course

Build the same course as `references/example-pipecat-course/` for a new topic. That folder is the
finished, reader-approved product: read it before writing anything, and point every review agent at it.

## What the finished thing is

One HTML page, published as an artifact, with:

- A sidebar of modules. Each module row shows "done / total" lessons. Each lesson row shows the
  lesson title and either a slide count, a red "not relevant" tag, or an orange "available" tag.
- One slide per lesson. Left: a banner (kind), the headline, the body, and for red/orange slides a
  reason box. Right: three boxes, Before / Now / What it means for us, one line each.
- Prev / Next buttons, arrow keys, a "Mark lesson done" toggle on every slide, a progress bar, a
  reset link. Progress is kept in the viewer's browser only.
- Dark and light theme from the system setting. Fits at 1440x900 without scrolling.

## Flow

Do the steps in order. Keep the user informed in one line at each step.

### 1. Intake

Get from the request: the topic, the before and after (versions, branches, states), the reader, and
the source material (repo path, PR number, diff, docs). Do not ask questions the request already
answers. If the source material is a PR, check out both sides so every fact can be traced in code.

### 2. Survey with parallel agents

Split the source material across parallel Explore agents (by area, by module, by file group).
Each agent returns, per change: what actually went wrong or what is new, what changed, the upstream
PR or commit, and whether the reader's setup uses that feature or provider at all. Merge into one
list of changes. That list is the lesson list. Group it into 4 to 8 modules by what the reader
cares about ("Calls that got stuck"), never by file or PR number.

### 3. Classify every lesson

Three kinds. Read `references/style-rules.md`, section "Relevance labels", and apply it to every
lesson before writing:

- `over`: relevant. Anything that changes what the reader already runs, including speed, memory,
  cost and timing changes.
- `avail`: an improvement the reader could adopt and has not. Orange banner. Needs a
  "what adopting it would take" box.
- `skip`: a feature or provider the reader does not use at all. Red banner. Needs a
  "why not relevant to us" box. When unsure, it is `avail`, not `skip`.

### 4. Set up the working folder

In the scratchpad, copy `template/course.html`, `template/build.py`, `template/lessons.py`,
`template/fix_entries.py`, `template/audit.py`. Fill `COURSE` and `MODULES` in `lessons.py`.

### 5. Write the lessons

One `add()` call per lesson in `lessons.py`. Field rules are in the comment at the top of that file
and in `references/style-rules.md`. Read both before writing. Every fact traced in the source, never
from memory of a changelog. Then:

```bash
python3 audit.py lengths
python3 build.py
```

Fix every lesson `audit.py lengths` flags before going on.

### 6. Look at the rendered page

Open `view.html` in the built-in browser at 1440x900, in dark and in light, and step through every
slide with the arrow key. Any slide whose content scrolls is too long: cut words, never shrink the
page. Check the sidebar tags, the banners and the reason boxes render on the right lessons.

### 7. Publish

Load the `artifact-design` skill, then publish the built `<slug>.html` as an artifact with a
2 to 4 word title. On every later fix, rebuild and republish to the same URL. Give the user the
full artifact URL.

### 8. Review with five agents in parallel, until every slide passes

```bash
python3 audit.py dump
```

Fill the two placeholders in `references/review-brief.md`. Split the lessons across five
general-purpose agents, run in the background, each given the filled brief and its share of
`review_dump.txt`, told to read one lesson at a time and to calibrate on
`references/example-pipecat-course/lessons_m_all.py` first. Each agent rates every lesson PASS or
FAIL on D1 to D5 and gives full replacement text for every FAIL.

When they return:

1. Trace every FAIL in the source before accepting it. Overrule findings the code contradicts and
   say so.
2. Apply the accepted fixes with `fix_entries.replace`, rerun `audit.py lengths`, rebuild,
   recheck fit in the browser, republish.
3. Run the next round on the lessons that changed. Stop only when a round returns no FAIL.

Report to the user per round: how many lessons passed clean, which had a fix and what it was, and
whether the last set of fixes was re-reviewed.

## Non-negotiable style

The reader's corrections during the first course are the standard. The full list is in
`references/style-rules.md`. The ones broken most often:

- Real names always (the provider, the service, the class, the setting, the file). No paraphrase.
- Title = the change or the bug itself. Never a verdict-only title.
- Say plainly whether the PR fixed it. Say which page, chart, file, full URL.
- Three boxes restate the body in the same words. No second story in the visual.
- Body under 110 words, box lines under 20, reason box under 45. Fits at 1440x900.
- Answers to the user about the course are short. No blog posts.

## Files in this skill

- `template/course.html`: the page, topic-agnostic. Placeholders `{{TITLE}}`, `{{BRAND}}`,
  `{{STORAGE_KEY}}`, `{{BEFORE_LABEL}}`, `{{NOW_LABEL}}`, `{{US_LABEL}}` and the
  `GEN MODULES` / `GEN LESSONS` / `GEN VIS` markers are filled by `build.py`. Do not hand-edit
  the built page.
- `template/build.py`, `template/lessons.py`, `template/fix_entries.py`, `template/audit.py`.
- `references/style-rules.md`: every writing rule, with the corrections that produced it.
- `references/review-brief.md`: the five-dimension rubric handed to each review agent.
- `references/example-pipecat-course/`: the finished Pipecat 1.2.1 to 1.8.1 course, unchanged:
  `course-base.html` (its page, with a hand-written 19-slide deep-dive lesson 1 and SVG
  diagrams), `lessons_m_all.py` (47 approved one-slide lessons), `build.py`, `fix_entries.py`,
  `review_brief.md`, and the built `pipecat-upgrade-course.html` / `view.html`. Use it to match
  tone, structure, box wording, banners and sidebar behaviour.

## Optional deep-dive lesson

If the user asks for one lesson to go step by step (as lesson 1 of the example does), write it by
hand in the built page's `GEN LESSONS` area as a multi-slide `les()` with kinds `over`, `setup`,
`trap`, `before`, `now`, `us`, and draw its SVG diagrams with the `box`, `tx`, `cap`, `arrow`
helpers in `course.html`. Copy the structure from the example's lesson 1. Do this only when asked.
