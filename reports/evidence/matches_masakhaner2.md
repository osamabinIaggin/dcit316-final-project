# Criterion matches - MasakhaNER 2.0 (Adelani et al., 2022)

Source: `data/sources/masakhaner2.pdf` -> `reports/evidence/masakhaner2.txt` (1545 lines)

## A1_language_referent

Pattern: `dialect|Akuapem|Asante|Ashanti|Fante|Akan`  -  6 matches

- L168: Akan/Twi (twi)      NC / Kwa                West                  9M    MAFAND-MT (Adelani et al., 2022)   4240/ 605/ 1211             6.3   155,985
- L181: Congo language family, and one language belongs                               ing all Bantu languages, Ghomálá’, Mossi, Akan
- L744: phophonology of noun classes in dagaare and akan.
- L1063: Akan/Twi (twi)               MAFAND-MT (Adelani et al., 2022)                          4240/ 605/ 1211               3588         2474      2375           1433                  6.3        155,985
- L1089: Akan/Twi (twi)          22     c,j,q,v,x,z     E, O                                             yes, 5 tones   no           SVO           isolating          strong prefixing                 active, 6
- L1109: Ghomálá’, Mossi, Akan and Wolof (Nurse and                                                                 the language names themselves. This characteristic

## A2_translated_or_native

Pattern: `translationese|translation corpus|MAFAND|translated into|Wikipedia`  -  28 matches

- L153: Bambara (bam)       NC / Mande              West                 14M    MAFAND-MT (Adelani et al., 2022)   4462/ 638/ 1274             6.5   155,552
- L154: Ghomálá’ (bbj)      NC / Grassfields        Central               1M    MAFAND-MT (Adelani et al., 2022)   3384/ 483/ 966             11.3    69,474
- L155: Éwé (ewe)           NC / Kwa                West                  7M    MAFAND-MT (Adelani et al., 2022)   3505/ 501/ 1001            15.3     90420
- L156: Fon (fon)           NC / Volta-Niger        West                  2M    MAFAND-MT (Adelani et al., 2022)   4343/ 621/ 1240             8.3   173,099
- L160: Luganda (lug)       NC / Bantu              East                  7M    MAFAND-MT (Adelani et al., 2022)   4942/ 706/ 1412            15.6   120,119
- L161: Luo (luo)           Nilo-Saharan            East                  4M    MAFAND-MT (Adelani et al., 2022)   5161/ 737/ 1474            11.7   229,927
- L162: Mossi (mos)         NC / Gur                West                  8M    MAFAND-MT (Adelani et al., 2022)   4532/ 648/ 1294             9.2   168,141
- L163: Naija (pcm)         English-Creole          West                 75M    MAFAND-MT (Adelani et al., 2022)   5646/ 806/ 1613             9.4   206,404
- L167: Setswana (tsn)      NC / Bantu              South                14M    MAFAND-MT (Adelani et al., 2022)   3489/ 499/ 996              8.8   141,069
- L168: Akan/Twi (twi)      NC / Kwa                West                  9M    MAFAND-MT (Adelani et al., 2022)   4240/ 605/ 1211             6.3   155,985
- L169: Wolof (wol)         NC / Senegambia         West                  5M    MAFAND-MT (Adelani et al., 2022)   4593/ 656/ 1312             7.4   181,048
- L224: We also considered using Wikipedia as our data source,
- L231: from either a monolingual or a translation corpus.                   bam      0.980    ✗      pcm      0.966     ✗
- L248: Translation corpus For the remaining languages
- L253: tion corpus, MAFAND-MT (Adelani et al., 2022),                   4.3       Quality Control
- L255: translated into 11 languages. We note that transla-              As discussed in subsection 4.2, language coordi-
- L259: tences is constrained by the size of the MAFAND-                 guage coordinators (i.e. post-intervention score).
- L1048: Bambara (bam)                MAFAND-MT (Adelani et al., 2022)                          4462/ 638/ 1274               4281         2557       429           2898                  6.5        155,552
- L1049: Ghomálá’ (bbj)               MAFAND-MT (Adelani et al., 2022)                          3384/ 483/ 966                2464         1371      1586           2457                 11.3         69,474
- L1050: Éwé (ewe)                    MAFAND-MT (Adelani et al., 2022)                          3505/ 501/ 1001               3931         5168      2064           2665                 15.3          90420
- L1051: Fon (fon)                    MAFAND-MT (Adelani et al., 2022)                          4343/ 621/ 1240               3572         2595      3082           5120                  8.3        173,099
- L1055: Luganda (lug)                MAFAND-MT (Adelani et al., 2022)                          4942/ 706/ 1412               6058         3706      5441           3484                 15.6        120,119
- L1056: Luo (luo)                    MAFAND-MT (Adelani et al., 2022)                          5161/ 737/ 1474               6806         5605      7099           7359                 11.7        229,927
- L1057: Mossi (mos)                  MAFAND-MT (Adelani et al., 2022)                          4532/ 648/ 1294               2804         3044      3209           6334                  9.2        168,141
- L1058: Naija (pcm)                  MAFAND-MT (Adelani et al., 2022)                          5646/ 806/ 1613               4711         5077      5940           3654                  9.4        206,404
- _... 3 further matches_

## A3_native_speakers

Pattern: `native speaker`  -  2 matches

- L240: critics, we asked native speakers to manually add                    mos      0.927    ✗      zul      0.953     ✓
- L665: NER tool used for annotation. We thank Daniel         research—the native speakers of the languages in

## A4_agreement

Pattern: `inter-annotator|Fleiss|kappa|Krippendorff|adjudicat|pre-intervention|post-intervention`  -  17 matches

- L229: of the data we use for annotation. Overall, we col-                        Fleiss’ QC flags         Fleiss’ QC flags
- L230: lected between 4.8K–11K sentences per language                       Lang. Kappa fixed?       Lang. Kappa fixed?
- L242: we ensured that the articles are from a variety of               Table 2: Inter-annotator agreement for our datasets cal-
- L243: topics e.g. politics, sports, culture, technology, so-           culated using Fleiss’ kappa κ at the entity level before
- L244: adjudication. QC flags (✓) are the languages that fixed
- L249: using the adjudication function of ELISA, which
- L251: ensures a high inter-annotator agreement score.
- L258: issues during the annotation. The number of sen-                 the Fleiss Kappa score after the intervention of lan-
- L259: tences is constrained by the size of the MAFAND-                 guage coordinators (i.e. post-intervention score).
- L260: MT corpus, which is between 4,800–8,000.                         The pre-intervention Fleiss Kappa score was much
- L261: lower. For example, for pcm, the pre-intervention
- L262: 4.2 NER Annotation Methodology                                   Fleiss Kappa score was 0.648 and improved to
- L266: tion (LOC), Organization (ORG), and date and time                matically adjudicated when there was agreement,
- L308: 2, before further adjudication and correction there                    pendix J provides the model hyper-parameters for
- L309: was already relatively high inter-annotator agree-                     fine-tuning the PLMs.
- L310: ment measured by Fleiss’ Kappa at the mention
- L679: try to cover 20 topologically diverse languages and   els. The data selection, annotation, adjudication,

## A5_compensation

Pattern: `compensat|remunerat|minimum wage|\bpaid\b`  -  1 matches

- L281: coordinators received appropriate remuneration.6                 marked it was flagged. Similarly, we flagged to-

## A6_datasheet

Pattern: `datasheet|data statement|data card|model card`  -  0 matches

_No match. Recorded as not reported._

## X_twi_mentions

Pattern: `\bTwi\b`  -  25 matches

- L168: Akan/Twi (twi)      NC / Kwa                West                  9M    MAFAND-MT (Adelani et al., 2022)   4240/ 605/ 1211             6.3   155,985
- L236: news articles except for chiShona and Kiswahili                      ibo      0.965    ✗      twi      0.932     ✗
- L356: Model              bam      bbj    ewe        fon        hau        ibo     kin     lug     luo     mos       nya        pcm        sna     swa     tsn     twi     wol      xho         yor        zul        AVG
- L372: Train Lang.          Data               bam       bbj       ewe       fon    hau    ibo    kin     lug      luo    mos      nya       pcm     sna   swa     tsn    twi     wol      xho     yor        zul       AVG
- L486: ing set achieves the best performance. However,                                                               twi          69     64     66    73      56 74 76 86       71    36    60    30
- L519: bam      twi, fon   wol, fon   (dgeo , dinv , sr); (dgeo , sr, dpho )        80.4         47.1        52.8       55.1     54.3          53.0     38.4
- L520: bbj      fon, ewe   twi, ewe   (stf , dsyn , dgeo ); (stf , dgeo , sr)       72.9         53.9        58.8       60.1     59.8          58.4     45.8
- L521: ewe      swa, twi   pcm, swa   (dgeo , stf , sr); (eo, dgeo , stf )          91.7         78.1        81.1       83.9     81.6          81.5     76.4
- L534: twi      swa, nya   swa, ewe   (eo, stf , dgeo ); (dgeo , stf , sr)          82.0         61.9        57.2       64.3     61.0          61.9     49.5
- L627: F1. It is most significant for fon, ibo, kin and twi     In this paper, we present the creation of
- L710: Track, pages 61–75, Virtual. Association for Machine       the case of Yorùbá and Twi. In Proceedings of the
- L1063: Akan/Twi (twi)               MAFAND-MT (Adelani et al., 2022)                          4240/ 605/ 1211               3588         2474      2375           1433                  6.3        155,985
- L1089: Akan/Twi (twi)          22     c,j,q,v,x,z     E, O                                             yes, 5 tones   no           SVO           isolating          strong prefixing                 active, 6
- L1200: twi         77.9    65.5        -12.4   52.2      -25.7    80.4    70.9        -9.5   62.3    -18.1   81.4      72.3       -9.1       63.2    -18.2
- L1228: twi                66.7       89.3       79.4      96.1          76.5     90.4       82.9    97.5           75.7      91.4          85.1    97.7
- L1297: The following definitions are listed here, originally                                                         twi
- L1299: twi
- L1392: twi     54    54      82     60      69          64          66          73      56      57     74     76    32       86    71      82      56          17      36      44      60     30
- L1397: bam    bbj    ewe     fon     hau         ibo         kin         lug     luo     mos    nya   pcm    sna     swa    tsn     twi     wol         xho     yor     zul     ave
- L1444: twi      33   60     79     70      76      72          53          74      62     55      81    73    3.8    67     67     76     80      64      52       82     76      38     63
- L1475: bam          twi, fon          wol, fon   (dgeo , dinv , sr); (dgeo , sr, dpho )           80.4     54.3          53.0         38.4         47.1         53.0
- L1476: bbj          fon, ewe          twi, ewe   (stf , dsyn , dgeo ); (stf , dgeo , sr)          72.9     59.8          58.4         45.8         53.9         58.4
- L1477: ewe          swa, twi          pcm, swa   (dgeo , stf , sr); (eo, dgeo , stf )             91.7     81.6          81.5         76.4         78.1         81.6
- L1490: twi          swa, nya          swa, ewe   (eo, stf , dgeo ); (dgeo , stf , sr)             82.0     61.0          61.9         49.5         61.9         53.7
- L1538: bam bbj ewe fon hau ibo                     kin    lug     luo mos nya pcm sna swa tsn                      twi    wol xho yor        zul   ave

## X_ewe_mentions

Pattern: `\bEwe\b|\bÉwé\b`  -  28 matches

- L155: Éwé (ewe)           NC / Kwa                West                  7M    MAFAND-MT (Adelani et al., 2022)   3505/ 501/ 1001            15.3     90420
- L189: Gur, Kwa, and Volta-Niger.                                                    Niger-Congo languages such as Fon, Ewe, Igbo
- L233: Monolingual corpus We collect a large monolin-                       ewe      0.991    ✓      sna      0.957     ✓
- L356: Model              bam      bbj    ewe        fon        hau        ibo     kin     lug     luo     mos       nya        pcm        sna     swa     tsn     twi     wol      xho         yor        zul        AVG
- L372: Train Lang.          Data               bam       bbj       ewe       fon    hau    ibo    kin     lug      luo    mos      nya       pcm     sna   swa     tsn    twi     wol      xho     yor        zul       AVG
- L466: 48 − 60 F1 except for ewe, nya, tsn, and zul with                                                            nor           70     59     64    79      56 78 77 85       66    42    57
- L469: ewe            69     59     63    76      44 66 66 82       61    39    58    70
- L520: bbj      fon, ewe   twi, ewe   (stf , dsyn , dgeo ); (stf , dgeo , sr)       72.9         53.9        58.8       60.1     59.8          58.4     45.8
- L521: ewe      swa, twi   pcm, swa   (dgeo , stf , sr); (eo, dgeo , stf )          91.7         78.1        81.1       83.9     81.6          81.5     76.4
- L522: fon      mos, bbj   yor, ewe   (dgeo , dsyn , sr); (stf , dgeo , dgen )      84.9         58.4        64.9       69.9     65.4          62.0     50.6
- L528: mos      fon, ewe   yor, fon   (dgeo , dinv , sr); (dgeo , stf , sr)         78.9         50.8        62.5       65.6     64.2          60.4     45.4
- L534: twi      swa, nya   swa, ewe   (eo, stf , dgeo ); (dgeo , stf , sr)          82.0         61.9        57.2       64.3     61.0          61.9     49.5
- L1050: Éwé (ewe)                    MAFAND-MT (Adelani et al., 2022)                          3505/ 501/ 1001               3931         5168      2064           2665                 15.3          90420
- L1075: Éwé (ewe)               35     c, j, q         ã, dz, E, ƒ, gb, G, kp, ny, N, O, ts, V          yes, 3 tones   yes          SVO           isolating          equal prefixing and suffixing    vestigial
- L1117: Fon, Ewe, Igbo and Yorùbá, the use of noun classes                                                         with a complex morphology. Each root or stem can
- L1188: ewe         89.5    75.6        -13.9   70.6      -18.9    90.0    76.9       -13.1     70    -20.0   91.0      79.7      -11.3       74.2    -16.8
- L1216: ewe                91.8       96.8       85.5      95.9          91.8     96.4       88.6    97.1           92.0      97.8          85.6    98.6
- L1269: MasakhaNER 2.0 based on performance on zero-                 50                                               ewe
- L1271: ewe
- L1374: ewe       50    58      92     61      69          59          63          76      44      60     66     66    37       82    61      54      53          39      39      39      58     70
- L1397: bam    bbj    ewe     fon     hau         ibo         kin         lug     luo     mos    nya   pcm    sna     swa    tsn     twi     wol         xho     yor     zul     ave
- L1431: ewe        38   63     75     65      72      68          54          73      53     45      81    71     12    69     76     69     79      59      52       78     73      55     63     40
- L1476: bbj          fon, ewe          twi, ewe   (stf , dsyn , dgeo ); (stf , dgeo , sr)          72.9     59.8          58.4         45.8         53.9         58.4
- L1477: ewe          swa, twi          pcm, swa   (dgeo , stf , sr); (eo, dgeo , stf )             91.7     81.6          81.5         76.4         78.1         81.6
- L1478: fon          mos, bbj          yor, ewe   (dgeo , dsyn , sr); (stf , dgeo , dgen )         84.9     65.4          62.0         50.6         58.4         61.4
- _... 3 further matches_

