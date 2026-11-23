[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/akbare12/news-22-b8-breaking-live/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/akbare12/news-22-b8-breaking-live/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# THE WORLD TODAY — Live Blog: Sunday 22 November 2026

One image summing up the world's news of Sunday 22 November 2026, told as a
**live blog**: timestamped updates in reverse-chronological order, newest first,
all times UTC — the day as it happened, from the 00:04 Gaza toll update to the
18:00 Democrats-win-258 call.

## How to read it

- **Top updates** — 18:00 UTC: Democrats win 258 House seats (Hubbard beats Foxx
  by 330 votes in the NC recount; largest Dem majority since 1992). 17:13 UTC:
  two supertankers hit mines east of the Strait of Hormuz, north of Ghanam
  Island; both on fire.
- **Live feed** — 28 more timestamped updates, newest first, each with a named
  source and a verification badge: REPORTED (confirmed by 2+ sources) or CLAIM
  (one side alleges, unverified).
- **Where it happened** — a map with 8 numbered pins: 1 Hormuz, 2 Antalya,
  3 Washington, 4 Benghazi, 5 Khartoum, 6 Kyiv, 7 Banten, 8 Gaza.
- **Numbers strip** — 258 House seats · 2 tankers hit · 194 COP31 parties ·
  330 votes in NC · 36 missing in Banten · 1,661 Gaza toll.
- **Not yet** — 4 House races uncalled · COP32 venue not set · Gaza ceasefire
  talks: no deal announced. These are not presented as done.
- **Date check** — every story was first reported on 22 Nov. Excluded on purpose:
  El Chapo Isidro captured 20 Nov · BepiColombo Mercury orbit 21 Nov · ICJ
  Myanmar ruling 19 Nov · Wall St rout 20 Nov · FBI NCIC hack first reported
  21 Nov.

## The 30 stories (newest first)

| Time (UTC) | Story | Source |
|---|---|---|
| 18:00 | Democrats win 258 House seats; Hubbard beats Foxx by 330 in NC recount | AP · Reuters |
| 17:13 | Two supertankers hit mines east of Strait of Hormuz, both on fire | Iran navy · AP |
| 15:36 | Merkury hit at Benghazi — Ukraine: 7 naval drones sank Russian corvette | France 24 (CLAIM) |
| 15:03 | Khartoum drones kill 4, UN building damaged; blamed on RSF | AP (CLAIM) |
| 14:48 | Zelenskyy pleads for Patriots; Russia fired ~2,700 drones in a week | BBC |
| 14:20 | Iran shows underground missile city, dual-missile launcher | IRGC media |
| 13:16 | Saudis stop Houthi attack; Rabigh refinery claimed hit | Reuters (CLAIM) |
| 12:00 | COP31 ends, no deal — EU + ~130 parties reject text with no fossil fuels | CNN · Reuters |
| 10:25 | Ex-Italian police chief found dead amid Sicily bombing inquiry | ANSA |
| 09:53 | UAE condemns Iranian attack on Bahrain as sovereignty violation | WAM |
| 09:41 | Europe protests, day 3 — cost & housing marches | AP |
| 07:47 | Settlers burn 12 cars in West Bank villages | WAFA |
| 07:36 | Benghazi ammo depot blast inside naval base | Local auth. |
| 06:58 | Eisenkot–Likud unity talks stall | Israeli media |
| 06:15 | Finland: war spills over after Baltic cargo-ship drone strike | Finnish govt |
| 05:48 | WCK: 3 killed in Gaza aid-van strike were not its team | WCK |
| 04:22 | Ex-UN envoy de Soto: Iran war was "perfectly avoidable" | MED Dialogues |
| 04:19 | Banten factory fire — 3 dead, 36 missing in Cikande | BBC |
| 03:56 | Fidan: Israel may use Druze support to provoke Syria operation | Anadolu (CLAIM) |
| 03:24 | Bahrain blames Iran for industrial-site strike | France 24 |
| 03:18 | Fidan: US-Israel war fallout threatens global markets | Anadolu |
| 02:38 | Aoun: Israel must leave "every inch" of Lebanon | Al Jazeera |
| 02:14 | Gaza: 350,000 families homeless; protest near Yellow Line | Al Jazeera |
| 02:09 | Pezeshkian: Iran in "silent economic war"; blockade hits 130 days | IRNA |
| 01:35 | Settlers attack homes in Hebron and Ramallah | WAFA |
| 01:04 | Turkey: Israel blocking thousands of Gaza container homes | Anadolu (CLAIM) |
| 00:44 | Hind Rajab Foundation urges Germany to arrest Israeli soldier | HRF |
| 00:26 | Fred Nile, NSW Christian Democratic figurehead, dies at 92 | Guardian |
| 00:09 | Teen gamer, 16, and his mother help FBI rescue missing girl | FBI |
| 00:04 | Gaza death toll since Oct 2025 ceasefire: 1,661 | Gaza health min. |

Note: Fred Nile died on 21 Nov and was announced on 22 Nov; the story is listed
by its first report on 22 Nov. The Banten toll shown (3 dead, 36 missing) is the
figure first reported on 22 Nov. The Gaza protest entry (02:14) sits between the
02:38 and 02:09 updates in the day's running order, as first reported on 22 Nov.

## How the image was made

`draw.py` draws `entry.png` (1024×1024, 174,072 bytes) with Pillow: masthead,
live bar, numbers strip, two hero updates, a sketch map with 8 numbered pins,
and the 28-entry live feed. `main.py` is a stdlib-only copy program that writes
`entry.png` to `/output/entry.png` and verifies its size and SHA-256; it runs
twice with byte-identical output. No network is used at run time.

## Sources

AP · Reuters · BBC · CNN · France 24 · Al Jazeera · Guardian · SCMP · IRNA ·
Anadolu · WAFA · HRF · WCK · CNBC · The Hindu · Daily Summary Of (final edition
22 Nov 2026, updated 23:45 UTC) · One Turn.

## License

MIT — see LICENSE.
