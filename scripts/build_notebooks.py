#!/usr/bin/env python3
"""Write the four analysis notebooks and execute them so outputs are saved in place.

    .venv/bin/python scripts/build_notebooks.py

The slow model runs live in scripts/run_sentiment.py; the notebooks read its saved
outputs and recompute everything that runs in seconds.
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"

SETUP = """import sys, json
from pathlib import Path
ROOT = Path.cwd().parent
sys.path.insert(0, str(ROOT))
import pandas as pd
from IPython.display import Image, display, Markdown
pd.set_option("display.width", 160); pd.set_option("display.max_colwidth", 90)"""

NOTEBOOKS = {
    "01_documentation_audit.ipynb": [
        ("md", "# 01 · Documentation audit\n\nSearches the four audited papers for the six accountability "
               "criteria (A1–A6) and shows the evidence behind each cell of the disclosure matrix."),
        ("code", SETUP),
        ("code", "import subprocess\nprint(subprocess.run([sys.executable, str(ROOT/'scripts/audit_documentation.py')],"
                 " capture_output=True, text=True, cwd=ROOT).stdout)"),
        ("md", "## Disclosure matrix"),
        ("code", "pd.read_csv(ROOT/'reports/disclosure_matrix.csv')"),
        ("md", "## Evidence for the headline cells\n\nEach quote is located in text extracted from the PDF, in reading order."),
        ("code", """import re
def find(stem, pattern, width=260):
    t = (ROOT/f'reports/evidence/{stem}_prose.txt').read_text(errors='replace')
    flat = re.sub(r'\\s+', ' ', re.sub(r'-\\n\\s*', '', t))
    m = re.search(pattern, flat)
    return m.group(0)[:width] if m else 'NOT FOUND'
for stem, pat in [
    ('masakhaner2', r'translation corpus, MAFAND-MT.{0,330}'),
    ('masakhaner2', r'Table 2 reports.{0,200}'),
    ('afrisenti', r'A significant portion of tweets in Twi.{0,160}'),
    ('afrisenti', r'annotators who are native speakers of Twi.{0,260}'),
    ('afrihate', r'compensated.{0,80}'),
]:
    print(f'[{stem}]', find(stem, pat), '\\n')"""),
        ("md", "## Criterion match counts\n\nZero matches for A6 in every paper: none ships a datasheet or data statement."),
        ("code", """rows = []
for stem in ['afrisenti','afrihate','masakhaner2','flores_correction']:
    text = (ROOT/f'reports/evidence/matches_{stem}.md').read_text()
    for crit, n in re.findall(r'## (\\w+)\\n\\nPattern: .*?-  (\\d+) matches', text):
        rows.append({'paper': stem, 'criterion': crit, 'matches': int(n)})
pd.DataFrame(rows).pivot(index='criterion', columns='paper', values='matches')"""),
    ],
    "02_domain_ladder.ipynb": [
        ("md", "# 02 · Domain ladder\n\nHow far each Twi corpus sits from Twi as it is written on social media. "
               "FLORES-200 and MasakhaNER 2.0 are translations into Twi; AfriSenti is natively written."),
        ("code", SETUP),
        ("code", "import subprocess\nout = subprocess.run([sys.executable, str(ROOT/'scripts/run_ladder.py')], capture_output=True, text=True, cwd=ROOT)\nprint(out.stdout[-2500:])"),
        ("code", "pd.read_csv(ROOT/'reports/metrics/ladder_profile.csv').set_index('corpus').T.round(3)"),
        ("code", "json.loads((ROOT/'reports/metrics/ladder_overlap.json').read_text())"),
        ("code", "display(Image(str(ROOT/'reports/figures/fig1_domain_ladder.png'), width=760))"),
        ("md", "**Caveat.** English-token share is estimated with a lexicon built from FLORES English minus every "
               "word in FLORES Twi/Akan, so it is zero for FLORES by construction. Read it as a rough estimate for the "
               "other two corpora only."),
    ],
    "03_sentiment_experiment.ipynb": [
        ("md", "# 03 · Sentiment systems on natively written Twi\n\nAfriSenti Twi test split (n = 949). "
               "The TF-IDF baseline is retrained here; transformer and NLLB outputs are loaded from "
               "`reports/predictions/` and `data/derived/`, written by `scripts/run_sentiment.py`."),
        ("code", SETUP),
        ("code", """from collections import Counter
from src.corpus import load_afrisenti
train, dev, test = (load_afrisenti(s) for s in ('train','dev','test'))
print({s: len(x) for s, x in zip(('train','dev','test'), (train, dev, test))})
print('test labels:', Counter(t.label for t in test))"""),
        ("md", "## Baseline retrained live\n\nC is chosen on the dev split; the test split is used once."),
        ("code", """from scripts.run_sentiment import tfidf_logreg
from src.evaluation import score
pred, info = tfidf_logreg(train, dev, test)
print(info)
saved = pd.read_csv(ROOT/'reports/predictions/all_systems_test.csv', keep_default_na=False)
print('matches saved predictions:', (saved['tfidf_logreg'] == pred).mean())
{k: round(v, 4) for k, v in score([t.label for t in test], pred).items()}"""),
        ("md", "## All systems"),
        ("code", "pd.read_csv(ROOT/'reports/metrics/sentiment_results.csv', index_col=0)"),
        ("code", """res = json.loads((ROOT/'reports/metrics/sentiment_results.json').read_text())
pd.DataFrame({s: {'macro_f1_ci95': [round(x,3) for x in r['macro_f1_ci95']],
                  'mcnemar_p_vs_baseline': r.get('mcnemar_vs_tfidf_logreg', {}).get('p_value')}
              for s, r in res['results'].items()}).T"""),
        ("code", "res['notes']"),
        ("code", "display(Image(str(ROOT/'reports/figures/fig2_macro_f1.png'), width=760))\ndisplay(Image(str(ROOT/'reports/figures/fig3_neutral_collapse.png'), width=760))"),
        ("md", "## Translations: twi_Latn vs aka_Latn source code\n\nSame tweets, same model; only the declared source language changes."),
        ("code", """a = pd.read_csv(ROOT/'data/derived/translations_twi_Latn.csv', keep_default_na=False)['english']
b = pd.read_csv(ROOT/'data/derived/translations_aka_Latn.csv', keep_default_na=False)['english']
pd.DataFrame({'tweet': saved['text'], 'twi_Latn -> eng': a, 'aka_Latn -> eng': b}).head(12)"""),
    ],
    "04_error_analysis.ipynb": [
        ("md", "# 04 · Error analysis\n\nWhere each system fails, sliced by orthography, English mixing, length and emoji."),
        ("code", SETUP),
        ("code", "import subprocess\nout = subprocess.run([sys.executable, str(ROOT/'scripts/run_error_analysis.py')], capture_output=True, text=True, cwd=ROOT)\nprint(out.stdout[-1500:], out.stderr[-800:])"),
        ("code", "pd.read_csv(ROOT/'reports/metrics/slices.csv')"),
        ("code", "display(Image(str(ROOT/'reports/figures/fig4_confusion.png'), width=900))\ndisplay(Image(str(ROOT/'reports/figures/fig5_slices.png'), width=760))"),
        ("md", "## Sentiment lost in translation\n\nGold label positive or negative; NLLB twi_Latn → English → English model says neutral."),
        ("code", "pd.read_csv(ROOT/'reports/error_analysis/translation_sentiment_loss_sample.csv', keep_default_na=False)[['text','gold','nllb_twi_english','xlmt','tfidf_logreg']].head(12)"),
        ("md", "## Tweets every non-trivial system gets wrong"),
        ("code", "pd.read_csv(ROOT/'reports/error_analysis/all_systems_wrong_sample.csv', keep_default_na=False)[['text','gold','tfidf_logreg','xlmt','nllb_twi','orthography']].head(12)"),
        ("md", "## Label flips caused only by the source-language code"),
        ("code", "pd.read_csv(ROOT/'reports/error_analysis/source_code_flips_sample.csv', keep_default_na=False).head(10)"),
        ("code", "json.loads((ROOT/'reports/error_analysis/summary.json').read_text())"),
    ],
}


def main() -> int:
    NB.mkdir(exist_ok=True)
    ep = ExecutePreprocessor(timeout=900, kernel_name="dcit316")
    for name, cells in NOTEBOOKS.items():
        nb = nbf.v4.new_notebook()
        nb.cells = [nbf.v4.new_markdown_cell(s) if k == "md" else nbf.v4.new_code_cell(s) for k, s in cells]
        ep.preprocess(nb, {"metadata": {"path": str(NB)}})
        nbf.write(nb, NB / name)
        print(f"  executed {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
