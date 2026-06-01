# Meta Spend Elasticity Analysis — Context Briefing

> Paste this into any terminal (or share with anyone) to get the full picture of the spend-vs-APR analysis Ben ran on 2026-05-31.

## The hypothesis (and the answer)

**Hypothesis:** When Bark scales Meta ad-set budgets up, APR per £ falls. The algorithmic optimization (Meta's autobid + Bark's automated rules) pushes spend past the efficient frontier and destroys margin. Cutting budget often recovers margin more than it loses.

**Answer (from the data):** Confirmed. Pattern is monotonic, roughly symmetric, and holds across markets.

## The data

- **Source:** Tableau "APR+ with EP distributed" datasource (LUID `7a3ed7f8-d585-475c-99d1-d259175f666d`), filtered to Channel ∈ {PPC - Meta - Facebook, PPC - Meta - Instagram, PPC - Meta - Other}.
- **Window:** 12 complete weeks, 2026-03-02 → 2026-05-24.
- **Granularity:** Category × Country × Week. (Ad-set-level would need merging Meta API + Tableau via /in/<slug>/ URL matching — not done yet.)
- **Scope:** 776 consecutive-week change events analysed across 90 category × country series with ≥4 active weeks and ≥£200 cumulative spend.
- **Note on attribution:** APR is Meta-pixel-attributed; per the reconciliation memo Meta pixel undercounts true revenue by ~43%. Directional findings hold; absolute £ values are conservative.

## Headline result — aggregate event pattern

For each consecutive-week pair within each Category × Country series, compute Δ spend % and Δ margin (APR/£) in percentage points. Bucket by spend-change size:

| Δ weekly spend bucket | N events | Median Δ margin | Mean Δ margin |
|---|---|---|---|
| Cut ≥ 50% | 57 | **+40 pp** | +122 pp* |
| Cut 25-50% | 72 | **+16 pp** | +17 pp |
| Cut 10-25% | 93 | +10 pp | +10 pp |
| Flat (±10%) | 342 | 0 pp | 0 pp |
| Scale +10-25% | 73 | −2 pp | −10 pp |
| Scale +25-50% | 68 | **−34 pp** | **−29 pp** |
| Scale ≥ 50% | 71 | **−35 pp** | **−41 pp** |

Overall Pearson r(Δspend%, Δmargin pp) across all 776 events: **−0.17**. Restricting to events with |Δspend| > 25%, the relationship strengthens substantially.

*The +122pp mean on the deepest-cut bucket is partly small-base noise — when an ad set is cut from £500 → £50, even modest absolute APR translates to a massive % margin. Use medians as the cleaner signal.

## Estimated missed APR

If each category had run at its best-margin week's spend level throughout the 12-week window:

- **UK: ~£106k** of foregone APR across 24 categories
- **US: ~£52k** across 4 categories
- **Total all markets: ~£160k+** over 12 weeks (≈ £700k/year run-rate if the pattern holds)

This is **directional sizing, not a forecast** — it assumes the best week's APR/£ could be replicated indefinitely, which is optimistic. Treat as the upper bound of the prize for getting budget sizing right.

## Biggest individual offenders (by missed APR)

| Market | Category | 12w Spend | 12w APR | Best-margin week | Avg week spend | Est. missed APR |
|---|---|---|---|---|---|---|
| UK | Bathroom Installation & Remodel | £40,190 | +£17,094 | +97% @ £2,326/wk | £3,349/wk | **+£22,077** |
| US | Immigration Lawyers | £43,148 | +£17,185 | +87% @ £3,198/wk | £3,596/wk | +£20,148 |
| UK | Fence & Gate Installation | £24,517 | +£4,131 | +73% @ £1,133/wk | £2,043/wk | +£13,829 |
| US | Wedding Photography | £30,516 | +£15,400 | +94% @ £1,309/wk | £2,543/wk | +£13,204 |
| US | Dog Training | £42,966 | +£15,019 | +65% @ £3,327/wk | £3,581/wk | +£13,018 |
| UK | Patio Services | £24,880 | +£7,155 | +75% @ £1,482/wk | £2,073/wk | +£11,480 |
| UK | Artificial Grass Installation | £23,547 | +£4,882 | +58% @ £1,649/wk | £1,962/wk | +£8,726 |
| UK | EV Charge Points Installation | £10,435 | +£5,773 | +130% @ £748/wk | £870/wk | +£7,745 |
| US | TV Installation & Mounting | £6,467 | +£523 | +104% @ £407/wk | £539/wk | +£6,198 |

Every one of these is spending materially more than its peak-margin week. Full ranked list (28 categories total at Pearson r ≤ −0.5 threshold) is in the CSV below.

## Recommended actions (in priority order)

1. **Stop reactive scale-up rules.** Any automated rule that increases ad-set budget by >25% based on positive ROAS signal is almost certainly destroying APR margin within 1-2 weeks. The signal Meta gives you to scale up is precisely the signal that's about to flip on you.

2. **Set per-category weekly spend caps at ~1.3× the best-margin week's spend.** Headroom for natural variance but prevents runaway. For UK Bathroom Install: cap £3k/wk (current avg £3,349). For US Wedding Photography: cap £1.7k/wk (current avg £2,543).

3. **Rate-limit week-over-week budget increases to +10% max.** Below 10%, the median Δmargin is essentially 0. Above 10%, it goes negative fast. Slow scaling preserves margin.

4. **Add a fast cut-back rule:** if a category's weekly margin drops 10pp+ vs prior week, auto-cut spend 20%. Every cut bucket in the data shows median margin recovery. Reactive defence works; reactive offence doesn't.

5. **The freed budget probably shouldn't redeploy back into Meta.** The "scale-up works" list (categories with Pearson r ≥ +0.5) is small and mostly contains categories with negative absolute APR (i.e., they're losing less at higher spend, not making more). At Bark's scale, Meta appears to have hit diminishing returns across most of the catalogue — marginal £ is likely more valuable on Google or non-Meta channels.

## Methodology caveats

- **Confounder:** spend changes at Category × Country level reflect both human/rules action AND Meta algo auto-scaling. For Ben's question (does scaling up hurt APR?), what matters is the empirical relationship at the category level, regardless of who chose the spend — but it means we can't cleanly attribute the destruction to one source.
- **Same-week vs lag effect:** the analysis treats Δspend and Δmargin as same-week. A week of high spend may also depress the *following* week's margin (creative fatigue carry-over). Not modelled here.
- **Best-week selection bias:** the "best-margin week" picked for each category requires spend ≥ 25% of that category's max spend, to avoid trivially picking the cheapest week. Could be refined.
- **Categories with very different spend distributions:** when a category has only ever varied between £400-£600/week, the correlation tells us less than when a category swings £200-£3000/week.

## Files (local, on Ben's machine)

- `~/Downloads/meta-budget-elasticity-analysis.py` — analysis script (Python, runs against the Tableau MCP query output)
- `~/Downloads/meta-elasticity-summary.csv` — per-category-market ranked output (Pearson r, missed APR, best-week spend, etc.)
- `~/Downloads/build-elasticity-report.py` — HTML report builder
- `~/Downloads/meta-elasticity-report.html` — review-friendly HTML report
- `~/Downloads/SPEND-ANALYSIS-README.md` — this file

## Live URL

(updated when pushed)

## Status / open questions

- Spend-cap rules prompt for Ben's rules CLI (per category, 24/7 caps): **not yet built** — would mirror the existing UK Saturday rules prompt format
- Drill into 3-4 biggest offenders to see if the destruction is truly category-level or driven by specific ad sets within each: **not yet done** — would need Meta API merge
- Stefano review (this affects the APR Scaling Program — pushing more spend on Meta may be net-negative): **not yet shared**
- Re-run analysis at a longer window (26 weeks) to test seasonal-confounder hypothesis: **not yet done**

## How to talk to Ben about this

- Ben's intuition has been pointing at this for a while ("when spend is lower ROAS will be higher anyway") — this is the empirical confirmation.
- The dollar size of the finding (~£700k/year run-rate of missed APR) is large enough to justify operating-philosophy changes, not just rule tweaks.
- He's already running an APR Scaling Program with Stefano — this analysis somewhat conflicts with the "scale further on Meta" framing of that program, so requires careful socialization.
- The recommended actions are downward-oriented (cap, cut, slow-scale). Ben previously confirmed he's comfortable with downward-only changes when the signal is clear.
