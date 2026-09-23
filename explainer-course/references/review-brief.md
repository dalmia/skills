# Review brief for one course slide

Fill in the two placeholders, then hand this whole file plus the slide's block from
`review_dump.txt` to each review agent. One agent reads one lesson at a time.

You are reviewing slides of a training course about {{TOPIC, e.g. upgrading Pipecat 1.2.1 -> 1.8.1 in the form-bharo voice-agent repo}}.
The reader is {{READER, e.g. the product owner}}: not an engineer, impatient, wants to understand each change fast.
The reader has given this feedback repeatedly and it is the standard:

- Plain English. Short sentences. No jargon, no invented shorthand, no metaphors. Real names only:
  the actual product, provider, service, class, setting and file names, in code font for code names.
  NEVER a paraphrase in place of the real name ("voice service" for TTS, "the model" for a named LLM,
  "counts the audio", "ready-made rewrites", "stamped", "patch-up code", "written off", "track written").
- Every slide must say: what the bug/change is (what actually went wrong on a real run, or what is new),
  what changed, and what it means for the reader (fixed by upgrading / fixed in this PR / to fix after
  merge / decided to leave / not relevant / available not used). The reader should never have to ask
  "what is the bug?", "did the PR fix this or not?", or "which page/chart/file?".
- Title = the change or the bug itself, said plainly. Not a verdict-only title.
- Red lessons (banner NOT RELEVANT TO US): the body explains the bug plainly, and a separate red box says
  exactly why it does not apply (which feature is never turned on, which provider/class is not used).
  "Not relevant" means a feature or provider the reader does not use at all. An improvement to something
  the reader does use is never "not relevant"; it is orange.
- Orange lessons (banner IMPROVEMENT AVAILABLE. NOT USED YET): body says what is new, orange box says
  exactly what adopting it would take (which file, which setting, which decision).
- The visual is three boxes: Before / Now / What it means for us. Each box is one short line. The boxes
  must say exactly what the text says, in the same words, nothing extra, nothing contradictory. The
  visual is an aid to the text, not a second story.
- No number without saying what it counts. No claim not supported by the text. No "For us:" prefix in
  headlines.

Rate the slide on these 5 dimensions, PASS or FAIL, and for every FAIL give the exact replacement text
(the full corrected headline / body / box line / why box), not advice:

- D1 Plain language: banned words, jargon, sentence length, real names.
- D2 Complete: bug/change + what changed + what it means for the reader are all present and unambiguous.
- D3 Front-loaded and decisive: title states the thing; verdict (fixed / to fix / decided / not relevant /
  available) is unmistakable; red/orange box gives the concrete reason.
- D4 Visual matches text: the three boxes restate the text one line each, same facts, same names, no new
  claims, before/now/us are the right split.
- D5 Length: body under 110 words, each box line under 20 words, red/orange box under 45 words.

Output format, per slide:

    LESSON <n>: D1 PASS/FAIL, D2 PASS/FAIL, D3 PASS/FAIL, D4 PASS/FAIL, D5 PASS/FAIL
    Dx: <what is wrong, one line>
    FIX: <field>: <full replacement text>

Do not rewrite slides that pass. Do not add facts you cannot see in the slide text; if a fact is missing,
say what is missing and propose wording that stays inside what the slide already states.

To calibrate on what PASS looks like, read a few finished lessons in
`references/example-pipecat-course/lessons_m_all.py` before you start.
