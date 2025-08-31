#!/usr/bin/env python3
"""
scripts/update_activity.py
- Maintains activity.json (list of active dates).
- Generates activity.svg (spiral visualization).
Run this in repo root (GitHub Action will run it there).
"""

import os
import json
import datetime
import math

# --- config (tweak if you like) ---
DOT_BASE = 6            # base dot radius
WIDTH = 1200
HEIGHT = 420
DAYS = 365              # how many days to display
# ----------------------------------

cwd = os.getcwd()
ACT_JSON = os.path.join(cwd, "activity.json")
SVG_FILE = os.path.join(cwd, "activity.svg")

today = datetime.date.today()
today_s = today.isoformat()

# load existing activity (list of ISO date strings)
if os.path.exists(ACT_JSON):
    try:
        with open(ACT_JSON, "r") as f:
            activity = sorted(set(json.load(f)))
    except Exception:
        activity = []
else:
    activity = []

# add today
if today_s not in activity:
    activity.append(today_s)

# keep only last DAYS days
cutoff = today - datetime.timedelta(days=DAYS - 1)
activity = sorted(d for d in activity if datetime.date.fromisoformat(d) >= cutoff)

# write activity.json
with open(ACT_JSON, "w") as f:
    json.dump(activity, f, indent=2)

# Prepare all DAYS dates (oldest -> newest)
dates_all = [(today - datetime.timedelta(days=days)).isoformat() for days in range(DAYS - 1, -1, -1)]
active_set = set(activity)

# SVG geometry
cx = WIDTH // 2
cy = HEIGHT // 2
max_radius = min(cx, cy) - 60
# use sqrt spacing so points spread nicely
scale = max_radius / math.sqrt(max(1, DAYS))

svg_parts = []
# background (white)
svg_parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>')

for i, d in enumerate(dates_all):
    # radial distance increases roughly with sqrt(i) (nice spiral spacing)
    r = scale * math.sqrt(i)
    angle = 0.45 * i                          # controls spiral tightness (tweak 0.3..0.6)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)

    if d in active_set:
        age = (today - datetime.date.fromisoformat(d)).days
        # recent days appear stronger (age 0 -> intensity 1; older -> fades)
        intensity = 1.0 - min(age, 120) / 120.0
        green_val = int(120 + 135 * intensity)   # range ~120..255
        green_val = max(0, min(255, green_val))
        color = f"rgb(30,{green_val},60)"
        radius = DOT_BASE + int(3 * intensity)
    else:
        color = "#e7e7e7"
        radius = DOT_BASE

    # circle with title for hover tooltip (date)
    svg_parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}">')
    svg_parts.append(f'  <title>{d} - {"active" if d in active_set else "inactive"}</title>')
    svg_parts.append('</circle>')

# footer text with total active days
total_active = len(active_set)
svg_parts.append(f'<text x="{cx}" y="{HEIGHT - 28}" font-size="18" text-anchor="middle" fill="#333">Active days tracked: {total_active}</text>')

svg = f'<?xml version="1.0" encoding="utf-8"?>\n'
svg += f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">\n'
svg += "\n".join(svg_parts)
svg += "\n</svg>"

with open(SVG_FILE, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Wrote {ACT_JSON} (entries={len(activity)}) and {SVG_FILE}")
#!/usr/bin/env python3
"""
scripts/update_activity.py
- Maintains activity.json (list of active dates).
- Generates activity.svg (spiral visualization).
Run this in repo root (GitHub Action will run it there).
"""

import os
import json
import datetime
import math

# --- config (tweak if you like) ---
DOT_BASE = 6            # base dot radius
WIDTH = 1200
HEIGHT = 420
DAYS = 365              # how many days to display
# ----------------------------------

cwd = os.getcwd()
ACT_JSON = os.path.join(cwd, "activity.json")
SVG_FILE = os.path.join(cwd, "activity.svg")

today = datetime.date.today()
today_s = today.isoformat()

# load existing activity (list of ISO date strings)
if os.path.exists(ACT_JSON):
    try:
        with open(ACT_JSON, "r") as f:
            activity = sorted(set(json.load(f)))
    except Exception:
        activity = []
else:
    activity = []

# add today
if today_s not in activity:
    activity.append(today_s)

# keep only last DAYS days
cutoff = today - datetime.timedelta(days=DAYS - 1)
activity = sorted(d for d in activity if datetime.date.fromisoformat(d) >= cutoff)

# write activity.json
with open(ACT_JSON, "w") as f:
    json.dump(activity, f, indent=2)

# Prepare all DAYS dates (oldest -> newest)
dates_all = [(today - datetime.timedelta(days=days)).isoformat() for days in range(DAYS - 1, -1, -1)]
active_set = set(activity)

# SVG geometry
cx = WIDTH // 2
cy = HEIGHT // 2
max_radius = min(cx, cy) - 60
# use sqrt spacing so points spread nicely
scale = max_radius / math.sqrt(max(1, DAYS))

svg_parts = []
# background (white)
svg_parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>')

for i, d in enumerate(dates_all):
    # radial distance increases roughly with sqrt(i) (nice spiral spacing)
    r = scale * math.sqrt(i)
    angle = 0.45 * i                          # controls spiral tightness (tweak 0.3..0.6)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)

    if d in active_set:
        age = (today - datetime.date.fromisoformat(d)).days
        # recent days appear stronger (age 0 -> intensity 1; older -> fades)
        intensity = 1.0 - min(age, 120) / 120.0
        green_val = int(120 + 135 * intensity)   # range ~120..255
        green_val = max(0, min(255, green_val))
        color = f"rgb(30,{green_val},60)"
        radius = DOT_BASE + int(3 * intensity)
    else:
        color = "#e7e7e7"
        radius = DOT_BASE

    # circle with title for hover tooltip (date)
    svg_parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}">')
    svg_parts.append(f'  <title>{d} - {"active" if d in active_set else "inactive"}</title>')
    svg_parts.append('</circle>')

# footer text with total active days
total_active = len(active_set)
svg_parts.append(f'<text x="{cx}" y="{HEIGHT - 28}" font-size="18" text-anchor="middle" fill="#333">Active days tracked: {total_active}</text>')

svg = f'<?xml version="1.0" encoding="utf-8"?>\n'
svg += f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">\n'
svg += "\n".join(svg_parts)
svg += "\n</svg>"

with open(SVG_FILE, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Wrote {ACT_JSON} (entries={len(activity)}) and {SVG_FILE}")
