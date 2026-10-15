#!/usr/bin/env python3
"""Slice the test-set predictions and draw the result figures.

    python3 scripts/run_error_analysis.py

Reads reports/predictions/all_systems_test.csv and reports/metrics/sentiment_results.json.
Writes reports/metrics/slices.csv, reports/error_analysis/*.csv and figures 2-5.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score

from src.corpus import DIGIT_FOR_VOWEL, LABELS, english_lexicon, surface_profile

METRICS = ROOT / "reports/metrics"
FIGURES = ROOT / "reports/figures"
ERRORS = ROOT / "reports/error_analysis"
SYSTEMS = ["majority", "tfidf_logreg", "english_only", "xlmt", "nllb_twi", "nllb_aka"]
NAMES = {
    "majority": "Majority class",
    "tfidf_logreg": "TF-IDF + LogReg (Twi-trained)",
    "english_only": "English Twitter-RoBERTa",
    "xlmt": "XLM-T (multilingual)",
    "nllb_twi": "NLLB twi_Latn -> English",
    "nllb_aka": "NLLB aka_Latn -> English",
}


def add_slices(df: pd.DataFrame) -> pd.DataFrame:
    english = english_lexicon()
    prof = pd.DataFrame([surface_profile(t, english) for t in df["text"]])
    df = pd.concat([df, prof], axis=1)
    df["orthography"] = np.select(
        [df["open_vowel_token_share"] > 0, df["digit_substitution"] == 1],
        ["uses ɛ/ɔ", "writes 3 for ɛ"], "neither")
    df["english_mix"] = pd.cut(df["english_token_share"], [-0.01, 0.0, 0.25, 1.0],
                               labels=["none", "1-25%", ">25%"])
    df["length"] = pd.cut(df["n_tokens"], [-1, 5, 12, 1000], labels=["<=5 tokens", "6-12", ">12"])
    df["emoji"] = np.where(df["has_emoji"] == 1, "has emoji", "no emoji")
    return df


def slice_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dim in ("orthography", "english_mix", "length", "emoji"):
        for value, part in df.groupby(dim, observed=True):
            row = {"dimension": dim, "slice": value, "n": len(part),
                   "gold_neutral_rate": round((part["gold"] == "neutral").mean(), 4)}
            for s in SYSTEMS[1:]:
                row[f"{s}_macro_f1"] = round(f1_score(part["gold"], part[s], labels=list(LABELS),
                                                      average="macro", zero_division=0), 4)
                row[f"{s}_pred_neutral"] = round((part[s] == "neutral").mean(), 4)
            rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    ERRORS.mkdir(parents=True, exist_ok=True)
    df = add_slices(pd.read_csv(ROOT / "reports/predictions/all_systems_test.csv", keep_default_na=False))
    res = json.loads((METRICS / "sentiment_results.json").read_text())["results"]

    slices = slice_table(df)
    slices.to_csv(METRICS / "slices.csv", index=False)

    trans = pd.read_csv(ROOT / "data/derived/translations_twi_Latn.csv", keep_default_na=False)["english"]
    trans_aka = pd.read_csv(ROOT / "data/derived/translations_aka_Latn.csv", keep_default_na=False)["english"]
    df["nllb_twi_english"], df["nllb_aka_english"] = trans, trans_aka
    keep = ["text", "gold", "tfidf_logreg", "english_only", "xlmt", "nllb_twi", "nllb_twi_english",
            "orthography", "english_mix"]
    lost = df[(df["gold"] != "neutral") & (df["nllb_twi"] == "neutral")]
    lost.sample(min(25, len(lost)), random_state=22128981)[keep].to_csv(
        ERRORS / "translation_sentiment_loss_sample.csv", index=False)
    wrong_all = df[(df["tfidf_logreg"] != df["gold"]) & (df["xlmt"] != df["gold"])
                   & (df["nllb_twi"] != df["gold"])]
    wrong_all.sample(min(25, len(wrong_all)), random_state=22128981)[keep].to_csv(
        ERRORS / "all_systems_wrong_sample.csv", index=False)
    flips = df[df["nllb_twi"] != df["nllb_aka"]]
    flips.sample(min(25, len(flips)), random_state=22128981)[
        ["text", "gold", "nllb_twi", "nllb_twi_english", "nllb_aka", "nllb_aka_english"]].to_csv(
        ERRORS / "source_code_flips_sample.csv", index=False)
    subst = df[df["digit_substitution"] == 1]
    copied = subst["nllb_twi_english"].map(lambda s: bool(DIGIT_FOR_VOWEL.search(s)))
    copy_through = {
        "tweets_with_3_for_e": int(len(subst)),
        "translations_still_containing_3_spellings": int(copied.sum()),
        "nllb_twi_pred_neutral_when_copied": round(float((subst.loc[copied, "nllb_twi"] == "neutral").mean()), 4),
        "nllb_twi_pred_neutral_when_not_copied": round(float((subst.loc[~copied, "nllb_twi"] == "neutral").mean()), 4),
        "nllb_twi_pred_neutral_tweets_without_3": round(float((df.loc[df["digit_substitution"] == 0, "nllb_twi"] == "neutral").mean()), 4),
    }
    summary = {
        "copy_through": copy_through,
        "gold_nonneutral_predicted_neutral_by_nllb_twi": int(len(lost)),
        "all_three_nonmajority_systems_wrong": int(len(wrong_all)),
        "nllb_twi_vs_aka_label_disagreements": int(len(flips)),
        "n_test": int(len(df)),
    }
    (ERRORS / "summary.json").write_text(json.dumps(summary, indent=2))

    order = SYSTEMS
    f1 = [res[s]["macro_f1"] for s in order]
    ci = np.array([res[s]["macro_f1_ci95"] for s in order])
    fig, ax = plt.subplots(figsize=(8.5, 4))
    colors = ["#9A9A9A", "#2F6B4F", "#B5482F", "#4C6A92", "#C9A227", "#D9C27A"]
    ax.barh([NAMES[s] for s in order], f1, xerr=[np.array(f1) - ci[:, 0], ci[:, 1] - np.array(f1)],
            color=colors, capsize=3)
    for i, v in enumerate(f1):
        ax.text(v + 0.02, i, f"{v:.3f}", va="center", fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Macro-F1 on AfriSenti Twi test (n = 949), 95% bootstrap CI")
    ax.set_title("Figure 2. Sentiment systems on natively written Twi")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig2_macro_f1.png", dpi=200)

    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    vals = [res[s]["predicted_neutral_rate"] for s in order[1:]]
    sfr = [res[s]["silent_failure_rate"] for s in order[1:]]
    x = np.arange(len(vals))
    ax.bar(x - 0.2, vals, 0.4, label="Predicted neutral rate", color="#4C6A92")
    ax.bar(x + 0.2, sfr, 0.4, label="Silent-failure rate (non-neutral called neutral)", color="#B5482F")
    gold_neutral = (df["gold"] == "neutral").mean()
    ax.axhline(gold_neutral, ls="--", color="black", lw=1)
    ax.text(len(vals) - 0.5, gold_neutral + 0.02, f"gold neutral rate {gold_neutral:.3f}", ha="right", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([NAMES[s] for s in order[1:]], fontsize=8, rotation=12)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title("Figure 3. How often each system defaults to neutral")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig3_neutral_collapse.png", dpi=200)

    shown = ["tfidf_logreg", "english_only", "xlmt", "nllb_twi"]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.4))
    for ax, s in zip(axes, shown):
        cm = confusion_matrix(df["gold"], df[s], labels=list(LABELS))
        ax.imshow(cm, cmap="Blues")
        for (i, j), v in np.ndenumerate(cm):
            ax.text(j, i, v, ha="center", va="center", fontsize=9,
                    color="white" if v > cm.max() / 2 else "black")
        ax.set_xticks(range(3))
        ax.set_xticklabels(["neg", "neu", "pos"])
        ax.set_yticks(range(3))
        ax.set_yticklabels(["neg", "neu", "pos"])
        ax.set_title(NAMES[s], fontsize=9)
        ax.set_xlabel("predicted")
    axes[0].set_ylabel("gold")
    fig.suptitle("Figure 4. Confusion matrices on the test split", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig4_confusion.png", dpi=200)

    heat = slices.set_index(["dimension", "slice"])[[f"{s}_macro_f1" for s in shown]]
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    ax.imshow(heat.values, cmap="RdYlGn", vmin=0, vmax=0.8, aspect="auto")
    for (i, j), v in np.ndenumerate(heat.values):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8)
    ax.set_xticks(range(len(shown)))
    ax.set_xticklabels([NAMES[s] for s in shown], fontsize=8, rotation=10)
    labels = [f"{d}: {s} (n={n})" for (d, s), n in zip(heat.index, slices["n"])]
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_title("Figure 5. Macro-F1 by slice of the test split")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig5_slices.png", dpi=200)

    print(slices.to_string(index=False))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
