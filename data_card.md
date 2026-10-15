# Data card

Gideon Elorm Glago (22128981). Covers every dataset this project reads. None of the data is
committed to the repository; `scripts/fetch_data.py` downloads it, pinned to a commit, and
`data/raw/MANIFEST.md` records the checksum of each file.

## AfriSenti, Twi subset

| | |
|---|---|
| What it is | Tweets labelled positive, neutral or negative by native Twi speakers |
| Source | `afrisenti-semeval/afrisent-semeval-2023` on GitHub, commit `5aec3cf` |
| Size | 3,481 train, 388 dev, 949 test (4,818 tweets) |
| Test labels | positive 450, negative 353, neutral 146 |
| Agreement | Free-marginal multi-rater kappa 0.51 for Twi (AfriSenti paper, Table 5) |
| Language assignment | 2,000 tweets labelled as Twi by native speakers; the rest assigned by a model trained on those 2,000 |
| Licence | The data README asks users to cite the SemEval-2023 and AfriSenti papers. The repository declares no licence file, so I treat the data as research-use only and do not redistribute it |
| Personal data | Tweets are public posts. Handles and URLs appear to be stripped in the release (0 matches for `@` handles or URLs across 4,818 tweets) |

The paper reports the Twi splits as 3,482 / 389 / 950. Those are the line counts of the released
files including the header row, so the two sources agree once the header is excluded.

## MasakhaNER 2.0, Twi subset

| | |
|---|---|
| What it is | Named-entity annotations on Twi news text |
| Source | `masakhane-io/masakhane-ner`, commit `ba5843c`, all three splits |
| Use here | Surface statistics only (6,056 sentences). Entity labels are not used |
| Provenance | Twi text comes from MAFAND-MT, French and English news translated into Twi |
| Licence | No licence file in the repository; research use, not redistributed |

## FLORES-200

| | |
|---|---|
| What it is | 2,009 English Wikimedia sentences (dev + devtest) translated into each language |
| Source | `dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz` |
| Files read | `twi_Latn`, `aka_Latn`, `ewe_Latn`, `eng_Latn` |
| Use here | Surface statistics, vocabulary overlap, and the English lexicon used to estimate English-token share |
| Note | `aka_Latn` and `twi_Latn` are independent translations: 8 of 2,009 lines are identical and their vocabulary Jaccard similarity is 0.358 |

## Audited papers

Four PDFs (AfriSenti, MasakhaNER 2.0, AfriHate, the FLORES correction paper) are downloaded by
`scripts/fetch_sources.py`. Only short matched lines are committed, under `reports/evidence/`.

## Safe access

Committed derived files: per-system predictions keyed by test-row number
(`reports/predictions/all_systems_test_ids.csv`), the NLLB English translations, and samples of at
most 25 tweets per error type in `reports/error_analysis/`. The full tweet text stays out of the
repository.

Everything above is public and needs no account, key or approval. No private data, credentials or
scraped content is used. The models (Twitter-RoBERTa, XLM-T, NLLB-200 distilled 600M) are public on
Hugging Face and download on first run.
