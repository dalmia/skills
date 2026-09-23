# Lessons 2..48, one slide each. Lesson 1 is hand-written in course-base.html.
# Each entry: module index, title, kind, headline, text, before / now / us (one line each), why (red or orange box).
MODULES = [0, 1, 2, 3, 4, 5, 6, 7]

L = []
def add(m, title, kind, head, text, before, now, us, why=None):
    L.append(dict(m=m, title=title, kind=kind, head=head, text=text, before=before, now=now, us=us, why=why))

# ================================================================ MODULE 1  Turn-taking
add(0, "A transcript marked finished mid-sentence", "skip",
 "A turn closed mid-sentence because STT marked half a sentence as final",
 "Some STT services send a transcript marked final, then keep sending more words of the same sentence. Pipecat saw the final mark, skipped its wait, and closed the caller’s turn while the rest was still coming. The agent replied to half an answer. Pipecat 1.6.0 (PR #5043): when more words arrive after a final mark, that final mark is cancelled and the turn stays open.",
 "A transcript marked final closed the turn at once, even if more words were still coming.",
 "More words after a final mark cancel it. The turn stays open.",
 "Sarvam STT sends one transcript per turn, no partial text and no final mark. Never happened on our calls.",
 "Sarvam STT sends one transcript at the end of the caller’s turn, never partial text, and never the final mark this fix watches for. No words ever arrive after a final mark on our calls, so this bug could not happen.")

add(0, "One extra FILL FORM LLM call after a pause in bulk dictation", "over",
 "A brief pause mid-sentence in bulk dictation ran one extra FILL FORM LLM call, never a wrong reply. Fixed by upgrading",
 "Bulk dictation is when the caller says the whole form in one go. It closes turns with a different class, <code>TurnAnalyzerUserTurnStopStrategy</code>, which had the same bug as lesson 1: opening a turn wiped VAD’s record of whether the caller was speaking, so a brief pause mid-sentence started the 0.97 second wait for the Sarvam STT transcript. In bulk dictation we wrap that class in <code>deferred()</code>: when the wait ends it does not close the turn, it runs one FILL FORM LLM call instead. The only effect was one extra FILL FORM LLM call mid-dictation. Pipecat 1.7.0 (PR #5159): opening a turn no longer wipes that record. Nothing to do.",
 "A brief pause started the 0.97 second wait. Turn stayed open. One extra FILL FORM LLM call ran.",
 "Opening a turn no longer wipes VAD’s record of whether the caller was speaking.",
 "Bulk dictation no longer runs that extra FILL FORM LLM call. Fixed by upgrading.")

add(0, "Smart Turn stuck after a mute", "over",
 "Smart Turn could keep half-heard speech after a mute. At most one extra FILL FORM LLM call. Fixed by upgrading",
 "Smart Turn is the model that judges, in bulk dictation, whether the caller has finished. When we mute the caller, Smart Turn stops hearing audio mid-judgement. In 1.2.1, if the turn then ended some other way, nothing reset Smart Turn, and once audio flowed again it could report a finish for a turn already over. Pipecat 1.6.0 (PR #4967) resets Smart Turn whenever a turn ends. For us it needs a bulk dictation agent with <code>mute_user_while_agent_speaking</code> on, and a turn closed by our 120 second limit on one dictation turn. Even then <code>deferred()</code> limits it to one extra FILL FORM LLM call. Nothing to do.",
 "Smart Turn kept speech from a turn that was already over and could report a finish for it later.",
 "Smart Turn is reset every time a turn ends.",
 "Needs mute_user_while_agent_speaking on and the 120 second limit. At most one extra FILL FORM LLM call. Fixed by upgrading.")

add(0, "The NEXT REPLY LLM marking a turn finished too late", "skip",
 "A late NEXT REPLY LLM judgement closed a turn while the caller was talking again",
 "With <code>filter_incomplete_user_turns</code> on, Pipecat sends each caller turn to the NEXT REPLY LLM to judge whether it is complete. That judgement takes time. By the time it arrived, the caller had sometimes started talking again, and Pipecat closed the turn anyway, cutting them off. Pipecat 1.5.0 (PR #4938): a turn is not closed while VAD says the caller is speaking.",
 "The late NEXT REPLY LLM judgement closed the turn even if the caller was talking again.",
 "No turn closes while VAD hears the caller.",
 "filter_incomplete_user_turns is off in our code. No such judgement exists on our calls.",
 "We never turn on filter_incomplete_user_turns, so no such late judgement exists on our calls. The classes we use to end a caller’s turn already wait for the caller to stop.")

add(0, "Answering twice", "skip",
 "The caller heard two replies to one answer",
 "With <code>filter_incomplete_user_turns</code> on, Pipecat sends each caller turn to the NEXT REPLY LLM to judge whether it is complete. When that judgement said incomplete, Pipecat started a timer to re-prompt the caller. If that timer fired at the same moment the NEXT REPLY LLM’s reply arrived, both were spoken. Pipecat 1.5.0 (PR #4938): one spoken reply at a time, and the timer is cancelled when a reply starts.",
 "The re-prompt and the NEXT REPLY LLM’s reply could both play. The caller heard two replies.",
 "One spoken reply at a time. The timer is cancelled when a reply starts.",
 "filter_incomplete_user_turns is off in our code. Never happened on our calls.",
 "Both the timer and the fix live in UserTurnCompletionLLMServiceMixin, which only runs with filter_incomplete_user_turns on. We never turn it on.")

add(0, "Smart Turn’s time added to the wait", "over",
 "In bulk dictation, the wait after a pause ran long by Smart Turn’s thinking time. Fixed by upgrading",
 "After a pause in bulk dictation, <code>TurnAnalyzerUserTurnStopStrategy</code> waits 0.97 seconds for the Sarvam STT transcript. In 1.2.1 it ran Smart Turn first and started the 0.97 seconds only after Smart Turn answered, so Smart Turn’s time, 50 to 120 milliseconds by Pipecat’s own figure, was added on top. Pipecat 1.7.0 (PR #5007) counts the 0.97 seconds from the pause itself. For us, reaching that wait runs one FILL FORM LLM call (<code>deferred()</code> stops the class from ending the turn), so that call now starts 50 to 120 milliseconds earlier. Not measured on our servers. Nothing to do.",
 "The 0.97 second wait started only after Smart Turn answered. Smart Turn’s time was added on top.",
 "The 0.97 second wait is counted from the pause itself.",
 "The FILL FORM LLM call in bulk dictation starts 50 to 120 milliseconds earlier. Fixed by upgrading.")

add(0, "A re-prompt over a caller who had carried on", "skip",
 "The agent’s re-prompt talked over a caller who had already carried on talking",
 "With <code>filter_incomplete_user_turns</code> on, when the caller seemed to stop mid-answer, Pipecat spoke a re-prompt. In 1.2.1 only a full interruption cancelled it. A caller who simply carried on talking did not count as one, so the re-prompt talked over them. Pipecat 1.5.0 (PR #4938): the re-prompt is cancelled as soon as VAD hears the caller again.",
 "The re-prompt played over a caller who had carried on talking.",
 "The re-prompt is cancelled the moment VAD hears the caller.",
 "filter_incomplete_user_turns and user_idle_timeout are both off in our code. Never happened on our calls.",
 "That re-prompt exists only with filter_incomplete_user_turns on. Pipecat’s other prompt for a silent caller exists only with user_idle_timeout above 0. Our code sets neither.")

add(0, "A soft sound mid-word", "over",
 "A soft stretch inside a word could make VAD end the caller’s turn. Fixed by upgrading, on every call",
 "VAD (<code>SileroVADAnalyzer</code>) counts a 32 millisecond slice as speech only if Silero’s confidence is at least 0.7 and the loudness is at least 0.6. In 1.2.1 loudness was measured on each slice alone, so a soft stretch inside a word could fail six slices in a row: 0.2 seconds, the silence our VAD needs before it reports a stop. VAD reported a stop mid-word, and Sarvam STT sent its transcript early. Pipecat 1.8.0 (PR #5232) measures loudness over the last 400 milliseconds, so the loud start of the word keeps the soft middle above 0.6. Every call gets this. Not measured how often it happened. Nothing to do.",
 "Loudness measured per 32 millisecond slice. A soft middle of a word could read as silence, ending the turn.",
 "Loudness measured over the last 400 milliseconds. The loud start of the word covers the soft middle.",
 "Every call. Fewer turns cut mid-word. Fixed by upgrading.")

# ================================================================ MODULE 2  Calls that got stuck
add(1, "TTS replies with no audio", "over",
 "Pipecat 1.8.1 stops using TTS after 3 silent replies in a row. This PR turns that off",
 "Sometimes TTS answers a request with no audio. In 1.2.1 each line was tried on its own: one silent line, then the next one played. In 1.8.1 Pipecat counts silent replies, and after three in a row stops sending anything to TTS for the rest of the call: the call keeps running, the agent never speaks again (Pipecat 1.8.0, PR #5393). The limit is <code>max_consecutive_zero_audio_contexts</code>. This PR sets it to 0, which means no limit, on every TTS service in <code>bot.py</code>, so every line is tried, as in 1.2.1. A test fails if any TTS service in <code>bot.py</code> is created without that setting. Done in this PR.",
 "Every line is sent to TTS. A silent reply costs one silent line.",
 "After 3 silent replies in a row, Pipecat stops using TTS for the rest of the call.",
 "This PR sets the limit to 0, no limit. Behaviour stays as in 1.2.1. Done in this PR.")

add(1, "A caller muted for the whole call", "over",
 "A silent intro leaves the caller muted for the whole call. Our own mute class still has this bug. Fix after the merge",
 "With an intro script, we mute the caller until the intro and the first question have finished playing. If TTS returns no audio for the intro, it never finishes playing, so we never unmute: the caller talks and every word is dropped until they hang up. Pipecat 1.8.0 (PR #5390) changed its own class, <code>MuteUntilFirstBotCompleteUserMuteStrategy</code>: it also unmutes when TTS reports an error before the intro starts, and 1.8.1 reports no audio as an error, even with lesson 10’s limit at 0. Our class, <code>MuteUntilNthBotCompleteUserMuteStrategy</code> in <code>bot.py</code>, only watches for those lines finishing. Fix: make it also unmute on that TTS error, with a test. Not in this PR.",
 "Unmute only when the intro and first question finish playing. No audio, no unmute, caller muted all call.",
 "Pipecat’s MuteUntilFirstBotCompleteUserMuteStrategy also unmutes on a TTS error. Our MuteUntilNthBotCompleteUserMuteStrategy does not.",
 "Still broken for agents with an intro script. To fix after the merge.")

add(1, "A reply with no sound paused the call", "over",
 "On Sarvam TTS agents, a silent reply froze the call. Fixed by upgrading",
 "Sarvam TTS, used for languages other than English, Hindi and Hinglish, pauses the pipeline while a line plays so two lines never overlap, and unpauses when the line finishes playing. A line with no audio never finishes, so in 1.2.1 the pause stayed until the caller interrupted. Worst case was the closing line: our code sends it, then asks Pipecat to stop once it has played, and the stop waited behind the pause until the caller hung up. Pipecat 1.8.0 (PR #5394) pauses only when there is audio to wait for. Google TTS never pauses. Nothing to do.",
 "Sarvam TTS paused for every line. A silent line kept the pause on until the caller interrupted.",
 "Sarvam TTS pauses only when there is audio to wait for.",
 "Sarvam TTS agents no longer freeze on a silent line. Fixed by upgrading.")

add(1, "A stuck audio send", "over",
 "Sending audio to a browser or phone line that stopped taking it could hang the call forever. Fixed by upgrading",
 "The output transport sends the agent’s audio to the browser or the phone line. In 1.2.1, if the other side stopped taking audio but kept the connection open, one send could wait forever: the agent went silent and the call could not finish ending. Pipecat 1.8.0 (PR #5424) gives each send 10 seconds (<code>audio_out_write_timeout_secs</code>). After that the transport is marked unusable, later audio is dropped, and the call can end. Browser, Twilio and Exotel calls all get this. This hang never showed in our logs. Fixed by upgrading. Nothing to do.",
 "A send had no time limit. A browser or phone line that stopped taking audio kept the call from ending.",
 "Each send gets 10 seconds, then the call can end.",
 "Browser, Twilio and Exotel calls all get this. Never showed in our logs. Fixed by upgrading.")

add(1, "A hanging setup step", "over",
 "A call that could not finish setting up now ends after 20 seconds, not 5 minutes. Decided: leave it",
 "Before the agent can speak, the pipeline connects Sarvam STT and loads the noise filter model. In 1.2.1, if one of those hung, the caller heard silence until Pipecat’s 5 minute idle timeout ended the call. Pipecat 1.8.0 (PR #5316) gives that setup 20 seconds. After setup, a start signal passes through every part of the pipeline, and that gets another 20 seconds. If either runs longer, the call ends. The noise filter model is not in our Docker image, so the first call after each deploy downloads it inside those 20 seconds. Not measured; if it takes over 20 seconds, that first call ends. Decided: leave it for now.",
 "A hung setup meant silence for up to 5 minutes.",
 "Setup and start each get 20 seconds. If either runs longer, the call ends.",
 "First call after a deploy downloads the noise filter model within those 20 seconds. Time unmeasured. Decided: leave it.")

add(1, "One failed cleanup blocked the rest", "over",
 "One part failing to close no longer stops the others closing. Fixed by upgrading; our saved call data was never affected",
 "When a call ends, Pipecat asks each part of the pipeline to clean up: close Sarvam STT, stop the noise filter, and so on. In 1.2.1 this ran one part at a time, and one failure skipped every part after it, so those parts were never closed. Pipecat 1.8.0 (PR #5316) logs the failure and cleans up the rest. None of our own parts has a cleanup step, and saving the recording, transcript and metrics runs in our own code after the pipeline stops, so it was never affected. Fixed by upgrading. Nothing to do.",
 "Cleanup ran one part at a time. One failure skipped the rest.",
 "Every part is cleaned up. A failure is logged.",
 "Fixed by upgrading. Our saving of the recording, transcript and metrics never depended on this.")

add(1, "The goodbye that never got said", "skip",
 "A goodbye written by the NEXT REPLY LLM was never spoken",
 "With <code>filter_incomplete_user_turns</code> on, Pipecat 1.5.0 allowed one spoken reply per caller turn. The line Pipecat makes the agent say when the caller stays silent counts as a second reply in the same turn, so the NEXT REPLY LLM wrote it and Pipecat silently dropped it, including a final goodbye. Pipecat 1.2.1 did not have this limit. Pipecat 1.7.0 (PR #5146): that line is always spoken.",
 "Not in 1.2.1. From 1.5.0, the line for a silent caller was written and dropped. Goodbye unsaid.",
 "From 1.7.0 the line for a silent caller is always spoken.",
 "We do not turn on filter_incomplete_user_turns or use LLMMessagesAppendFrame. Our goodbye is a TTSSpeakFrame.",
 "Needs filter_incomplete_user_turns on and the silent-caller line sent with LLMMessagesAppendFrame. We use neither. Our closing line is a TTSSpeakFrame, spoken as written.")

add(1, "Closing lines cut off mid-sentence", "skip",
 "A closing line sent just before the pipeline ended was cut off",
 "<code>PipelineWorker.end()</code> stopped the pipeline at once, so a line sent just before it, such as a goodbye, was cut off mid-sentence. Pipecat 1.8.0 (PR #5399): <code>end()</code> and <code>activate_worker()</code> first wait for lines already sent to finish playing. Cancelling still stops at once.",
 "end() stopped at once. A goodbye sent just before was cut off.",
 "end() waits for lines already sent.",
 "We never call end(). Our closing line already played in full.",
 "Our code ends a call with stop_when_done(), which ends the call only after the closing line has played and did not change, or with cancel(), which stops at once in both versions. We never call end() or activate_worker().")

# ================================================================ MODULE 3  Browser and phone
add(2, "Firefox’s empty end-of-list entry made a connection request fail", "over",
 "Every Firefox browser call sent our server a request it answered with an error. Fixed by upgrading",
 "To connect a browser call, the browser sends our server its network addresses. Firefox always ends the list with an empty entry meaning no more addresses. In 1.2.1 that empty entry made Pipecat’s code fail, and our <code>PATCH /offer</code> route returned an error. The addresses before it were already added, so the call may still have connected; not checked. Pipecat 1.7.0 (PR #5126) accepts the empty entry. Fixed by upgrading. Nothing to do.",
 "Firefox’s empty end-of-list entry made our PATCH /offer route return an error.",
 "The empty entry is accepted as end of list.",
 "Firefox calls no longer hit that error. Whether they connected before is not known. Fixed by upgrading.")

add(2, "Early messages dropped on a slow browser", "skip",
 "Messages sent to the browser before it finished connecting were lost",
 "Beside audio, the server sends the browser small messages. In 1.2.1, on a slow network, a message sent before the browser had finished connecting was dropped, with no log. Pipecat 1.7.0 (PR #5112): messages are held and sent once the browser is connected.",
 "A message sent before the browser connected was dropped silently.",
 "The message is held and sent once the browser is connected.",
 "Our web page does not read the one message we send early, user-mute-started. Nothing showed before or after.",
 "The one message our server sends before the browser connects is user-mute-started, when the caller is muted for the intro. Our web page has no code that reads it, so nothing showed before and nothing shows now.")

add(2, "Browser audio at half speed", "skip",
 "Browser audio was read at half speed",
 "The browser sends audio at 48,000 samples a second, in stereo. Pipecat converts it to the pipeline’s rate, in mono. When the pipeline also ran at 48,000, Pipecat skipped the conversion, so the two stereo channels were read as one mono stream: garbled, at half speed. STT heard nonsense. Pipecat 1.7.0 (PR #5115): convert whenever stereo must become mono, not only when the rate differs.",
 "At 48,000 samples a second the stereo-to-mono conversion was skipped. Audio read at half speed.",
 "Conversion runs whenever stereo must become mono.",
 "Our browser calls run at 16,000 samples a second, so the conversion always ran. Never happened.",
 "run_bot_webrtc() runs our browser calls at 16,000 samples a second, so the rate never matched 48,000 and every piece of audio was converted in 1.2.1 too.")

add(2, "A dead audio track read 100 times a second", "over",
 "When a caller’s browser audio track died, the server logged 100 warnings a second. Now it logs once",
 "The server reads the caller’s browser audio in a loop. If the track ends mid-call, for example a headset unplugged, every read fails. In 1.2.1 the loop logged a warning, waited 10 milliseconds, and read again, about 100 warnings a second until the call ended. It did not tie up the CPU. Pipecat 1.3.0 (PR #4491) logs one warning, drops the dead track and stops reading it. Not checked how often a track dies mid-call on our calls. Fixed by upgrading. Nothing to do.",
 "A dead track: 100 warnings a second until the call ended.",
 "The dead track is dropped. One warning.",
 "One warning instead of 100 a second on browser calls. Fixed by upgrading.")

add(2, "Exotel messages used Twilio’s field name", "over",
 "Our Exotel messages now use Exotel’s spelling of the stream id. No behaviour change",
 "Every audio message we send to Exotel carries the call’s stream id. 1.2.1 labelled it <code>streamSid</code>, Twilio’s spelling. Exotel spells it <code>stream_sid</code>. Pipecat 1.8.0 (PR #5219) uses Exotel’s spelling. Pipecat’s changelog says Exotel treats the id as optional on messages from the bot, so the old spelling did no harm. Fixed by upgrading. Nothing to do.",
 "Audio messages to Exotel carried streamSid, Twilio’s spelling. Exotel treats the id as optional.",
 "They carry stream_sid, Exotel’s spelling.",
 "Applies to every Exotel call. No behaviour change. Fixed by upgrading.")

add(2, "Waiting on a phone line that had already closed", "over",
 "After a Twilio or Exotel caller hangs up, our server finishes the call up to 10 seconds sooner",
 "When a call ends, Pipecat closes the phone line and waits for Twilio or Exotel to confirm. If the line was already dead on their side, nothing confirmed, and 1.2.1 waited about 10 seconds before the call record was saved. Pipecat 1.4.0 (PR #4723) waits at most half a second (<code>ws_close_timeout</code>). A separate change in Pipecat 1.7.0 sets a 2 second wait for STT and TTS services that keep an open connection (a websocket) to their provider. Sarvam STT and Google TTS do not connect that way, so it does not touch us. Fixed by upgrading. Nothing to do.",
 "A dead phone line held the end of the call for about 10 seconds.",
 "The wait is at most 0.5 seconds.",
 "Twilio and Exotel calls end and get saved sooner. Fixed by upgrading.")

# ================================================================ MODULE 4  Numbers and records
add(3, "Token counts reported many times", "skip",
 "Pipecat counted one reply’s tokens several times when the provider sent a running count on every chunk",
 "The NEXT REPLY LLM streams its reply in chunks. Some providers attach the running token count to every chunk. Pipecat reported each one, so one reply could be added up three or four times in cost tracking. Pipecat 1.8.0 (PR #5190): keep the last count and report it once, when the reply ends.",
 "Every chunk with a token count was reported. One reply counted several times.",
 "The last count is reported once.",
 "OpenRouter, which our NEXT REPLY LLM uses, sends the count once. Not relevant to us.",
 "OpenRouter, which our NEXT REPLY LLM uses, sends the count once, in the last chunk (OpenRouter’s usage docs). The FILL FORM LLM does not go through this Pipecat code.")

add(3, "Why the Overall Latency chart is gone", "over",
 "Sarvam STT no longer reports a processing time. The playground chart that needed it is gone, and so is the page",
 "Pipecat 1.8.0 (PR #5209) stopped streaming STT services, Sarvam included, from reporting a processing time: audio arrives all the time, so there is no single piece of work to time. STT TTFB, the time to the first part of the transcript, is still sent. The playground page’s Overall Latency chart summed five timings per turn and needed that one, so it could never get a new point again. Our upgrade PR removed the chart, then deleted the playground page altogether (Module 6). The Call metrics dialog is unchanged: it reads <code>metrics.json</code>, which our own code fills without this Pipecat number. Fixed in this PR.",
 "Sarvam STT sent a processing time. The playground’s Overall Latency chart summed it with four others.",
 "No processing time from streaming STT. That chart could never draw again.",
 "Our upgrade PR removed the chart, then the whole playground page. Call metrics dialog unchanged. Fixed in this PR.")

add(3, "LLM response time measured the same way everywhere", "skip",
 "Three LLM classes measured response time from the wrong moment",
 "TTFB is the time from sending the request to the first part of the reply. <code>AnthropicLLMService</code> and <code>AWSBedrockLLMService</code> stopped the timer when the connection opened, before any reply. <code>GoogleLLMService</code> stopped it on a first chunk that could hold no text. Their numbers looked better than they were. Pipecat 1.8.0 (PR #5319): all classes stop at the first real content.",
 "Three LLM classes stopped the TTFB timer too early.",
 "All classes stop at the first real content.",
 "Our NEXT REPLY LLM uses OpenRouterLLMService, which measures TTFB the same way in both versions. Not relevant to us.",
 "We use none of those three. Our NEXT REPLY LLM goes through OpenRouterLLMService, which measures TTFB the same way in 1.2.1 and 1.8.1.")

add(3, "Dates read aloud in mixed languages", "skip",
 "A spoken date could mix two languages",
 "<code>normalize_dates()</code>, added in 1.5.0, turns a date in the reply into spoken words before TTS reads it. It took the month name from the server’s language setting, so a server set to German said “Mai 10th, two thousand and twenty-three”. Pipecat 1.6.0 (PR #4956): month names are always English.",
 "No normalize_dates() in 1.2.1. From 1.5.0, month name from the server’s language setting: “Mai 10th, two thousand and twenty-three”.",
 "Month names always English.",
 "Our code never adds normalize_dates() to a TTS service’s text_transforms. Not relevant to us.",
 "normalize_dates() runs only if a bot adds it to a TTS service’s text_transforms. Our code never does.")

add(3, "The saved words did not match what the NEXT REPLY LLM wrote", "skip",
 "The saved reply followed the TTS provider’s spelling, not the NEXT REPLY LLM’s",
 "Some TTS classes (ElevenLabs, Cartesia and others) report each word as they play it, and Pipecat built the saved reply from those reports. If the provider spelled a word differently, cafe for café, the transcript and the conversation history the NEXT REPLY LLM reads got the provider’s spelling. Pipecat 1.8.0 (PR #5370): match the words ignoring accents and save the NEXT REPLY LLM’s text.",
 "Saved reply built from the TTS provider’s word reports. cafe instead of café.",
 "Words matched ignoring accents. The NEXT REPLY LLM’s text is saved.",
 "Google TTS and Sarvam TTS do not report words as played. We always saved the NEXT REPLY LLM’s text.",
 "Google TTS and Sarvam TTS do not report each word as they play it. Pipecat saves the sentence exactly as the NEXT REPLY LLM wrote it, in both versions.")

# ================================================================ MODULE 5  Speed and memory
add(4, "Smart Turn stopped loading a large library", "over",
 "Every server start no longer loads the transformers library. Comes with the upgrade, nothing to do",
 "Smart Turn is the model bulk dictation uses to judge whether the caller has finished. In 1.2.1 loading Smart Turn also loaded transformers, a large library, to prepare the audio. Pipecat 1.3.0 (PR #4536) prepares it with a small numpy function, and Pipecat checked the prepared audio comes out almost exactly the same. Pipecat measured: peak memory about 566 MB to about 60 MB, load time about 5 seconds to about 0.3 seconds. <code>bot.py</code> loads Smart Turn at server start, so this happened on every start. Our install is not smaller: <code>pyproject.toml</code> still installs transformers and torch through the local-smart-turn option. Not measured on our server.",
 "Loading Smart Turn loaded transformers: about 566 MB peak memory, about 5 seconds to load, every server start.",
 "Smart Turn prepares audio with a small numpy function: about 60 MB peak memory, about 0.3 seconds to load.",
 "Every server start should be faster and use less memory. Not measured on our server. Install size unchanged. Comes with the upgrade.")

add(4, "Pipecat loads in half the time", "over",
 "Pipecat now loads NLTK on first use, so the server starts faster. The punkt_tab check moves to the first call after a deploy",
 "Loading Pipecat at server start used to load NLTK too, and through it scikit-learn and scipy. Pipecat 1.8.0 (PR #5253) loads NLTK on first use instead. Pipecat measured loading Pipecat going from about 2.2 seconds to about 1.0, once per server start. NLTK needs a data file, punkt_tab, which is not in our Docker image. In 1.2.1 the server checked for it, and downloaded it if missing, while starting. In 1.8.1 <code>PipelineWorker</code> does that check in the background during the first call’s setup after a deploy. Whether that makes the first call’s setup slower is not measured. Nothing to do; comes with the upgrade.",
 "Loading Pipecat took about 2.2 seconds because NLTK loaded with it. The punkt_tab check ran at server start.",
 "Loading Pipecat takes about 1.0 second. The punkt_tab check runs during the first call’s setup.",
 "Server starts faster. Whether the first call after a deploy is slower is not measured. Nothing to do.")

add(4, "Services now connect at the same time", "over",
 "Sarvam STT connects while the noise filter loads, instead of after it. Nothing to do",
 "Before a call starts, each part of the pipeline gets ready. In 1.2.1 this ran one part after another. Pipecat 1.8.0 (PR #5316) runs them all at once, so start-up takes as long as the slowest part. Only two of our parts do slow work at the start: Sarvam STT connecting, and the noise filter loading its model. Google TTS and OpenRouter open no connection at start. How much faster this makes a call start is not measured. Comes with the upgrade, nothing to do.",
 "Noise filter load, then Sarvam STT connect. One after the other.",
 "Both at the same time. Start-up takes as long as the slower one.",
 "Faster call start. How much is not measured. Comes with the upgrade, nothing to do.")

add(4, "The VAD thread is now shut down when the call ends", "over",
 "The VAD thread of a finished call is now shut down. Whether threads ever built up on our server was not checked",
 "<code>SileroVADAnalyzer</code> runs its model on a thread of its own (a background worker inside the server). In 1.2.1 nothing shut that thread down when the call ended. Pipecat 1.8.0 (PR #5350) shuts it down when the call is cleaned up. We build a new VAD per call. Python also ends an idle thread like this once nothing holds on to the finished call, so threads only built up if something kept old calls in memory. Not checked on our server. Fixed by upgrading, nothing to do.",
 "The VAD thread stayed until nothing held on to the finished call.",
 "The VAD thread is shut down when the call is cleaned up.",
 "Fixed by upgrading. Whether threads built up on our server was not checked.")

# ================================================================ MODULE 6  What we changed
add(5, "Scripted lines and the NEXT REPLY LLM’s context", "over",
 "New default: every scripted line enters the NEXT REPLY LLM’s context. This PR: only the intro does",
 "Every scripted line our code speaks (intro, acknowledgement, closing line, four more) has a setting, <code>append_to_context</code>: add this line to the NEXT REPLY LLM’s context. Old default: add only if a NEXT REPLY LLM reply came right after. That added the acknowledgement; our code then removed it for agents with fixed phrases. New default, Pipecat 1.4.0 (PR #4642): always add. With no setting, all seven lines would enter, and the NEXT REPLY LLM would copy the acknowledgement into every question. This PR: intro yes, the other six no; the removal code is deleted. Where the FILL FORM LLM words the acknowledgement, it now stays out too. Decided: keep it out.",
 "Default: add only if a reply came right after. The acknowledgement was added; our code removed it for fixed-phrase agents.",
 "Default: always add. Without a setting, all seven scripted lines would enter the context.",
 "This PR sets append_to_context on all seven lines: intro yes, the other six no. Done in this PR.")

add(5, "The noise filter’s model had to change", "over",
 "This PR sets the noise filter model to quail-vf-2.2-l-16khz. The old one does not load on the new aic-sdk",
 "The noise filter (ai-coustics, <code>AICFilter</code>) removes background noise before STT hears the caller. Pipecat 1.8.0 requires aic-sdk 3, so ours moved from 2.2.1 to 3.1.1. aic-sdk 3.1.1 needs model version v7, and our old model <code>quail-vf-2.1-l-16khz</code> is only published as v3 to v5: running it gives ModelDownloadError. This PR sets <code>AIC_MODEL_ID = \"quail-vf-2.2-l-16khz\"</code>, published as v7, which loads. It also adds <code>SafeAICFilter</code>: if the model ever fails to load, the call goes on without noise removal and the log says so. Tests check the model name and that the call goes on without noise removal.",
 "aic-sdk 2.2.1 with quail-vf-2.1-l-16khz.",
 "aic-sdk 3.1.1 needs model version v7. The 2.1 model has no v7: ModelDownloadError.",
 "This PR sets quail-vf-2.2-l-16khz, published as v7, and adds SafeAICFilter. Done.")

add(5, "Sarvam’s default moved to v4", "avail",
 "Pipecat’s default Sarvam STT model is now saaras:v4",
 "Pipecat 1.8.0 (PR #5382) changed the model <code>SarvamSTTService</code> uses when none is named, from saaras:v3 to saaras:v4. Our <code>bot.py</code> has named saaras:v3 since April 2026, so the default never applies to us and this PR did not change our model.",
 "Default model saaras:v3. We name saaras:v3 anyway.",
 "Default model saaras:v4. We still name saaras:v3.",
 "No change to our calls. Moving to v4 is one value, after a transcript comparison.",
 "One value in bot.py. First compare v3 and v4 transcripts on our own call audio. Same as Lesson 42 in Module 8.")

add(5, "Two classes were renamed", "over",
 "bot.py uses Pipecat’s new class names. Done in this PR",
 "Pipecat 1.3.0 renamed <code>PipelineTask</code> to <code>PipelineWorker</code> and <code>PipelineRunner</code> to <code>WorkerRunner</code>. Starting a call went from one step to two: <code>add_workers()</code>, then <code>run()</code>. The old names still work with a warning until Pipecat 2.0. Three other places still had the old names: the editor notes file <code>.cursor/rules/overview.md</code>, the imports in the recording tests, and one comment. All fixed in commit d9eb212.",
 "PipelineTask, PipelineRunner. Starting a call was one step.",
 "PipelineWorker, WorkerRunner. Starting a call is two steps: add_workers(), then run().",
 "bot.py, the tests and the notes all use the new names. Done.")

add(5, "The playground page is deleted", "over",
 "The playground page is deleted. Done in this PR",
 "The playground page, <code>/agents/&lt;agent id&gt;/playground</code>, was a test-call page with three tabs: Conversation, Logs, Metrics. Its Metrics tab had an Overall Latency chart that needed Sarvam STT’s processing time, which 1.8.1 no longer sends, so that chart could never draw again. First commit 1b4d93e removed the chart. Then, after you decided the page is not needed, the whole page was deleted, with the code only it used: MetricsPanel, MetricChart, LogsPanel, TabNavigation, and their tests. The public call page, <code>/agents/&lt;agent id&gt;</code>, is unchanged. Done in this PR.",
 "A playground page with a Metrics tab and an Overall Latency chart.",
 "1.8.1 no longer sends Sarvam STT’s processing time, so the chart could never draw again.",
 "The page and the code only it used are deleted. The public call page is unchanged. Done.")

# ================================================================ MODULE 7  Watch on deploy
add(6, "Recordings get longer", "over",
 "Recordings now include the time the caller is muted while the agent is not speaking",
 "<code>AudioBufferProcessor</code> builds the recording from the audio it receives from the caller and the agent. A silent caller still sends audio, so ordinary pauses were always in the file. What 1.2.1 left out: time when no audio reached it from either side. When our code mutes the caller, it drops the caller’s audio before it reaches <code>AudioBufferProcessor</code>. So when the agent was not speaking either, that stretch was missing. Example: between the intro and the first question, while the NEXT REPLY LLM writes it. Pipecat 1.3.0 (PR #4567) writes that stretch as silence. Recordings before and after the deploy are not directly comparable. Nothing to do.",
 "Time when the caller was muted and the agent silent was left out of the file.",
 "That time is written as silence.",
 "Recordings get longer, for example between the intro and the first question. Nothing to do.")

add(6, "Call durations get longer", "over",
 "Call duration in analytics gets longer on the deploy date, for agents with an intro script. Nothing to fix",
 "Each row in <code>transcript.json</code> has a timestamp: when our code wrote it. Call duration is the last row’s timestamp, plus its audio length, minus the first row’s. Before this PR the intro and the first question were one row, written when the question ended. This PR sends the intro with <code>append_to_context=True</code>, so the intro gets its own row, written when it ends. (Lesson 33 covers why: Pipecat 1.4.0 changed that default, so this PR sets it on every line.) The first timestamp is earlier, so the duration is longer, by the time to write and say the first question. How much longer is not measured. Nothing to fix.",
 "Intro + first question in one row. First timestamp when the question ended.",
 "Intro in its own row. First timestamp when the intro ended, earlier.",
 "Duration steps up on the deploy date, for agents with an intro script. Nothing to fix.")

add(6, "A broken API key now stops the service", "over",
 "A permanent STT or TTS error now marks the service unusable. For Sarvam STT the outcome is the same as before. Decided: leave it",
 "Pipecat 1.8.0 (PR #5242) marks STT or TTS unusable after a permanent error such as a rejected API key, and stops giving it work for the rest of the call, instead of retrying on every piece of audio. There is no setting to turn this off. <code>bot.py</code> does nothing when a service is marked unusable. For us the difference is small: Sarvam STT connects once, and in 1.2.1 a failed connect already gave one error and then dropped all caller audio. Not tested whether a Google TTS error is ever treated as permanent. A broken key looks like an agent that never hears the caller. Decided: leave it.",
 "A bad Sarvam key: one error, then all caller audio dropped for the rest of the call.",
 "A bad key: one error, STT marked unusable, all caller audio dropped for the rest of the call.",
 "For Sarvam STT the same outcome as before. No setting to turn it off. Decided: leave it.")

# ================================================================ MODULE 8  On the shelf
add(7, "A faster Sarvam STT service", "avail",
 "A second Sarvam STT class, built for lower delay",
 "Pipecat 1.8.0 (PR #5301) adds <code>SarvamRealtimeSTTService</code>: a different Sarvam server address, a different model (saaras:v3-realtime), and words sent as they are heard, not only at the end of the caller’s turn. Pipecat’s delay estimate for it is 1.00 seconds, against 1.17 seconds for <code>SarvamSTTService</code>, the class we use. Pipecat marks the 1.00 seconds as unmeasured.",
 "SarvamSTTService: transcript at the end of the caller’s turn. Delay figure 1.17 s.",
 "SarvamRealtimeSTTService: words as they are heard. Delay figure 1.00 s, unmeasured.",
 "Not used. A different model, so it needs a transcript quality check on our own calls.",
 "A few lines in bot.py to pick the new class, endpointing=\"manual\" so our own code, not Sarvam, decides when the caller’s turn ends, and a transcript quality check on our own calls, since it is a different model.")

add(7, "The newer Sarvam model, v4", "avail",
 "saaras:v4: a newer Sarvam STT model, with global English",
 "Pipecat 1.8.0 (PR #5382) adds saaras:v4 to <code>SarvamSTTService</code>. Same connection and settings as v3, plus what Sarvam calls global English (Pipecat’s changelog does not define it further), on top of Indian English and 22 Indian languages. It is also Pipecat’s new default, which we do not get because <code>bot.py</code> names saaras:v3.",
 "saaras:v3, named in bot.py.",
 "saaras:v4 available. Same settings, plus global English.",
 "Not used. One value to change, after comparing transcripts on our own calls.",
 "Change that one value, after comparing v3 and v4 transcripts on our own call audio.")

add(7, "Telling speech-to-text which words to expect", "avail",
 "Google, Cartesia and Smallest STT accept a list of words to listen for. Sarvam STT does not",
 "Google STT (adaptation, 1.8.0), Cartesia STT (keyterm, 1.7.0) and Smallest STT (keywords, 1.7.0) can be told which words to expect, so names like Anganwadi or a village are heard more reliably. Sarvam STT had a prompt setting in 1.2.1 that only the old saaras:v2.5 model honoured; our saaras:v3 ignored it and <code>bot.py</code> never set it. 1.8.0 removed it.",
 "Sarvam STT had a prompt setting our model ignored. Google, Cartesia and Smallest STT had no word list.",
 "Google, Cartesia and Smallest STT accept a word list. Sarvam’s unused prompt setting is removed.",
 "Not possible on SarvamSTTService. Would need SarvamRealtimeSTTService, effect unknown, or another STT provider.",
 "SarvamSTTService has no such setting now, and never had one our model honoured. SarvamRealtimeSTTService has a prompt setting, but Pipecat does not say whether it helps with specific words. Otherwise this needs a change of STT provider.")

add(7, "Phone keypad presses as an answer", "skip",
 "A keypad entry could stall the caller’s turn",
 "<code>DTMFAggregator</code> turns phone key presses into a transcript line such as DTMF: 3, so it counts as a spoken answer. It sent that line marked as not final, so Pipecat, waiting for a final transcript before ending the caller’s turn, kept waiting, and the turn hung. Pipecat 1.7.0 (PR #5172): the line is marked final.",
 "A keypad entry arrived marked not final. The turn could hang waiting.",
 "The keypad entry is marked final.",
 "We do not collect key presses. Twilio and Exotel send them, we drop them.",
 "DTMFAggregator is not in our pipeline. Twilio and Exotel send key presses, and we drop them.")

add(7, "Seconds of audio sent to STT", "avail",
 "Pipecat reports the seconds of audio sent to STT per call",
 "Pipecat 1.7.0 (PR #5055) adds this number, and it already arrives on our calls. Our <code>UsageObserver</code> keeps only NEXT REPLY LLM token counts and TTS character counts, so it drops this one. Today our STT cost is worked out after the call from the caller audio clips.",
 "Pipecat did not report seconds of audio sent to STT. Our STT cost came from the caller audio clips.",
 "Pipecat sends seconds of audio sent to STT. Our UsageObserver drops it.",
 "Not used. A few lines in UsageObserver would keep it.",
 "A few lines in UsageObserver to keep the number. Then decide: it counts all audio sent, silences included, while our current STT cost counts only the caller’s speech. Check which one Sarvam bills.")

add(7, "Numbers and dates spoken more naturally", "avail",
 "text_transforms: numbers, money and dates spoken as words before TTS reads them",
 "Pipecat 1.5.0 (PR #4854) adds <code>text_transforms</code> that rewrite a reply just before TTS reads it: Rs 500 as five hundred rupees, 10/05/2026 as tenth of May twenty twenty-six. <code>VoiceFormatter</code> bundles them. We use none.",
 "TTS reads the reply exactly as the NEXT REPLY LLM wrote it: “Rs 500”, “10/05/2026”.",
 "Optional rewrites before TTS: “five hundred rupees”, “tenth of May”.",
 "Not used. English words only, so English agents only.",
 "One setting on GoogleTTSService in bot.py. They write English words only, so a Hindi or Kannada agent would switch to English mid-sentence.")

add(7, "Thinking time measured apart from answering", "skip",
 "A new timing for the NEXT REPLY LLM: time to the first answer word, thinking excluded",
 "Pipecat’s existing timing for the NEXT REPLY LLM, TTFB, is the time from the request to the first token back. For a model that thinks before answering, that first token is a thinking token, so TTFB hides how long the caller really waited. Pipecat 1.8.0 (PR #5320) adds TTFAT: the time from the request to the first word of the actual answer, with thinking time reported separately.",
 "TTFB only: stops at the first thinking token.",
 "TTFAT added: time to the first answer word.",
 "We do not read TTFAT. We already have the same number from llm_services.py, in metrics.json.",
 "We do not read TTFAT. llm_services.py already saves, per turn, the time to the NEXT REPLY LLM’s first answer token after any thinking, in metrics.json. Same number.")

add(7, "New events for saving each turn’s audio", "avail",
 "New events: each turn’s audio once per turn, with the turn number",
 "Pipecat 1.8.0 (PR #5329) adds two events on <code>AudioBufferProcessor</code>, <code>on_user_turn_audio</code> and <code>on_bot_turn_audio</code>: each turn’s audio, once per turn, with the turn number. We still save turn audio from the old events: once per run of speech, several times a turn, no turn number. <code>bot.py</code> listens to the new <code>on_bot_turn_audio</code> only in 30 lines that recover the agent audio an interruption cuts off. Pipecat removes the old events in 2.0; our <code>pyproject.toml</code> does not allow Pipecat 2.0.",
 "Old events: audio once per run of speech, several times a turn, no turn number.",
 "New events: once per turn, with the turn number. Old events removed in Pipecat 2.0.",
 "Used only to recover cut-off agent audio. Switching fully deletes those 30 lines. Old events stay until Pipecat 2.0.",
 "Switch to the new events, delete those 30 lines, let turn_audio_recording.py use Pipecat’s turn number.")

# ---------------------------------------------------------------- build the structures build.py expects
VIS = {}
LESSONS = []
for i, e in enumerate(L):
    key = "s%d" % (i + 2)
    VIS[key] = "simple3(" + js({"before": e["before"], "after": e["now"], "us": e["us"]}) + ")"
    slide = [e["kind"], e["head"], e["text"], key]
    if e["why"]:
        slide.append(e["why"])
    LESSONS.append({"m": e["m"], "title": e["title"], "slides": [slide]})
assert len(L) == 47, len(L)
