# Translationese All the Way Down

Auditing what "supports Twi" means in social media NLP resources.

DCIT 316: Computational Models for Social Media Mining
Gideon Elorm Glago · 22128981 · Department of Computer Science, University of Ghana

## What this is

An accountability audit of every public resource that claims to cover a Ghanaian
language. Google Translate added Twi and Ewe in 2022; NLLB-200 covers both;
AfriSenti, AfriHate and MasakhaNER 2.0 all list Twi. This repository checks what
those claims deliver and what their documentation lets a third party verify.

Paper: `DCIT316_Audit_22128981_GideonElormGlago.docx` (source: the `.md` alongside it).

## Findings

- **Ga, the language of Accra, appears in none of the benchmarks surveyed.**
- The field does not agree what "Twi" denotes — FLORES-200 lists `aka_Latn` and
  `twi_Latn` separately, MasakhaNER 2.0 merges them as "Akan/Twi", AfriSenti says
  "Twi" unqualified. No resource names a dialect.
- **Both benchmarks that Twi capability claims rest on consist of text translated
  into Twi** — FLORES-200 from English Wikipedia, MasakhaNER 2.0 via MAFAND-MT from
  French/English news. The only natively written Twi corpus audited is 4,821 tweets.
- That corpus's authors flag it: "a significant portion of tweets in Twi were
  ambiguous." Its inter-annotator agreement is κ = 0.51.
- Agreement scores are not comparable across resources: MasakhaNER 2.0's κ = 0.932
  is post-adjudication, AfriSenti's κ = 0.51 is not.
- No resource audited ships a datasheet or data statement.

## Reproducing the audit

```
pip install -r requirements.txt
python3 scripts/fetch_sources.py        # downloads the 4 papers, writes MANIFEST.md
python3 scripts/audit_documentation.py  # extracts text, searches the 6 criteria
python3 scripts/build_docx.py           # renders the paper to .docx
```

`fetch_sources.py` records a SHA-256 for each download in
`data/sources/MANIFEST.md`, so the extraction can be checked against identical
files. The PDFs themselves are not committed.

## Layout

| Path | Contents |
|---|---|
| `scripts/fetch_sources.py` | Downloads the audited papers, records checksums |
| `scripts/audit_documentation.py` | pdftotext extraction and per-criterion search |
| `scripts/build_docx.py` | Markdown to Word for submission |
| `reports/evidence/matches_*.md` | Matched passages with line numbers, per paper |
| `reports/disclosure_matrix.csv` | The six criteria across four resources |
| `data/sources/MANIFEST.md` | URLs and checksums for the audited PDFs |

Each paper is extracted twice: `-layout` preserves table structure, and a second
pass in reading order makes prose searchable across the two-column layout.

## Criteria

| | Criterion |
|---|---|
| A1 | Is the language referent precise (Akan vs Twi vs dialect)? |
| A2 | Is the text natively written or translated? |
| A3 | Are native-speaker annotators stated? |
| A4 | Is agreement reported, and is it comparable? |
| A5 | Is annotator compensation disclosed? |
| A6 | Is a datasheet, data statement or model card present? |

A2 and A4 are this paper's contribution; the rest follow Gebru et al. (2021),
Mitchell et al. (2019) and Bender and Friedman (2018).

## Status

The capability half of the audit — language-ID degradation across the domain
ladder, and translate-then-classify on AfriSenti Twi — is specified in Section 5
of the paper and has not been run.
