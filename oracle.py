import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word): return str(jsnum(n)) + " " + (word if n == 1 else word + "s")
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

SPANS = [(7, 76, "a reading nook"), (13, 107, "a bedroom"), (23, 132, "a living room"), (37, 152, "a great room")]
BODY = 30
TARGET = 240
MINCEIL = 240
COVER = 37

def span_plan(lenM, widM):
    if not (lenM > 0) or not (widM > 0):
        return {"error": "the room sides must be positive"}
    area = round1(lenM * widM)
    span, verdict = 152, "a great room that wants two fans"
    for cap, s, v in SPANS:
        if area <= cap:
            span, verdict = s, v
            break
    return {"area": area, "span": span, "verdict": verdict}

def rod_plan(ceilingCm):
    if not (ceilingCm > 0):
        return {"error": "the ceiling height must be positive"}
    if ceilingCm < MINCEIL:
        return {"error": "the ceiling is below the labeled 240 cm minimum for a fan"}
    rod = round1(max(0, ceilingCm - BODY - TARGET))
    if rod == 0: verdict = "no room for a downrod"
    elif rod <= 15: verdict = "a short drop"
    elif rod <= 90: verdict = "a standard drop"
    else: verdict = "a long drop for a tall ceiling"
    return {"rod": rod, "verdict": verdict}

def count_plan(lenM, widM):
    if not (lenM > 0) or not (widM > 0):
        return {"error": "the room sides must be positive"}
    area = round1(lenM * widM)
    count = max(1, math.ceil(area / COVER))
    long_wall = round1(max(lenM, widM))
    spacing = round1(long_wall / count)
    if count == 1: verdict = "one fan covers it"
    elif count <= 3: verdict = "a row of fans"
    else: verdict = "a grid of fans"
    return {"area": area, "count": count, "spacing": spacing, "longWall": long_wall, "verdict": verdict}

def render_span(r, lenM, widM):
    return ("A room " + fmt(lenM) + " m by " + fmt(widM) + " m is " + fmt(r["area"])
            + " m2 - a labeled " + fmt(r["span"]) + " cm blade span for " + r["verdict"] + ".")

def render_rod(r, ceilingCm):
    mount = "a flush mount" if r["rod"] == 0 else "a labeled " + fmt(r["rod"]) + " cm downrod"
    return "A ceiling " + fmt(ceilingCm) + " cm high takes " + mount + " - " + r["verdict"] + "."

def render_count(r, *args):
    if r["count"] == 1:
        where = "centered at " + fmt(r["spacing"]) + " m on the " + fmt(r["longWall"]) + " m wall"
    else:
        where = "spaced " + fmt(r["spacing"]) + " m along the " + fmt(r["longWall"]) + " m wall"
    return plural(r["count"], "fan") + " for " + fmt(r["area"]) + " m2, " + where + " - " + r["verdict"] + "."

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[4,5],[3,3],[2,2],[6,7],[5,7.4],[5,7.5],[4.5,3],[2.6,5],[0,5],[3,0]]:
    add("spanPlan", span_plan, render_span, a)
for a in [[300],[250],[420],[285],[286],[240],[239],[0],[360],[361]]:
    add("rodPlan", rod_plan, render_rod, a)
for a in [[10,5],[5,4],[20,8],[6,6.2],[6.08,6.08],[37,1],[38,1],[3,3],[0,4],[12,12]]:
    add("countPlan", count_plan, render_count, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
