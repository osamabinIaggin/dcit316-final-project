# Model card

This project trains one model, the TF-IDF baseline, and evaluates four public ones. Scores for all
of them are in `reports/metrics/sentiment_results.csv`; the figures below are copied from that file.

## TF-IDF + logistic regression (trained here)

| | |
|---|---|
| Task | Three-way sentiment (negative, neutral, positive) on Twi tweets |
| Features | Character 2- to 5-grams within word boundaries (min_df 2) plus word unigrams and bigrams, sublinear TF-IDF |
| Classifier | scikit-learn `LogisticRegression`, `class_weight="balanced"`, seed 22128981 |
| Selection | C from {0.25, 0.5, 1, 2, 4, 8}, chosen by macro-F1 on the AfriSenti Twi dev split |
| Training data | AfriSenti Twi train (3,481 tweets) |
| Test result | AfriSenti Twi test (n = 949): accuracy 0.675, macro-F1 0.593 (95% CI 0.559 to 0.625), neutral-class F1 0.31 |
| Intended use | A reference point for this study, and a cheap first model for Twi tweet sentiment |
| Out of scope | Any Twi that is not informal social media text, other Akan varieties (performance unknown), Ga, Ewe, and any decision about individual people |
| Known weaknesses | Learns surface strings, so spelling variation (`3` vs ɛ) splits evidence across features. Inherits AfriSenti's label noise (kappa 0.51). |

## Public models evaluated, not trained

| Model | Source | Trained on Twi? | Notes |
|---|---|---|---|
| Twitter-RoBERTa sentiment (latest) | `cardiffnlp/twitter-roberta-base-sentiment-latest` | No | English only |
| XLM-T sentiment | `cardiffnlp/twitter-xlm-roberta-base-sentiment` | No | 8 training languages, none African; tokenizer loaded from `FacebookAI/xlm-roberta-base` (see `failure_log.md`, F5) |
| NLLB-200 distilled 600M | `facebook/nllb-200-distilled-600M` | Twi and Akan are among its 200 languages | Used only as a Twi-to-English translator, greedy decoding |

## Ethical considerations

Sentiment scores aggregated over Twi tweets will be biased towards "neutral" if produced by any of
the English-trained systems here, which would understate how strongly Twi-speaking users feel about
whatever is being measured. None of these models should be used to judge individual users.
