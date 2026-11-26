[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/ryan-akmal/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/ryan-akmal/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World in One Day — Thursday, 26 November 2026

**make.fun competition:** `news-image-20261126` — "Sum up 26 November's world news in one image"
**Entry title:** The World in One Day — Thursday, 26 November 2026

A one-page newspaper front page that sums up Thursday 26 November 2026 in
a single image. The date is named in the masthead; six stories cover trade,
Egypt, markets, North Korea, Ukraine and Russia's war toll, with six more
in the "Also in the news" strip.

## The six stories

1. **US unveils sweeping new tariffs** — Washington proposes Section 301
   duties on 14 trading partners to fight factory overcapacity; China is
   hit hardest, at nearly 45%, and markets recoil.
2. **Cairo tanker inferno kills 31** — A fuel tanker crashes on the
   highway near the Warraq tunnel in Giza; a huge fire follows, 31 killed,
   15 injured.
3. **Nasdaq sinks nearly 4% in AI rout** — US stocks fall further as AI
   fears intensify; Nvidia down 5% and all three main indexes slide.
4. **Pyongyang expels Swiss envoy** — North Korea orders Switzerland to
   close its diplomatic office in a sanctions row; Kim urges wider
   tactical nuclear deployment.
5. **Ukraine hits Russian air base** — A strike on Savasleyka airbase
   damages five planes — three MiG-31s and two Su-34s; 88 of 112 drones
   downed overnight.
6. **Russia's own toll: nearly 500,000 dead** — Moscow's own figures show
   almost half a million military deaths in the Ukraine war.

Also in the news: BepiColombo reaches Mercury orbit after an 8-year
journey; the Hera probe revisits the asteroid crater four years after the
DART impact; Israeli judges urge dropping the gravest charges against
Netanyahu; a Pakistani astronaut joins China's Shenzhou-24 mission;
Bangladesh raises garment wages 36%; Colombia frees 20 supermarket
hostages.

## How the image was made

`generate_image.py` draws the front page with Pillow: flat vector-style
pictograms and DejaVu typesetting, no photographs, no copied artwork, no
network. `main.ts` copies the finished `entry.png` to the output directory
the grader reads.

Run it: `python3 generate_image.py` (writes `entry.png`), then
`mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.
