# Data Card - DCIT 316 Final Course Project

Compiled by: Gideon Elorm Glago (22128981)
Covers: AfriSenti Twi (all splits), MasakhaNER 2.0 Twi (sentences only), FLORES-200 `twi_Latn`,
`aka_Latn`, `ewe_Latn` and `eng_Latn`, and the four papers audited in Section 5.2.

---

## 1. In one line

The only human-labelled sentiment data for a Ghanaian language, compared against the two Twi
benchmarks that capability claims rest on, both of which are translations into Twi.

## 2. Provenance

| | AfriSenti Twi | MasakhaNER 2.0 Twi | FLORES-200 |
|---|---|---|---|
| Source | `afrisenti-semeval/afrisent-semeval-2023`, commit `5aec3cf` | `masakhane-io/masakhane-ner`, commit `ba5843c` | `dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz` |
| Text | Tweets | News sentences | Wikimedia sentences |
| Natively written | Yes | No: MAFAND-MT, French and English news translated into Twi | No: translated from English |
| Collection | Twitter Academic API, location heuristics around Ghana plus stopword lists and sentiment lexicons | Translation | Professional translation, human-verified |
| Labels used here | Sentiment (positive, neutral, negative) by native speakers | None; text only | None; text only |
| Size used | 3,481 train, 388 dev, 949 test | 6,056 sentences | 2,009 sentences per file |
| Licence | No licence file; the README asks users to cite the SemEval-2023 and AfriSenti papers | No licence file | As released by Meta |

Every file is fetched by `scripts/fetch_data.py` and checksummed in `data/raw/MANIFEST.md`.

## 3. Composition

AfriSenti Twi test split: positive 450, negative 353, neutral 146. Only 15.4% is neutral, which
shapes every metric in the paper: a system that defaults to "neutral" is wrong almost everywhere.

Surface profile (`reports/metrics/ladder_profile.csv`):

| Corpus | Mean tokens | Tokens with ɛ/ɔ | Texts writing `3` for ɛ | Texts with emoji |
|---|---|---|---|---|
| FLORES-200 `twi_Latn` | 25.3 | 28.5% | 0.05% | 0% |
| FLORES-200 `aka_Latn` | 25.8 | 26.1% | 0.10% | 0% |
| MasakhaNER 2.0 Twi | 23.4 | 34.6% | 0.03% | 0% |
| AfriSenti Twi | 9.3 | 5.6% | 42.5% | 41.2% |

## 4. Known quality problems

These are findings, each reproduced by a committed script.

### 4.1 AfriSenti's Twi labels are noisy, by its authors' own account

Inter-annotator agreement for Twi is κ = 0.51 (free-marginal), and the paper says "a significant
portion of tweets in Twi were ambiguous". The neutral class is small and probably the noisiest.

### 4.2 Language membership is mostly model-assigned

Native speakers labelled 2,000 tweets as Twi or not; a model trained on those assigned the rest.

### 4.3 No tweet can be tied to a place

The release has no per-tweet location. The corpus supports claims about Twi tweets collected around
Ghana, not about verified Ghanaian authors.

### 4.4 Collection may over-sample emotional tweets

Collection used sentiment lexicons, which could explain the small neutral class. Untested.

### 4.5 FLORES's two Twi files are unlabelled for dialect

`aka_Latn` and `twi_Latn` are independent translations (8 of 2,009 lines identical, vocabulary
Jaccard 0.358). Neither file says which variety it is, and switching between them as NLLB's source
code changes the sentiment label for 25.6% of test tweets.

### 4.6 A split-size mismatch is a header row, not an error

The paper's 3,482 / 389 / 950 are the files' line counts including the header.

## 5. Safe access and restrictions

All data is public and needs no account or key. Raw text is not committed, because the AfriSenti
and MasakhaNER repositories declare no licence. Committed derived files are the per-system
predictions keyed by row number, NLLB's English translations, and samples of at most 25 tweets per
error type.
