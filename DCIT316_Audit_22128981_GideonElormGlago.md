# Translationese All the Way Down

**Auditing What "Supports Twi" Means in Social Media NLP Resources**

Gideon Elorm Glago

Student ID: 22128981

Department of Computer Science, University of Ghana

DCIT 316: Computational Models for Social Media Mining

---

## Abstract

Google Translate added Twi and Ewe in 2022. Meta's NLLB-200 covers both and was described as the
first system to reach high-quality translation for languages including Ewe. Several human-annotated
benchmarks now list Twi among their languages. On the face of it, Ghanaian languages have arrived in
NLP.

This paper audits what those claims deliver. I treat a claim of language support as two separable
things — **capability**, whether the system does the job on text people actually write, and
**accountability**, whether anyone outside the project can check. I audit the accountability half
directly, across the public resources that claim Twi or Ewe coverage, and specify a protocol for the
capability half.

Five findings. **First**, Ga — the language of Accra, the country's largest city — appears in none of
the benchmarks surveyed. **Second**, the field does not agree on what "Twi" denotes: FLORES-200 lists
`aka_Latn` and `twi_Latn` as separate entries, MasakhaNER 2.0 merges them as "Akan/Twi", AfriSenti
says "Twi" unqualified, and no resource examined names a dialect, though Akuapem and Asante Twi differ
in orthographic convention. **Third, and the paper's central result:** both benchmarks on which Twi
capability claims rest consist of text *translated into* Twi — FLORES-200 from English Wikipedia,
MasakhaNER 2.0 from the MAFAND-MT French/English news corpus, whose own authors caution that
"translationese may lead to undesired properties." The only corpus of natively written Twi in the set
is 4,821 tweets. **Fourth**, that corpus's creators flag it themselves: "a significant portion of
tweets in Twi were ambiguous," and its inter-annotator agreement of κ = 0.51 is the lower end of the
range they report. **Fifth**, agreement figures are not comparable across resources — MasakhaNER's
κ = 0.932 for Twi is explicitly *post-adjudication*, with pre-intervention scores unreported per
language.

None of these resources is careless; several are the most carefully documented work in African NLP.
The argument is not that the field is doing badly, but that a practitioner in Accra cannot currently
determine, from public documentation, what any of these systems will do on Ghanaian social media text
— and that the evaluation base for Twi is translated text nearly all the way down.

*(≈ 330 words)*

---

## 1. Introduction

### 1.1 The claims

In May 2022 Google Translate added ten African languages, Twi and Ewe among them. Meta's NLLB-200,
released the same year, covers 55 low-resource African languages including both. The accompanying
benchmark, FLORES-200, lists `twi_Latn`, `aka_Latn` and `ewe_Latn`. On the research side, AfriSenti
(Muhammad et al., 2023a) includes a Twi sentiment corpus, AfriHate (Muhammad et al., 2025) a Twi hate
speech corpus, and MasakhaNER 2.0 (Adelani et al., 2022) named-entity data for both Twi and Ewe.

A student or practitioner in Ghana reading this would reasonably conclude that the tooling problem for
Ghanaian languages is largely solved, or at least well underway.

### 1.2 The question

This paper asks what those claims are worth, and splits the question in two.

**Capability** — does the system do the job on the text people actually write? Ghanaian social media
text is informal, unpunctuated, orthographically variable and frequently code-mixed. Benchmarks are
none of those things.

**Accountability** — can someone outside the project check? Not "is the work good," but "is the
work *checkable*." These are different properties and only the second can be audited from a desk.

I audit accountability directly and report the results in Section 4. I specify the capability audit
in Section 5 but do not run it here; Section 7 is explicit about what that costs the paper's claims.

### 1.3 Why this is a social media mining question

Two reasons, and I want to be precise because the alternative framing — machine translation
evaluation — is somebody else's field.

First, the *only* natively written Twi corpus among the resources audited is a Twitter corpus. Every
other Twi resource is translated text. So the question "what does Twi data look like?" is currently,
almost by default, a social media question.

Second, the practical pipeline this affects is a social media mining pipeline. Somebody wanting to
analyse Ghanaian public discourse will reach for exactly these resources, and the gap between what
they promise and what they do on tweets is the gap that determines whether the analysis means
anything.

### 1.4 Precedent

Abdulmumin et al. (2024) had native speakers review FLORES for Hausa, Northern Sotho, Xitsonga and
isiZulu, found inconsistencies and inaccuracies, and released corrections. That work establishes both
that benchmark errors in African languages are real and that native-speaker review finds them.

It did not cover Twi, Ewe or any Ghanaian language. The benchmark underwriting Google's and Meta's
Ghanaian-language claims has not been checked in the way four other African languages have.

---

## 2. Scope and method

### 2.1 Resources audited

| Resource | Type | Ghanaian languages claimed |
|---|---|---|
| FLORES-200 | MT evaluation benchmark | `twi_Latn`, `aka_Latn`, `ewe_Latn` |
| NLLB-200 | MT model | Twi, Ewe |
| Google Translate | Deployed MT system | Twi, Ewe (added 2022) |
| AfriSenti | Sentiment corpus (Twitter) | Twi |
| AfriHate | Hate speech corpus (Twitter) | Twi |
| MasakhaNER 2.0 | NER corpus | Akan/Twi, Ewe |

Selection rule: publicly available, claims coverage of at least one Ghanaian language, and used as a
basis for evaluation or training in published work. This is not exhaustive — GhanaNLP's parallel
corpora, the English–Twi corpus of Azunre et al. (2021), and the ABENA/RoBAKO models are further
candidates, and Section 7 lists them as remaining work.

### 2.2 Accountability criteria

Six criteria, derived from the documentation norms of Gebru et al. (2021), Mitchell et al. (2019) and
Bender and Friedman (2018), and specialised to the question a Ghanaian user would actually ask.

| # | Criterion | Why it matters here |
|---|---|---|
| A1 | Is the language referent precise? | "Twi," "Akan" and "Akuapem/Asante Twi" are not interchangeable |
| A2 | Is the text natively written or translated? | Translationese is not the target distribution |
| A3 | Native-speaker annotators, stated? | Unstated good practice is still uncheckable |
| A4 | Is inter-annotator agreement reported, and is it comparable? | A post-adjudication κ is a different quantity from a raw one |
| A5 | Is annotator compensation disclosed? | An ethics claim that cannot be verified |
| A6 | Is a datasheet, data statement or model card present? | The field's own stated standard |

**A2 and A4 are the criteria this paper contributes.** The others are standard. A2 asks a question the
documentation literature does not routinely ask, and it turned out to be the one that mattered most.

### 2.3 What "not reported" means

An audit of documentation can establish that a fact is absent from the public record. It cannot
establish that the underlying practice was poor. Several teams here plainly did careful work; the
question is whether a third party can confirm it.

Every "not reported" cell below should be read as *unverifiable from the public record*, not as
*not done*. This distinction is load-bearing and Section 7 returns to it.

---

## 3. The coverage table

Before any measurement, the simplest question: which Ghanaian languages appear at all?

| Language | Approx. speakers | FLORES-200 | MasakhaNER 2.0 | AfriSenti | AfriHate | Google Translate | NLLB-200 |
|---|---|---|---|---|---|---|---|
| Twi / Akan | ~9M (L1, MasakhaNER) | ✓ (×2 entries) | ✓ | ✓ 4,821 | ✓ | ✓ (2022) | ✓ |
| Ewe | several million | ✓ | ✓ | — | — | ✓ (2022) | ✓ |
| **Ga** | ~1M, Accra | **—** | **—** | **—** | **—** | **—** | **—** |
| Dagbani | ~1M, Northern Region | not found* | — | — | — | — | — |

\* Ga's absence from FLORES-200 was confirmed directly against the released language list. Dagbani was
not separately confirmed and is marked accordingly; Section 7 lists it as pending.

**Ga is the language of Accra.** Greater Accra is Ghana's most populous region and the densest
concentration of Ghanaian social media users in the country. It appears in none of the benchmarks
surveyed. A researcher wanting to analyse Ghanaian online discourse in the language of the capital has
no evaluation data, no annotated corpus, and no supported translation system.

Ewe presents a narrower version of the same problem: benchmark presence, but **no social media corpus
at all**. Its coverage stops at translated text.

---

## 4. Accountability findings

### 4.1 Nobody agrees what "Twi" means

Three resources, three referents:

- **FLORES-200** lists `aka_Latn` and `twi_Latn` as **separate entries** — Akan the macrolanguage,
  Twi the variety.
- **MasakhaNER 2.0** labels the same territory **"Akan/Twi (twi)"** — one entry, both names.
- **AfriSenti** and **AfriHate** say **"Twi"**, unqualified.

None of the resources examined specifies a **dialect**. Akuapem Twi and Asante Twi differ, including
in orthographic convention; Fante is a further Akan variety. A search of the AfriSenti, AfriHate and
MasakhaNER 2.0 papers returned no occurrence of "Akuapem," "Asante" or "Fante" in a
dialect-specifying sense.

This is not pedantry. A model trained on one variety and evaluated on another will show a performance
gap that no one can attribute, because neither the training nor the evaluation data says which variety
it is. And a Ghanaian user cannot tell whether "supports Twi" means their Twi.

### 4.2 The central finding: the benchmarks are translations

**FLORES-200** consists of 842 English Wikimedia articles, ~3,001 sentences, translated into each
target language and human-verified. Twi content is therefore translated English Wikipedia prose.

**MasakhaNER 2.0** covers 20 languages; for those without sufficient monolingual text it draws on
**MAFAND-MT** (Adelani et al., 2022), a corpus of **French and English news articles translated into**
11 languages. Twi is one of these. The paper raises the issue itself, and also answers it:

> "We note that translationese may lead to undesired properties, e.g., unnaturalness. **However, we
> did not observe serious issues during the annotation.**"

The second sentence has to be taken seriously, and it does not rescue the corpus for the purpose at
issue here. "We did not observe serious issues during the annotation" is a claim about *annotatability*
— whether trained annotators could reliably mark entities in the text. That is a different property
from *representativeness*, which is whether the text resembles Twi as Ghanaians spontaneously produce
it. Translated news prose can be entirely clean, consistent and easy to annotate while still coming
from a distribution no Ghanaian Twitter user writes in. The authors answered the question they were
being asked, which was about data quality. The question this paper asks is about provenance, and on
that the first sentence stands unqualified.

**AfriSenti** collected tweets. Its Twi subset — 4,821 instances — is the only natively written Twi
corpus among the resources audited.

So the evaluation base for Twi looks like this:

| Rung | Resource | Domain | Natively written? |
|---|---|---|---|
| 1 | FLORES-200 | Wikipedia prose | **No** — translated from English |
| 2 | MasakhaNER 2.0 | News | **No** — translated from FR/EN via MAFAND-MT |
| 3 | AfriSenti | Twitter | **Yes** — 4,821 tweets |

Claims of Twi capability are made and evaluated on rungs 1 and 2. Ghanaian social media lives on
rung 3, which is the smallest corpus of the three and the only one nobody translated into existence.

The phrase "high-quality translation for Ewe" is a claim measured on text that was itself produced by
translation. That is not circular in the strict sense — FLORES translations are human and verified —
but it means the claim has never been tested against Ewe as Ewe speakers spontaneously write it,
because no such corpus exists.

### 4.3 The one natively written corpus flags itself

The AfriSenti authors report per-language annotation challenges. Their Twi entry:

> "A significant portion of tweets in Twi were ambiguous, making it difficult to categorize sentiment
> accurately. Some tweets contained symbols not in the Twi alphabet, which is a frequent
> occurrence..."

Consistent with that, AfriSenti's inter-annotator agreement for Twi is **κ = 0.51** (free-marginal
multi-rater kappa, Randolph 2005). The authors describe their range as "intermediate to good
(0.40 − 0.75)"; Twi sits in the lower part of it, and 0.51 on a three-class task is modest in absolute
terms.

I want to be fair about this: disclosing the problem is good practice, and AfriSenti's transparency is
why this finding is available at all. The point is what follows downstream — a model reporting strong
numbers on AfriSenti Twi is reporting agreement with labels its own creators flagged as difficult, and
almost nothing built on this corpus repeats that caveat.

### 4.4 Language membership is largely model-assigned

How does AfriSenti know a tweet is Twi? The paper is explicit: native speakers manually labelled
**2,000 tweets** in Twi and Xitsonga, and a language model fine-tuned on those 2,000 — citing
**Caswell et al. (2020)** — was then used to identify the rest.

Caswell et al. is the paper documenting that language identification systems scoring above 90% F1 on
held-out sets produced web corpora with human-judged precision around 5% for many low-resource
languages. Using it as the basis for a Twi detector is a reasonable engineering choice given the
alternatives, and AfriSenti discloses it. But it means the *language membership* of most of the corpus
is a model prediction, not a human judgement — and Burchell et al. (2024) show that language
identification on code-switched text, which Ghanaian Twitter abundantly is, remains unsolved.

### 4.5 Agreement figures are not comparable across resources

| Resource | Reported κ (Twi) | Metric | Stage |
|---|---|---|---|
| AfriSenti | 0.51 | Free-marginal multi-rater (Randolph) | Not stated as adjudicated |
| AfriHate | within 0.46–0.81 across languages | Free-marginal multi-rater (Randolph) | Not stated as adjudicated |
| MasakhaNER 2.0 | 0.932 | Fleiss' κ, entity level | **Post-intervention** |

MasakhaNER 2.0 states directly that Table 2 reports the score *after* language coordinators resolved
disagreements with annotators, and that "the pre-intervention Fleiss Kappa score was much lower." The
single illustrative example given is Nigerian Pidgin: **0.648 → 0.966**. Pre-intervention scores are
not reported per language.

So 0.932 and 0.51 are not the same kind of number, and a reader comparing them — as anyone selecting a
corpus would — will draw a false conclusion. Neither team hid anything; the figures are simply not
commensurable, and nothing in either paper warns you.

### 4.6 The disclosure matrix

| | FLORES-200 | AfriSenti | AfriHate | MasakhaNER 2.0 |
|---|---|---|---|---|
| **A1** Language referent precise | Partial — splits aka/twi, no dialect | No dialect | No dialect | Merges "Akan/Twi", no dialect |
| **A2** Natively written | **No** — translated | **Yes** | **Yes** | **No** — MAFAND-MT translation |
| **A3** Native-speaker annotators stated | Human-verified translation | **Yes** | **Yes**, explicit | **Yes** |
| **A4** IAA reported | n/a | Yes, κ = 0.51 | Yes, 0.46–0.81 | Yes, κ = 0.932 **post-adjudication** |
| **A5** Compensation disclosed | Not found | **Not found** | **Yes** — "more than the minimum wage" | **Yes** — "all annotators and language coordinators received appropriate remuneration" |
| **A6** Datasheet / data statement | Not found | **Not found** | **Not found** (ethics section present) | **Not found** |

The pattern worth naming: **no resource audited ships a datasheet or data statement**, despite these
being the field's own stated standard and despite several of these teams citing that literature. And
the criterion that separates the resources is A5, compensation — two disclose, and one of the two
gives an actual floor.

### 4.7 A minor discrepancy, flagged not claimed

AfriSenti's Table 6 gives the Twi splits as 3,482 train / 389 dev / 950 test, total 4,821. The dataset
as served from its public release reports 3,481 / 388 / 949, total 4,818 — three rows fewer, one per
split.

This is almost certainly a header-row or serving artefact rather than a substantive difference, and I
record it as an observation requiring direct confirmation against a downloaded copy rather than as a
finding. It is included because an audit that only reports the dramatic discrepancies is not an audit.

---

## 5. The capability audit — protocol

Not run in this paper. Specified here so it can be.

### 5.1 The domain ladder

Section 4.2's table is also an experimental design. Twi is the only Ghanaian language with data at
three levels, and the three differ in exactly the dimension that matters: distance from spontaneous
written Ghanaian language.

Measure the same systems at each rung. Any degradation from rung 1 to rung 3 is the gap between what
is claimed and what a social media mining pipeline would experience. Ewe stops at rung 2, and that
truncation is itself reportable.

### 5.2 Measurement 1 — language identification degradation

Run AfroLID (Adebara et al., 2022) and GlotLID (Kargaran et al., 2023) over Twi text from each rung
and measure the proportion correctly identified as Twi/Akan.

Reference-free: the gold label is each dataset's own claim about itself. Expected finding — accuracy
falling as text becomes informal — would quantify how much of the LID reliability reported on clean
benchmarks survives contact with tweets. It also cross-checks Section 4.4, since AfriSenti's own Twi
membership was assigned this way.

### 5.3 Measurement 2 — translate-then-classify

The measurement that matters, because it is the pipeline a Ghanaian practitioner would actually build
given the tools available.

1. Take AfriSenti Twi instances with gold sentiment labels.
2. Translate Twi → English with NLLB-200 (distilled 600M, CPU-feasible), and a sample through Google
   Translate so the largest public claim is tested directly.
3. Classify the English output with a strong English sentiment model.
4. Measure how often the gold sentiment label survives the round trip.

**Controls, without which the measurement means nothing:**

- *High-resource control.* Same pipeline on a language where MT is known-good (e.g. Swahili or
  French → English). If sentiment survives at a high rate there and collapses for Twi, the difference
  is attributable to the translation step rather than to the English classifier.
- *English control.* The English classifier's accuracy on native English text, establishing its ceiling.
- *Direct-classification control.* A multilingual classifier applied to the Twi text without
  translating, so the translate-then-classify route can be compared against not translating at all.

**What this can and cannot conclude.** It can establish that sentiment information is lost across the
translation step. It **cannot** establish that a translation is linguistically wrong — that requires
native-speaker judgement, which this paper does not have. The claim available is *information loss*,
not *translation error*, and Section 7 holds it to that.

### 5.4 What would falsify the paper's framing

If translate-then-classify preserves sentiment on Twi at rates comparable to the high-resource
control, then the translationese finding in Section 4.2 is a documentation curiosity with no practical
consequence, and the paper's framing is wrong. That is the result I would have to report.

---

## 6. What this costs, concretely

A student in this department wanting to analyse Ghanaian Twitter discourse in Twi today faces the
following, none of which is discoverable without the audit above:

1. They cannot work in Ga at all.
2. They will train or evaluate on Twi data that is mostly translated from English or French, unless
   they use the single 4,821-tweet corpus.
3. If they use that corpus, they inherit labels its creators describe as difficult, at κ = 0.51, on
   text whose language membership was mostly assigned by a model.
4. They cannot tell which variety of Twi any of it is.
5. If they compare corpora by reported agreement, they will conclude MasakhaNER's annotation is far
   more reliable than AfriSenti's, which the numbers do not actually support.

Every one of these is recoverable from public documents. None is stated in any single place, and
several require reading a methods section closely enough to notice a subordinate clause.

---

## 7. Limitations

**This is a documentation audit, and absence of evidence is the finding.** "Not reported" means
unverifiable from the public record. It does not mean the practice was absent. AfriSenti not stating
compensation does not mean annotators were unpaid; I do not know, which is precisely the point being
measured.

**The capability half is unrun.** Section 5 is a protocol. Until it is executed, the paper establishes
that Twi benchmarks are translations and cannot establish what that costs in performance. The
translationese finding is a fact about provenance; its practical consequence is a hypothesis.

**No native-speaker component.** I do not read Twi or Ewe well enough to judge translation quality, so
I cannot replicate Abdulmumin et al.'s method on Ghanaian languages. That work remains undone and is
the single highest-value extension.

**Coverage is incomplete.** GhanaNLP's parallel corpora, Azunre et al.'s English–Twi corpus, the
ABENA/RoBAKO models, AfroXLMR and Khaya were not audited. Dagbani's absence was inferred rather than
confirmed against each release. NLLB-200's and Google Translate's documentation was assessed from
public materials rather than from the full 190-page NLLB report.

**Speaker figures are approximate**, taken from the resources themselves rather than from census data.

**I am not a neutral party.** I am a Ghanaian student who would like these resources to work, and an
audit that finds problems is a more interesting paper than one that does not. I have tried to control
for that by reporting Section 4.7's non-finding and by stating in Section 5.4 what result would
falsify the framing.

---

## 8. Conclusion

Google and Meta added Twi and Ewe. Three human-annotated benchmarks list Twi. By the ordinary meaning
of the words, Ghanaian languages are supported.

Audited, the support has a specific shape. Ga, the language of Ghana's capital, is in none of it. The
field does not agree whether "Twi" names a language, a variety, or a macrolanguage, and never says
which dialect. Both benchmarks that Twi capability claims are measured on consist of text translated
into Twi, one of them from a corpus whose own authors warn about unnaturalness. The single corpus of
Twi as Ghanaians actually write it holds 4,821 tweets, carries an agreement score of 0.51, was flagged
as ambiguous by the people who built it, and had its language membership assigned largely by a model
trained on 2,000 examples. And the agreement scores that a user would compare across these corpora are
not the same quantity.

None of this is misconduct, and most of it was findable only because these teams documented their work
better than the field's norm. That is the uncomfortable part. The resources that disclose most are the
ones an audit can criticise, and the deployed commercial systems — which disclose least — are the ones
whose claims are largest and least checkable.

What is missing is not effort. It is a Ga corpus, a natively written Twi corpus larger than one
Twitter export, a convention for saying which Twi, and the habit of reporting agreement in a form that
survives comparison.

---

## References

Abdulmumin, I., Mkhwanazi, S., Mbooi, M. S., Muhammad, S. H., Ahmad, I. S., Putini, N., Mathebula, M.,
Shingange, M., Gwadabe, T., and Marivate, V. (2024). Correcting FLORES Evaluation Dataset for Four
African Languages. arXiv:2409.00626. https://arxiv.org/abs/2409.00626

Adebara, I., Elmadany, A., Abdul-Mageed, M., and Inciarte, A. (2022). AfroLID: A Neural Language
Identification Tool for African Languages. In *Proceedings of EMNLP 2022*, Abu Dhabi.
https://aclanthology.org/2022.emnlp-main.128/

Adelani, D. I., Neubig, G., Ruder, S., Rijhwani, S., et al. (2022). MasakhaNER 2.0: Africa-centric
Transfer Learning for Named Entity Recognition. In *Proceedings of EMNLP 2022*.
https://aclanthology.org/2022.emnlp-main.298/

Azunre, P., Osei, S., Addo, S., Adu-Gyamfi, L. A., Moore, S., et al. (2021). English-Twi Parallel
Corpus for Machine Translation. arXiv:2103.15625. https://arxiv.org/abs/2103.15625

Bender, E. M., and Friedman, B. (2018). Data Statements for Natural Language Processing: Toward
Mitigating System Bias and Enabling Better Science. *TACL*, 6:587–604.

Burchell, L., Birch, A., Thompson, R. P., and Heafield, K. (2024). Code-Switched Language
Identification is Harder Than You Think. In *Proceedings of EACL 2024*. https://arxiv.org/abs/2402.01505

Caswell, I., Breiner, T., van Esch, D., and Bapna, A. (2020). Language ID in the Wild: Unexpected
Challenges on the Path to a Thousand-Language Web Text Corpus. In *Proceedings of COLING 2020*.
https://aclanthology.org/2020.coling-main.579/

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., and Crawford,
K. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12):86–92.

Kargaran, A. H., Imani, A., Yvon, F., and Schütze, H. (2023). GlotLID: Language Identification for
Low-Resource Languages. In *Findings of EMNLP 2023*.
https://aclanthology.org/2023.findings-emnlp.410/

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji,
I. D., and Gebru, T. (2019). Model Cards for Model Reporting. In *Proceedings of FAccT 2019*, 220–229.

Muhammad, S. H., Abdulmumin, I., Ayele, A. A., Ousidhoum, N., Adelani, D. I., Yimam, S. M., Ahmad,
I. S., Beloucif, M., Mohammad, S. M., Ruder, S., et al. (2023a). AfriSenti: A Twitter Sentiment
Analysis Benchmark for African Languages. In *Proceedings of EMNLP 2023*, 13968–13981, Singapore.
https://aclanthology.org/2023.emnlp-main.862/

Muhammad, S. H., Abdulmumin, I., Yimam, S. M., Adelani, D. I., Ahmad, I. S., Ousidhoum, N., Ayele,
A. A., Mohammad, S. M., Beloucif, M., and Ruder, S. (2023b). SemEval-2023 Task 12: Sentiment Analysis
for African Languages (AfriSenti-SemEval). In *Proceedings of SemEval-2023*, 2319–2337.
https://aclanthology.org/2023.semeval-1.315/

Muhammad, S. H., Abdulmumin, I., Ayele, A. A., Adelani, D. I., et al. (2025). AfriHate: A Multilingual
Collection of Hate Speech and Abusive Language Datasets for African Languages. In *Proceedings of
NAACL 2025*. https://aclanthology.org/2025.naacl-long.92/

Randolph, J. J. (2005). Free-Marginal Multirater Kappa: An Alternative to Fleiss' Fixed-Marginal
Multirater Kappa. Joensuu University Learning and Instruction Symposium.

NLLB Team, Costa-jussà, M. R., Cross, J., Çelebi, O., Elbayad, M., et al. (2022). No Language Left
Behind: Scaling Human-Centered Machine Translation. arXiv:2207.04672.
https://arxiv.org/abs/2207.04672
