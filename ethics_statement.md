# Ethics statement

## Data

All text comes from public research releases. I did not scrape, collect or annotate
anything new. AfriSenti tweets are public posts with handles and links removed by the dataset's
authors. I report results only in aggregate. The handful of tweets quoted in the error analysis are
short, carry no handles, and are already distributed in a public benchmark.

## Redistribution

The AfriSenti and MasakhaNER repositories declare no licence, so the raw data is
kept out of this repository and fetched from the source instead. The NLLB translations of the test tweets are committed because the error analysis depends on them. Per-system predictions are committed by row number, without the tweet text.

## Who this could harm

The audit criticises the documentation of resources built by small,
often volunteer-heavy African NLP teams. Those teams documented more than most of the field does, and that is why an audit could find anything. I have tried to describe absences ("not reported") as
absences, without implying poor practice, and to quote each source in full where the context
changes the meaning.

## Language and community

The paper makes claims about Twi, a language I do not read well enough
to judge translation quality. No claim in it rests on my own reading of Twi text. Where a judgement
needs a native speaker, the paper says so and leaves it undone.

## Commercial systems

Google Translate is discussed but not tested. Testing it properly needs the
paid Cloud Translation API, and I had no key; pasting 949 tweets through the web page by hand would
not have produced a reproducible result.
