#!/usr/bin/env python3
"""Download the audited papers and record a checksum for each.

    python3 scripts/fetch_sources.py

Sources land in data/sources/ and are not committed; data/sources/MANIFEST.md
records the URL, size and SHA-256 so a reader can obtain identical files.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/sources"

SOURCES = {
    "afrisenti.pdf": "https://aclanthology.org/2023.emnlp-main.862.pdf",
    "masakhaner2.pdf": "https://aclanthology.org/2022.emnlp-main.298.pdf",
    "afrihate.pdf": "https://aclanthology.org/2025.naacl-long.92.pdf",
    "flores_correction.pdf": "https://arxiv.org/pdf/2409.00626",
}


def fetch(name: str, url: str) -> Path | None:
    out = DEST / name
    if out.exists() and out.stat().st_size > 10_000:
        print(f"  have {name}")
        return out
    print(f"  get  {name}")
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "90", "-o", str(out), url],
        capture_output=True,
    )
    if result.returncode != 0 or not out.exists() or out.stat().st_size < 10_000:
        print(f"  FAIL {name} <- {url}", file=sys.stderr)
        out.unlink(missing_ok=True)
        return None
    return out


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, url in SOURCES.items():
        path = fetch(name, url)
        if path is None:
            rows.append((name, url, "FAILED", "-"))
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append((name, url, f"{path.stat().st_size:,} B", digest[:16]))

    manifest = ["# Source manifest", "",
                "Papers audited in Section 4. Not committed; re-fetch with "
                "`python3 scripts/fetch_sources.py`.", "",
                "| File | URL | Size | SHA-256 (first 16) |",
                "|---|---|---|---|"]
    manifest += [f"| `{n}` | {u} | {s} | `{d}` |" for n, u, s, d in rows]
    (DEST / "MANIFEST.md").write_text("\n".join(manifest) + "\n")

    failed = [r for r in rows if r[2] == "FAILED"]
    print(f"\n{len(rows) - len(failed)}/{len(rows)} fetched -> {DEST}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
