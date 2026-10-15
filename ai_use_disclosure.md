# AI-Use Disclosure and Verification Statement

Student: Gideon Elorm Glago (22128981)
Assignment: DCIT 316 Final Course Project, "Translationese All the Way Down"
Date: 15 October 2026

---

## 1. Declaration

No AI was used to fabricate data, results, figures or citations. Every number in the manuscript,
slides and cards is computed by a committed script from public data and written into the
manuscript by `scripts/fill_manuscript.py`. Nothing was typed from memory or estimated.

No AI system was used as an annotator or as a judge of Twi text. AfriSenti's human labels are the
only labels in this project.


## 2. What I decided and did myself

- The research questions, and the decision to audit existing resources instead of proposing a new
  model.
- Which criteria matter to a Ghanaian user, including the two criteria this paper adds: whether the
  text is natively written, and whether agreement scores are comparable.
- Not to grade translations or relabel tweets myself. I speak Twi, but I am not a trained translator
  or annotator, and one untrained rater is not a check on a benchmark labelled by three native
  speakers.
- Publishing the repository publicly while keeping the full tweet text out of it.
- Acting on the gradebook feedback from IA1 to IA6: testing proposed causes by intervention,
  scoping conclusions to the systems tested, and not treating non-significance as equivalence.

## 3. Verification performed

| Check | Result |
|---|---|
| `python -m pytest -q tests` | 9 passed |
| Fresh clone of the GitHub repo, data re-fetched, pipeline re-run | metrics, figures and filled manuscript identical to the committed files |
| Five notebooks executed top to bottom with nbconvert | 0 error outputs |
| Every quotation from an audited paper | located in text extracted from the PDF (`notebooks/01_documentation_audit.ipynb`) |
| Every reference | matched against the publisher's BibTeX, saved in `reports/references/` |
| Page ranges and author lists in the bibliography | match the saved BibTeX |
| Placeholders in the manuscript | 231 filled from results files, 0 left unfilled |
| Figures opened and inspected | axes, labels and legends readable |
| XLM-T tokenizer substitution | three English sentences classified positive, negative, neutral as expected |
| Emoji ablation sanity check | predictions on the 538 emoji-free tweets unchanged after removing emoji |

## 4. What I rejected or changed

- A draft quoted MasakhaNER 2.0's warning about translationese without the authors' next sentence
  ("However, we did not observe serious issues during the annotation."). Both sentences are now
  quoted, with the reason the second one does not answer the provenance question.
- A guessed ACL Anthology ID for Burchell et al. (2024) pointed to an unrelated paper. Every
  reference was then checked; the correct ID is `2024.eacl-long.38`.
- A draft claimed FLORES `aka_Latn` and `twi_Latn` differ by dialect. The measured difference in
  word-final ɛ/ɔ (0.166 vs 0.156) does not support it, so no dialect claim is made.
- A draft sentence said performance on tweets would be "about a third lower" than on FLORES.
  Nothing measured that, so it was removed.
- A draft said the twi_Latn and aka_Latn runs "score almost the same". It now reports the McNemar
  test (p = 0.69) and says this does not show equivalence.
- The error analysis proposed that copied `3` spellings cause NLLB's neutral calls. The spelling-fix
  test did not support it (p = 0.76), and the paper says so.
- The conclusions originally said in-domain data "beats every system that claims broader
  coverage". They are now limited to the systems and test set evaluated.

## 5. Responsibility statement

I understand and can explain every script, metric, figure, interpretation and limitation in this
repository. In particular I can explain why the baseline is trained on Twi while the comparison
systems are not; why macro-F1 and the silent-failure rate are the headline metrics on a test set
that is only 15% neutral; why MasakhaNER's κ = 0.932 and AfriSenti's κ = 0.51 cannot be compared;
what the emoji ablation shows and why the unchanged emoji-free predictions matter; why the spelling
fix helped XLM-T but not the translation pipeline; and why a non-significant McNemar result between
twi_Latn and aka_Latn is not evidence that they are equivalent.

The analytical judgements are mine, and so is responsibility for the submission.
