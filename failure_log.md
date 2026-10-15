# Failure log

Things that went wrong or turned out false, in the order they happened, and what changed because of
them.

| # | What happened | Effect on the project |
|---|---|---|
| F1 | The first topic was a routing-and-abstention mechanism for code-mixed sentiment. It could only be written as a proposal with no results. | Dropped. The project became an audit, which produces findings that can be checked. |
| F2 | `pdftotext -layout` interleaves the two columns of ACL papers on one line, so quotes that wrap across a line break could not be found. | Each paper is now extracted twice. The second pass, in reading order, is used for prose. |
| F3 | A draft quoted MasakhaNER 2.0's warning about translationese and left out the next sentence: "However, we did not observe serious issues during the annotation." | Caught by checking the quote against the reading-order text. The paper now quotes both sentences and argues why the second one concerns annotatability, not provenance. |
| F4 | A guessed ACL Anthology ID for Burchell et al. (2024) pointed to an unrelated paper. | Every reference was then checked against the Anthology's BibTeX. The correct ID is `2024.eacl-long.38`. |
| F5 | XLM-T's tokenizer files failed to load under transformers 5, which tried to read them as a tiktoken vocabulary. | XLM-T is loaded with the `FacebookAI/xlm-roberta-base` tokenizer, which has the same vocabulary. A three-sentence English sanity check gave positive, negative and neutral as expected. |
| F6 | The first experiment run died silently when its parent shell exited. The rerun then stalled on a Hugging Face download lock the dead process had left behind. | Lock cleared; NLLB weights downloaded with curl into `models/` and loaded from disk. |
| F7 | I expected FLORES `aka_Latn` and `twi_Latn` to differ in word-final ɛ/ɔ, a convention associated with Asante writing. The measured rates are 0.166 and 0.156. | No dialect claim is made. The finding that survives is that the two files are independent translations (8 of 2,009 lines identical). |
| F8 | The AfriSenti paper reports Twi splits of 3,482 / 389 / 950; the released files hold 3,481 / 388 / 949 rows. | Explained by the header row: the paper's figures equal the files' line counts. Recorded as resolved, not as a finding. |
| F9 | The English-token estimate uses a lexicon that excludes every FLORES Twi/Akan word, so it reads zero on FLORES by construction. | Reported with that caveat and not used to compare FLORES with the other corpora. |
| F10 | Ga's absence was confirmed against the FLORES-200 language list only. Dagbani was not checked against every resource. | The coverage table marks Dagbani as unconfirmed. |
| F11 | The error analysis linked NLLB's copied `3` spellings to its neutral predictions. Rewriting `3` as ɛ before translation removed the copying (188 translations to 2) but did not significantly change the pipeline's accuracy (McNemar p = 0.76). | The copy-through explanation is reported as not supported for the NLLB pipeline. The same rewrite did help XLM-T (p = 0.027), and the paper reports both. |
| F12 | The hackathon feedback asked for a small independently labelled test sample. I cannot label Twi sentiment reliably. | No such sample was made. The paper states this and treats AfriSenti's labels (κ = 0.51) as an unverified limitation, without claiming any specific label is wrong. |
