#!/usr/bin/env python3
"""Independent check of the relative-distance widget.

Reads the shipped data.js, reimplements the speed models and the routing from the
written description rather than from the widget's code, and prints the numbers the
widget's own file records. Shares no code with the page.
"""
import json, math, heapq, re, sys

TXT = open(sys.argv[1] if len(sys.argv) > 1 else
           "/Users/luke/teaching-interactive/github/web/relative-distance/data.js").read()


def arr(name):
    mm = re.search(r"\b" + name + r":\[(.*?)\]", TXT, re.S)
    body = mm.group(1)
    return [int(v) for v in body.split(",")] if body.strip() else []


X0 = int(re.search(r"x0:(-?\d+)", TXT).group(1))
Y0 = int(re.search(r"y0:(-?\d+)", TXT).group(1))
Q = float(re.search(r"q:([\d.]+)", TXT).group(1))
N = int(re.search(r"\bn:(\d+)", TXT).group(1))
M = int(re.search(r"\bm:(\d+)", TXT).group(1))
PLACES = json.loads(re.search(r"places:(\[\[.*?\]\])", TXT, re.S).group(1))

nx, ny = arr("nx"), arr("ny")
eu, ev, el, eg, es, ef, ec = (arr(k) for k in ("eu", "ev", "el", "eg", "es", "ef", "ec"))

X = [0.0] * N; Y = [0.0] * N
ax = ay = 0
for i in range(N):
    ax += nx[i]; ay += ny[i]
    X[i] = X0 + ax * Q; Y[i] = Y0 + ay * Q

U = [0] * M; V = [0] * M
au = 0
for i in range(M):
    au += eu[i]; U[i] = au; V[i] = au + ev[i]

L = [v / 10.0 for v in el]
GR = [v / 1000.0 for v in eg]

# --- speed models, written from the widget's stated description ---------------
def v_foot(g, steps):
    if steps:
        return 1.5 / 3.6
    return 6.0 * math.exp(-3.5 * abs(g + 0.05)) / 3.6

def v_bike(g):
    a = 0.5 * 1.226 * 0.40
    b = 90.0 * 9.80665 * (0.005 + g)
    lo, hi = 0.02, 30.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if b * mid + a * mid ** 3 < 150.0:
            lo = mid
        else:
            hi = mid
    return min(max(lo, v_foot(g, 0)), 22.0 / 3.6)

FOOT, BIKE, CAR, STEPS, CF, CB, BF, BB = 1, 2, 4, 8, 16, 32, 64, 128

def arc_cost(e, fwd, mode):
    f = ef[e]
    g = GR[e] if fwd else -GR[e]
    if mode in (0, 1):
        if not (f & FOOT): return None
        if mode == 1 and ((f & STEPS) or abs(GR[e]) > 0.05): return None
        return L[e] / v_foot(g, f & STEPS)
    if mode == 2:
        if not (f & BIKE): return None
        if not (f & (BF if fwd else BB)): return None
        return L[e] / v_bike(g)
    if not (f & CAR): return None
    if not (f & (CF if fwd else CB)): return None
    return L[e] / (es[e] / 3.6)

def solve(mode, source, reverse=False):
    adj = [[] for _ in range(N)]
    for e in range(M):
        cf, cb = arc_cost(e, True, mode), arc_cost(e, False, mode)
        if cf is not None:
            (adj[V[e]] if reverse else adj[U[e]]).append((U[e] if reverse else V[e], cf))
        if cb is not None:
            (adj[U[e]] if reverse else adj[V[e]]).append((V[e] if reverse else U[e], cb))
    d = [math.inf] * N; d[source] = 0.0
    q = [(0.0, source)]
    while q:
        du, u = heapq.heappop(q)
        if du > d[u]: continue
        for v, w in adj[u]:
            if du + w < d[v]:
                d[v] = du + w; heapq.heappush(q, (du + w, v))
    return d

def usable(mode):
    ok = [False] * N
    for e in range(M):
        if arc_cost(e, True, mode) is not None or arc_cost(e, False, mode) is not None:
            ok[U[e]] = ok[V[e]] = True
    return ok

def nearest(px, py, pred=None):
    best, bd = -1, math.inf
    for i in range(N):
        if pred and not pred(i): continue
        d = (X[i] - px) ** 2 + (Y[i] - py) ** 2
        if d < bd: bd, best = d, i
    return best

PN = {}
for name, qx, qy in PLACES:
    PN[name] = nearest(X0 + qx * Q, Y0 + qy * Q)

def time_to(node, dist):
    """A trip ends within 150 m of the destination."""
    best = math.inf
    for i in range(N):
        if (X[i] - X[node]) ** 2 + (Y[i] - Y[node]) ** 2 <= 150.0 ** 2:
            best = min(best, dist[i])
    return best

MODES = ["on foot", "on foot, avoiding steep ground", "by bike", "by car"]
START = PN["Waterfront Station"]
TARGETS = ["Lonsdale Quay", "Commercial & Hastings", "Park Royal", "Upper Lonsdale",
           "Kitsilano Beach", "Jericho Beach"]

print("start: Waterfront Station, node", START)
print(f"{'':34s} " + "".join(f"{t[:16]:>18s}" for t in ("there", "back")))
res = {}
for mode in range(4):
    ok = usable(mode)
    src = START if ok[START] else nearest(X[START], Y[START], lambda i: ok[i])
    fwd = solve(mode, src)
    rev = solve(mode, src, reverse=True)
    reach = sum(1 for t in fwd if t < math.inf)
    use = sum(1 for b in ok if b)
    print(f"\n--- {MODES[mode]} --- reachable {reach} of {use} usable "
          f"({round(100*(use-reach)/use)}% out of reach)")
    for t in TARGETS:
        node = PN[t]
        o, b = time_to(node, fwd), time_to(node, rev)
        km = math.hypot(X[node] - X[src], Y[node] - Y[src]) / 1000
        f = lambda v: "unreachable" if v == math.inf else f"{v/60:.3f} min"
        print(f"  {t:26s} {km:5.2f} km {f(o):>18s} {f(b):>18s}")
        res[(mode, t)] = (o, b, km)
json.dump({f"{k[0]}|{k[1]}": [None if v[0] == math.inf else v[0],
                              None if v[1] == math.inf else v[1], v[2]]
           for k, v in res.items()}, open("verify.json", "w"), indent=1)
