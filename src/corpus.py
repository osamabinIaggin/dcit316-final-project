"""Loaders for the three Twi corpora and the surface features used to compare them."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"

LABELS = ("negative", "neutral", "positive")

# Twi's Latin alphabet has no c, j, q, v, x or z (MasakhaNER 2.0, Table 9).
NON_TWI_LETTERS = set("cjqvxz")
OPEN_VOWELS = set("ɛɔƐƆ")
TOKEN = re.compile(r"[^\W\d_]+(?:[3][^\W\d_]*)*|[^\W\d_]*3[^\W\d_]+", re.UNICODE)
DIGIT_FOR_VOWEL = re.compile(r"[^\W\d_]3|3[^\W\d_]", re.UNICODE)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿]")
HANDLE_OR_URL = re.compile(r"@\w+|https?://\S+|\bwww\.\S+")


@dataclass(frozen=True)
class Tweet:
    text: str
    label: str


def load_afrisenti(split: str) -> list[Tweet]:
    path = RAW / "afrisenti_twi" / f"{split}.tsv"
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE)
        return [Tweet(r["tweet"], r["label"]) for r in reader]


def load_flores(lang: str) -> list[str]:
    lines = []
    for split in ("dev", "devtest"):
        lines += (RAW / "flores200" / split / f"{lang}.{split}").read_text(
            encoding="utf-8").splitlines()
    return lines


def load_masakhaner_sentences() -> list[str]:
    sentences, current = [], []
    for split in ("train", "dev", "test"):
        for line in (RAW / "masakhaner2_twi" / f"{split}.txt").read_text(
                encoding="utf-8").splitlines():
            if not line.strip():
                if current:
                    sentences.append(" ".join(current))
                current = []
            else:
                current.append(line.split()[0])
    if current:
        sentences.append(" ".join(current))
    return sentences


def tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(HANDLE_OR_URL.sub(" ", text))]


def english_lexicon() -> set[str]:
    """English word types (FLORES English plus scikit-learn's stop list) absent from FLORES Twi and Akan."""
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

    eng = {t for line in load_flores("eng_Latn") for t in tokens(line)} | set(ENGLISH_STOP_WORDS)
    twi = {t for lang in ("twi_Latn", "aka_Latn")
           for line in load_flores(lang) for t in tokens(line)}
    return {t for t in eng - twi if len(t) > 2}


def surface_profile(text: str, english: set[str]) -> dict[str, float]:
    toks = tokens(text)
    n = max(len(toks), 1)
    return {
        "n_tokens": len(toks),
        "open_vowel_token_share": sum(any(c in OPEN_VOWELS for c in t) for t in toks) / n,
        "digit_substitution": int(bool(DIGIT_FOR_VOWEL.search(text))),
        "non_twi_letter_token_share": sum(any(c in NON_TWI_LETTERS for c in t) for t in toks) / n,
        "english_token_share": sum(t in english for t in toks) / n,
        "has_emoji": int(bool(EMOJI.search(text))),
        "has_handle_or_url": int(bool(HANDLE_OR_URL.search(text))),
        "word_final_open_vowel_share": sum(t[-1] in "ɛɔ" for t in toks) / n,
    }
