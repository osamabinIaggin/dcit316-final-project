#!/usr/bin/env python3
"""Evaluate five sentiment systems on the AfriSenti Twi test split.

    python3 scripts/run_sentiment.py

Systems:
  majority       most frequent training label
  tfidf_logreg   character + word TF-IDF, logistic regression trained on Twi (baseline)
  english_only   English Twitter-RoBERTa applied directly to Twi
  xlmt           multilingual XLM-T sentiment model, zero-shot on Twi
  nllb_twi       NLLB-200 (src twi_Latn) -> English, then english_only
  nllb_aka       NLLB-200 (src aka_Latn) -> English, then english_only

Model outputs are cached under reports/predictions/ and data/derived/, so a
rerun only recomputes what is missing.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from src.corpus import LABELS, load_afrisenti
from src.evaluation import bootstrap_macro_f1, mcnemar, score

PRED = ROOT / "reports/predictions"
DERIVED = ROOT / "data/derived"
METRICS = ROOT / "reports/metrics"
SEED = 22128981

ENGLISH_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
XLMT_MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
# XLM-T keeps xlm-roberta-base's vocabulary; its own tokenizer files fail to load
# under transformers 5 (misread as tiktoken). See failure_log.md, F4.
XLMT_TOKENIZER = "FacebookAI/xlm-roberta-base"
NLLB_MODEL = str(ROOT / "models/nllb-200-distilled-600M") if (ROOT / "models/nllb-200-distilled-600M/pytorch_model.bin").exists() else "facebook/nllb-200-distilled-600M"


def device():
    import torch
    return "mps" if torch.backends.mps.is_available() else "cpu"


def tfidf_logreg(train, dev, test) -> tuple[list[str], dict]:
    char = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
    word = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    xtr = hstack([char.fit_transform([t.text for t in train]), word.fit_transform([t.text for t in train])])
    xdv = hstack([char.transform([t.text for t in dev]), word.transform([t.text for t in dev])])
    xte = hstack([char.transform([t.text for t in test]), word.transform([t.text for t in test])])
    ytr, ydv = [t.label for t in train], [t.label for t in dev]
    search = {}
    for c in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        clf = LogisticRegression(C=c, max_iter=3000, class_weight="balanced", random_state=SEED)
        clf.fit(xtr, ytr)
        search[c] = f1_score(ydv, clf.predict(xdv), average="macro")
    best = max(search, key=search.get)
    clf = LogisticRegression(C=best, max_iter=3000, class_weight="balanced", random_state=SEED)
    clf.fit(xtr, ytr)
    return list(clf.predict(xte)), {"C_search_dev_macro_f1": search, "chosen_C": best}


def classify(model_name: str, texts: list[str], tokenizer: str | None = None) -> list[str]:
    from transformers import pipeline
    clf = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer or model_name,
                   device=device(), truncation=True, max_length=128)
    out = clf(texts, batch_size=32)
    return [o["label"].lower() for o in out]


def translate(texts: list[str], src: str) -> list[str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(NLLB_MODEL, src_lang=src)
    model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL).to(device()).eval()
    eng = tok.convert_tokens_to_ids("eng_Latn")
    out = []
    for i in range(0, len(texts), 16):
        batch = tok(texts[i:i + 16], return_tensors="pt", padding=True,
                    truncation=True, max_length=128).to(device())
        with torch.no_grad():
            gen = model.generate(**batch, forced_bos_token_id=eng, max_new_tokens=96, num_beams=1)
        out += tok.batch_decode(gen, skip_special_tokens=True)
        print(f"    {src}: {min(i + 16, len(texts))}/{len(texts)}", end="\r", flush=True)
    print()
    return out


def cached(path: Path, column: str, compute) -> list[str]:
    if path.exists():
        return pd.read_csv(path, keep_default_na=False)[column].tolist()
    t0 = time.time()
    values = compute()
    pd.DataFrame({column: values}).to_csv(path, index=False)
    print(f"  wrote {path.relative_to(ROOT)} in {time.time() - t0:.0f}s")
    return values


def main() -> int:
    for d in (PRED, DERIVED, METRICS):
        d.mkdir(parents=True, exist_ok=True)
    train, dev, test = (load_afrisenti(s) for s in ("train", "dev", "test"))
    texts, gold = [t.text for t in test], [t.label for t in test]

    preds, notes = {}, {}
    majority = max(LABELS, key=lambda lab: sum(t.label == lab for t in train))
    preds["majority"] = [majority] * len(test)
    preds["tfidf_logreg"], notes["tfidf_logreg"] = tfidf_logreg(train, dev, test)
    preds["english_only"] = cached(PRED / "english_only.csv", "pred",
                                   lambda: classify(ENGLISH_MODEL, texts))
    preds["xlmt"] = cached(PRED / "xlmt.csv", "pred", lambda: classify(XLMT_MODEL, texts, XLMT_TOKENIZER))
    for src, key in (("twi_Latn", "nllb_twi"), ("aka_Latn", "nllb_aka")):
        english = cached(DERIVED / f"translations_{src}.csv", "english",
                         lambda src=src: translate(texts, src))
        preds[key] = cached(PRED / f"{key}.csv", "pred",
                            lambda english=english: classify(ENGLISH_MODEL, english))

    results = {}
    for name, pred in preds.items():
        lo, hi = bootstrap_macro_f1(gold, pred)
        results[name] = {**score(gold, pred), "macro_f1_ci95": [lo, hi]}
        if name != "tfidf_logreg":
            results[name]["mcnemar_vs_tfidf_logreg"] = mcnemar(gold, preds["tfidf_logreg"], pred)

    a = pd.read_csv(DERIVED / "translations_twi_Latn.csv", keep_default_na=False)["english"]
    b = pd.read_csv(DERIVED / "translations_aka_Latn.csv", keep_default_na=False)["english"]
    notes["nllb_source_code"] = {
        "identical_translations": int((a == b).sum()),
        "n": len(a),
        "label_agreement_after_translation": float(np.mean(
            [x == y for x, y in zip(preds["nllb_twi"], preds["nllb_aka"])])),
    }
    notes["test_label_distribution"] = {lab: gold.count(lab) for lab in LABELS}
    notes["majority_label"] = majority

    table = pd.DataFrame(results).T
    table.index.name = "system"
    cols = ["accuracy", "macro_f1", "weighted_f1", "f1_negative", "f1_neutral", "f1_positive",
            "predicted_neutral_rate", "silent_failure_rate"]
    table[cols].astype(float).round(4).to_csv(METRICS / "sentiment_results.csv")
    (METRICS / "sentiment_results.json").write_text(json.dumps({"results": results, "notes": notes},
                                                               indent=2, default=float))
    out = pd.DataFrame({"text": texts, "gold": gold, **preds})
    out.to_csv(PRED / "all_systems_test.csv", index=False)
    out.drop(columns="text").rename_axis("test_row").to_csv(PRED / "all_systems_test_ids.csv")
    print(table[cols].astype(float).round(3).to_string())
    print(json.dumps(notes, indent=2, default=float))
    return 0


if __name__ == "__main__":
    sys.exit(main())
