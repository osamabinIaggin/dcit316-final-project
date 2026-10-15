#!/usr/bin/env python3
"""Fill the manuscript template with numbers read from the saved results.

    .venv/bin/python scripts/fill_manuscript.py

Placeholders look like {{results.xlmt.macro_f1|.3f}} or {{ladder.AfriSenti twi.digit_substitution|%}}.
A placeholder that resolves to nothing stops the build.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "reports/metrics"
TEMPLATE = ROOT / "manuscript/FINAL_PROJECT_template.md"
OUT = ROOT / "FINAL_PROJECT_22128981_GideonElormGlago.md"


def context() -> dict:
    res = json.loads((M / "sentiment_results.json").read_text())
    slices = {f'{r["dimension"]}/{r["slice"]}': r for r in csv.DictReader((M / "slices.csv").open())}
    dist = res["notes"]["test_label_distribution"]
    src = res["notes"]["nllb_source_code"]
    derived = {
        "n_test": sum(dist.values()),
        "gold_neutral_rate": dist["neutral"] / sum(dist.values()),
        "translations_changed_by_code": src["n"] - src["identical_translations"],
        "labels_changed_by_code_rate": 1 - src["label_agreement_after_translation"],
        "copy_through_rate": (lambda c: c["translations_still_containing_3_spellings"]
                              / c["tweets_with_3_for_e"])(
            json.loads((ROOT / "reports/error_analysis/summary.json").read_text())["copy_through"]),
    }
    robust = json.loads((M / "robustness.json").read_text())
    r4 = robust["R4_feature_ablation"]
    robust["R4"] = {"char_only": r4["char_only"], "word_only": r4["word_only"],
                    "both": r4["char_plus_word (reported baseline)"],
                    "keep_emoji": r4["char_plus_word_keeping_emoji"]}
    return {
        "robust": robust,
        "derived": derived,
        "results": res["results"],
        "notes": res["notes"],
        "ladder": {r["corpus"]: r for r in csv.DictReader((M / "ladder_profile.csv").open())},
        "overlap": json.loads((M / "ladder_overlap.json").read_text()),
        "errors": json.loads((ROOT / "reports/error_analysis/summary.json").read_text()),
        "slices": slices,
    }


def resolve(ctx: dict, path: str):
    """Walk dotted keys, preferring the longest key so names like "MasakhaNER 2.0 twi" resolve."""
    node, parts = ctx, path.split(".")
    while parts:
        if isinstance(node, list):
            node = node[int(parts.pop(0))]
            continue
        for k in range(len(parts), 0, -1):
            key = ".".join(parts[:k])
            if key in node:
                node, parts = node[key], parts[k:]
                break
        else:
            raise KeyError(f"{path!r}: no key at {'.'.join(parts)!r}")
    return node


def render(match: re.Match, ctx: dict) -> str:
    path, _, fmt = match.group(1).partition("|")
    value = resolve(ctx, path.strip())
    if not fmt:
        return f"{value:,}" if isinstance(value, int) else str(value)
    value = float(value)
    if fmt == "%":
        return f"{value:.1%}"
    if fmt == "p":
        return "< 0.001" if value < 0.001 else f"{value:.3f}"
    return format(value, fmt)


def main() -> int:
    ctx = context()
    text = TEMPLATE.read_text()
    filled = re.sub(r"\{\{(.+?)\}\}", lambda m: render(m, ctx), text)
    OUT.write_text(filled)
    n = len(re.findall(r"\{\{", text))
    print(f"{OUT.name}: {n} placeholders filled, {len(filled.split()):,} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
