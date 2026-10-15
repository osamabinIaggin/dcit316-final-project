"""Classification metrics with bootstrap intervals and paired significance tests."""

from __future__ import annotations

import math
import random

from sklearn.metrics import accuracy_score, f1_score

from src.corpus import LABELS


def silent_failure_rate(gold: list[str], pred: list[str]) -> float:
    """Share of genuinely non-neutral items that were predicted neutral."""
    pairs = [(g, p) for g, p in zip(gold, pred) if g != "neutral"]
    return sum(p == "neutral" for _, p in pairs) / len(pairs)


def score(gold: list[str], pred: list[str]) -> dict[str, float]:
    per_class = f1_score(gold, pred, labels=list(LABELS), average=None, zero_division=0)
    return {
        "accuracy": accuracy_score(gold, pred),
        "macro_f1": f1_score(gold, pred, labels=list(LABELS), average="macro", zero_division=0),
        "weighted_f1": f1_score(gold, pred, labels=list(LABELS), average="weighted", zero_division=0),
        **{f"f1_{lab}": float(v) for lab, v in zip(LABELS, per_class)},
        "predicted_neutral_rate": sum(p == "neutral" for p in pred) / len(pred),
        "silent_failure_rate": silent_failure_rate(gold, pred),
    }


def bootstrap_macro_f1(gold: list[str], pred: list[str], n: int = 1000,
                       seed: int = 22128981) -> tuple[float, float]:
    rng = random.Random(seed)
    idx = range(len(gold))
    stats = []
    for _ in range(n):
        sample = [rng.choice(idx) for _ in idx]
        stats.append(f1_score([gold[i] for i in sample], [pred[i] for i in sample],
                              labels=list(LABELS), average="macro", zero_division=0))
    stats.sort()
    return stats[int(0.025 * n)], stats[int(0.975 * n) - 1]


def mcnemar(gold: list[str], a: list[str], b: list[str]) -> dict[str, float]:
    """Exact two-sided McNemar test on items where exactly one system is right."""
    only_a = sum(x == g != y for g, x, y in zip(gold, a, b))
    only_b = sum(y == g != x for g, x, y in zip(gold, a, b))
    n, k = only_a + only_b, min(only_a, only_b)
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
    return {"only_a_correct": only_a, "only_b_correct": only_b, "p_value": p}
