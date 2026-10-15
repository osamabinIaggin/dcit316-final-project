#!/usr/bin/env python3
"""Download the three Twi corpora used in the experiments, pinned by commit.

    python3 scripts/fetch_data.py

Writes to data/raw/ (not committed) and records URL, row count and SHA-256 in
data/raw/MANIFEST.md.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"

AFRISENTI_SHA = "5aec3cfcf87b59f885e98641f72e52182776429d"
MASAKHANER_SHA = "ba5843cd08aa491d5f96a5e809e71eb9ec461391"

AFRISENTI = "https://raw.githubusercontent.com/afrisenti-semeval/afrisent-semeval-2023/{sha}/data/twi/{split}.tsv"
MASAKHANER = "https://raw.githubusercontent.com/masakhane-io/masakhane-ner/{sha}/MasakhaNER2.0/data/twi/{split}.txt"
FLORES = "https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz"
FLORES_MEMBERS = [f"{split}/{lang}.{split}" for split in ("dev", "devtest")
                  for lang in ("twi_Latn", "aka_Latn", "ewe_Latn", "eng_Latn")]


def curl(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sfL", "--max-time", "180", "-o", str(out), url], check=True)


def main() -> int:
    rows = []
    for split in ("train", "dev", "test"):
        out = RAW / "afrisenti_twi" / f"{split}.tsv"
        url = AFRISENTI.format(sha=AFRISENTI_SHA, split=split)
        curl(url, out)
        rows.append((out, url))
        out = RAW / "masakhaner2_twi" / f"{split}.txt"
        url = MASAKHANER.format(sha=MASAKHANER_SHA, split=split)
        curl(url, out)
        rows.append((out, url))

    archive = RAW / "flores200.tar.gz"
    if not (RAW / "flores200").exists():
        curl(FLORES, archive)
        with tarfile.open(archive) as tar:
            for member in FLORES_MEMBERS:
                src = tar.extractfile(f"./flores200_dataset/{member}")
                dest = RAW / "flores200" / member
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src.read())
        archive.unlink()
    rows += [(RAW / "flores200" / m, FLORES) for m in FLORES_MEMBERS]

    lines = ["# Data manifest", "",
             "Fetched by `scripts/fetch_data.py`. Not committed; licences and "
             "access notes are in `data_card.md`.", "",
             "| File | Lines | SHA-256 (first 16) | Source |", "|---|---|---|---|"]
    for path, url in rows:
        n = sum(1 for _ in path.open(encoding="utf-8"))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        lines.append(f"| `{path.relative_to(RAW)}` | {n:,} | `{digest}` | {url} |")
    (RAW / "MANIFEST.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[4:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
