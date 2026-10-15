# Model Card - Final Project TF-IDF Baseline

Author: Gideon Elorm Glago (22128981) | DCIT 316 Final Course Project
Status: coursework artefact, built as a comparison point. Not fit for deployment; see section 6.

---

## 1. Model details

| | |
|---|---|
| Name | `tfidf_logreg` |
| Architecture | `TfidfVectorizer(char_wb, 2- to 5-grams, min_df=2)` plus `TfidfVectorizer(word, 1- and 2-grams)`, both sublinear TF, into `LogisticRegression(class_weight="balanced", max_iter=3000)` |
| Target | Three-way sentiment (negative, neutral, positive) |
| Training data | AfriSenti Twi train, 3,481 tweets |
| Selection | C from {0.25, 0.5, 1, 2, 4, 8} by dev macro-F1; C = 4 chosen. Test split used once |
| Seed | 22128981 |
| Code | `scripts/run_sentiment.py`, `src/corpus.py`, `src/evaluation.py` |

## 2. Intended use

Intended: a reference point that answers whether systems claiming Twi support beat a simple model
trained on Twi.

Out of scope: measuring real public opinion, moderation, or any decision about a person.

## 3. Design decisions

- Character n-grams because Twi tweets spell the same word several ways (`yɛ`, `y3`, `ye`);
  sub-word pieces share evidence across spellings.
- Word n-grams use scikit-learn's default token pattern, which discards emoji and punctuation. The
  character n-grams keep them. Section 5 tests whether keeping emoji in the word features matters.
- Class weighting because the neutral class is 15% of the data.
- One small hyperparameter search on dev only, so the comparison with untuned off-the-shelf systems
  is not biased by tuning on test.

## 4. Evaluation results

AfriSenti Twi test, n = 949 (`reports/metrics/sentiment_results.csv`).

| System | Accuracy | Macro-F1 [95% CI] | Neutral F1 | Silent failure | McNemar p vs baseline |
|---|---|---|---|---|---|
| Majority class | 0.474 | 0.214 [0.205, 0.224] | 0.00 | 0.0% | < 0.001 |
| tfidf_logreg (this model) | 0.675 | 0.593 [0.559, 0.625] | 0.31 | 9.6% | n/a |
| English Twitter-RoBERTa | 0.251 | 0.243 [0.215, 0.271] | 0.28 | 83.3% | < 0.001 |
| XLM-T | 0.335 | 0.337 [0.306, 0.367] | 0.28 | 53.2% | < 0.001 |
| NLLB twi_Latn to English | 0.373 | 0.373 [0.343, 0.403] | 0.28 | 50.6% | < 0.001 |
| NLLB aka_Latn to English | 0.367 | 0.367 [0.336, 0.396] | 0.27 | 50.1% | < 0.001 |

Silent failure is the share of positive or negative tweets predicted neutral.

## 5. Sensitivity

| Variant | C | Test macro-F1 [95% CI] |
|---|---|---|
| Character only | 8 | 0.578 [0.548, 0.609] |
| Word only | 4 | 0.569 [0.537, 0.602] |
| Both (this model) | 4 | 0.593 [0.559, 0.625] |
| Both, word tokens keep emoji | 4 | 0.585 [0.553, 0.617] |

The intervals overlap; the result does not depend on the feature set, and keeping emoji in the word
features gives no measurable gain.

## 6. Limitations and risks

- It learns surface strings. A spelling it has not seen gives it nothing to work with.
- The neutral class is its weak point (F1 0.31), and that class is the smallest and probably the
  noisiest in AfriSenti (κ = 0.51).
- Trained and tested on one corpus of tweets collected around Ghana. Performance on other Twi text,
  other Akan varieties, Ga or Ewe is unknown.
- Beating the off-the-shelf systems here does not show that no multilingual model could do better.
  An Africa-centric model fine-tuned on AfriSenti was not tested.

## 7. Other models evaluated, not trained

| Model | Source | Trained on Twi? | Note |
|---|---|---|---|
| Twitter-RoBERTa sentiment (latest) | `cardiffnlp/twitter-roberta-base-sentiment-latest` | No | English only |
| XLM-T sentiment | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | No | Eight training languages, none African; tokenizer from `FacebookAI/xlm-roberta-base` (`failure_log.md` #5) |
| NLLB-200 distilled 600M | `facebook/nllb-200-distilled-600M` | Twi and Akan among its 200 languages | Used only as a translator, greedy decoding |
