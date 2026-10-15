# Translationese All the Way Down

Auditing what "supports Twi" means in social media NLP resources.

Gideon Elorm Glago · 22128981 · DCIT 316: Computational Models for Social Media Mining ·
Department of Computer Science, University of Ghana

Manuscript: `FINAL_PROJECT_22128981_GideonElormGlago.pdf` · Slides:
`FINAL_PROJECT_22128981_GideonElormGlago_slides.pptx`

## Research questions

1. Accountability: what do public resources that claim Twi coverage disclose about the language
   variety, where the text came from, the annotators and their agreement?
2. Distribution: how far is the text those claims are measured on from Twi as written on social
   media?
3. Capability: how do the tools a Ghanaian analyst would reach for perform on natively written
   Twi tweets, against a baseline trained on Twi?

## Reproducing everything

Tested on macOS (Apple silicon), Python 3.14, with `pdftotext` (poppler) and Google Chrome installed.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/fetch_data.py            # corpora, pinned to commits, checksummed
.venv/bin/python scripts/fetch_sources.py         # the four audited papers
.venv/bin/python scripts/audit_documentation.py   # RQ1: criterion search over the papers
.venv/bin/python scripts/run_ladder.py            # RQ2: corpus surface statistics, Figure 1
.venv/bin/python scripts/run_sentiment.py         # RQ3: five systems on AfriSenti Twi test
.venv/bin/python scripts/run_error_analysis.py    # slices, error samples, Figures 2-5
.venv/bin/python scripts/build_notebooks.py       # executes notebooks/ with outputs saved
.venv/bin/python -m pytest -q tests               # unit tests
.venv/bin/python scripts/fill_manuscript.py       # writes numbers into the manuscript
.venv/bin/python scripts/build_pdf.py             # manuscript PDF
.venv/bin/python scripts/build_slides.py          # slides
```

`run_sentiment.py` downloads three models from Hugging Face on first run (about 4 GB in total) and
takes roughly 15 minutes on an M-series laptop, most of it NLLB translation. Model outputs are
cached in `reports/predictions/` and `data/derived/`; delete them to recompute.

## Data access

All data is public and needs no account or key. Raw corpora are not committed:
`scripts/fetch_data.py` downloads AfriSenti Twi and MasakhaNER 2.0 Twi from pinned GitHub commits and
FLORES-200 from Meta's release, and writes a checksum manifest to `data/raw/MANIFEST.md`. The
AfriSenti and MasakhaNER repositories declare no licence, so the text is fetched from source rather
than redistributed. Committed files derived from it are the model predictions and NLLB translations
needed to check the results. See `data_card.md`.

## Where every claim comes from

| Claim in the paper | File |
|---|---|
| Disclosure matrix (Table 2) | `reports/disclosure_matrix.csv`, evidence in `reports/evidence/matches_*.md` |
| Quotes from audited papers | `notebooks/01_documentation_audit.ipynb` (located in extracted text) |
| Corpus surface statistics (Table 3, Figure 1) | `reports/metrics/ladder_profile.csv` |
| Vocabulary coverage, FLORES aka vs twi | `reports/metrics/ladder_overlap.json` |
| System scores, CIs, McNemar (Table 4, Figure 2) | `reports/metrics/sentiment_results.csv`, `.json` |
| Neutral collapse (Figure 3) | `reports/metrics/sentiment_results.json` |
| Slice results (Table 5, Figure 5) | `reports/metrics/slices.csv` |
| Error counts and examples | `reports/error_analysis/` |
| Per-tweet predictions of every system | `reports/predictions/all_systems_test_ids.csv` (by test row) |
| NLLB translations (twi_Latn and aka_Latn) | `data/derived/translations_*.csv` |

Numbers in the manuscript are inserted by `scripts/fill_manuscript.py` from these files.

## Repository layout

| Path | Contents |
|---|---|
| `src/` | Corpus loaders, surface features, metrics |
| `scripts/` | Every step above, runnable in order |
| `notebooks/` | Four executed notebooks, one per stage |
| `tests/` | Unit tests for features and metrics |
| `reports/` | Metrics, figures, predictions, evidence, error analysis, verified BibTeX |
| `manuscript/` | Manuscript template with placeholders |

## Documentation

`data_card.md` · `model_card.md` · `ethics_statement.md` · `ai_use_disclosure.md` ·
`failure_log.md` · `literature_matrix.md` · `reproducibility_checklist.md`
