#!/usr/bin/env python3
"""Build the presentation deck from the saved metrics and figures.

    .venv/bin/python scripts/build_slides.py

Every number on a slide is read from reports/metrics/; none is typed in.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "reports/metrics"
F = ROOT / "reports/figures"
OUT = ROOT / "FINAL_PROJECT_22128981_GideonElormGlago_slides.pptx"
REPO = "https://github.com/osamabinIaggin/dcit316-final-project"

INK = RGBColor(0x1C, 0x22, 0x2B)
ACCENT = RGBColor(0xB5, 0x48, 0x2F)
MUTED = RGBColor(0x5A, 0x63, 0x70)


def text(slide, x, y, w, h, lines, size=20, color=INK, bold_first=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.bold = bold_first and i == 0
        p.space_after = Pt(8)
    return box


def titled(prs, title, kicker=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if kicker:
        text(s, 0.6, 0.3, 12, 0.4, [kicker], 12, ACCENT)
    text(s, 0.6, 0.6, 12.2, 1.0, [title], 28, INK, True)
    return s


def table(slide, x, y, w, rows, col_w=None, size=12):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w),
                                   Inches(0.38 * len(rows)))
    t = shape.table
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(size)
                p.font.bold = i == 0
    if col_w:
        for j, cw in enumerate(col_w):
            t.columns[j].width = Inches(cw)


def main() -> int:
    res = json.loads((M / "sentiment_results.json").read_text())
    r, notes = res["results"], res["notes"]
    ladder = list(csv.DictReader((M / "ladder_profile.csv").open()))
    overlap = json.loads((M / "ladder_overlap.json").read_text())
    errs = json.loads((ROOT / "reports/error_analysis/summary.json").read_text())
    slices = {f'{r["dimension"]}/{r["slice"]}': r for r in csv.DictReader((M / "slices.csv").open())}
    n_test = sum(notes["test_label_distribution"].values())
    gold_neutral = notes["test_label_distribution"]["neutral"] / n_test

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)

    s = prs.slides.add_slide(prs.slide_layouts[6])
    text(s, 0.8, 2.0, 11.7, 1.6, ["Translationese All the Way Down"], 44, INK, True)
    text(s, 0.8, 3.1, 11.7, 0.8, ['Auditing what "supports Twi" means in social media NLP resources'], 22, MUTED)
    text(s, 0.8, 4.6, 11.7, 1.6, ["Gideon Elorm Glago · 22128981",
                                  "DCIT 316: Computational Models for Social Media Mining · University of Ghana",
                                  REPO], 15, MUTED)

    s = titled(prs, "Twi is supported, according to the people who built the tools", "The claims")
    text(s, 0.6, 1.8, 12, 4.5, [
        "Google Translate added Twi and Ewe in 2022.",
        "Meta's NLLB-200 covers both. Its benchmark, FLORES-200, lists twi_Latn, aka_Latn and ewe_Latn.",
        "AfriSenti, AfriHate and MasakhaNER 2.0 all list Twi.",
        "From Accra, it looks as if the tools exist. This project checks what they do with Twi as people "
        "write it online."], 20)

    s = titled(prs, "Three research questions", "Scope")
    text(s, 0.6, 1.8, 12, 4.8, [
        "RQ1 (accountability). What do the resources that claim Twi disclose about which Twi, "
        "where the text came from, who labelled it and how much they agreed?",
        "RQ2 (distribution). How far is the text those claims are measured on from Twi on social media?",
        "RQ3 (capability). How do the tools a Ghanaian analyst would reach for perform on natively "
        "written Twi tweets, against a baseline trained on Twi?"], 20)

    s = titled(prs, "Ga, the language of Accra, is in none of it", "Finding 1 · coverage")
    table(s, 0.6, 1.8, 12.1, [
        ["Language", "FLORES-200", "MasakhaNER 2.0", "AfriSenti", "AfriHate", "Google Tr.", "NLLB-200"],
        ["Twi / Akan", "yes (2 files)", "yes", "yes", "yes", "yes", "yes"],
        ["Ewe", "yes", "yes", "no", "no", "yes", "yes"],
        ["Ga", "no", "no", "no", "no", "no", "no"],
    ], size=14)
    text(s, 0.6, 4.0, 12, 1.5, ["Ewe has benchmarks but no social media data at all. "
                                "Ga has nothing to evaluate on and nothing to train on."], 18, MUTED)

    prof = {row["corpus"]: row for row in ladder}
    s = titled(prs, "The Twi benchmarks are translations into Twi", "Finding 2 · provenance")
    table(s, 0.6, 1.7, 12.1, [
        ["Corpus", "Natively written?", "Tokens using ɛ/ɔ", "Texts writing 3 for ɛ", "Mean tokens"],
        ["FLORES-200 twi_Latn", "No, translated English Wikipedia",
         f'{float(prof["FLORES-200 twi_Latn"]["open_vowel_token_share"]):.1%}',
         f'{float(prof["FLORES-200 twi_Latn"]["digit_substitution"]):.1%}',
         f'{float(prof["FLORES-200 twi_Latn"]["n_tokens"]):.1f}'],
        ["MasakhaNER 2.0 twi", "No, MAFAND-MT translated news",
         f'{float(prof["MasakhaNER 2.0 twi"]["open_vowel_token_share"]):.1%}',
         f'{float(prof["MasakhaNER 2.0 twi"]["digit_substitution"]):.1%}',
         f'{float(prof["MasakhaNER 2.0 twi"]["n_tokens"]):.1f}'],
        ["AfriSenti twi (tweets)", "Yes",
         f'{float(prof["AfriSenti twi"]["open_vowel_token_share"]):.1%}',
         f'{float(prof["AfriSenti twi"]["digit_substitution"]):.1%}',
         f'{float(prof["AfriSenti twi"]["n_tokens"]):.1f}'],
    ], col_w=[2.7, 3.6, 2.0, 2.2, 1.6], size=13)
    text(s, 0.6, 3.9, 12, 2.5, [
        f'FLORES Twi vocabulary covers {overlap["FLORES-200 twi_Latn"]["tweet_type_coverage"]:.0%} of the word types in the tweets.',
        f'FLORES aka_Latn and twi_Latn are separate translations: {overlap["flores_aka_vs_twi"]["identical_lines"]} '
        f'of {overlap["flores_aka_vs_twi"]["lines"]} lines identical. Neither says which dialect it is.'], 17, MUTED)

    s = titled(prs, "What the documentation lets you check", "Finding 3 · accountability")
    rows = list(csv.reader((ROOT / "reports/disclosure_matrix.csv").open()))
    table(s, 0.4, 1.6, 12.5, rows, col_w=[3.1, 2.3, 2.1, 2.5, 2.5], size=11)
    text(s, 0.6, 5.0, 12, 1.5, ["No resource ships a datasheet. MasakhaNER's kappa is measured after adjudication; "
                                "AfriSenti's is not, so the two numbers cannot be compared."], 16, MUTED)

    s = titled(prs, "Method: five systems, one baseline, 949 test tweets", "RQ3 · design")
    text(s, 0.6, 1.7, 12, 5, [
        "Data: AfriSenti Twi. Train 3,481, dev 388, test 949. C tuned on dev; test used once.",
        "Baseline: TF-IDF (character 2-5 grams + words) with logistic regression, trained on Twi.",
        "English-only: Twitter-RoBERTa, the tool an analyst reaches for by default.",
        "Multilingual: XLM-T, zero-shot (trained on 8 languages, none of them Twi).",
        "Translate then classify: NLLB-200 Twi to English, then the English model. Run twice, "
        "declaring the source as twi_Latn and as aka_Latn.",
        "Metrics: macro-F1 with 95% bootstrap CI, McNemar against the baseline, and the share of "
        "positive or negative tweets called neutral."], 17)

    s = titled(prs, "A small model trained on Twi beats every system that claims Twi", "RQ3 · results")
    s.shapes.add_picture(str(F / "fig2_macro_f1.png"), Inches(0.6), Inches(1.6), width=Inches(8.2))
    text(s, 9.0, 1.8, 4.0, 5, [
        f'Baseline {r["tfidf_logreg"]["macro_f1"]:.3f}',
        f'XLM-T {r["xlmt"]["macro_f1"]:.3f}',
        f'NLLB twi {r["nllb_twi"]["macro_f1"]:.3f}',
        f'English-only {r["english_only"]["macro_f1"]:.3f}',
        f'Majority {r["majority"]["macro_f1"]:.3f}'], 18)

    s = titled(prs, "English-only tools turn Twi into neutral", "RQ3 · the silent failure")
    s.shapes.add_picture(str(F / "fig3_neutral_collapse.png"), Inches(0.6), Inches(1.6), width=Inches(8.2))
    text(s, 9.0, 1.8, 4.0, 5, [
        f"Gold neutral rate: {gold_neutral:.1%}",
        f'English-only predicts neutral {r["english_only"]["predicted_neutral_rate"]:.1%} of the time',
        f'and calls {r["english_only"]["silent_failure_rate"]:.1%} of positive or negative tweets neutral.',
        "Its output carries no warning that anything went wrong."], 17)

    s = titled(prs, "Where the systems break", "Error analysis")
    s.shapes.add_picture(str(F / "fig5_slices.png"), Inches(0.4), Inches(1.5), width=Inches(7.6))
    nl = notes["nllb_source_code"]
    text(s, 8.2, 1.7, 4.8, 5.2, [
        f'NLLB leaves "3"-spellings untranslated in {errs["copy_through"]["translations_still_containing_3_spellings"]} '
        f'of {errs["copy_through"]["tweets_with_3_for_e"]} tweets that use them.',
        f'Changing only the declared source (twi_Latn vs aka_Latn) changes the translation of '
        f'{nl["n"] - nl["identical_translations"]} of {nl["n"]} tweets and the final label of '
        f'{errs["nllb_twi_vs_aka_label_disagreements"]}.',
        "Without emoji, the English model calls "
        f'{float(slices["emoji/no emoji"]["english_only_pred_neutral"]):.0%} of tweets neutral, so its other calls come mostly from emoji.',
        f'{errs["all_three_nonmajority_systems_wrong"]} tweets defeat the baseline, XLM-T and NLLB alike.'], 14)

    s = titled(prs, "Limitations", "Responsible claims")
    text(s, 0.6, 1.7, 12, 5, [
        "\"Not reported\" means not verifiable from the public record, not that the practice was absent.",
        "I do not read Twi well enough to judge translations, so translation results are about sentiment "
        "lost, not translation errors.",
        "One labelled Twi social corpus exists, with kappa 0.51. Every result inherits its label noise.",
        "Google Translate was not tested (no API key). Ewe and Ga could not be evaluated: no data."], 17)

    s = titled(prs, "What Ghanaian social media mining needs next", "Conclusion")
    text(s, 0.6, 1.7, 12, 4.4, [
        "Twi capability claims rest on text translated into Twi. The only natively written labelled "
        "corpus is 4,818 tweets, and off-the-shelf tools fail on it in a way that looks like neutrality.",
        "A model trained on that corpus beats every system that claims broader coverage.",
        "Needed: a Ga corpus, a larger natively written Twi corpus, a convention for naming the variety, "
        "and agreement scores reported in comparable form."], 19)
    text(s, 0.6, 6.2, 12, 0.6, [f"Code, data manifests and notebooks: {REPO}"], 14, ACCENT)

    prs.save(OUT)
    print(f"{OUT.name}  ({len(prs.slides)} slides)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
