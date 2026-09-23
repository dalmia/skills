# Writing rules for every slide

These came from the reader's corrections while the Pipecat course was built. Each one was
given after a slide broke it. Apply them to every lesson before any review round.

## Words

- Real names, every time. The provider (Sarvam, Google), the service (STT, TTS, VAD), the class
  (`MuteUntilFirstBotCompleteUserMuteStrategy`), the setting (`append_to_context`), the file
  (`bot.py`), the page ("the Call metrics dialog"). When two things share a generic name, always use
  the distinguishing one (for this repo: NEXT REPLY LLM vs FILL FORM LLM, never "the LLM").
- No paraphrase in place of a name. Rejected examples: "voice service", "sends audio" (say TTS),
  "the model", "counts the audio", "ready-made rewrites", "stamped", "patch-up code", "track written",
  "written off".
- No invented labels. Do not coin a phrase and reuse it. No "For us:" prefix. No quotes or capitals to
  turn a phrase into a term.
- No jargon words the reader has not met: no "frame", "flush", "guard", "hook", "race" unless the slide
  defines it in the same sentence with the real class name.
- Spell out what every number counts: "0.97 seconds of silence", "about 566 MB peak memory". Never a
  bare number.
- Short sentences, one idea each. No em-dashes. No metaphors, no analogies, no slang.

## What every slide must contain

1. The bug or the change itself, as it happened on a real run: who did what, what the caller/user saw.
2. What changed (name the version and the upstream PR number when there is one).
3. What it means for the reader, with an unmistakable verdict:
   fixed by upgrading / fixed in this PR / to fix after merge / decided: keep it / nothing to do /
   not relevant / improvement available, not used.
4. When the PR touched it: say plainly whether the PR fixed it or not. "Did the PR fix this?" must never
   be a question the reader has to ask.
5. Which page, chart, file or URL, when one is involved. Full URLs, local and production, never a partial
   path.

## Title and headline

- Sidebar title = the change or the bug, plainly ("TTS replies with no audio"), never a verdict alone
  ("Not relevant") and never a question.
- Headline = the bug or change in one sentence, plus the verdict at the end for relevant slides.
- Do not put "why not relevant" in the title. That goes in the red box.

## Relevance labels

- Red, "Not relevant to us": only a feature or a provider the reader does not use at all (a keypad
  aggregator not in the pipeline, a provider class never constructed). The body still explains the bug.
  The red box says exactly which feature is off or which class is not used.
- Orange, "Improvement available. Not used yet": anything that would improve what the reader already
  runs, that they have not adopted. The orange box says exactly what adopting it would take.
- Everything else is a normal slide, including performance and cost changes that arrive with an upgrade.
- Wrong classification was the most repeated correction. When unsure, it is orange, not red.

## Visual

- Three boxes, always: Before / Now / What it means for us. One line each, under 20 words.
- Each box restates the text in the same words. Nothing in a box that is not in the body. Nothing
  contradictory. The visual is an aid to the text, not a second story.
- No custom diagram unless the reader asked for a deep-dive lesson. The three boxes are the visual.

## Length and fit

- Body under 110 words. Box lines under 20 words. Red/orange box under 45 words.
- Every slide must fit without scrolling at 1440x900. Check the rendered page, not the source.

## Facts

- Every fact traced in the actual source (both versions, the diff, the repo). Never from memory of a
  changelog. Line numbers in a slide go stale after commits; prefer names over line numbers.
- Before saying something is not used, search every place it could be configured, not just the obvious
  one, and name where you looked.
- Reviewer findings are not facts. Trace each one in the code before applying it; overrule it when the
  code disagrees, and say so.
