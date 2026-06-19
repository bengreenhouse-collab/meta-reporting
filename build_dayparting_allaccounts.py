#!/usr/bin/env python3
"""Generate the all-accounts dayparting dashboard (account + category DoW)."""
from pathlib import Path

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# occurrences of each weekday in the 90d window (Mon..Sun)
DIVISORS = [13, 13, 12, 12, 13, 13, 13]
NDAYS = sum(DIVISORS)  # 89

# ---- Account 90d totals (Meta, GBP-normalised), ordered by revenue ----
ACCOUNTS = [
    ("🇬🇧", "United Kingdom", 730492, 567320),
    ("🇺🇸", "United States",  593349, 445496),
    ("🇨🇦", "Canada",          84849,  54315),
    ("🇿🇦", "South Africa",    18673,  13002),
    ("🇮🇪", "Ireland",         14443,  14999),
    ("🇩🇪", "Deutschland",      6391,   5858),
    ("🇫🇷", "France",           3901,   3796),
    ("🇳🇿", "New Zealand",      2949,   1530),
    ("🇦🇺", "Australia",        2854,   2923),
]

# ---- Account x DoW: name -> {day: (rev, spend)} in Mon..Sun order ----
ACCT_DOW = {
 "United Kingdom": [(123973,87845),(128779,101697),(122649,97187),(113359,89500),(106597,91964),(64382,43483),(70753,55643)],
 "United States":  [(105829,71594),(104666,74538),(93778,67251),(92063,66198),(88494,69090),(50950,44656),(57569,52168)],
 "Canada":         [(10989,6174),(14552,9629),(14990,9251),(15150,9187),(12936,8670),(7637,5117),(8594,6287)],
 "South Africa":   [(3396,1927),(3277,1905),(2771,1748),(2893,1888),(2764,2010),(1729,1865),(1843,1658)],
 "Ireland":        [(2154,2224),(3176,2950),(2559,2874),(2372,2721),(2707,3361),(946,394),(528,476)],
 "Deutschland":    [(886,911),(1228,830),(968,771),(756,750),(1143,908),(512,719),(899,971)],
 "France":         [(707,528),(654,559),(419,498),(592,617),(558,605),(453,442),(519,548)],
 "New Zealand":    [(539,280),(578,415),(0,0),(38,69),(515,248),(640,261),(640,256)],
 "Australia":      [(726,456),(602,571),(0,66),(42,253),(501,594),(584,516),(398,467)],
}

# ---- Category x DoW per account: name -> [(rev,spend) Mon..Sun] ----
CATS = {
 "🇬🇧 United Kingdom": {
  "Landscaping":[(17345,10063),(16900,11387),(16516,10917),(13732,9880),(13610,9526),(10259,5746),(10588,7457)],
  "Home & Domiciliary Care":[(9438,6884),(11114,7696),(10677,6836),(10395,6588),(7836,6619),(4566,4067),(5273,5274)],
  "Bathroom Installation & Remodel":[(11063,6731),(11600,7385),(9511,7142),(9788,6782),(8387,6891),(4946,3223),(4922,4063)],
  "Painting & Decoration - Interior":[(8729,6879),(8902,7092),(8242,6901),(8463,6778),(8381,7296),(6128,3634),(6392,5368)],
  "Tree Surgery & Removal":[(6474,4777),(6919,6060),(7832,5533),(5625,4850),(6048,5296),(3843,2331),(3150,1766)],
  "Driveway Installation":[(8362,6630),(7887,7433),(8583,7059),(7452,7010),(7732,7353),(4413,3006),(4441,4045)],
  "Fence & Gate Installation":[(5290,3832),(5479,4380),(5029,4319),(4117,3962),(4258,4053),(2493,1989),(3099,2625)],
  "House Cleaning":[(5497,3955),(6623,4755),(6456,4393),(5099,3814),(5045,4063),(2883,1919),(3655,2607)],
  "Artificial Grass Installation":[(5440,3799),(4720,4143),(4930,4188),(4351,3852),(4382,4295),(2599,1841),(3091,2315)],
  "Patio Services":[(5010,3713),(6715,4924),(5597,4843),(5239,4326),(4793,4178),(2788,1712),(3231,2353)],
  "Wedding Photography":[(3265,2074),(3363,2351),(2908,2205),(2824,1975),(2731,2194),(1834,1099),(2549,1414)],
  "Roof Repair":[(5044,4276),(4671,5181),(4205,4730),(3565,4148),(4160,4670),(2546,2076),(2440,2661)],
  "Brick & Block Paving Services":[(2961,2065),(3038,2450),(3188,2350),(3156,2119),(2100,1450),(916,562),(722,703)],
  "Garage Door Installation":[(2220,1864),(3230,2409),(2542,2368),(2393,2109),(2051,2255),(1558,874),(2110,1193)],
  "Electric Charge Points Installation":[(2820,1622),(3432,1897),(2735,1958),(3059,1693),(2158,1748),(1245,805),(1673,1030)],
 },
 "🇺🇸 United States": {
  "Immigration Lawyers":[(13870,7262),(11518,7483),(9183,6749),(8968,6575),(9586,7067),(5149,4819),(6073,5490)],
  "Dog Training":[(13446,7072),(9789,7433),(10209,6609),(9098,6639),(9369,7099),(5260,4966),(4321,5806)],
  "House Cleaning":[(11377,7393),(10474,7656),(11336,6780),(10050,6741),(10019,7076),(5058,4489),(5662,5322)],
  "DJ":[(9968,8535),(12555,9141),(11211,8323),(11302,8311),(8762,7267),(5226,3543),(6997,4215)],
  "Architectural Services":[(9131,5810),(9016,6260),(8268,5763),(9239,5502),(8157,5503),(4417,3268),(4895,3879)],
  "Wedding Photography":[(8087,5242),(8561,5500),(7830,4995),(8092,4760),(7026,5342),(4339,3387),(4760,3897)],
  "Catering":[(7185,4858),(6794,5095),(6969,4547),(5631,4584),(5963,5021),(4417,3563),(4539,4250)],
  "Web Design":[(5825,4680),(6315,4911),(6044,4586),(5272,4366),(5707,4890),(2873,3103),(4005,3583)],
  "Photo Booth Hire":[(5089,3708),(4542,3580),(4725,3305),(4314,3206),(3995,3402),(2926,2325),(3262,2792)],
  "Limousine Hire":[(4541,2901),(4691,3117),(4237,2733),(4298,2799),(3488,2981),(2546,2004),(3235,2306)],
  "Bookkeeping Services":[(3492,3080),(4239,3075),(2152,2811),(2739,2597),(3776,2700),(1710,1927),(2426,2197)],
  "Personal Trainers":[(4225,3077),(4440,3270),(4107,2927),(3335,2886),(3770,3199),(2258,2253),(2466,2603)],
  "Residential Interior Designers":[(2974,1821),(4300,1902),(2408,1673),(2976,1655),(2427,1844),(1616,1253),(1846,1474)],
  "Private Investigators":[(2300,1891),(2174,1984),(1867,1802),(2536,1847),(2132,2070),(1390,1398),(1549,1554)],
  "TV Installation & Mounting":[(1396,1074),(1263,1134),(1146,1025),(1043,1008),(955,1087),(678,720),(874,844)],
 },
 "🇨🇦 Canada": {
  "Bathroom Installation & Remodel":[(2089,891),(2312,1589),(3179,1781),(3178,1740),(2567,1526),(1493,761),(1557,927)],
  "House Cleaning":[(1732,721),(1669,754),(1366,515),(1583,593),(1436,594),(932,482),(1298,707)],
  "Fence & Gate Installation":[(1902,846),(1616,847),(1129,674),(1352,674),(1202,721),(1096,637),(1478,895)],
  "Driveway Installation":[(329,283),(1688,789),(1926,903),(1808,833),(1318,688),(426,259),(541,330)],
  "Property Extensions":[(732,377),(1880,1185),(2402,1325),(2153,1261),(1572,1150),(778,346),(458,399)],
  "Home & Domiciliary Care":[(648,498),(1157,761),(1075,763),(782,705),(910,707),(492,432),(482,458)],
  "Painting & Decoration - Interior":[(912,486),(994,477),(724,327),(573,375),(785,402),(485,420),(861,475)],
  "Landscaping":[(709,479),(680,461),(600,375),(863,503),(620,465),(404,397),(671,524)],
  "General Builders":[(53,24),(227,420),(391,594),(319,461),(241,396),(66,17),(14,27)],
 },
 "🇿🇦 South Africa": {
  "Solar Panel Installation":[(1340,522),(1359,562),(1030,507),(827,503),(973,548),(425,523),(492,490)],
  "Roof Repair":[(973,539),(986,537),(877,509),(799,506),(748,542),(620,515),(764,529)],
  "Divorce Lawyers":[(253,181),(157,163),(145,121),(297,172),(252,196),(83,165),(45,134)],
  "Tree Surgery & Removal":[(220,149),(196,141),(160,103),(254,128),(148,146),(131,138),(185,110)],
  "Painting & Decoration - Interior":[(183,121),(102,113),(160,85),(107,123),(221,129),(89,108),(106,83)],
  "Bathroom Installation & Remodel":[(83,91),(97,88),(126,91),(202,119),(86,107),(83,97),(99,77)],
  "Wedding Photography":[(32,114),(120,107),(46,81),(80,91),(94,113),(77,121),(29,83)],
  "Catering":[(59,63),(40,60),(24,53),(60,57),(57,65),(43,64),(37,45)],
 },
}

# ---- Per-account recommendation blocks (analyst judgement) ----
ACCT_RECS = [
 ("🇬🇧 UK", "pull", "Friday weakest, Saturday best — and budget is allocated the wrong way round.",
  "Friday is the lowest-ROAS day (1.16) yet carries the <b>highest</b> spend (£92k/90d); Saturday is the highest-ROAS day (1.48) on the <b>lowest</b> spend (£43k). Shift budget Fri→Sat. Caveat: Saturday's strength is partly because it's already throttled — ease the cap gradually and watch marginal ROAS rather than flooding it. No UK day loses money, so this is a tilt, not a pause."),
 ("🇺🇸 US", "pull", "Clean weekend wind-down — pull harder Sat/Sun, push Mon.",
  "Mon–Thu run ~1.39–1.48; Sat 1.14 and Sun 1.10 are the laggards (Sun APR just 9%). Weekend already gets less budget; the data says go further. Monday is the power day (1.48) — push it."),
 ("🇨🇦 CA", "steady", "Boring-profitable. Light touch — feed Monday, trim Sunday.",
  "Every day 1.37–1.78. Monday is best (1.78) but under-fed (lowest spend). Sunday weakest (1.37) but still healthy. Small Mon push, small Sun trim, otherwise leave it."),
 ("🇿🇦 ZA", "pull", "Kill Saturday. Front-load Mon/Tue.",
  "Saturday loses money (0.93 / −8% APR) yet gets more budget than Sunday. Mon/Tue are the engine (1.72–1.76). Cut Saturday hard, trim Sunday, push Mon/Tue."),
 ("🇮🇪 IE", "pull", "Fully inverted — weekdays lose money, Saturday prints. Structural.",
  "Weekdays mostly negative (Fri worst at 0.81 / −24% APR) and soak ~95% of spend; Saturday returns 2.40 on €4/day. Cut Fri/Wed/Thu, shift to Sat — but the weekday targeting is the real problem, dayparting alone won't fix a losing account."),
 ("🇩🇪 DE", "pull", "Worst Saturday in the portfolio (−40%). Also losing Mon & Sun.",
  "Cut Saturday hard, trim Sunday and Monday (both negative). Tuesday is the star (1.48); Wed/Fri also solid — concentrate budget there."),
 ("🇫🇷 FR", "watch", "Thin and marginal. Monday only solid day.",
  "Monday 1.34 is the lone bright spot; Wed–Sun hover at or below break-even. Small Mon/Tue tilt, but fix account economics before fine dayparting."),
 ("🇳🇿 NZ", "push", "Weekend PUSH — inverts UK/US. Just scale the whole thing.",
  "Sat 2.45 / Sun 2.50 / Fri 2.08, all on tiny spend. The entire account is under-fed at huge ROAS. Push everything, weekend hardest. Volume too low to micro-tune."),
 ("🇦🇺 AU", "watch", "Monday only. Account net-negative — fix targeting & build volume first.",
  "Monday 1.59 is the one consistently good day; the rest is weak or noise. Don't build daypart rules yet — drive profitable volume first."),
]

# ---- Per-account category cluster recommendations ----
CAT_RECS = {
 "🇬🇧 United Kingdom": [
  ("pull", "Cut Friday across the board",
   "Friday is the weakest day for almost every UK category — Driveway (1.05), Artificial Grass (1.02), Garage Door (0.91 loss), Fence (1.05), House Cleaning (1.24), Painting (1.15). A blanket Friday ×0.8 at account level is well supported."),
  ("push", "Ease the Saturday throttle — weekend-strong cluster",
   "Wedding Photography (Sat 1.67 / Sun 1.80), Tree Surgery (Sat 1.65 / Sun 1.78), Garage Door (Sat 1.78 / Sun 1.77), Patio (Sat 1.63), Painting (Sat 1.69) all peak at the weekend on the lowest spend. These want MORE weekend budget, not less — relax any weekend pull for this cluster."),
  ("pull", "Weekday-led: trim weekend on Home & Domiciliary Care",
   "Opposite shape — strong Mon–Thu (1.37–1.58), weak weekend (Sat 1.12, Sun 1.00 break-even). Pull Sat/Sun here while pushing the weekend-strong cluster above."),
  ("watch", "Roof Repair is loss-making (0.96 ROAS / −4% APR)",
   "Only Mon (1.18) and Sat (1.23) clear break-even; Tue–Fri + Sun all below 1.0. This needs a creative/targeting review or an account-level budget cut, not just dayparting. Driveway (1.15) is the next-thinnest — watch."),
 ],
 "🇺🇸 United States": [
  ("pull", "Weekend wind-down cluster — trim Sat & Sun",
   "House Cleaning (Sun 1.06 / Sat 1.13), Immigration Lawyers (Sun 1.11 / Sat 1.07), Wedding Photography (Sun 1.22 / Sat 1.28), Personal Trainers (Sun 0.95 / Sat 1.00), Catering (Sun 1.07). Sunday especially. Dog Training Sunday is an outright loss (0.74) — cut it hardest."),
  ("push", "Monday power day",
   "Immigration Lawyers (Mon 1.91), Dog Training (Mon 1.90), House Cleaning (Mon 1.54). Push Monday budget for the lead-gen categories."),
  ("steady", "DON'T blanket-pull weekends on DJ",
   "DJ inverts the pattern — Sun 1.66 and Sat 1.47 are its best days (event-driven). A market-wide weekend pull would hurt it. Carve DJ out of any weekend rule."),
  ("watch", "Category losses: Web Design Sat (0.93), Bookkeeping Wed (0.77) & Sat (0.89), TV Install Fri (0.88)/Sat (0.94)",
   "Targeted day cuts on these specific cells. Web Design and Bookkeeping are the lowest-ROAS US categories overall (1.20 / 1.12) — candidates for budget reallocation to House Cleaning / Immigration / Architectural."),
 ],
 "🇨🇦 Canada": [
  ("push", "Scale the winners — they're strong every day",
   "House Cleaning (2.29 avg, 1.84–2.67 across the week), Driveway (1.97), Fence & Gate (1.85), Bathroom (1.78). These can absorb more budget on almost any day."),
  ("pull", "Soft Saturday cluster",
   "Saturday is the one consistent weak spot — Landscaping (1.02), Painting (1.15), Home Care (1.14). Mild Saturday trim on these; Sunday weak for Property Extensions (1.15) and Home Care (1.05)."),
  ("watch", "General Builders is loss-making (0.68 ROAS)",
   "Negative most of the week (Wed 0.66, Thu 0.69, Fri 0.61, Sat tiny). Review creative/targeting or cut — dayparting won't rescue it. (Per-category CA day-cells are ~£15–250/90d, so treat single cells as directional.)"),
 ],
 "🇿🇦 South Africa": [
  ("pull", "Cut Saturday — loss-making across the board",
   "Solar Panel (Sat 0.81), Divorce Lawyers (Sat 0.50), Tree Surgery (Sat 0.95), Bathroom (Sat 0.86). Saturday is the clear account-wide drag. Sunday also weak for Solar (1.00) and Divorce (0.34)."),
  ("push", "Front-load Mon/Tue on the two big categories",
   "Solar Panel Installation (Mon 2.57 / Tue 2.42) and Roof Repair (Mon 1.81 / Tue 1.84) are the volume engine and peak early-week. Concentrate budget Mon–Wed."),
  ("pull", "Weekend-pause candidates: Divorce Lawyers, Wedding Photography, Catering",
   "Divorce Lawyers loses money both weekend days (Sat 0.50, Sun 0.34); Wedding Photography (0.6–0.8 most days) and Catering (~0.6–0.9) are structurally weak. Consider weekend pause / overall trim. (ZA day-cells are ~£40–560/90d — directional, not precise.)"),
 ],
}

# ---------- rendering ----------
def roas_class(r):
    if r is None: return "t-na"
    if r < 0.85: return "t-vneg"
    if r < 1.0:  return "t-neg"
    if r < 1.15: return "t-low"
    if r < 1.3:  return "t-mild"
    if r < 1.5:  return "t-ok"
    if r < 1.8:  return "t-good"
    if r < 2.2:  return "t-strong"
    return "t-vstrong"

def apr_class(a):
    if a is None: return "t-na"
    p = a * 100
    if p <= -25: return "t-vneg"
    if p < -10:  return "t-neg"
    if p < 0:    return "t-low"
    if p < 10:   return "t-mild"
    if p < 25:   return "t-ok"
    if p < 40:   return "t-good"
    if p < 55:   return "t-strong"
    return "t-vstrong"

def cell_roas(rev, spend, floor):
    if spend < floor or spend == 0:
        return '<td class="cell t-na" title="low spend %d">·</td>' % spend
    r = rev / spend
    return '<td class="cell %s" title="ROAS %.2fx | rev %d spend %d">%.2f</td>' % (roas_class(r), r, rev, spend, r)

def fmt_gbp(v):
    av = abs(v); sign = "-" if v < 0 else ""
    if av >= 1000: return f"{sign}£{av/1000:.1f}k"
    return f"{sign}£{av:.0f}"

def cell_apr(rev, spend, floor, div):
    if spend < floor or spend == 0:
        return '<td class="cell t-na" title="low spend %d">·</td>' % spend
    apr = rev - spend
    a = apr / rev if rev else -1
    avg = apr / div
    return '<td class="cell %s" title="avg £%.0f/day | %.0f%% margin | %d-day total £%d">%s</td>' % (apr_class(a), avg, a*100, div, apr, fmt_gbp(avg))

TAGCLASS = {"push":"push","pull":"pull","steady":"steady","watch":"watch"}
TAGTEXT  = {"push":"PUSH","pull":"PULL","steady":"STEADY","watch":"WATCH"}

def acct_table(metric):
    floor = 200
    rows = []
    for flag, name, rev, spend in ACCOUNTS:
        cells = []
        for i in range(7):
            r, s = ACCT_DOW[name][i]
            cells.append(cell_roas(r, s, floor) if metric == "roas" else cell_apr(r, s, floor, DIVISORS[i]))
        tot_s = ("%.2fx" % (rev/spend)) if metric=="roas" else fmt_gbp((rev-spend)/NDAYS)
        rows.append('<tr><td class="country">%s %s</td>%s<td class="num"><strong>%s</strong></td></tr>'
                    % (flag, name, "".join(cells), tot_s))
    head = "".join('<th class="num">%s</th>' % d for d in DAYS)
    lbl = "90d ROAS" if metric=="roas" else "Avg/day £"
    return ('<div class="panel" style="padding:8px"><div style="overflow-x:auto">'
            '<table class="heatmap"><thead><tr><th>Account</th>%s<th class="num">%s</th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>' % (head, lbl, "".join(rows)))

def cat_table(acct):
    floor = 120
    rows = []
    cats = CATS[acct]
    # order by total spend desc
    order = sorted(cats.items(), key=lambda kv: -sum(s for _, s in kv[1]))
    for name, days in order:
        cells = "".join(cell_roas(r, s, floor) for r, s in days)
        trev = sum(r for r, _ in days); tspend = sum(s for _, s in days)
        wk_r = sum(r for r, _ in days[:5]); wk_s = sum(s for _, s in days[:5])
        we_r = days[5][0]+days[6][0]; we_s = days[5][1]+days[6][1]
        wk = ("%.2f" % (wk_r/wk_s)) if wk_s else "·"
        we = ("%.2f" % (we_r/we_s)) if we_s else "·"
        rows.append('<tr><td class="country" style="font-weight:600">%s</td>%s'
                    '<td class="num">%s</td><td class="num">%s</td><td class="num muted">£%s</td></tr>'
                    % (name, cells, wk, we, f"{tspend:,.0f}"))
    head = "".join('<th class="num">%s</th>' % d for d in DAYS)
    return ('<div class="panel" style="padding:8px"><div style="overflow-x:auto">'
            '<table class="heatmap"><thead><tr><th>Category</th>%s'
            '<th class="num">Wkdy</th><th class="num">Wknd</th><th class="num">90d spend</th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>' % (head, "".join(rows)))

def recs_block(recs):
    items = []
    for tag, title, body in recs:
        items.append('<li><span class="badge badge-%s">%s</span><div><strong>%s</strong><br>'
                     '<span class="muted" style="color:#475569">%s</span></div></li>'
                     % (TAGCLASS[tag], TAGTEXT[tag], title, body))
    return '<ul class="signal-list">%s</ul>' % "".join(items)

def acct_cards():
    cards = []
    for flag, name, rev, spend in ACCOUNTS:
        roas = rev/spend; apr = (rev-spend)/rev
        cls = "pos" if apr >= 0.15 else ("warn" if apr >= 0 else "neg")
        cards.append('<div class="card %s"><div class="flag">%s</div><div class="label">%s</div>'
                     '<div class="value">%.2fx</div><div class="sub">%.0f%% APR · £%s rev</div></div>'
                     % (cls, flag, name, roas, apr*100, f"{rev:,.0f}"))
    return '<div class="cards">%s</div>' % "".join(cards)

LEGEND_ROAS = '''<div class="legend">
<span style="background:#991b1b;color:#fff">&lt;0.85x</span>
<span style="background:#dc2626;color:#fff">0.85–1.0</span>
<span style="background:#fca5a5;color:#7f1d1d">1.0–1.15</span>
<span style="background:#fde68a;color:#78350f">1.15–1.3</span>
<span style="background:#bbf7d0;color:#14532d">1.3–1.5</span>
<span style="background:#4ade80;color:#052e16">1.5–1.8</span>
<span style="background:#16a34a;color:#fff">1.8–2.2</span>
<span style="background:#15803d;color:#fff">≥2.2x</span>
<span style="background:#f1f5f9;color:#94a3b8">low spend</span></div>'''

LEGEND_APR = '''<div class="legend">
<span style="background:#991b1b;color:#fff">≤−25%</span>
<span style="background:#dc2626;color:#fff">−25 to −10</span>
<span style="background:#fca5a5;color:#7f1d1d">−10 to 0</span>
<span style="background:#fde68a;color:#78350f">0 to 10</span>
<span style="background:#bbf7d0;color:#14532d">10 to 25</span>
<span style="background:#4ade80;color:#052e16">25 to 40</span>
<span style="background:#16a34a;color:#fff">40 to 55</span>
<span style="background:#15803d;color:#fff">≥55%</span>
<span style="background:#f1f5f9;color:#94a3b8">low spend</span></div>'''

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{background:#f7f8fc;color:#111827;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;line-height:1.5}
.top-bar{height:4px;background:linear-gradient(90deg,#E85555,#FA9750,#F7BF53,#47BF9C,#2D7AF1)}
.wrap{max-width:1180px;margin:0 auto;padding:24px}
.header{padding:8px 0 24px;border-bottom:1px solid #e5e7eb;margin-bottom:24px}
.header h1{font-size:24px;font-weight:700;color:#0f172a;letter-spacing:-0.02em}
.header .meta{color:#64748b;font-size:13px;margin-top:6px}
.header .meta strong{color:#334155}
h2{font-size:18px;font-weight:700;color:#0f172a;margin:36px 0 14px;letter-spacing:-0.01em}
h2 .sub{font-size:13px;color:#64748b;font-weight:500;margin-left:8px}
h3{font-size:15px;font-weight:700;color:#0f172a;margin:20px 0 10px}
p{color:#334155;margin-bottom:10px}p.muted{color:#64748b;font-size:13px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:8px 0 16px}
.card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px}
.card .flag{font-size:18px}
.card .label{color:#64748b;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;margin-top:4px}
.card .value{font-size:22px;font-weight:700;color:#0f172a;margin-top:4px;font-variant-numeric:tabular-nums}
.card .sub{color:#64748b;font-size:12px;margin-top:2px;font-variant-numeric:tabular-nums}
.card.pos .value{color:#047857}.card.neg .value{color:#b91c1c}.card.warn .value{color:#b45309}
.panel{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin-bottom:14px}
.panel h3{margin-top:0}
.panel.callout{background:#fffbeb;border-color:#fde68a}
.acct-rec{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px;margin-bottom:10px}
.acct-rec .ah{display:flex;gap:10px;align-items:center;margin-bottom:4px}
.acct-rec .ah .nm{font-weight:700;font-size:15px;color:#0f172a}
.acct-rec .tldr{font-weight:600;color:#334155}
.acct-rec .body{color:#475569;font-size:13px;margin-top:4px}
table{width:100%;border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid #f1f5f9;white-space:nowrap}
th{color:#475569;font-weight:600;text-transform:uppercase;font-size:10px;letter-spacing:0.06em;background:#f8fafc;border-bottom:1px solid #e2e8f0}
td.num,th.num{text-align:right}td.country{font-weight:600;color:#0f172a}
.heatmap td.cell{text-align:center;font-weight:600;font-size:12.5px;padding:9px 4px;border:1px solid #fff}
.heatmap td.cell.t-na{background:#f1f5f9;color:#94a3b8;font-weight:500}
.heatmap td.cell.t-vneg{background:#991b1b;color:#fff}
.heatmap td.cell.t-neg{background:#dc2626;color:#fff}
.heatmap td.cell.t-low{background:#fca5a5;color:#7f1d1d}
.heatmap td.cell.t-mild{background:#fde68a;color:#78350f}
.heatmap td.cell.t-ok{background:#bbf7d0;color:#14532d}
.heatmap td.cell.t-good{background:#4ade80;color:#052e16}
.heatmap td.cell.t-strong{background:#16a34a;color:#fff}
.heatmap td.cell.t-vstrong{background:#15803d;color:#fff}
.muted{color:#64748b}.pos{color:#047857;font-weight:600}.neg{color:#b91c1c;font-weight:600}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px;font-size:11px}
.legend span{padding:3px 9px;border-radius:6px;font-weight:600}
.signal-list{list-style:none;padding:0}
.signal-list li{padding:10px 0;border-bottom:1px solid #f1f5f9;display:flex;gap:12px;align-items:flex-start}
.signal-list li:last-child{border-bottom:none}
.signal-list .badge{flex-shrink:0;display:inline-block;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:700;text-transform:uppercase}
.badge-push{background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0}
.badge-pull{background:#fef2f2;color:#991b1b;border:1px solid #fecaca}
.badge-watch{background:#fffbeb;color:#92400e;border:1px solid #fde68a}
.badge-steady{background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe}
.tag{font-size:11px;padding:2px 8px;border-radius:10px;font-weight:700;text-transform:uppercase}
.tag.push{background:#ecfdf5;color:#065f46}.tag.pull{background:#fef2f2;color:#991b1b}
.tag.watch{background:#fffbeb;color:#92400e}.tag.steady{background:#eff6ff;color:#1e40af}
.cat-section{margin-top:20px}
.footer{margin-top:48px;padding-top:18px;border-top:1px solid #e5e7eb;color:#64748b;font-size:12px}
"""

def acct_recs_html():
    out = []
    for tag_flag, tagkey, tldr, body in [(r[0], r[1], r[2], r[3]) for r in ACCT_RECS]:
        out.append('<div class="acct-rec"><div class="ah"><span class="nm">%s</span>'
                   '<span class="tag %s">%s</span></div><div class="tldr">%s</div>'
                   '<div class="body">%s</div></div>'
                   % (tag_flag, TAGCLASS[tagkey], TAGTEXT[tagkey], tldr, body))
    return "".join(out)

def cat_sections():
    out = []
    for acct, recs in CAT_RECS.items():
        out.append('<div class="cat-section"><h3>%s — category × day-of-week (ROAS)</h3>%s%s</div>'
                   % (acct, cat_table(acct), recs_block(recs)))
    return "".join(out)

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dayparting — All Accounts · Account + Category Day-of-Week</title>
<style>{CSS}</style></head><body>
<div class="top-bar"></div><div class="wrap">
<div class="header"><h1>Dayparting — All Meta Accounts</h1>
<div class="meta">9 accounts · <strong>last 90 days</strong> to 2026-05-27 · channel <strong>PPC – Meta (FB + IG + Other)</strong><br>
Source: Tableau <em>📁 APR+ with EP distributed</em> (Bark-attributed). ROAS = Revenue+ ÷ Spend · APR+ % = (Revenue+ − Spend) ÷ Revenue+ · GBP-normalised for cross-account comparison. SG/IN excluded (no Meta spend).</div></div>

<h2>Account overview <span class="sub">90d ROAS, ranked by revenue</span></h2>
{acct_cards()}

<h2>Table 1 — ROAS by day of week <span class="sub">Revenue+ ÷ Spend</span></h2>
{LEGEND_ROAS}
{acct_table("roas")}

<h2>Table 2 — Average APR+ £ per day <span class="sub">Revenue+ − Spend on a typical weekday (GBP)</span></h2>
<p class="muted">Number = average £ profit on a typical day (90d total ÷ occurrences of that weekday: 12–13 over the window). Colour = APR margin % (so red/green still flags efficiency, not just size). Hover for the day count + period total.</p>
{LEGEND_APR}
{acct_table("apr")}

<h2>Account-level budget read</h2>
<p class="muted">PUSH = add budget · PULL = trim · STEADY = hold · WATCH = fix economics before dayparting</p>
{acct_recs_html()}

<h2>Category-level day-of-week <span class="sub">top categories by revenue, UK · US · CA · ZA</span></h2>
<p class="muted">ROAS heatmap per category (Wkdy = Mon–Fri blended, Wknd = Sat+Sun blended). Smaller markets (IE, DE, FR, NZ, AU) are too thin to cut by category × day — use the account-level read above for those.</p>
{cat_sections()}

<div class="footer"><p><strong>Method:</strong> Bark-attributed Revenue+ and Marketing Spend from Tableau, last 90 days, Meta channel only, grouped by day of week (DATEPART weekday). ROAS and APR are blended over the 90d window per day-of-week. Per-category day cells in CA/ZA are low-volume (£15–560 over 90d) — treat single cells as directional; the weekday/weekend split and cluster verdicts are the reliable signal.</p>
<p><strong>Caveat on high-ROAS / low-spend cells:</strong> a day showing strong ROAS on constrained spend (e.g. UK Saturday) is partly strong <em>because</em> it's throttled. Scale into it gradually and watch marginal ROAS, don't assume the average holds as budget climbs.</p></div>
</div></body></html>"""

out = Path.home() / "Downloads" / "meta-reporting" / "dayparting-allaccounts-27may2026"
out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(html, encoding="utf-8")
print(out / "index.html")
