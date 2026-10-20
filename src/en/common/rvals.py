# -*- coding: utf-8 -*-
"""Load dynamic R results (bootstrap intervals, CS-coefficients, invariance, NCT, ELSOC, etc.) for English lessons and materials.
Reads numbers from the canonical R/output/ directory and formats all prose strings in English."""
import csv, os, re
if not globals().get("ROOT"):
    ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
O = ROOT + "/R/output/"
RV = {}
f3 = lambda x: f"{float(x):.3f}".replace("-", "−")
f2 = lambda x: f"{float(x):.2f}"
def rows(fn):
    with open(O + fn, encoding="utf-8") as fh: return list(csv.DictReader(fh))

ITEM_EN = {
    "lone1": "Lack of companionship",
    "lone2": "Feeling left out",
    "lone3": "Feeling isolated",
    "lone4": "No one understands me",
    "dep1": "Depressed mood",
    "dep2": "Loss of interest",
    "dep3": "Sleep problems",
    "dep4": "Fatigue",
    "dep5": "Worthlessness",
}
PHQ_EN = {
    "phq1": "Little interest",
    "phq2": "Depressed mood",
    "phq3": "Sleep problems",
    "phq4": "Fatigue",
    "phq5": "Appetite change",
    "phq6": "Trouble concentrating",
    "phq7": "Low self-worth",
    "phq8": "Psychomotor retardation",
}

CS_STEP = 0.08
def cs_judge(v):
    v = float(v)
    if v >= 0.5 + CS_STEP: return "≥ 0.5: rank order is reasonably stable and can be interpreted (with care)"
    if v >= 0.5: return "just at 0.5, only one grid step above the cutoff (a different random seed could drop it one step): marginally stable, interpret rank order with caution"
    if v >= 0.25: return "0.25–0.5: minimally acceptable; report rank order for reference only"
    return "< 0.25: unstable; do not interpret rank order"
def cs_short(v):
    v = float(v)
    if 0.5 <= v < 0.5 + CS_STEP: return "just at 0.5, marginally stable"
    return "stable, ≥ 0.5" if v >= 0.5 else ("minimally acceptable, 0.25–0.5" if v >= 0.25 else "unstable, < 0.25")

# ---- 8.3 & 10.2 CS-coefficients ----
for tag, fn in [("8", "L8-3_CS.csv"), ("10", "L10-2_table5_CS.csv")]:
    for r in rows(fn):
        name, val = list(r.values())
        k = "in" if name.startswith("in") else "out"
        RV[f"cs{tag}_{k}"] = f2(val); RV[f"cs{tag}_{k}_judge"] = cs_judge(val); RV[f"cs{tag}_{k}_short"] = cs_short(val)
        RV[f"cs{tag}_{k}_raw"] = f"{float(val):.3f}"

# ---- 8.2 edge-weight bootstrap ----
B8 = rows("L8-2_cl_edge_boot.csv")
for r in B8:
    k = f'{r["node1"]}>{r["node2"]}'
    for c in ["sample", "mean", "q2.5", "q97.5"]: RV[f"b8_{k}_{c}"] = f3(r[c])
    RV[f"b8_{k}_prop0"] = f3(r["prop0"])
zero_lo = [f'{r["node1"]} → {r["node2"]}' for r in B8[:10] if abs(float(r["q2.5"])) < 5e-4]
RV["b8_zero_lower"] = ", ".join(zero_lo) if zero_lo else "(none in this run)"
RV["b8_n_zero_lower"] = str(len(zero_lo))
def _near0(r): return float(r["q2.5"]) if float(r["sample"]) > 0 else -float(r["q97.5"])
_first0 = next((i for i, r in enumerate(B8) if abs(_near0(r)) < 5e-4), None)
if zero_lo:
    RV["b8_zero_lower_text"] = "Among the top 10 cross-lagged edges, those whose bound nearer 0 equals 0 are: " + RV["b8_zero_lower"]
else:
    _m = min(_near0(r) for r in B8[:10])
    _t = f"None of the top 10 cross-lagged edges has an interval touching 0: on the side nearer 0, the smallest absolute bound is {_m:.3f}"
    if _first0 is not None:
        _r = B8[_first0]; _t += f", whereas starting from the #{_first0 + 1} strongest edge ({_r['node1']} → {_r['node2']}), the bound is at or near 0"
    RV["b8_zero_lower_text"] = _t
log82 = open(O + "L8-2_log.txt", encoding="utf-8").read()
diff = re.findall(r"^\s*\S+->\S+\s+\S+->\S+\s+\S+\s+\S+\s+(TRUE|FALSE)\s*$", log82, re.M)
RV["b8_diff_total"] = str(len(diff)); RV["b8_diff_sig"] = str(diff.count("TRUE"))
RV["b8_diff_text"] = ("all non-significant (every interval includes 0)" if diff.count("TRUE") == 0 else f"{diff.count('TRUE')} pairs significant")
m = re.search(r"手写 bootstrap（\s*(\d+)\s*次）：lone3 → dep1 的区间 = \[\s*([-\d.e]+)\s*,\s*([-\d.e]+)\s*\]；\s*被压为 0 的比例 = ([\d.]+)", log82)
RV["hand_n"], RV["hand_lo"], RV["hand_hi"], RV["hand_p0"] = m.group(1), f3(m.group(2)), f3(m.group(3)), f3(m.group(4))

# ---- 10.2 edge-weight bootstrap (Table 4) ----
B10 = rows("L10-2_table4_bootstrap_edges.csv")
for r in B10:
    k = f'{r["node1"]}>{r["node2"]}'
    for c in ["sample", "q2.5", "q97.5", "prop0"]: RV[f"b10_{k}_{c}"] = f3(r[c])
RV["b10_n_excl0"] = str(sum(1 for r in B10 if float(r["q2.5"]) > 0 or float(r["q97.5"]) < 0))
RV["b10_n"] = str(len(B10))

# ---- 3.5 Exercise A & 8.3 Exercise 1 ----
_l83 = open(O + "sol_L8-3_log.txt", encoding="utf-8").read()
m = re.search(r"孤独 → 抑郁 = ([\d.]+) ；抑郁 → 孤独 = ([\d.]+) ；差值 = ([-\d.]+)", _l83)
RV["sol83_sum_ld"], RV["sol83_sum_dl"], RV["sol83_diff"] = m.groups()
m = re.search(r"2\.5% = ([-\d.]+) ，97\.5% = ([-\d.]+) ；差值 ≤ 0 的比例 = ([\d.]+)", _l83)
RV["sol83_q025"], RV["sol83_q975"], RV["sol83_p0"] = m.groups()
m = re.search(r"LASSO（lambda.min）非零系数个数 = (\d+) ；假变量中的非零个数 = (\d+)", open(O + "sol_L3-5_log.txt", encoding="utf-8").read())
RV["sol25_min_n"], RV["sol25_min_false"] = m.group(1), m.group(2)

# ---- 5.3 RI-CLPM vs truth (R/L5-3b.R) ----
for r in rows("L5-3b_truth.csv"):
    k = f'ri53_{r["model"]}_{r["path"].replace(" ", "")}'
    for c in ["truth", "course", "q05", "q95", "sd"]: RV[f"{k}_{c}"] = f3(r[c])
    RV[f"{k}_pct"] = str(round(100 * float(r["pct"])))
    pc = float(r["pct"])
    hi, lo = round((1 - pc) * 200), round(pc * 200)
    RV[f"{k}_pos"] = ("larger than all 200 replicate estimates" if hi == 0 else "smaller than all 200 replicate estimates" if lo == 0
                      else f"exceeded by only {hi} of 200 replicate samples" if pc >= .95
                      else f"at or above only {lo} of 200 replicate samples" if pc <= .05
                      else f"at the {round(100 * pc)}th percentile across 200 replicate samples")

# ---- Simulated truth matrices ----
def _matrix(fn):
    with open(ROOT + "/data/" + fn, encoding="utf-8") as fh:
        r = list(csv.reader(fh))
    cols = r[0][1:]
    return {(row[0], c): float(v) for row in r[1:] for c, v in zip(cols, row[1:])}
TRUE_POP, TRUE_WIN = _matrix("true_B_population.csv"), _matrix("true_B_within.csv")
for (k, j), v in TRUE_POP.items(): RV[f"pop_{k}>{j}"] = f3(v)
for (k, j), v in TRUE_WIN.items(): RV[f"win_{k}>{j}"] = f3(v)

def truth_table_rows(n=10):
    """Lesson 10.2 Estimate vs. Truth comparison table rows."""
    edges = [r for r in rows("L10-2_table2_edges_AR_CL.csv") if r["from"] != r["to"]][:n]
    b10 = {(r["node1"], r["node2"]): r for r in B10}
    out = []
    for r in edges:
        k, j = r["from"], r["to"]
        p0 = b10.get((k, j), {}).get("prop0")
        out.append([f'{ITEM_EN[k]} → {ITEM_EN[j]} ({k} → {j})', f3(r["weight"]), f3(TRUE_POP[(k, j)]), f3(TRUE_WIN[(k, j)]), f3(p0) if p0 else "—"])
    return out
_top = [r for r in rows("L10-2_table2_edges_AR_CL.csv") if r["from"] != r["to"]][:10]
RV["truth10_n_near0"] = str(sum(1 for r in _top if abs(TRUE_POP[(r["from"], r["to"])]) < 0.02))
_ld = max(((k, j) for (k, j) in TRUE_POP if k.startswith("lone") and j.startswith("dep")), key=lambda e: abs(TRUE_POP[e]))
_B10m = {(r[""], c): float(v) for r in rows("L10-2_table2_B_matrix.csv") for c, v in r.items() if c}
RV["truth_ld_from"], RV["truth_ld_to"] = _ld
RV["truth_ld_pop"], RV["truth_ld_win"], RV["truth_ld_est"] = f3(TRUE_POP[_ld]), f3(TRUE_WIN[_ld]), f3(_B10m[_ld])
_r = next(r for r in B10 if (r["node1"], r["node2"]) == ("lone4", "dep4"))
RV["b10_lone4>dep4_cover"] = "includes" if float(_r["q2.5"]) <= TRUE_POP[("lone4", "dep4")] <= float(_r["q97.5"]) else "does not include"

# ==== Two truths: 7.2 recovery, 7.4 EI, 7.5 full procedure ====
def _bmat(fn):
    return {(r[""], j): float(v) for r in rows(fn) for j, v in r.items() if j}
def _pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return sab / (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** .5
def _ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for t in range(i, j + 1): r[o[t]] = (i + j) / 2 + 1
        i = j + 1
    return r
_OFF = sorted(k for k in TRUE_POP if k[0] != k[1])
_TGT = {k for k in _OFF if abs(TRUE_POP[k]) >= 0.05}
_WIN = {k for k in _OFF if TRUE_WIN[k] != 0}
_TRAIT = _TGT - _WIN
RV["rec72_n_pop"], RV["rec72_n_win"], RV["rec72_n_trait"] = str(len(_TGT)), str(len(_WIN)), str(len(_TRAIT))
RV["rec72_n_both"] = str(len(_TGT & _WIN))
RV["rec72_n_trait_same"] = str(sum(1 for k, j in _TRAIT if k[:3] == j[:3]))
RV["rec72_trait_lo"], RV["rec72_trait_hi"] = f3(min(abs(TRUE_POP[k]) for k in _TRAIT)), f3(max(abs(TRUE_POP[k]) for k in _TRAIT))
RV["rec72_pop_maxsmall"] = f3(max(abs(TRUE_POP[k]) for k in _OFF if k not in _TGT))
_REC = {}
for rule, fn in [("min", "L7-2_B_lambda_min.csv"), ("1se", "L7-2_B_lambda_1se.csv"), ("ebic", "L7-2_B_ebic.csv")]:
    E = _bmat(fn)
    for k in _OFF: RV[f"est72_{rule}_{k[0]}>{k[1]}"] = f3(E[k])
    est = {k for k in _OFF if E[k] != 0}
    for tag, T, truth in [("pop", TRUE_POP, _TGT), ("win", TRUE_WIN, _WIN)]:
        v = dict(n_true=len(truth), hit=len(truth & est), miss=len(truth - est), fp=len(est - truth),
                 n_est=len(est), r=_pearson([E[k] for k in _OFF], [T[k] for k in _OFF]), trait_hit=len(est & _TRAIT))
        _REC[(rule, tag)] = v
        for c, x in v.items(): RV[f"rec72_{rule}_{tag}_{c}"] = f3(x) if c == "r" else str(x)
_EI = rows("L7-4_EI.csv"); _nodes = [r.get("节点") or r.get("node") for r in _EI]
_tout = {t: [sum(M[(k, j)] for j in _nodes if j != k) for k in _nodes] for t, M in [("pop", TRUE_POP), ("win", TRUE_WIN)]}
_tin = {t: [sum(M[(k, j)] for k in _nodes if k != j) for j in _nodes] for t, M in [("pop", TRUE_POP), ("win", TRUE_WIN)]}
_eout, _ein = [float(r["outEI"]) for r in _EI], [float(r["inEI"]) for r in _EI]
for t in ["pop", "win"]:
    RV[f"ei74_rho_out_{t}"] = f2(_pearson(_ranks(_eout), _ranks(_tout[t])))
    RV[f"ei74_rho_in_{t}"] = f2(_pearson(_ranks(_ein), _ranks(_tin[t])))
    for n, vo, vi in zip(_nodes, _tout[t], _tin[t]): RV[f"ei74_{t}_out_{n}"], RV[f"ei74_{t}_in_{n}"] = f3(vo), f3(vi)
    _o = sorted(zip(_nodes, _tout[t]), key=lambda x: -x[1])
    RV[f"ei74_{t}_out_top"], RV[f"ei74_{t}_out_top2"] = _o[0][0], _o[1][0]
    RV[f"ei74_{t}_out_lone4_rank"] = str(1 + sum(1 for v in _tout[t] if v > _tout[t][_nodes.index("lone4")]))
    for tag, a, b in [("ld", "lone", "dep"), ("dl", "dep", "lone")]:
        M = TRUE_POP if t == "pop" else TRUE_WIN
        RV[f"ei74_{t}_sum_{tag}"] = f3(sum(M[(k, j)] for k in _nodes for j in _nodes if k.startswith(a) and j.startswith(b)))
for n, v in zip(_nodes, _eout): RV[f"ei74_est_out_{n}"] = f3(v)
RV["ei74_est_out_top"] = max(zip(_nodes, _eout), key=lambda x: x[1])[0]
for tag, a, b in [("ld", "lone", "dep"), ("dl", "dep", "lone")]:
    _cl = _bmat("L7-2_B_lambda_min.csv")
    RV[f"ei74_est_sum_{tag}"] = f3(sum(_cl[(k, j)] for k in _nodes for j in _nodes if k.startswith(a) and j.startswith(b)))
_l75 = open(O + "L7-5b_log.txt", encoding="utf-8").read()
for tag, pat in [("lasso", r"仅 LASSO（lambda.min）"), ("p01", r"LASSO \+ SEM 重估，最终模型（p < \.01）"),
                 ("p05", r"LASSO \+ SEM 重估，最终模型（p < \.05）"), ("free01", r"对照：不约束模型（p < \.01）")]:
    _m = re.search("^" + pat + r"\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$", _l75, re.M)
    RV[f"sem75_{tag}_hit"], RV[f"sem75_{tag}_fp"], RV[f"sem75_{tag}_miss"], RV[f"sem75_{tag}_n"] = _m.groups()
_m = re.search(r"总体目标值中的交叉滞后边 (\d+) 条", _l75); RV["sem75_n_true"] = _m.group(1)
_m = re.search(r"相关（被保留的路径）= ([\d.]+) ；LASSO 边权与总体目标值的相关（同一批路径）= ([\d.]+)", _l75)
RV["sem75_r_sem"], RV["sem75_r_lasso"] = _m.groups()
_m = re.search(r"lone3 → dep1 总体目标值 ([\d.]+) ；LASSO ([\d.]+) ；SEM 重估 ([\d.]+)", _l75)
RV["sem75_l3d1_lasso"], RV["sem75_l3d1_sem"] = _m.group(2), _m.group(3)

def boot_table_rows(edges, src="b8"):
    """Generate table rows for Lesson 8.2: [Edge, Sample Est., Bootstrap Mean, 2.5%, 97.5%, prop0]"""
    out = []
    for e in edges:
        k = e.replace(" ", "").replace("→", ">")
        out.append([e, RV[f"{src}_{k}_sample"], RV.get(f"{src}_{k}_mean", "—"), RV[f"{src}_{k}_q2.5"], RV[f"{src}_{k}_q97.5"], RV[f"{src}_{k}_prop0"]])
    return out

VPAT = re.compile(r"\{\{V:([^}]+)\}\}")
def fillV(s):
    def rep(m):
        k = m.group(1)
        if k not in RV: raise KeyError("Unknown R result key in prose: " + k)
        return RV[k]
    return VPAT.sub(rep, s)

# ---- 7.6 Measurement invariance & sample-size planning ----
_PART = {"1 纵向 longitudinal": "long", "2 多组 gender": "sex", "3 改动后 modified": "bad"}
_LEV = {"构形": "conf", "度量": "metr", "标量": "scal", "部分标量": "part"}
for r in rows("L7-6_invariance_fit.csv"):
    k = f'mi_{_PART[r["part"]]}_{_LEV[r["model"].split()[0]]}'
    RV[k + "_chisq"] = f2(r["chisq"]); RV[k + "_df"] = str(int(float(r["df"])))
    for c in ["CFI", "RMSEA"]: RV[f"{k}_{c}"] = f3(r[c])
    for c in ["dCFI", "dRMSEA"]:
        if r[c] != "NA": RV[f"{k}_{c}"] = ("+" if float(r[c]) > 0 else "") + f3(r[c])
log76 = open(O + "L7-6_log.txt", encoding="utf-8").read()
_lrt = re.findall(r"^([fg]_(?:metr|scal))\s+\d+\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s*$", log76, re.M)
for name, chi, ddf, p in _lrt:
    k = f'mi_{"long" if name[0] == "f" else "sex"}_{name[2:]}'
    RV[k + "_dchisq"], RV[k + "_ddf"], RV[k + "_lrtp"] = chi, ddf, f"{float(p):.3f}"
_fm = re.search(r"F2\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\n\s*F3\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)", log76)
RV["mi_long_F2"], RV["mi_long_F2_p"], RV["mi_long_F3"], RV["mi_long_F3_p"] = f3(_fm.group(1)), f3(_fm.group(3)), f3(_fm.group(4)), f3(_fm.group(6))
_sx = re.search(r"女性的抑郁因子均值比男性高 ([\d.]+)（SE = ([\d.]+)，p = ([\d.]+)）", log76)
RV["mi_sex_diff"], RV["mi_sex_diff_se"], RV["mi_sex_diff_p"] = _sx.group(1), _sx.group(2), _sx.group(3)
_nn = re.search(r"各组人数：\s*\n\s*男\s+女\s*\n\s*(\d+)\s+(\d+)", log76)
RV["mi_n_m"], RV["mi_n_f"] = _nn.group(1), _nn.group(2)
_sc = re.findall(r"^\s*(\S+) 的截距 = (\S+) 的截距\s+([\d.]+)\s*$", log76, re.M)
RV["mi_score1_a"], RV["mi_score1_b"], RV["mi_score1_x2"] = _sc[0][0], _sc[0][1], f2(_sc[0][2])
RV["mi_score2_x2"] = f2(_sc[1][2])
_f3 = re.search(r"第 3 波孤独因子均值：原始数据 ([-\d.]+)；改动后、强加标量不变性 ([-\d.]+)；改动后、部分不变性 ([-\d.]+)", log76)
RV["mi_F3_orig"], RV["mi_F3_forced"], RV["mi_F3_part"] = f3(_f3.group(1)), f3(_f3.group(2)), f3(_f3.group(3))
RV["ss_reps"] = re.search(r"每个 N 重复 (\d+) 次", log76).group(1)
RV["ss_n_target"] = re.search(r"目标边 (\d+) 条", log76).group(1)
RV["ss_n_near0"] = re.search(r"几乎为 0 的边（\|B\| < 0.02） (\d+) 条", log76).group(1)
SS76 = rows("L7-6_power.csv")
for r in SS76:
    for c in ["power_target", "p_all8", "fpr_near0", "r_with_true"]:
        RV[f'ss_{r["rule"]}_{r["N"]}_{c}'] = f2(r[c])
def _first_n(rule, col, thr):
    ns = [int(r["N"]) for r in SS76 if r["rule"] == rule and float(r[col]) >= thr]
    return str(min(ns)) if ns else "(not reached within the simulated N range)"
RV["ss_min_power80_n"] = _first_n("min", "power_target", 0.8)
RV["ss_1se_power80_n"] = _first_n("1se", "power_target", 0.8)
RV["ss_min_all8_80_n"] = _first_n("min", "p_all8", 0.8)
def ss_table_rows():
    out = []
    for n in sorted({int(r["N"]) for r in SS76}):
        g = lambda rule, c: RV[f"ss_{rule}_{n}_{c}"]
        out.append([str(n), g("min", "power_target"), g("min", "p_all8"), g("min", "fpr_near0"), g("min", "r_with_true"), g("1se", "power_target"), g("1se", "fpr_near0")])
    return out
sol76 = open(O + "sol_L7-6_log.txt", encoding="utf-8").read()
_blk = re.findall(r"^\s*(构形|度量|标量) \S+\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\S+)\s+(\S+)\s*$", sol76, re.M)
for tag, part in (("dep", _blk[0:3]), ("coach", _blk[3:6])):
    for lev, chi, df, cfi, rmsea, dcfi, drmsea in part:
        k = f"sol76_{tag}_{_LEV[lev]}"
        RV[k + "_chisq"], RV[k + "_df"], RV[k + "_CFI"], RV[k + "_RMSEA"] = chi, df, f3(cfi), f3(rmsea)
        if dcfi != "NA": RV[k + "_dCFI"] = ("+" if float(dcfi) > 0 else "") + f3(dcfi)
_ps = re.findall(r"度量 vs 构形 = ([\d.]+) ；标量 vs 度量 = ([\d.]+)", sol76)
(RV["sol76_dep_p_metr"], RV["sol76_dep_p_scal"]), (RV["sol76_coach_p_metr"], RV["sol76_coach_p_scal"]) = _ps[0], _ps[1]
_dm = re.search(r"第 2、3 波的抑郁因子均值（第 1 波 = 0）： ([-\d.]+)，([-\d.]+)", sol76)
RV["sol76_dep_F2"], RV["sol76_dep_F3"] = f3(_dm.group(1)), f3(_dm.group(2))
_w = re.search(r"^\s*(\S+) 的截距 = (\S+) 的截距\s+([\d.]+)\s*$", sol76, re.M)
RV["sol76_worst_a"], RV["sol76_worst_b"], RV["sol76_worst_x2"] = _w.group(1), _w.group(2), _w.group(3)
_pp = re.search(r"部分标量（放开 (\S+) 的截距）\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\S+)", sol76)
RV["sol76_part_item"], RV["sol76_part_chisq"], RV["sol76_part_df"], RV["sol76_part_CFI"], RV["sol76_part_dCFI"] = _pp.group(1), _pp.group(2), _pp.group(3), f3(_pp.group(4)), f3(_pp.group(6))
_cm = re.search(r"完全标量 ([-\d.]+)（SE ([\d.]+)），([-\d.]+)（SE ([\d.]+)） ；部分标量 ([-\d.]+)（SE ([\d.]+)），([-\d.]+)（SE ([\d.]+)）", sol76)
RV["sol76_coach_F2_full"], RV["sol76_coach_F3_full"], RV["sol76_coach_F2_part"], RV["sol76_coach_F3_part"] = (f3(_cm.group(i)) for i in (1, 3, 5, 7))
RV["sol76_coach_F_se"] = _cm.group(2)
RV["sol76_coach_ncomplete"] = re.search(r"三波社会幸福感 5 题都完整的人数： (\d+)", sol76).group(1)
_fmin = [float(r["fpr_near0"]) for r in SS76 if r["rule"] == "min"]; _f1 = [float(r["fpr_near0"]) for r in SS76 if r["rule"] == "1se"]
RV["ss_min_fpr_lo"], RV["ss_min_fpr_hi"] = f2(min(_fmin)), f2(max(_fmin))
RV["ss_1se_fpr_lo"], RV["ss_1se_fpr_hi"] = f2(min(_f1)), f2(max(_f1))
_chk = re.findall(r"^T([123])\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", sol76, re.M)
for t, emo, soc, psy, wb in _chk: RV[f"sol76_chk_soc_T{t}"] = soc

# ---- 7.7 Group comparison (R/L7-7.R & R/solutions/L7-7_solution.R) ----
for i, r in enumerate(rows("L7-7_perm_summary.csv"), 1):
    for c in ["M", "p_M", "S", "p_S", "p_lone3_dep1"]: RV[f"pg{i}_{c}"] = f3(r[c])
    for c in ["n1", "n2", "nperm", "edges_p05", "edges_holm05"]: RV[f"pg{i}_{c}"] = str(int(float(r[c])))
log77 = open(O + "L7-7_log.txt", encoding="utf-8").read()
_parts = re.split(r"^===== 第 \d 部分", log77, flags=re.M)[1:]
for i, b in enumerate(_parts, 1):
    m = re.search(r"M（差得最多的边）= ([\d.]+)：(\S+) → (\S+)（\S+ ([-\d.]+)，\S+ ([-\d.]+)）", b)
    RV[f"pg{i}_M_from"], RV[f"pg{i}_M_to"], RV[f"pg{i}_M_b1"], RV[f"pg{i}_M_b2"] = m.group(2), m.group(3), f3(m.group(4)), f3(m.group(5))
    m = re.search(r"S（整体强度之差）= [\d.]+（\S+ ([\d.]+)，\S+ ([\d.]+)）", b)
    RV[f"pg{i}_S1"], RV[f"pg{i}_S2"] = m.group(1), m.group(2)
    m = re.search(r"M 的 95% 分位数 = ([\d.]+)，S 的 95% 分位数 = ([\d.]+)", b)
    RV[f"pg{i}_M_q95"], RV[f"pg{i}_S_q95"] = m.group(1), m.group(2)
    m = re.search(r"^\s*lone3\s+dep1\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([\d.]+)", b, re.M)
    if m: RV[f"pg{i}_l3d1_b1"], RV[f"pg{i}_l3d1_b2"] = f3(m.group(1)), f3(m.group(2))
    m = re.search(r"用时 (\d+) 秒", b); RV[f"pg{i}_secs"] = m.group(1)
m = re.search(r"最小可能的 p = 1/1001 = ([\d.]+)；72 条边做 Holm 校正，最小的 p 要乘以 72 → ([\d.]+)", log77)
RV["pg_pmin"], RV["pg_holm_min"] = m.group(1), m.group(2)
sol77 = open(O + "sol_L7-7_log.txt", encoding="utf-8").read()
m = re.search(r"M = ([\d.]+)（(\S+) → (\S+)：男 ([\d.]+)，女 ([\d.]+)），置换 p = ([\d.]+)", sol77)
RV["sol77_M"], RV["sol77_M_from"], RV["sol77_M_to"], RV["sol77_M_m"], RV["sol77_M_f"], RV["sol77_pM"] = m.groups()
m = re.search(r"S = ([\d.]+)（男 ([\d.]+)，女 ([\d.]+)），置换 p = ([\d.]+)", sol77)
RV["sol77_S"], RV["sol77_S_m"], RV["sol77_S_f"], RV["sol77_pS"] = m.groups()
RV["sol77_n05"] = re.search(r"未校正 p < .05 的有 (\d+) 条", sol77).group(1)
RV["sol77_pmin"] = re.search(r"最小可能的 p = ([\d.]+)", sol77).group(1)
m = re.search(r"lone3 → dep1：男 ([\d.]+)，女 ([\d.]+)，单条边置换 p = ([\d.]+)", sol77)
RV["sol77_l3d1_m"], RV["sol77_l3d1_f"], RV["sol77_l3d1_p"] = m.groups()

# ---- Final Exam Part B ----
_bm = rows("L7-2_B_lambda_min.csv")
_cl = []
for r in _bm:
    k = r[""]
    for j, v in r.items():
        if j and j != k: _cl.append((float(v), k, j))
for tag, pre_k, pre_j in [("ld", "lone", "dep"), ("dl", "dep", "lone")]:
    v, k, j = max((x for x in _cl if x[1].startswith(pre_k) and x[2].startswith(pre_j)), key=lambda x: abs(x[0]))
    RV[f"fx_{tag}_from"], RV[f"fx_{tag}_to"], RV[f"fx_{tag}_b"] = k, j, f3(v)
    RV[f"fx_{tag}_from_zh"], RV[f"fx_{tag}_to_zh"] = ITEM_EN[k], ITEM_EN[j]
RV["fx_n_cl"] = str(sum(1 for x in _cl if x[0] != 0))
_ei = rows("L7-4_EI.csv")
for c, tag in [("outEI", "out"), ("inEI", "in")]:
    top = max(_ei, key=lambda r: float(r[c]))
    node_id = top.get("节点") or top.get("node")
    RV[f"fx_{tag}_top"], RV[f"fx_{tag}_top_zh"], RV[f"fx_{tag}_top_v"] = node_id, ITEM_EN[node_id], f2(top[c])
_s6 = {r["analysis"]: r for r in rows("L10-2_table6_sensitivity.csv")}
RV["fx_sens_1se_r"], RV["fx_sens_1se_n"] = f2(_s6["lambda.1se"]["r_with_main"]), _s6["lambda.1se"]["n_CL_edges"]
RV["fx_sens_rep_r"], RV["fx_sens_rep_n"] = f2(_s6["T2→T3 复现"]["r_with_main"]), _s6["T2→T3 复现"]["n_CL_edges"]
RV["fx_sens_cov_r"] = f3(_s6["协变量 gender+age"]["r_with_main"])
_b10 = rows("L10-2_table2_B_matrix.csv")
RV["fx_sens_main_n"] = str(sum(1 for r in _b10 for j, v in r.items() if j not in ("", r[""]) and v not in ("", "NA") and float(v) != 0))

# ---- ELSOC real-data case ----
def _el_must(pat, text, label):
    m = re.search(pat, text, re.M)
    if not m:
        raise SystemExit("rvals: missing in ELSOC log: " + label)
    return m
_elog = open(O + "data_elsoc_log.txt", encoding="utf-8").read()
_clog = open(O + "case_elsoc_log.txt", encoding="utf-8").read()
_dsrc = open(ROOT + "/R/data_elsoc.R", encoding="utf-8").read()
_csrc = open(ROOT + "/R/case_elsoc.R", encoding="utf-8").read()
RV["el_doi"] = _el_must(r'DOI\s*<-\s*"([^"]+)"', _dsrc, "DOI").group(1)
RV["el_version"] = _el_must(r'VERSION\s*<-\s*"([^"]+)"', _dsrc, "VERSION").group(1)
RV["el_file"] = _el_must(r'FILE_NAME\s*<-\s*"([^"]+)"', _dsrc, "FILE_NAME").group(1)
RV["el_md5"] = _el_must(r'FILE_MD5\s*<-\s*"([0-9a-f]{32})"', _dsrc, "FILE_MD5").group(1)
RV["el_boot_n"] = _el_must(r"B_BOOT\s*<-\s*(\d+)", _csrc, "B_BOOT").group(1)
m = _el_must(r"原始数据：\s*(\d+)\s*行\s*×\s*(\d+)\s*列", _elog, "raw dimensions")
RV["el_n_raw"], RV["el_n_col"] = m.group(1), m.group(2)
m = _el_must(r"原始样本\s*(\d+)\s*人，补充样本（([^）]+)）\s*(\d+)\s*人", _elog, "sample composition")
RV["el_n_orig"], RV["el_sup_when"], RV["el_n_sup"] = m.group(1), "from 2018 onward", m.group(3)
_waves = _el_must(r"第\s*1\s*波（(\d+)\s*年）PHQ-8 完整：(\d+)\s*人\s*第\s*2\s*波（(\d+)\s*年）PHQ-8 完整：(\d+)\s*人\s*第\s*3\s*波（(\d+)\s*年）PHQ-8 完整：(\d+)\s*人", _elog, "wave completeness").groups()
RV["el_y1"], RV["el_n_w1"], RV["el_y2"], RV["el_n_w2"], RV["el_y3"], RV["el_n_w3"] = _waves
m = _el_must(r"第 1[–-]2 波都完整：\s*(\d+)\s*人；第 1[–-]3 波都完整：\s*(\d+)\s*人", _elog, "multi-wave complete")
RV["el_n_w12"], RV["el_n"] = m.group(1), m.group(2)
m = _el_must(r"女性\s*(\d+)\s*人（([\d.]+)%），(\d+)\s*年年龄 M = ([\d.]+)，SD = ([\d.]+)，范围\s*(\d+)[–-](\d+)", _elog, "demographics")
RV["el_n_f"], RV["el_pct_f"], RV["el_age_y"], RV["el_age_m"], RV["el_age_sd"], RV["el_age_lo"], RV["el_age_hi"] = m.groups()
m = _el_must(r"PHQ-8 总分（8[–-]40）：(\d+) M = ([\d.]+)，(\d+) M = ([\d.]+)，(\d+) M = ([\d.]+)；\1 与 \3 总分相关 r = ([\d.]+)", _clog, "total scores")
RV["el_tot_y1"], RV["el_tot_m1"], RV["el_tot_y2"], RV["el_tot_m2"], RV["el_tot_y3"], RV["el_tot_m3"], RV["el_tot_r"] = m.groups()
_el_desc_raw = [m.groups() for m in re.finditer(r"(?m)^\s*(phq\d)\s+(\S+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", _clog)]
EL_DESC = [(k, PHQ_EN[k], m1, sd1, m2, m3) for k, _zh_lbl, m1, sd1, m2, m3 in _el_desc_raw]
_Brows = rows("case_elsoc_B.csv")
_labs = [r[""] for r in _Brows]
_B = {r[""]: r for r in _Brows}
_n_cl = _n_neg = 0
_max_abs = 0.0
for i in _labs:
    for j in _labs:
        if i == j: continue
        v = float(_B[i][j])
        if v == 0: continue
        _n_cl += 1
        if v < 0: _n_neg += 1
        _max_abs = max(_max_abs, abs(v))
m = _el_must(r"非零交叉滞后边：(\d+) / (\d+) 条；最大 \|B\| = ([\d.]+)", _clog, "2016->2017 edge count")
RV["el_n_cl"], RV["el_n_cell"], RV["el_max_b"] = m.group(1), m.group(2), m.group(3)
RV["el_n_neg"] = str(_n_neg)
RV["el_n_plus"] = str(_n_cl - _n_neg)
_ar_line = _el_must(r"(?m)^((?:-?[\d.]+ +){7}-?[\d.]+)\s*$", _clog, "autoregressive row")
_ar_vals = _ar_line.group(1).split()
EL_AR = [(k, PHQ_EN[k], v) for k, v in zip(_labs, _ar_vals)]
_ar_hi = max(EL_AR, key=lambda t: float(t[2]))
_ar_lo = min(EL_AR, key=lambda t: float(t[2]))
RV["el_ar_hi_zh"], RV["el_ar_hi"] = _ar_hi[1], _ar_hi[2]
RV["el_ar_lo_zh"], RV["el_ar_lo"] = _ar_lo[1], _ar_lo[2]
_bt = rows("case_elsoc_boot.csv")
EL_TOP = []
for r in _bt[:8]:
    a, b = r["edge"].split(">")
    EL_TOP.append((a, PHQ_EN[a], b, PHQ_EN[b], f3(r["sample"]), f3(r["q2.5"]), f3(r["q97.5"]), f3(r["prop0"])))
m = _el_must(r"最强 8 条边中，区间不含 0 的有 (\d+) 条", _clog, "intervals excluding 0")
RV["el_top_n"], RV["el_top_excl0"] = "8", m.group(1)
RV["el_top1_from_zh"], RV["el_top1_to_zh"], RV["el_top1_b"] = EL_TOP[0][1], EL_TOP[0][3], EL_TOP[0][4]
RV["el_top1_lo"], RV["el_top1_hi"] = EL_TOP[0][5], EL_TOP[0][6]
RV["el_top2_from_zh"], RV["el_top2_to_zh"], RV["el_top2_b"] = EL_TOP[1][1], EL_TOP[1][3], EL_TOP[1][4]
m = _el_must(r"(\d+)\s*→\s*(\d+)\s*非零交叉滞后边：(\d+) / (\d+) 条；与 (\d+)\s*→\s*(\d+) 的 (\d+) 条交叉滞后边的相关 r = ([\d.]+)", _clog, "replication")
RV["el_rep_y1"], RV["el_rep_y2"], RV["el_n_cl_rep"], RV["el_rep_den"], RV["el_rep_r"] = m.group(1), m.group(2), m.group(3), m.group(4), m.group(8)
m = _el_must(r"最强 8 条边中，在 \d+ → \d+ 里同方向且非零的有 (\d+) 条", _clog, "replication same sign")
RV["el_rep_same"] = m.group(1)
m = _el_must(r"N = (\d+)；非零交叉滞后边 (\d+) / (\d+) 条；与主分析交叉滞后边的相关 r = ([\d.]+)", _clog, "covariate sensitivity")
RV["el_n_sens"], RV["el_n_cl_sens"], RV["el_sens_den"], RV["el_r_sens"] = m.group(1), m.group(2), m.group(3), m.group(4)
_ei = sorted(rows("case_elsoc_EI.csv"), key=lambda r: -float(r["outEI"]))
EL_EI = [(r.get("节点") or r.get("node"), PHQ_EN[r.get("节点") or r.get("node")], f3(r["outEI"]), f3(r["inEI"])) for r in _ei]
_in_top = max(_ei, key=lambda r: float(r["inEI"]))
_out_id = _ei[0].get("节点") or _ei[0].get("node")
_in_id = _in_top.get("节点") or _in_top.get("node")
RV["el_out_top"], RV["el_out_top_zh"], RV["el_out_top_v"] = _out_id, PHQ_EN[_out_id], f3(_ei[0]["outEI"])
RV["el_in_top"], RV["el_in_top_zh"], RV["el_in_top_v"] = _in_id, PHQ_EN[_in_id], f3(_in_top["inEI"])

# ---- 0.2 quick run ----
RV["quick_n_cl"] = re.search(r"72 个交叉滞后格子中不为 0 的：(\d+) 条", open(O + "L0-2_log.txt", encoding="utf-8").read()).group(1)

# ---- 10.2 / 10.3 Wysocki et al. (2025) full-procedure sensitivity analysis (R/L10-2b.R) ----
def _fp_p(v):
    if v in ("", "NA"): return "—"
    v = float(v)
    return "< 0.001" if v < 0.001 else f"{v:.3f}"
_FP10_INT = ["n_lasso_main", "n_cl12", "n_cl23", "n_keep", "free_df", "eq_ddf", "fin_df", "n_sig01", "n_sig01_ld", "n_sig01_dl",
             "n_sig01_within", "n_sig05", "n_both", "n_lasso_only", "n_sem_only", "top_n", "top_kept", "top3_kept",
             "n_boot_excl0", "n_boot_excl0_kept", "n_true", "found_lasso", "fp_lasso", "found_full", "fp_full",
             "n_true_w", "found_lasso_w", "fp_lasso_w", "found_full_w", "fp_full_w"]
_FP10_F2 = ["free_chisq", "eq_dchisq", "fin_chisq", "ld_lasso", "dl_lasso", "ld_full", "dl_full"]
_FP10_F3 = ["free_cfi", "free_tli", "free_rmsea", "free_rmsea_lo", "free_rmsea_hi", "free_srmr", "eq_p",
            "fin_cfi", "fin_tli", "fin_rmsea", "fin_srmr", "r_lasso_sem"]
_FP10_F1 = ["aic_equal", "aic_free", "bic_equal", "bic_free"]
_fps = {r["statistic"]: r["value"] for r in rows("L10-2b_summary.csv")}
_fpe = rows("L10-2b_edges.csv")
_l10top = [r for r in rows("L10-2_table2_edges_AR_CL.csv") if r["from"] != r["to"]]
for k in _FP10_INT: RV["fp10_" + k] = str(int(float(_fps[k])))
for k in _FP10_F2: RV["fp10_" + k] = f2(_fps[k]).replace("-", "−")
for k in _FP10_F3: RV["fp10_" + k] = f3(_fps[k])
for k in _FP10_F1: RV["fp10_" + k] = f"{float(_fps[k]):.1f}"
RV["fp10_free_p"] = "< 0.001" if float(_fps["free_p"]) < 0.001 else "= " + f3(_fps["free_p"])
_eq = float(_fps["use_equal"]) == 1
RV["fp10_final"] = ("constrained model (each T1→T2 path set equal to T2→T3)" if _eq else "unconstrained model (two wave-pairs estimated separately; T1→T2 reported below)")
RV["fp10_final_short"] = "constrained model" if _eq else "unconstrained model"
for r in _fpe:
    k = f'{r["from"]}>{r["to"]}'
    RV[f"fp10_{k}_sem"] = f3(r["sem_est"]); RV[f"fp10_{k}_p"] = _fp_p(r["sem_p"])
    RV[f"fp10_{k}_kept"] = "retained" if r["kept_p01"] == "TRUE" else ("not in SEM" if r["in_sem"] != "TRUE" else "pruned")
    RV[f"fp10_{k}_t23"] = f3(r["lasso_t23"]); RV[f"fp10_{k}_free"] = f3(r["free_est"]); RV[f"fp10_{k}_free_p"] = _fp_p(r["free_p"])
_top = [r for r in _fpe if float(r["lasso"]) != 0][:int(float(_fps["top_n"]))]
RV["fp10_top_edges"] = ",".join(f'{r["from"]}>{r["to"]}' for r in _top)
_drop = [r for r in _top if r["kept_p01"] != "TRUE"]
RV["fp10_top_dropped"] = ", ".join(f'"{ITEM_EN[r["from"]]} → {ITEM_EN[r["to"]]}" ({r["from"]} → {r["to"]}; LASSO {f3(r["lasso"])}, SEM re-estimate {f3(r["sem_est"])}, p = {_fp_p(r["sem_p"])})' for r in _drop) or "(none: all top edges were retained)"
RV["fp10_top_dropped_n_text"] = f"{len(_drop)} pruned" if _drop else "all retained"
def _kept_list(a, b):
    ks = sorted((r for r in _fpe if r["kept_p01"] == "TRUE" and float(r["lasso"]) != 0 and r["from"].startswith(a) and r["to"].startswith(b)), key=lambda r: -abs(float(r["sem_est"])))
    return ", ".join(f'"{ITEM_EN[r["from"]]} → {ITEM_EN[r["to"]]}" ({f3(r["sem_est"])})' for r in ks) or "(none)"
RV["fp10_kept_ld_list"], RV["fp10_kept_dl_list"] = _kept_list("lone", "dep"), _kept_list("dep", "lone")
RV["fp10_exp_fp01"] = f"{int(float(_fps['n_keep'])) * 0.01:.2f}"; RV["fp10_exp_fp05"] = f"{int(float(_fps['n_keep'])) * 0.05:.2f}"
for r in _l10top: RV[f'fp10_{r["from"]}>{r["to"]}_label'] = f'{ITEM_EN[r["from"]]} → {ITEM_EN[r["to"]]} ({r["from"]} → {r["to"]})'
