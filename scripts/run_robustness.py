#!/usr/bin/env python3
"""Test the causes proposed in the error analysis, and the baseline's sensitivity.

    .venv/bin/python scripts/run_robustness.py

R1  Emoji ablation: rerun the English and XLM-T models with emoji removed.
R2  Spelling fix: rewrite in-word "3" as "ɛ", then rerun NLLB -> English model.
R3  McNemar test between the twi_Latn and aka_Latn translation runs.
R4  Baseline feature ablation: character only, word only, both, and word
    features with a token pattern that keeps emoji.

Writes reports/metrics/robustness.json and reports/predictions/robustness_*.csv.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from scripts.run_sentiment import (ENGLISH_MODEL, SEED, XLMT_MODEL, XLMT_TOKENIZER, cached,
                                   classify, translate)
from src.corpus import DIGIT_FOR_VOWEL, EMOJI, LABELS, load_afrisenti
from src.evaluation import bootstrap_macro_f1, mcnemar, score

PRED = ROOT / "reports/predictions"
METRICS = ROOT / "reports/metrics"
IN_WORD_3 = re.compile(r"(?<=[^\W\d_])3|3(?=[^\W\d_])", re.UNICODE)
EMOJI_TOKENS = r"(?u)\b\w\w+\b|[\U0001F000-\U0001FAFF☀-➿]"


def macro(gold, pred):
    return round(f1_score(gold, pred, labels=list(LABELS), average="macro", zero_division=0), 4)


def neutral_rate(pred):
    return round(sum(p == "neutral" for p in pred) / len(pred), 4)


def emoji_ablation(texts, gold, base):
    stripped = [re.sub(r"\s+", " ", EMOJI.sub(" ", t)).strip() or "." for t in texts]
    has = [bool(EMOJI.search(t)) for t in texts]
    idx = [i for i, h in enumerate(has) if h]
    out = {"n_with_emoji": len(idx)}
    for name, model, tok in (("english_only", ENGLISH_MODEL, None), ("xlmt", XLMT_MODEL, XLMT_TOKENIZER)):
        ablated = cached(PRED / f"robustness_{name}_no_emoji.csv", "pred",
                         lambda model=model, tok=tok: classify(model, stripped, tok))
        before = [base[name][i] for i in idx]
        after = [ablated[i] for i in idx]
        g = [gold[i] for i in idx]
        nonneutral_before = [i for i, p in zip(idx, before) if p != "neutral"]
        out[name] = {
            "macro_f1_with_emoji": macro(g, before),
            "macro_f1_emoji_removed": macro(g, after),
            "pred_neutral_with_emoji": neutral_rate(before),
            "pred_neutral_emoji_removed": neutral_rate(after),
            "nonneutral_predictions_with_emoji": len(nonneutral_before),
            "of_which_become_neutral": sum(ablated[i] == "neutral" for i in nonneutral_before),
            "unchanged_on_emoji_free_tweets": sum(ablated[i] == base[name][i]
                                                  for i in range(len(texts)) if not has[i]),
            "n_emoji_free": len(texts) - len(idx),
            "mcnemar_before_vs_after": mcnemar(g, before, after),
        }
    return out


def spelling_fix(texts, gold, base):
    idx = [i for i, t in enumerate(texts) if DIGIT_FOR_VOWEL.search(t)]
    fixed = [IN_WORD_3.sub("ɛ", texts[i]) for i in idx]
    english = cached(ROOT / "data/derived/translations_twi_Latn_3_to_e.csv", "english",
                     lambda: translate(fixed, "twi_Latn"))
    pred = cached(PRED / "robustness_nllb_twi_3_to_e.csv", "pred",
                  lambda: classify(ENGLISH_MODEL, english))
    xlmt = cached(PRED / "robustness_xlmt_3_to_e.csv", "pred",
                  lambda: classify(XLMT_MODEL, fixed, XLMT_TOKENIZER))
    g = [gold[i] for i in idx]
    old_eng = pd.read_csv(ROOT / "data/derived/translations_twi_Latn.csv", keep_default_na=False)["english"]
    return {
        "n_tweets_with_3_for_e": len(idx),
        "examples": [{"original": texts[i], "normalised": f} for i, f in list(zip(idx, fixed))[:5]],
        "nllb_twi": {
            "macro_f1_before": macro(g, [base["nllb_twi"][i] for i in idx]),
            "macro_f1_after": macro(g, pred),
            "pred_neutral_before": neutral_rate([base["nllb_twi"][i] for i in idx]),
            "pred_neutral_after": neutral_rate(pred),
            "translations_with_3_spellings_before": sum(bool(DIGIT_FOR_VOWEL.search(old_eng[i])) for i in idx),
            "translations_with_3_spellings_after": sum(bool(DIGIT_FOR_VOWEL.search(e)) for e in english),
            "mcnemar_before_vs_after": mcnemar(g, [base["nllb_twi"][i] for i in idx], pred),
        },
        "xlmt": {
            "macro_f1_before": macro(g, [base["xlmt"][i] for i in idx]),
            "macro_f1_after": macro(g, xlmt),
            "pred_neutral_before": neutral_rate([base["xlmt"][i] for i in idx]),
            "pred_neutral_after": neutral_rate(xlmt),
            "mcnemar_before_vs_after": mcnemar(g, [base["xlmt"][i] for i in idx], xlmt),
        },
    }


def feature_ablation(train, dev, test):
    configs = {
        "char_only": [("char_wb", (2, 5), None)],
        "word_only": [("word", (1, 2), None)],
        "char_plus_word (reported baseline)": [("char_wb", (2, 5), None), ("word", (1, 2), None)],
        "char_plus_word_keeping_emoji": [("char_wb", (2, 5), None), ("word", (1, 2), EMOJI_TOKENS)],
    }
    out = {}
    for name, specs in configs.items():
        vecs = [TfidfVectorizer(analyzer=a, ngram_range=r, min_df=2 if a == "char_wb" else 1,
                                sublinear_tf=True, **({"token_pattern": tp} if tp else {}))
                for a, r, tp in specs]
        xtr = hstack([v.fit_transform([t.text for t in train]) for v in vecs])
        xdv = hstack([v.transform([t.text for t in dev]) for v in vecs])
        xte = hstack([v.transform([t.text for t in test]) for v in vecs])
        ytr, ydv, yte = [t.label for t in train], [t.label for t in dev], [t.label for t in test]
        best_c, best = None, -1
        for c in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
            clf = LogisticRegression(C=c, max_iter=3000, class_weight="balanced", random_state=SEED).fit(xtr, ytr)
            s = f1_score(ydv, clf.predict(xdv), average="macro")
            if s > best:
                best_c, best = c, s
        clf = LogisticRegression(C=best_c, max_iter=3000, class_weight="balanced", random_state=SEED).fit(xtr, ytr)
        pred = list(clf.predict(xte))
        lo, hi = bootstrap_macro_f1(yte, pred)
        out[name] = {"chosen_C": best_c, "dev_macro_f1": round(best, 4),
                     "test_macro_f1": round(score(yte, pred)["macro_f1"], 4),
                     "test_macro_f1_ci95": [round(lo, 4), round(hi, 4)]}
    return out


def main() -> int:
    train, dev, test = (load_afrisenti(s) for s in ("train", "dev", "test"))
    texts, gold = [t.text for t in test], [t.label for t in test]
    saved = pd.read_csv(PRED / "all_systems_test.csv", keep_default_na=False)
    base = {c: saved[c].tolist() for c in ("english_only", "xlmt", "nllb_twi", "nllb_aka")}

    results = {
        "R1_emoji_ablation": emoji_ablation(texts, gold, base),
        "R2_spelling_fix": spelling_fix(texts, gold, base),
        "R3_twi_vs_aka": {
            "macro_f1_twi": macro(gold, base["nllb_twi"]),
            "macro_f1_aka": macro(gold, base["nllb_aka"]),
            "mcnemar": mcnemar(gold, base["nllb_twi"], base["nllb_aka"]),
        },
        "R4_feature_ablation": feature_ablation(train, dev, test),
    }
    (METRICS / "robustness.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
