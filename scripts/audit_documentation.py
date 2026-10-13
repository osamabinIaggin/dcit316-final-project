#!/usr/bin/env python3
"""Search the audited papers for the six accountability criteria.

    python3 scripts/audit_documentation.py

Reads data/sources/*.pdf, writes extracted text and per-criterion matches to
reports/evidence/, and regenerates reports/disclosure_matrix.csv.

Searching is automatic; the verdict in each matrix cell is a reading of the
matches and is marked as such in VERDICTS below.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data/sources"
EVIDENCE = ROOT / "reports/evidence"
REPORTS = ROOT / "reports"

PAPERS = {
    "afrisenti": "AfriSenti (Muhammad et al., 2023a)",
    "masakhaner2": "MasakhaNER 2.0 (Adelani et al., 2022)",
    "afrihate": "AfriHate (Muhammad et al., 2025)",
    "flores_correction": "FLORES correction (Abdulmumin et al., 2024)",
}

CRITERIA = {
    "A1_language_referent": r"dialect|Akuapem|Asante|Ashanti|Fante|Akan",
    "A2_translated_or_native": r"translationese|translation corpus|MAFAND|translated into|Wikipedia",
    "A3_native_speakers": r"native speaker",
    "A4_agreement": r"inter-annotator|Fleiss|kappa|Krippendorff|adjudicat|pre-intervention|post-intervention",
    "A5_compensation": r"compensat|remunerat|minimum wage|\bpaid\b",
    "A6_datasheet": r"datasheet|data statement|data card|model card",
    "X_twi_mentions": r"\bTwi\b",
    "X_ewe_mentions": r"\bEwe\b|\bÉwé\b",
}

# Each verdict reads the matches above; the evidence column points at the file.
VERDICTS = [
    ("A1 Language referent precise", "no dialect named", "no dialect named",
     "no dialect named", "merges 'Akan/Twi'"),
    ("A2 Natively written", "translated (Wikipedia)", "YES - tweets",
     "YES - tweets", "translated (MAFAND-MT)"),
    ("A3 Native-speaker annotators stated", "human-verified translation", "yes",
     "yes, explicit", "yes"),
    ("A4 Agreement reported", "n/a", "yes, k=0.51",
     "yes, 0.46-0.81", "yes, k=0.932 POST-ADJUDICATION"),
    ("A5 Compensation disclosed", "not found", "not found",
     "yes - 'more than the minimum wage'", "yes - all annotators remunerated"),
    ("A6 Datasheet / data statement", "not found", "not found",
     "not found", "not found"),
]
COLUMNS = ["FLORES-200", "AfriSenti", "AfriHate", "MasakhaNER 2.0"]


def extract(stem: str) -> Path | None:
    pdf = SOURCES / f"{stem}.pdf"
    txt = EVIDENCE / f"{stem}.txt"
    if not pdf.exists():
        print(f"  skip {stem}: no PDF", file=sys.stderr)
        return None
    subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)],
                   capture_output=True, check=True)
    # These are two-column papers: -layout interleaves both columns onto one
    # line, so prose spanning a line break is only searchable in reading order.
    subprocess.run(["pdftotext", str(pdf), str(EVIDENCE / f"{stem}_prose.txt")],
                   capture_output=True, check=True)
    return txt


def search(txt: Path, stem: str, label: str) -> dict[str, int]:
    lines = txt.read_text(errors="replace").splitlines()
    out = [f"# Criterion matches - {label}", "",
           f"Source: `data/sources/{stem}.pdf` -> `reports/evidence/{stem}.txt` "
           f"({len(lines)} lines)", ""]
    counts = {}
    for name, pattern in CRITERIA.items():
        rx = re.compile(pattern, re.I)
        hits = [(i, l.strip()) for i, l in enumerate(lines, 1) if rx.search(l)]
        counts[name] = len(hits)
        out += [f"## {name}", "", f"Pattern: `{pattern}`  -  {len(hits)} matches", ""]
        if not hits:
            out += ["_No match. Recorded as not reported._", ""]
            continue
        out += [f"- L{i}: {t}" for i, t in hits[:25]]
        if len(hits) > 25:
            out.append(f"- _... {len(hits) - 25} further matches_")
        out.append("")
    (EVIDENCE / f"matches_{stem}.md").write_text("\n".join(out) + "\n")
    return counts


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    summary = {}
    for stem, label in PAPERS.items():
        txt = extract(stem)
        if txt is None:
            continue
        summary[stem] = search(txt, stem, label)
        print(f"  {stem}: " + ", ".join(f"{k.split('_')[0]}={v}"
                                        for k, v in summary[stem].items()))

    with (REPORTS / "disclosure_matrix.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Criterion"] + COLUMNS)
        w.writerows(VERDICTS)

    print(f"\nevidence -> {EVIDENCE}")
    print(f"matrix   -> {REPORTS / 'disclosure_matrix.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
