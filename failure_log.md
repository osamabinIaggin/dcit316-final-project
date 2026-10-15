# Failure Log

Things that went wrong, or that I nearly got wrong, in the final project. Two of them changed a
conclusion.

Gideon Elorm Glago (22128981)

---

## 1. The first topic could not produce a result

What happened. The first design was a language-aware router that abstains on code-mixed comments.
It could only be written as a proposal: the mechanism had no results, and the contribution read as
"the model says it doesn't know".

Fix. Dropped it for an audit, which ends in findings that can be checked.

Why it matters. The brief scores evaluation, results and error analysis at 15 marks. A proposal
with no measurements would have scored nothing there.

## 2. Two-column PDFs broke the quote search

What happened. A search for MasakhaNER's translationese warning found nothing, though the sentence
is in the paper.

Cause. `pdftotext -layout` keeps the two columns of an ACL paper side by side, so a sentence that
wraps is split by text from the other column.

Fix. Each paper is extracted twice: `-layout` for tables, reading order for prose.

## 3. I quoted half of a passage

What happened. A draft quoted "We note that translationese may lead to undesired properties" and
stopped. The next sentence is "However, we did not observe serious issues during the annotation."

Fix. Found when the reading-order extraction made the full passage visible. The paper quotes both
sentences and explains that the second concerns annotatability, while the paper's question is
provenance.

Why it matters. Someone checking the source would have read the cut as selective quotation, and
they would have been right.

## 4. A guessed reference ID pointed at the wrong paper

What happened. The Anthology ID I used for Burchell et al. (2024) resolved to an unrelated paper on
controlled text generation.

Fix. Every reference was then checked against the publisher's BibTeX, now saved in
`reports/references/`. The correct ID is `2024.eacl-long.38`.

## 5. XLM-T would not load

What happened. transformers 5 tried to read XLM-T's SentencePiece vocabulary as a tiktoken file and
raised an error.

Fix. XLM-T is loaded with the `FacebookAI/xlm-roberta-base` tokenizer, which has the same
vocabulary. Three English sentences came out positive, negative and neutral as expected before the
full run.

## 6. The experiment died silently, then hung

What happened. The first background run exited with no traceback when its parent shell closed. The
rerun stalled at 335 MB of a 2.5 GB download, waiting on a lock the dead process had left.

Fix. Cleared the lock, downloaded the NLLB weights with curl into `models/`, and loaded them from
disk.

## 7. The dialect hypothesis did not survive measurement

What happened. I expected FLORES `aka_Latn` to show more word-final ɛ/ɔ than `twi_Latn`, as a sign of
an Asante versus Akuapem split.

Result. 0.166 against 0.156. No dialect claim is made. What does hold is that the two files are
independent translations: 8 of 2,009 lines are identical.

## 8. A "discrepancy" was a header row

What happened. AfriSenti's paper gives Twi splits of 3,482 / 389 / 950; the released files hold
3,481 / 388 / 949 rows. An earlier draft listed this as a finding.

Cause. The paper's figures equal the files' line counts, header included.

Fix. Recorded in the data card as resolved.

## 9. The spelling explanation did not hold up

What happened. The error analysis found that NLLB copies `3` spellings into its English output in
188 of 387 tweets, and that those tweets are called neutral more often (60.1% against 46.7%). I was
ready to write that the copied spellings cause the pipeline's neutral calls.

Test. Rewriting `3` as ɛ before translation removed the copying (188 translations to 2) and lowered
the neutral rate, but macro-F1 moved from 0.342 to 0.349, McNemar p = 0.76.

Fix. The paper reports the explanation as not supported for the NLLB pipeline. The same rewrite does
help XLM-T (0.322 to 0.362, p = 0.027), and the paper reports that too.

Why it matters. This is the correction I would most likely have missed: the correlation was clean
and the story was tidy. IA1's feedback was to separate hypotheses from verified causes, and this was
the case where they came apart.

## 10. I nearly called two settings equivalent

What happened. A draft said the twi_Latn and aka_Latn runs "score almost the same".

Fix. An exact McNemar test gives p = 0.69. The paper now says there is no evidence of an accuracy
difference, that this does not show equivalence, and that the code still changes the label for a
quarter of tweets.

