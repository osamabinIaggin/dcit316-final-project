# Literature matrix

Every entry was checked against the publisher's record; BibTeX for ACL Anthology papers is saved in
`reports/references/`.

| Work | Venue | What it provides | How this project uses it | Checked via |
|---|---|---|---|---|
| Muhammad et al., AfriSenti | EMNLP 2023 | Twitter sentiment data for 14 African languages, Twi among them | Main evaluation data; audited for documentation | Anthology `2023.emnlp-main.862` |
| Muhammad et al., SemEval-2023 Task 12 | SemEval 2023 | Shared task built on AfriSenti | Citation required by the data README | Anthology `2023.semeval-1.315` |
| Muhammad et al., AfriHate | NAACL 2025 | Hate and abusive language data, 15 languages incl. Twi | Audited for documentation | Anthology `2025.naacl-long.92` |
| Adelani et al., MasakhaNER 2.0 | EMNLP 2022 | NER for 20 languages incl. Twi and Ewe | Second rung of the domain ladder; audited | Anthology `2022.emnlp-main.298` |
| Adelani et al., MAFAND-MT | NAACL 2022 | Translated news corpus that MasakhaNER's Twi text comes from | Provenance of the translationese finding | Anthology `2022.naacl-main.223` |
| NLLB Team, No Language Left Behind | arXiv 2022 | NLLB-200 model and FLORES-200 benchmark | Translation system under test; first rung of the ladder | arXiv 2207.04672 |
| Abdulmumin et al., Correcting FLORES | arXiv 2024 | Native-speaker corrections of FLORES for four African languages | Precedent; shows Ghanaian languages unchecked | arXiv 2409.00626 |
| Barbieri et al., TweetEval | Findings EMNLP 2020 | English tweet sentiment benchmark | Training data lineage of the English model | Anthology `2020.findings-emnlp.148` |
| Loureiro et al., TimeLMs | ACL 2022 demos | Twitter-RoBERTa models | The English-only system | Anthology `2022.acl-demo.25` |
| Barbieri et al., XLM-T | LREC 2022 | Multilingual Twitter model fine-tuned for sentiment in 8 languages | The multilingual zero-shot system | Anthology `2022.lrec-1.27` |
| Caswell et al., Language ID in the Wild | COLING 2020 | Evidence that LID precision collapses on web text for low-resource languages | Context for AfriSenti's model-assigned language labels | Anthology `2020.coling-main.579` |
| Burchell et al., Code-switched LID | EACL 2024 | LID on code-switched text remains unsolved | Why sentence-level language labels are fragile | Anthology `2024.eacl-long.38` |
| Adebara et al., AfroLID | EMNLP 2022 | LID for 517 African languages | Named in future work; not run | Anthology `2022.emnlp-main.128` |
| Kargaran et al., GlotLID | Findings EMNLP 2023 | Open LID for low-resource languages | Named in future work; not run | Anthology `2023.findings-emnlp.410` |
| Bender & Friedman, Data Statements | TACL 2018 | Documentation standard for NLP data | Basis for criteria A1, A3, A6 | Anthology `Q18-1041` |
| Gebru et al., Datasheets for Datasets | CACM 2021 | Documentation standard | Basis for criteria A3, A5, A6 | Publisher record |
| Mitchell et al., Model Cards | FAccT 2019 | Model documentation standard | Basis for A6 and this repo's model card | Publisher record |
| Randolph, Free-marginal kappa | 2005 symposium paper | The agreement statistic AfriSenti and AfriHate report | Why their kappa is not comparable to Fleiss' | Cited in AfriSenti |
