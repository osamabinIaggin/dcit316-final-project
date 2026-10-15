# Ethics Statement

Gideon Elorm Glago (22128981) | DCIT 316 Final Course Project

---

## 1. The data represents real people

Unlike the synthetic Week 10 corpus in IA6, AfriSenti's tweets were written by real Twitter users.
The dataset's authors removed handles and links before release (none of the 4,818 Twi tweets
contains an `@` handle or URL), and the release carries no user IDs or per-tweet location. I added
nothing that could link a tweet back to its author.

## 2. What I did not do

I did not scrape, collect or annotate any new data, and I contacted no one. Every corpus is a public
research release, downloaded from a pinned commit by `scripts/fetch_data.py`. The four audited papers
are public PDFs.

## 3. Redistribution

The AfriSenti and MasakhaNER repositories declare no licence. I therefore keep the raw text out of
this public repository and fetch it from the source instead. What is committed:

- per-system predictions keyed by test-row number, without the tweet text;
- NLLB's English translations of the test tweets, which the error analysis depends on;
- samples of at most 25 tweets per error type in `reports/error_analysis/`, quoted for analysis.

## 4. Misrepresentation risk

Two sentences could travel out of this repository and mislead.

The first is the claim the paper audits: "supports Twi". The paper shows that the evidence behind
it is translated text in standard orthography, so I report every capability result next to the
distance between that text and tweets.

The second is my own headline. "A TF-IDF model beats XLM-T on Twi" is true for these systems on this
test set and nothing wider. An Africa-centric model fine-tuned on AfriSenti was not tested and could
well do better. The abstract, discussion and conclusion state that scope.

## 5. Harm if the English-only tool were deployed

An analyst measuring Ghanaian public mood with the English Twitter model would see Twi speakers as
far calmer than they are: it labels 83.3% of positive and negative Twi tweets neutral, and the emoji
ablation shows its few non-neutral calls come from the emoji. The error gives no warning. The people
most affected would be those who post mainly in Twi, whose complaints would disappear into
"neutral" while English-language posts were counted at face value.

## 6. The people the audit criticises

The documentation audit names AfriSenti, AfriHate, MasakhaNER 2.0 and FLORES-200, built by
research teams, many of them African-led and volunteer-heavy, who documented more than most of the
field does. That openness is why an audit could find anything. I describe absences as absences
("not found in the paper") and do not infer poor practice from them, and I quote each source in full
where the surrounding sentence changes the meaning.

## 7. My language ability

My Twi and Pidgin are fluent; my Ga and Ewe are not, as I stated in IA6. Fluency is not the same as
training as a translator or annotator, so I did not grade NLLB's translations or relabel any tweets.
No result in the paper depends on my own reading of Twi text.

## 8. Commercial systems

Google Translate is discussed but not tested. Testing it properly needs the paid Cloud Translation
API, which I did not have, and pasting 949 tweets through the web page by hand would not produce a
reproducible result.

## 9. Reuse

Anyone reusing this repository should carry forward: AfriSenti's Twi labels have κ = 0.51 and their
authors describe many Twi tweets as ambiguous; FLORES-200's two Twi files are unlabelled for dialect;
and no capability number here should be quoted without the test set and the systems it applies to.
