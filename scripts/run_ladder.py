#!/usr/bin/env python3
"""Measure how far each Twi corpus sits from natively written social media text.

    python3 scripts/run_ladder.py

Writes reports/metrics/ladder_profile.csv, reports/metrics/ladder_overlap.json
and reports/figures/fig1_domain_ladder.png.
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
import pandas as pd

from src.corpus import (english_lexicon, load_afrisenti, load_flores,
                        load_masakhaner_sentences, surface_profile, tokens)

METRICS = ROOT / "reports/metrics"
FIGURES = ROOT / "reports/figures"


def corpora() -> dict[str, list[str]]:
    tweets = [t.text for s in ("train", "dev", "test") for t in load_afrisenti(s)]
    return {
        "FLORES-200 twi_Latn": load_flores("twi_Latn"),
        "FLORES-200 aka_Latn": load_flores("aka_Latn"),
        "MasakhaNER 2.0 twi": load_masakhaner_sentences(),
        "AfriSenti twi": tweets,
    }


def main() -> int:
    METRICS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    english = english_lexicon()
    data = corpora()

    rows = []
    for name, texts in data.items():
        prof = pd.DataFrame([surface_profile(t, english) for t in texts])
        row = {"corpus": name, "n_texts": len(texts)}
        row.update(prof.mean().round(4).to_dict())
        rows.append(row)
    profile = pd.DataFrame(rows)
    profile.to_csv(METRICS / "ladder_profile.csv", index=False)

    vocab = {k: {t for x in v for t in tokens(x)} for k, v in data.items()}
    tweet_tokens = [t for x in data["AfriSenti twi"] for t in tokens(x)]
    overlap = {}
    for name in ("FLORES-200 twi_Latn", "FLORES-200 aka_Latn", "MasakhaNER 2.0 twi"):
        overlap[name] = {
            "tweet_token_coverage": round(sum(t in vocab[name] for t in tweet_tokens) / len(tweet_tokens), 4),
            "tweet_type_coverage": round(len(vocab["AfriSenti twi"] & vocab[name]) / len(vocab["AfriSenti twi"]), 4),
        }
    a, t = load_flores("aka_Latn"), load_flores("twi_Latn")
    overlap["flores_aka_vs_twi"] = {
        "identical_lines": sum(x == y for x, y in zip(a, t)),
        "lines": len(a),
        "type_jaccard": round(len(vocab["FLORES-200 aka_Latn"] & vocab["FLORES-200 twi_Latn"])
                              / len(vocab["FLORES-200 aka_Latn"] | vocab["FLORES-200 twi_Latn"]), 4),
    }
    (METRICS / "ladder_overlap.json").write_text(json.dumps(overlap, indent=2))

    shown = {
        "open_vowel_token_share": "Tokens using ɛ/ɔ",
        "digit_substitution": "Texts writing 3 for ɛ",
        "non_twi_letter_token_share": "Tokens with c/j/q/v/x/z",
        "english_token_share": "English-lexicon tokens",
        "has_emoji": "Texts with emoji",
    }
    fig, ax = plt.subplots(figsize=(9, 4.2))
    width = 0.2
    colors = ["#4C6A92", "#8FA9C9", "#C9A227", "#B5482F"]
    for i, (_, r) in enumerate(profile.iterrows()):
        ax.bar([j + i * width for j in range(len(shown))], [r[k] for k in shown],
               width, label=r["corpus"], color=colors[i])
    ax.set_xticks([j + 1.5 * width for j in range(len(shown))])
    ax.set_xticklabels(shown.values(), fontsize=9)
    ax.set_ylabel("Share")
    ax.set_title("Figure 1. Surface profile of the three Twi corpora")
    ax.legend(fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES / "fig1_domain_ladder.png", dpi=200)

    print(profile.to_string(index=False))
    print(json.dumps(overlap, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
