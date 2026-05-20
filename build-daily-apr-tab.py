#!/usr/bin/env python3
"""Generate the inner HTML for a Daily APR tab matching the existing dark-theme dashboard.

Outputs: tab-daily-apr.snippet.html (the <div id="tab-daily-apr"> block to inject).

Reads data from /Users/ben.greenhouse/Downloads/meta-apr-raw.json which holds the
last-14-days Meta (Facebook + Instagram + Other) daily APR pull from Tableau.
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

RAW = json.loads(Path("/Users/ben.greenhouse/Downloads/meta-apr-raw.json").read_text())

WINDOW_START = datetime(2026, 5, 6)
WINDOW_END = datetime(2026, 5, 19)

ALL_DATES = []
d = WINDOW_START
while d <= WINDOW_END:
    ALL_DATES.append(d)
    d += timedelta(days=1)

COUNTRY_ORDER = ["United Kingdom", "United States", "Canada", "South Africa",
                 "Ireland", "France", "Deutschland"]
COUNTRY_FLAG = {
    "United Kingdom": "🇬🇧", "United States": "🇺🇸", "Canada": "🇨🇦",
    "South Africa": "🇿🇦", "Ireland": "🇮🇪", "France": "🇫🇷", "Deutschland": "🇩🇪",
}

by_country = defaultdict(dict)
for row in RAW:
    date_s = row["DAY(Calendar Date)"][:10]
    date = datetime.strptime(date_s, "%Y-%m-%d")
    if not (WINDOW_START <= date <= WINDOW_END):
        continue
    by_country[row["Country"]][date_s] = {
        "spend": row["Marketing Spend £"],
        "ppr":   row["PPR Revenue £"],
        "apr":   row["APR £"],
    }

daily_totals = {}
for d in ALL_DATES:
    key = d.strftime("%Y-%m-%d")
    s = p = a = 0
    for c in by_country:
        r = by_country[c].get(key)
        if r:
            s += r["spend"]; p += r["ppr"]; a += r["apr"]
    daily_totals[key] = {"spend": s, "ppr": p, "apr": a}


def fmt_money(v, short=False):
    if v == 0: return "£0"
    sign = "-" if v < 0 else ""
    av = abs(v)
    if short and av >= 1000:
        return f"{sign}£{av/1000:.1f}k"
    return f"{sign}£{av:,.0f}"


def fmt_pct(v):
    return "—" if v is None else f"{v*100:.0f}%"


def interpolate_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t); g = int(g1 + (g2 - g1) * t); b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


COLOR_LOW = "#f97316"
COLOR_HIGH = "#10b981"
COLOR_NEG = "#ef4444"


def apr_color(v, pos_min, pos_max):
    if v < 0: return COLOR_NEG
    if pos_max == pos_min: return COLOR_HIGH
    t = (v - pos_min) / (pos_max - pos_min)
    return interpolate_color(COLOR_LOW, COLOR_HIGH, t)


def bar_chart_svg(country_data, width=1100, height=240, show_yaxis=True):
    pad_top = 24; pad_bottom = 48; pad_left = 56 if show_yaxis else 12; pad_right = 14
    inner_w = width - pad_left - pad_right
    inner_h = height - pad_top - pad_bottom

    aprs = []
    for d in ALL_DATES:
        key = d.strftime("%Y-%m-%d")
        v = country_data.get(key)
        if isinstance(v, dict):
            aprs.append(v.get("apr", 0))
        else:
            aprs.append(v if v is not None else 0)

    mx = max(aprs + [0]); mn = min(aprs + [0]); rng = mx - mn or 1
    zero_y = pad_top + inner_h * (mx / rng)
    positives = [v for v in aprs if v > 0]
    pos_min = min(positives) if positives else 0
    pos_max = max(positives) if positives else 0

    n = len(ALL_DATES); bar_w = inner_w / n; gap = bar_w * 0.18
    actual_bar_w = bar_w - gap

    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" style="display:block;font-family:inherit;">']

    if show_yaxis:
        ticks = sorted(set([0, mx, mn]))
        if mx > 0: ticks.append(mx / 2)
        if mn < 0: ticks.append(mn / 2)
        ticks = sorted(set(round(t, -1) for t in ticks))
        for tv in ticks:
            ty = pad_top + inner_h * ((mx - tv) / rng)
            if tv == 0:
                parts.append(f'<line x1="{pad_left}" y1="{ty:.1f}" x2="{width-pad_right}" y2="{ty:.1f}" stroke="rgba(255,255,255,.25)" stroke-width="1"/>')
            else:
                parts.append(f'<line x1="{pad_left}" y1="{ty:.1f}" x2="{width-pad_right}" y2="{ty:.1f}" stroke="rgba(255,255,255,.06)" stroke-width="1" stroke-dasharray="2,3"/>')
            parts.append(f'<text x="{pad_left - 6}" y="{ty + 4:.1f}" font-size="10" text-anchor="end" fill="#64748b">{fmt_money(tv, short=True)}</text>')
    else:
        parts.append(f'<line x1="{pad_left}" y1="{zero_y:.1f}" x2="{width-pad_right}" y2="{zero_y:.1f}" stroke="rgba(255,255,255,.25)" stroke-width="1"/>')

    for i, d in enumerate(ALL_DATES):
        v = aprs[i]
        bx = pad_left + i * bar_w + gap / 2
        color = apr_color(v, pos_min, pos_max)
        if v >= 0:
            by = pad_top + inner_h * ((mx - v) / rng); bh = zero_y - by
        else:
            by = zero_y; bh = pad_top + inner_h * ((mx - v) / rng) - zero_y
        if bh < 1: bh = 0
        parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{actual_bar_w:.1f}" height="{bh:.1f}" fill="{color}" rx="2" ry="2"/>')

        label_v = fmt_money(v, short=True)
        if v >= 0:
            ly = by - 4 if v > 0 else zero_y - 4
        else:
            ly = by + bh + 11
        if v != 0:
            parts.append(f'<text x="{bx + actual_bar_w/2:.1f}" y="{ly:.1f}" font-size="10" text-anchor="middle" fill="{color}" font-weight="600">{label_v}</text>')

        dx = bx + actual_bar_w / 2
        weekday = d.strftime("%a"); day_num = d.strftime("%d %b")
        wcolor = "#475569" if d.weekday() >= 5 else "#94a3b8"
        parts.append(f'<text x="{dx:.1f}" y="{height - pad_bottom + 14}" font-size="10" text-anchor="middle" fill="{wcolor}">{weekday}</text>')
        parts.append(f'<text x="{dx:.1f}" y="{height - pad_bottom + 28}" font-size="10" text-anchor="middle" fill="#64748b">{day_num}</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def country_totals(c):
    days = by_country.get(c, {})
    s = sum(d["spend"] for d in days.values())
    p = sum(d["ppr"]   for d in days.values())
    a = sum(d["apr"]   for d in days.values())
    pct = a / p if p else None
    return {"spend": s, "ppr": p, "apr": a, "pct": pct, "days": len(days)}


gtot = {"spend": sum(v["spend"] for v in daily_totals.values()),
        "ppr":   sum(v["ppr"]   for v in daily_totals.values()),
        "apr":   sum(v["apr"]   for v in daily_totals.values())}
gtot["pct"] = gtot["apr"] / gtot["ppr"] if gtot["ppr"] else None


parts = ['<div id="tab-daily-apr" class="country-section">']
parts.append('  <div class="section">')
parts.append('    <div class="section-hd"><h2>📊 Daily APR — Meta (FB + IG + Other), all markets · last 14 days</h2></div>')
parts.append(f'    <div class="section-sub">2026-05-06 → 2026-05-19 · Source: Tableau APR+ datasource · Bars colour-scaled per chart: greenest = highest, orange = lowest positive, red = negative</div>')

# Global stat pills
gcls = "pos" if gtot["apr"] >= 0 else "neg"
parts.append('    <div class="summary-bar" style="padding:0;margin-bottom:14px;border:0">')
parts.append(f'      <div class="stat-pill"><div class="num">{fmt_money(gtot["spend"])}</div><div class="lbl">14d Spend</div></div>')
parts.append(f'      <div class="stat-pill"><div class="num">{fmt_money(gtot["ppr"])}</div><div class="lbl">14d PPR Rev</div></div>')
parts.append(f'      <div class="stat-pill"><div class="num {gcls}">{fmt_money(gtot["apr"])}</div><div class="lbl">14d APR</div></div>')
parts.append(f'      <div class="stat-pill"><div class="num {gcls}">{fmt_pct(gtot["pct"])}</div><div class="lbl">Avg APR rate</div></div>')
parts.append('    </div>')

# Hero chart
parts.append('    <div style="background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:16px 20px;margin-bottom:24px">')
parts.append('      <div style="font-size:13px;font-weight:600;color:#e2e8f0;margin-bottom:2px">All markets combined</div>')
parts.append('      <div style="font-size:11px;color:#64748b;margin-bottom:10px">Daily APR across UK + US + CA + ZA + IE + FR + DE</div>')
parts.append(f'      {bar_chart_svg(daily_totals, width=1100, height=260)}')
parts.append('    </div>')

# Per-market mini sections
for c in COUNTRY_ORDER:
    if c not in by_country: continue
    t = country_totals(c)
    flag = COUNTRY_FLAG.get(c, "🌐")
    apr_cls = "pos" if t["apr"] >= 0 else "neg"
    parts.append('    <div style="background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:14px 20px;margin-bottom:14px">')
    parts.append('      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">')
    parts.append(f'        <span style="font-size:20px">{flag}</span>')
    parts.append(f'        <span style="font-size:14px;font-weight:600;color:#e2e8f0">{c}</span>')
    parts.append(f'        <span style="font-size:11px;color:#64748b;margin-left:auto">Spend <strong style="color:#e2e8f0">{fmt_money(t["spend"])}</strong> · APR <strong class="{apr_cls}">{fmt_money(t["apr"])} ({fmt_pct(t["pct"])})</strong> · {t["days"]}/14 days</span>')
    parts.append('      </div>')
    parts.append(f'      {bar_chart_svg(by_country[c], width=1100, height=200)}')
    parts.append('    </div>')

parts.append('    <div style="margin-top:18px;padding:12px 16px;background:rgba(247,191,83,.06);border-left:3px solid #f7bf53;border-radius:4px;font-size:12px;color:#94a3b8">')
parts.append('      <strong style="color:#f7bf53">Note on attribution:</strong> APR values are Meta-pixel attributed. Per the existing reconciliation memo, Meta pixel undercounts barks by ~43%; multiply by ~1.75 for true APR estimate. Some loss days are real; others reflect pixel undercount.')
parts.append('    </div>')

parts.append('  </div>')
parts.append('</div>')

out = Path("/tmp/meta-reporting/tab-daily-apr.snippet.html")
out.write_text("\n".join(parts))
print(f"✓ wrote {out}")
print(f"  bytes: {out.stat().st_size:,}")
print(f"  2026-05-18 combined APR: £{daily_totals['2026-05-18']['apr']:,}")
