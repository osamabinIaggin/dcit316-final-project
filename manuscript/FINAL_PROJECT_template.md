# Translationese All the Way Down

Auditing what "supports Twi" means in social media NLP resources

<div class="authors">
Gideon Elorm Glago · Student ID 22128981<br/>
Department of Computer Science, University of Ghana<br/>
DCIT 316: Computational Models for Social Media Mining<br/>
Repository: <a href="https://github.com/osamabinIaggin/dcit316-final-project">https://github.com/osamabinIaggin/dcit316-final-project</a>
</div>

## Abstract

Google Translate, Meta's NLLB-200 and three human-annotated benchmarks list Twi as a supported
language. This project asks what that support is worth for Twi as it is written on social media.
I audited four resources against six documentation criteria, measured how far the three existing
Twi corpora sit from tweet text, and evaluated five sentiment systems on the {{derived.n_test}}-tweet
AfriSenti Twi test split. None of the resources names a Twi dialect; FLORES-200 holds two
independent Twi translations under the codes `aka_Latn` and `twi_Latn`; and both benchmarks behind
Twi capability claims are translations into Twi. The tweets differ sharply from them:
{{ladder.AfriSenti twi.digit_substitution|%}} write `3` in place of ɛ, against 0.1% or fewer of
benchmark sentences. On the test split, a TF-IDF and logistic regression baseline trained on Twi
reaches macro-F1 {{results.tfidf_logreg.macro_f1|.3f}}. An English Twitter model reaches
{{results.english_only.macro_f1|.3f}}, XLM-T {{results.xlmt.macro_f1|.3f}}, and NLLB translation
followed by English classification {{results.nllb_twi.macro_f1|.3f}} (all p < 0.001 against the
baseline). The off-the-shelf systems fail by predicting neutral: the English model labels
{{results.english_only.silent_failure_rate|%}} of positive and negative tweets as neutral. NLLB
passes `3`-spellings through untranslated in {{derived.copy_through_rate|%}} of affected tweets, and
declaring the source as `aka_Latn` instead of `twi_Latn` changes the final label for
{{derived.labels_changed_by_code_rate|%}} of tweets. For Ghanaian social media, a little in-domain
labelled data beats every system that claims broader coverage.

## 1. Introduction

Google Translate added Twi and Ewe in 2022. Meta's NLLB-200 translates both, and its evaluation set,
FLORES-200, carries files for `twi_Latn`, `aka_Latn` and `ewe_Latn`. On the research side, AfriSenti
(Muhammad et al., 2023a), AfriHate (Muhammad et al., 2025) and MasakhaNER 2.0 (Adelani et al., 2022a)
all list Twi among their languages. A student in Accra who wants to analyse Ghanaian online
discourse could fairly conclude that the tools exist.

I wanted to know what that support amounts to for the text people in Ghana actually post. Twi on
social media is short, informal and often mixed with English, and it is often typed without the
letters ɛ and ɔ. AfriSenti's authors put this down to keyboards that lack those letters, and note that
ɛ is typed as `3` and ɔ as `c`. Benchmarks rarely look like this.

A claim that a system "supports Twi" bundles two different things. One is capability: does the
system work on the text you have? The other is accountability: can someone outside the project find
out which Twi was covered, where the text came from, who labelled it and how reliably? The second can
be checked from documents; the first needs experiments. This project does both.

**Research questions.**

- **RQ1 (accountability).** What do the public resources that claim Twi coverage disclose about the
  language variety, the provenance of the text, the annotators and their agreement?
- **RQ2 (distribution).** How far is the text these claims are measured on from Twi as it is written
  on social media?
- **RQ3 (capability).** How do the tools a Ghanaian analyst would reach for perform on natively
  written Twi tweets, compared with a simple baseline trained on Twi?

**Contributions.** A documentation audit of four resources against six criteria, two of which
(provenance of the text, and comparability of agreement scores) are added here; a measurement of the
distance between the three Twi corpora that exist; and an evaluation of five sentiment systems on
AfriSenti Twi, with an error analysis by orthography, English mixing, length and emoji. All code,
saved predictions, metrics and executed notebooks are in the repository above.

## 2. Related work

**African-language social media data.** AfriSenti (Muhammad et al., 2023a) and its shared task
(Muhammad et al., 2023b) released sentiment-labelled tweets for 14 African languages; the Twi subset
is the only human-labelled sentiment data for a Ghanaian language I could find. AfriHate (Muhammad et
al., 2025) adds hate and abusive-language labels for 15 languages including Twi. MasakhaNER 2.0
(Adelani et al., 2022a) annotates named entities in 20 languages including Twi and Ewe, and draws the
text for several of them from MAFAND-MT (Adelani et al., 2022b), a corpus of French and English news
translated into African languages.

**Translation benchmarks and their quality.** FLORES-200 was built for NLLB-200 (NLLB Team et al.,
2022) by translating 2,009 English Wikimedia sentences into roughly 200 languages. Abdulmumin et al.
(2024) had native speakers review the FLORES files for Hausa, Northern Sotho, Xitsonga and isiZulu
and found enough errors to release corrections. No Ghanaian language was covered.

**Language identification.** Caswell et al. (2020) showed that identifiers which score well on
held-out sets can produce web corpora in which most text labelled as a low-resource language is
something else. Burchell et al. (2024) found that identifying languages in code-switched text
remains unsolved. Both matter here because AfriSenti assigned most of its Twi tweets to Twi with a
model trained on 2,000 hand-labelled examples.

**Sentiment models for tweets.** The English model evaluated here comes from the TimeLMs series
(Loureiro et al., 2022), fine-tuned on the TweetEval sentiment task (Barbieri et al., 2020). XLM-T
(Barbieri et al., 2022) continues training XLM-R on multilingual tweets and fine-tunes it for
sentiment in eight languages, none of them African.

**Documentation standards.** Data statements (Bender and Friedman, 2018), datasheets (Gebru et al.,
2021) and model cards (Mitchell et al., 2019) set out what dataset and model creators should record.
The audit criteria in Section 4.1 build on them.

The gap this project addresses: the African NLP literature reports what systems achieve on its
benchmarks, and the documentation literature says what should be disclosed, but I found no work that
checks Ghanaian-language claims against both the documentation and the text Ghanaians write.

## 3. Data and ethics

| Source | What is used | Size | Natively written? |
|---|---|---|---|
| AfriSenti Twi, commit `5aec3cf` | Tweets with sentiment labels | 3,481 train, 388 dev, 949 test | Yes |
| MasakhaNER 2.0 Twi, commit `ba5843c` | Sentences only, no entity labels | 6,056 sentences | No (MAFAND-MT translation) |
| FLORES-200 `twi_Latn`, `aka_Latn`, `eng_Latn` | dev + devtest | 2,009 sentences each | No (translated from English) |
| Four papers (AfriSenti, AfriHate, MasakhaNER 2.0, FLORES correction) | Text extracted from the PDFs | n/a | n/a |

The AfriSenti Twi test split holds {{notes.test_label_distribution.positive}} positive,
{{notes.test_label_distribution.negative}} negative and {{notes.test_label_distribution.neutral}}
neutral tweets. Its reported inter-annotator agreement is 0.51 (free-marginal kappa).

Everything is public. `scripts/fetch_data.py` downloads each file from a pinned commit and records a
SHA-256 checksum, so no raw data is committed; the AfriSenti and MasakhaNER repositories declare no
licence, and I did not want to redistribute text I had no explicit permission to share. AfriSenti
tweets carry no user handles or links (none of the 4,818 tweets contains one). No new data was
collected and no person was contacted. The few tweets quoted in Section 7 are already distributed in
a public benchmark and identify nobody.

I do not read Twi well enough to judge translation quality, so no result depends on my reading of
Twi. Where a native speaker's judgement is needed, the paper says so. The full data card, ethics
statement and AI-use disclosure are in the repository.

## 4. Methods

### 4.1 Documentation audit (RQ1)

Each paper is converted to text twice with `pdftotext`: once with `-layout`, which keeps tables
intact, and once in reading order, because `-layout` interleaves the two columns of an ACL paper and
breaks any sentence that wraps. `scripts/audit_documentation.py` searches both for patterns tied to
six criteria and saves every matching line with its line number.

| | Criterion | Basis |
|---|---|---|
| A1 | Is the language referent precise (Akan, Twi, a named dialect)? | Bender and Friedman (2018) |
| A2 | Is the text natively written or translated? | Added here |
| A3 | Are native-speaker annotators stated? | Gebru et al. (2021) |
| A4 | Is agreement reported, and in a form comparable across resources? | Added here |
| A5 | Is annotator pay disclosed? | Gebru et al. (2021) |
| A6 | Is there a datasheet, data statement or model card? | Gebru et al. (2021); Mitchell et al. (2019) |

The search is automatic; each verdict in the matrix is my reading of the matches, and the matches are
committed so the reading can be checked. "Not found" means the fact is absent from the public paper,
not that the practice did not happen.

### 4.2 Domain ladder (RQ2)

The three Twi corpora differ in how far they sit from spontaneous writing: FLORES-200 is translated
encyclopaedic prose, MasakhaNER 2.0 is translated news, and AfriSenti is tweets. For every text I
compute the share of tokens using ɛ or ɔ, whether the text writes `3` inside a word in place of ɛ,
the share of tokens containing letters outside the Twi alphabet (c, j, q, v, x, z), the share of
emoji-bearing texts, and an English-token share. The English lexicon is FLORES English plus
scikit-learn's stop-word list, minus every word that appears in FLORES Twi or Akan; this makes the
estimate zero on FLORES by construction, so it is only compared across the other two corpora. I also
measure how much of the tweets' vocabulary each benchmark covers, and how similar the FLORES
`aka_Latn` and `twi_Latn` files are.

### 4.3 Sentiment systems (RQ3)

All systems are scored on the 949-tweet AfriSenti Twi test split, which is used once.

| System | What it is | Role |
|---|---|---|
| Majority class | Most frequent training label ({{notes.majority_label}}) | Floor |
| **TF-IDF + logistic regression** | Character 2–5-grams and word 1–2-grams, class-balanced, C chosen on dev | **Baseline**: trained on Twi |
| English-only | `cardiffnlp/twitter-roberta-base-sentiment-latest`, applied directly to Twi | What an analyst uses by default |
| XLM-T | `cardiffnlp/twitter-xlm-roberta-base-sentiment`, zero-shot | Multilingual, no Twi training |
| NLLB → English | `nllb-200-distilled-600M` translates Twi to English, then the English-only model | Translate-then-classify |

The NLLB pipeline is run twice on identical input, once declaring the source as `twi_Latn` and once
as `aka_Latn`, because FLORES treats these as separate languages and no resource says which one
tweets belong to. Decoding is greedy with at most 96 new tokens.

**Metrics.** Macro-F1 is the primary metric because the classes are unbalanced; accuracy, weighted
F1 and per-class F1 are also reported. A 95% bootstrap interval (1,000 resamples, seed 22128981)
accompanies each macro-F1, and an exact McNemar test compares each system with the baseline. I also
report the **silent-failure rate**: of the tweets whose gold label is positive or negative, the share
predicted neutral. This error produces no warning, because a confident "neutral" looks like an
ordinary answer.

**Error analysis.** The test split is cut by orthography (uses ɛ/ɔ, writes `3` for ɛ, neither), by
English-token share, by length and by the presence of emoji, and macro-F1 is computed per slice.
Samples of three error types are saved for inspection: sentiment lost through translation, tweets
every non-trivial system gets wrong, and label changes caused only by the declared source language.

## 5. Results

### 5.1 Coverage

| Language | FLORES-200 | MasakhaNER 2.0 | AfriSenti | AfriHate | Google Translate | NLLB-200 |
|---|---|---|---|---|---|---|
| Twi / Akan | yes (two files) | yes | yes | yes | yes (2022) | yes |
| Ewe | yes | yes | no | no | yes (2022) | yes |
| Ga | no | no | no | no | no | no |
| Dagbani | not confirmed | no | no | no | no | no |

*Table 1. Which Ghanaian languages each resource claims. Ga's absence from FLORES-200 was checked
against the released file list; Dagbani was not checked against every resource.*

Ga is the language of Accra, the country's largest urban area, and none of these resources covers
it. Ewe has benchmark files but no social media data, so nothing in this paper's experiments could
be repeated for it.

### 5.2 Documentation audit (RQ1)

| Criterion | FLORES-200 | AfriSenti | AfriHate | MasakhaNER 2.0 |
|---|---|---|---|---|
| A1 Language referent | Two files, `aka_Latn` and `twi_Latn`; no dialect | "Twi", no dialect | "Twi", no dialect | "Akan/Twi", no dialect |
| A2 Natively written | No, translated from English | Yes, tweets | Yes, tweets | No, MAFAND-MT translation |
| A3 Native-speaker annotators | Human-verified translation | Yes | Yes | Yes |
| A4 Agreement | n/a | κ = 0.51 | 0.46–0.81 across languages | κ = 0.932, after adjudication |
| A5 Annotator pay disclosed | Not found | Not found | "more than the minimum wage" | "appropriate remuneration" |
| A6 Datasheet or data statement | Not found | Not found | Not found | Not found |

*Table 2. Disclosure matrix. Evidence lines for every cell are in `reports/evidence/`.*

**Nobody says which Twi.** FLORES-200 has two files, `aka_Latn` and `twi_Latn`. They are not copies:
only {{overlap.flores_aka_vs_twi.identical_lines}} of {{overlap.flores_aka_vs_twi.lines}} lines are
identical, and the Jaccard similarity of their vocabularies is
{{overlap.flores_aka_vs_twi.type_jaccard|.2f}}. MasakhaNER 2.0 merges the two names into "Akan/Twi";
AfriSenti and AfriHate say "Twi". None of the four papers mentions Akuapem, Asante or Fante, the
varieties a Ghanaian reader would ask about.

**The benchmarks are translations.** FLORES-200 is English Wikimedia text translated into Twi. For
Twi, MasakhaNER 2.0 uses MAFAND-MT, which its paper describes as "French and English news articles
translated into 11 languages". The authors add: "We note that translationese may lead to undesired
properties, e.g., unnaturalness. However, we did not observe serious issues during the annotation."
That second sentence is about whether annotators could label the text reliably. It says nothing
about whether the text resembles Twi as people write it, which is the property at issue here. The
only natively written Twi among the four resources is in the two Twitter collections.

**The natively written corpus flags its own difficulty.** AfriSenti's authors write that "a
significant portion of tweets in Twi were ambiguous, making it difficult to categorize sentiment
accurately", and report κ = 0.51 for Twi. They also explain that native speakers labelled 2,000
tweets as Twi or not, and a model trained on those labels assigned the rest, which is the setting
Caswell et al. (2020) warn about.

**Agreement scores cannot be compared.** MasakhaNER 2.0's κ = 0.932 for Twi is measured after
language coordinators resolved disagreements; the paper says the pre-intervention score "was much
lower" and gives one example (Nigerian Pidgin, 0.648 before and 0.966 after). AfriSenti's 0.51 is a
free-marginal kappa with no adjudication step described. A reader choosing between the corpora on
reported agreement would be comparing two different quantities.

**No datasheets.** The A6 search found no datasheet, data statement or data card in any of the four
papers. AfriHate and MasakhaNER 2.0 disclose that annotators were paid; AfriSenti does not say.

### 5.3 Distance from social media text (RQ2)

| Corpus | Texts | Mean tokens | Tokens with ɛ/ɔ | Texts writing `3` for ɛ | Tokens with c/j/q/v/x/z | Texts with emoji |
|---|---|---|---|---|---|---|
| FLORES-200 `twi_Latn` | {{ladder.FLORES-200 twi_Latn.n_texts}} | {{ladder.FLORES-200 twi_Latn.n_tokens|.1f}} | {{ladder.FLORES-200 twi_Latn.open_vowel_token_share|%}} | {{ladder.FLORES-200 twi_Latn.digit_substitution|%}} | {{ladder.FLORES-200 twi_Latn.non_twi_letter_token_share|%}} | {{ladder.FLORES-200 twi_Latn.has_emoji|%}} |
| FLORES-200 `aka_Latn` | {{ladder.FLORES-200 aka_Latn.n_texts}} | {{ladder.FLORES-200 aka_Latn.n_tokens|.1f}} | {{ladder.FLORES-200 aka_Latn.open_vowel_token_share|%}} | {{ladder.FLORES-200 aka_Latn.digit_substitution|%}} | {{ladder.FLORES-200 aka_Latn.non_twi_letter_token_share|%}} | {{ladder.FLORES-200 aka_Latn.has_emoji|%}} |
| MasakhaNER 2.0 Twi | {{ladder.MasakhaNER 2.0 twi.n_texts}} | {{ladder.MasakhaNER 2.0 twi.n_tokens|.1f}} | {{ladder.MasakhaNER 2.0 twi.open_vowel_token_share|%}} | {{ladder.MasakhaNER 2.0 twi.digit_substitution|%}} | {{ladder.MasakhaNER 2.0 twi.non_twi_letter_token_share|%}} | {{ladder.MasakhaNER 2.0 twi.has_emoji|%}} |
| AfriSenti Twi | {{ladder.AfriSenti twi.n_texts}} | {{ladder.AfriSenti twi.n_tokens|.1f}} | {{ladder.AfriSenti twi.open_vowel_token_share|%}} | {{ladder.AfriSenti twi.digit_substitution|%}} | {{ladder.AfriSenti twi.non_twi_letter_token_share|%}} | {{ladder.AfriSenti twi.has_emoji|%}} |

*Table 3. Surface profile of the three Twi corpora (`reports/metrics/ladder_profile.csv`).*

![Figure 1. Surface profile of the three Twi corpora. The two benchmarks write ɛ and ɔ; the tweets mostly write 3 or nothing.](reports/figures/fig1_domain_ladder.png)

The tweets are a different kind of text. They are less than half as long as benchmark sentences.
In the benchmarks, between {{ladder.FLORES-200 aka_Latn.open_vowel_token_share|%}} and
{{ladder.MasakhaNER 2.0 twi.open_vowel_token_share|%}} of tokens contain ɛ or ɔ; in the tweets,
{{ladder.AfriSenti twi.open_vowel_token_share|%}} do, and {{ladder.AfriSenti twi.digit_substitution|%}}
of tweets write `3` inside a word instead. The English-token estimate is
{{ladder.AfriSenti twi.english_token_share|%}} for the tweets and
{{ladder.MasakhaNER 2.0 twi.english_token_share|%}} for MasakhaNER (it is zero for FLORES by
construction). Vocabulary overlap is low: FLORES `twi_Latn` covers
{{overlap.FLORES-200 twi_Latn.tweet_type_coverage|%}} of the word types in the tweets
({{overlap.FLORES-200 twi_Latn.tweet_token_coverage|%}} of tokens), and MasakhaNER covers
{{overlap.MasakhaNER 2.0 twi.tweet_type_coverage|%}}.

### 5.4 Sentiment systems on natively written Twi (RQ3)

| System | Accuracy | Macro-F1 [95% CI] | F1 neg / neu / pos | Predicted neutral | Silent failure | McNemar p vs baseline |
|---|---|---|---|---|---|---|
| Majority class | {{results.majority.accuracy|.3f}} | {{results.majority.macro_f1|.3f}} [{{results.majority.macro_f1_ci95.0|.3f}}, {{results.majority.macro_f1_ci95.1|.3f}}] | {{results.majority.f1_negative|.2f}} / {{results.majority.f1_neutral|.2f}} / {{results.majority.f1_positive|.2f}} | {{results.majority.predicted_neutral_rate|%}} | {{results.majority.silent_failure_rate|%}} | {{results.majority.mcnemar_vs_tfidf_logreg.p_value|p}} |
| **TF-IDF + LogReg (baseline)** | **{{results.tfidf_logreg.accuracy|.3f}}** | **{{results.tfidf_logreg.macro_f1|.3f}}** [{{results.tfidf_logreg.macro_f1_ci95.0|.3f}}, {{results.tfidf_logreg.macro_f1_ci95.1|.3f}}] | {{results.tfidf_logreg.f1_negative|.2f}} / {{results.tfidf_logreg.f1_neutral|.2f}} / {{results.tfidf_logreg.f1_positive|.2f}} | {{results.tfidf_logreg.predicted_neutral_rate|%}} | {{results.tfidf_logreg.silent_failure_rate|%}} | — |
| English-only | {{results.english_only.accuracy|.3f}} | {{results.english_only.macro_f1|.3f}} [{{results.english_only.macro_f1_ci95.0|.3f}}, {{results.english_only.macro_f1_ci95.1|.3f}}] | {{results.english_only.f1_negative|.2f}} / {{results.english_only.f1_neutral|.2f}} / {{results.english_only.f1_positive|.2f}} | {{results.english_only.predicted_neutral_rate|%}} | {{results.english_only.silent_failure_rate|%}} | {{results.english_only.mcnemar_vs_tfidf_logreg.p_value|p}} |
| XLM-T | {{results.xlmt.accuracy|.3f}} | {{results.xlmt.macro_f1|.3f}} [{{results.xlmt.macro_f1_ci95.0|.3f}}, {{results.xlmt.macro_f1_ci95.1|.3f}}] | {{results.xlmt.f1_negative|.2f}} / {{results.xlmt.f1_neutral|.2f}} / {{results.xlmt.f1_positive|.2f}} | {{results.xlmt.predicted_neutral_rate|%}} | {{results.xlmt.silent_failure_rate|%}} | {{results.xlmt.mcnemar_vs_tfidf_logreg.p_value|p}} |
| NLLB `twi_Latn` → English | {{results.nllb_twi.accuracy|.3f}} | {{results.nllb_twi.macro_f1|.3f}} [{{results.nllb_twi.macro_f1_ci95.0|.3f}}, {{results.nllb_twi.macro_f1_ci95.1|.3f}}] | {{results.nllb_twi.f1_negative|.2f}} / {{results.nllb_twi.f1_neutral|.2f}} / {{results.nllb_twi.f1_positive|.2f}} | {{results.nllb_twi.predicted_neutral_rate|%}} | {{results.nllb_twi.silent_failure_rate|%}} | {{results.nllb_twi.mcnemar_vs_tfidf_logreg.p_value|p}} |
| NLLB `aka_Latn` → English | {{results.nllb_aka.accuracy|.3f}} | {{results.nllb_aka.macro_f1|.3f}} [{{results.nllb_aka.macro_f1_ci95.0|.3f}}, {{results.nllb_aka.macro_f1_ci95.1|.3f}}] | {{results.nllb_aka.f1_negative|.2f}} / {{results.nllb_aka.f1_neutral|.2f}} / {{results.nllb_aka.f1_positive|.2f}} | {{results.nllb_aka.predicted_neutral_rate|%}} | {{results.nllb_aka.silent_failure_rate|%}} | {{results.nllb_aka.mcnemar_vs_tfidf_logreg.p_value|p}} |

*Table 4. AfriSenti Twi test split, n = {{derived.n_test}}. Gold neutral rate
{{derived.gold_neutral_rate|%}}. Silent failure: share of positive or negative tweets predicted
neutral. C = {{notes.tfidf_logreg.chosen_C}} was chosen on dev.*

![Figure 2. Macro-F1 with 95% bootstrap intervals. Only the model trained on Twi is far from the floor.](reports/figures/fig2_macro_f1.png)

The baseline trained on 3,481 Twi tweets reaches macro-F1 {{results.tfidf_logreg.macro_f1|.3f}}. No
system that claims wider coverage comes close: translate-then-classify reaches
{{results.nllb_twi.macro_f1|.3f}}, XLM-T {{results.xlmt.macro_f1|.3f}}, and the English-only model
{{results.english_only.macro_f1|.3f}}, just above the majority-class floor of
{{results.majority.macro_f1|.3f}}. Every difference from the baseline is significant (McNemar
p < 0.001), and none of the confidence intervals overlaps the baseline's.

![Figure 3. Predicted-neutral and silent-failure rates against the gold neutral rate (dashed).](reports/figures/fig3_neutral_collapse.png)

The failure has a direction. Only {{derived.gold_neutral_rate|%}} of test tweets are neutral, yet
the English-only model predicts neutral for {{results.english_only.predicted_neutral_rate|%}} of
them and turns {{results.english_only.silent_failure_rate|%}} of the positive and negative tweets
into neutral. XLM-T and the NLLB pipeline do the same to about half
({{results.xlmt.silent_failure_rate|%}} and {{results.nllb_twi.silent_failure_rate|%}}). Averaged
over a corpus, this would report Twi speakers as far calmer than they are, and nothing in the
output would show it.

## 6. Error analysis

![Figure 4. Confusion matrices. The transformer systems pile predictions into the neutral column.](reports/figures/fig4_confusion.png)

| Slice | n | Baseline | English-only | XLM-T | NLLB twi |
|---|---|---|---|---|---|
| Uses ɛ/ɔ | {{slices.orthography/uses ɛ/ɔ.n}} | {{slices.orthography/uses ɛ/ɔ.tfidf_logreg_macro_f1|.3f}} | {{slices.orthography/uses ɛ/ɔ.english_only_macro_f1|.3f}} | {{slices.orthography/uses ɛ/ɔ.xlmt_macro_f1|.3f}} | {{slices.orthography/uses ɛ/ɔ.nllb_twi_macro_f1|.3f}} |
| Writes `3` for ɛ | {{slices.orthography/writes 3 for ɛ.n}} | {{slices.orthography/writes 3 for ɛ.tfidf_logreg_macro_f1|.3f}} | {{slices.orthography/writes 3 for ɛ.english_only_macro_f1|.3f}} | {{slices.orthography/writes 3 for ɛ.xlmt_macro_f1|.3f}} | {{slices.orthography/writes 3 for ɛ.nllb_twi_macro_f1|.3f}} |
| Neither | {{slices.orthography/neither.n}} | {{slices.orthography/neither.tfidf_logreg_macro_f1|.3f}} | {{slices.orthography/neither.english_only_macro_f1|.3f}} | {{slices.orthography/neither.xlmt_macro_f1|.3f}} | {{slices.orthography/neither.nllb_twi_macro_f1|.3f}} |
| Has emoji | {{slices.emoji/has emoji.n}} | {{slices.emoji/has emoji.tfidf_logreg_macro_f1|.3f}} | {{slices.emoji/has emoji.english_only_macro_f1|.3f}} | {{slices.emoji/has emoji.xlmt_macro_f1|.3f}} | {{slices.emoji/has emoji.nllb_twi_macro_f1|.3f}} |
| No emoji | {{slices.emoji/no emoji.n}} | {{slices.emoji/no emoji.tfidf_logreg_macro_f1|.3f}} | {{slices.emoji/no emoji.english_only_macro_f1|.3f}} | {{slices.emoji/no emoji.xlmt_macro_f1|.3f}} | {{slices.emoji/no emoji.nllb_twi_macro_f1|.3f}} |
| English share >25% | {{slices.english_mix/>25%.n}} | {{slices.english_mix/>25%.tfidf_logreg_macro_f1|.3f}} | {{slices.english_mix/>25%.english_only_macro_f1|.3f}} | {{slices.english_mix/>25%.xlmt_macro_f1|.3f}} | {{slices.english_mix/>25%.nllb_twi_macro_f1|.3f}} |
| No English | {{slices.english_mix/none.n}} | {{slices.english_mix/none.tfidf_logreg_macro_f1|.3f}} | {{slices.english_mix/none.english_only_macro_f1|.3f}} | {{slices.english_mix/none.xlmt_macro_f1|.3f}} | {{slices.english_mix/none.nllb_twi_macro_f1|.3f}} |

*Table 5. Macro-F1 by slice (`reports/metrics/slices.csv`; all slices in Figure 5).*

![Figure 5. Macro-F1 by slice for the four main systems.](reports/figures/fig5_slices.png)

**The English model is reading the emoji.** On tweets without emoji it predicts neutral for
{{slices.emoji/no emoji.english_only_pred_neutral|%}} of them and scores
{{slices.emoji/no emoji.english_only_macro_f1|.3f}}; with emoji it scores
{{slices.emoji/has emoji.english_only_macro_f1|.3f}}. Its errors fall slightly as the English share
rises ({{slices.english_mix/>25%.english_only_macro_f1|.3f}} above 25%, from
{{slices.english_mix/none.english_only_macro_f1|.3f}} with none), but that slice holds only
{{slices.english_mix/>25%.n}} tweets.

**Translation passes informal spelling through untouched.** Of the
{{errors.copy_through.tweets_with_3_for_e}} test tweets that write `3` for ɛ,
{{errors.copy_through.translations_still_containing_3_spellings}} ({{derived.copy_through_rate|%}})
come back from NLLB with those words still in them: `s3`, `de3`, `y3di` reach the English classifier
as unknown strings. Those tweets are then called neutral
{{errors.copy_through.nllb_twi_pred_neutral_when_copied|%}} of the time, against
{{errors.copy_through.nllb_twi_pred_neutral_when_not_copied|%}} when the spelling was absorbed.
Standard orthography does not rescue translation either: on tweets that use ɛ/ɔ the NLLB pipeline
scores {{slices.orthography/uses ɛ/ɔ.nllb_twi_macro_f1|.3f}}.

**Which "Twi" you declare changes the answer.** Translating the same tweets as `twi_Latn` and as
`aka_Latn` gives identical output for only {{notes.nllb_source_code.identical_translations}} of
{{notes.nllb_source_code.n}}. The final sentiment label differs for
{{errors.nllb_twi_vs_aka_label_disagreements}} tweets ({{derived.labels_changed_by_code_rate|%}}),
though the two settings score almost the same overall. The naming confusion in Section 5.2 is
therefore an input to the result: an analyst who picks the other code gets a different label for
one tweet in four, and nothing in the documentation tells them which code is right.

**The baseline is steady.** Its macro-F1 stays between 0.55 and 0.65 on every slice, including the
spelling variants that defeat translation. Its weak point is the neutral class (F1
{{results.tfidf_logreg.f1_neutral|.2f}}), the smallest and, given κ = 0.51, probably the noisiest.

**Hard cases.** {{errors.all_three_nonmajority_systems_wrong}} tweets are misclassified by the
baseline, XLM-T and the NLLB pipeline alike. Samples are saved in `reports/error_analysis/`. I cannot
read them well enough to say whether the systems or the gold labels are wrong, and with the
creators' own note that many Twi tweets are ambiguous, some of these are likely label errors.

## 7. Discussion

The three questions have connected answers. The resources that claim Twi measure their claims on
translated, standard-orthography prose (RQ1, RQ2), while Twi online is short, mixed with English and
emoji, and spelled with digits in place of letters (RQ2). On that text, every system built for
broad coverage loses to a small model trained on 3,481 tweets, and loses by turning sentiment into
neutral (RQ3).

For anyone mining Ghanaian social media, the practical conclusion is uncomfortable but cheap to act
on. Off-the-shelf multilingual and translation-based pipelines are the wrong default for Twi. Even
a modest amount of in-domain labelled data, with a linear model, does better. The pressing work is
collecting and labelling more natively written text, for Twi and especially for Ga and Ewe, where
none exists.

The documentation findings explain why this is hard to see from the outside. A model card that
reports FLORES scores for `twi_Latn` reports performance on translated Wikipedia sentences, in one of
two unlabelled Twi files, with no statement of the variety. A practitioner cannot tell from it how the model will
behave on tweets, or that switching to `aka_Latn` changes a quarter of the labels.

These teams documented more than most of the field does, and that openness is what made this audit
possible. The commercial systems whose claims reach the most users disclose the least, and one of
them, Google Translate, could not be tested here at all.

## 8. Limitations

- **Absent is not the same as not done.** "Not found" in Table 2 means the fact is missing from the
  public paper. The practice may have happened.
- **Label quality.** Every capability result depends on AfriSenti's labels (κ = 0.51 for Twi, with
  ambiguity noted by the authors). Some of what looks like system error is probably label noise.
- **No native-speaker judgement.** I do not read Twi well enough to evaluate translations, so the
  NLLB results show that sentiment was lost, not that a translation was wrong.
- **One dataset, one task.** Sentiment on one Twitter corpus. Hate speech (AfriHate Twi) and other
  tasks could behave differently.
- **Models chosen.** XLM-T was not trained on any African language; an Africa-centric model
  fine-tuned for sentiment might do much better. Google Translate was not tested because I had no
  API key. Language identifiers (AfroLID, GlotLID) were not run.
- **Surface features are proxies.** The English-token estimate and the orthography slices are
  heuristics, tested in `tests/`, but not validated against human judgement.
- **Coverage.** Ga's absence was checked against FLORES-200's file list; Dagbani was not checked
  everywhere. GhanaNLP corpora and the Khaya translator were not audited.

## 9. Conclusion

Twi is listed as supported by the largest translation systems and by three human-annotated
benchmarks. The benchmarks those claims rest on are translations into Twi, written in a spelling
that most Twi tweets do not use, under two language codes that nobody distinguishes, and the
agreement scores attached to them cannot be compared. On 949 natively written Twi tweets, an
English-only model, a multilingual model and a translate-then-classify pipeline all lose to a
TF-IDF baseline trained on Twi, mostly by calling emotional tweets neutral.

What is missing is data written the way Ghanaians write, a convention for naming the variety, and
agreement reported in comparable form. Until those exist, the safest way to analyse Twi on social
media is to label some of it and train on it.

## AI-use statement

I used Claude (Anthropic) through Claude Code to brainstorm the topic, write code and draft text.
Every quotation was located by script in the source PDFs, every reference was checked against the
publisher's record, and every number is written into this manuscript by
`scripts/fill_manuscript.py` from files the code produced. Details are in `ai_use_disclosure.md`.

## References

Abdulmumin, I., Mkhwanazi, S., Mbooi, M. S., Muhammad, S. H., Ahmad, I. S., Putini, N., Mathebula, M., Shingange, M., Gwadabe, T., and Marivate, V. (2024). Correcting FLORES evaluation dataset for four African languages. arXiv:2409.00626.

Adelani, D. I., Neubig, G., Ruder, S., Rijhwani, S., et al. (2022a). MasakhaNER 2.0: Africa-centric transfer learning for named entity recognition. In *Proceedings of EMNLP 2022*, 4488–4508.

Adelani, D. I., Alabi, J. O., Fan, A., Kreutzer, J., et al. (2022b). A few thousand translations go a long way! Leveraging pre-trained models for African news translation. In *Proceedings of NAACL 2022*, 3053–3070.

Barbieri, F., Camacho-Collados, J., Espinosa Anke, L., and Neves, L. (2020). TweetEval: Unified benchmark and comparative evaluation for tweet classification. In *Findings of EMNLP 2020*, 1644–1650.

Barbieri, F., Espinosa Anke, L., and Camacho-Collados, J. (2022). XLM-T: Multilingual language models in Twitter for sentiment analysis and beyond. In *Proceedings of LREC 2022*, 258–266.

Bender, E. M., and Friedman, B. (2018). Data statements for natural language processing: Toward mitigating system bias and enabling better science. *Transactions of the ACL*, 6, 587–604.

Burchell, L., Birch, A., Thompson, R., and Heafield, K. (2024). Code-switched language identification is harder than you think. In *Proceedings of EACL 2024*, 646–658.

Caswell, I., Breiner, T., van Esch, D., and Bapna, A. (2020). Language ID in the wild: Unexpected challenges on the path to a thousand-language web text corpus. In *Proceedings of COLING 2020*, 6588–6608.

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., and Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92.

Loureiro, D., Barbieri, F., Neves, L., Espinosa Anke, L., and Camacho-Collados, J. (2022). TimeLMs: Diachronic language models from Twitter. In *Proceedings of ACL 2022: System Demonstrations*, 251–260.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., and Gebru, T. (2019). Model cards for model reporting. In *Proceedings of FAT* 2019*, 220–229.

Muhammad, S. H., Abdulmumin, I., Ayele, A. A., Ousidhoum, N., Adelani, D. I., Yimam, S. M., et al. (2023a). AfriSenti: A Twitter sentiment analysis benchmark for African languages. In *Proceedings of EMNLP 2023*, 13968–13981.

Muhammad, S. H., Abdulmumin, I., Yimam, S. M., Adelani, D. I., Ahmad, I. S., Ousidhoum, N., Ayele, A. A., Mohammad, S. M., Beloucif, M., and Ruder, S. (2023b). SemEval-2023 Task 12: Sentiment analysis for African languages (AfriSenti-SemEval). In *Proceedings of SemEval-2023*, 2319–2337.

Muhammad, S. H., Abdulmumin, I., Ayele, A. A., Adelani, D. I., et al. (2025). AfriHate: A multilingual collection of hate speech and abusive language datasets for African languages. In *Proceedings of NAACL 2025*, 1854–1871.

NLLB Team, Costa-jussà, M. R., Cross, J., Çelebi, O., Elbayad, M., et al. (2022). No language left behind: Scaling human-centered machine translation. arXiv:2207.04672.
