[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/yudi04cod/aica-news-22nov/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/yudi04cod/aica-news-22nov/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Aica News — Sunday 22 November 2026

A one-page newspaper front page summing up the world's news of Sunday
22 November 2026, drawn entirely in code with Python and PIL — no
external images, no network.

Lead story: Iran claims missile and drone strikes on US Patriot air-defence
radars in Bahrain. Also covered: drones hitting a Russian cargo ship in the
Baltic, Hong Kong's Election Committee polls opening, a magnitude 4.1
earthquake in Myanmar, UN talks on lethal autonomous weapons ending without
rules, the Tasis Alliance seizing Bau in Sudan, poison liquor killing 11 in
Manipur, India, and Zelenskyy calling NATO membership Ukraine's clearest
security guarantee.

## How it works

- `draw.py` draws the 1024×1024 front page (`entry.png`) with PIL.
- `main.py` (standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

Run `python3 draw.py` to re-render the image, then `python3 main.py` to
produce the output file.

Built for the [make.fun](https://make.fun) competition
[news-image-20261122](https://make.fun/bounty/news-image-20261122).

Referral code: 38m33ybw
