# -*- coding: utf-8 -*-
# 真实数据案例 materials/case_elsoc.html。由 src/build_materials.py 在写作工作坊之后 exec
# （可用 page、sec、L、E、_qz、_RVG）。正文里的运行结果写成 {{V:键}} 或直接用 _RVG 里的表，
# 键在 src/common/rvals.py 从 R/output/data_elsoc_log.txt、case_elsoc_*.csv 读取。不要手抄。
RV, fillV = _RVG["RV"], _RVG["fillV"]
def fill_all(s):
    """f-string 会把 {{V:键}} 收成 {V:键}；两种写法都换成日志里的数。"""
    s = fillV(s)
    def rep(m):
        k = m.group(1)
        if k not in RV:
            raise KeyError("正文引用了不存在的 R 结果键：" + k)
        return RV[k]
    return re.sub(r"(?<!\{)\{V:([^}]+)\}(?!\})", rep, s)
def _tbl(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)   # 表头里可以有尚未替换的 {{V:键}}
    body = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'
def Q(src):
    return _qz.quiz(fill_all(src))   # 数值题的答案也来自日志，先替换再交给测验渲染器

_y1, _y2, _y3 = "{{V:el_y1}}", "{{V:el_y2}}", "{{V:el_y3}}"
desc = _tbl(["题目", "中文", f"{_y1} 均值", f"{_y1} 标准差", f"{_y2} 均值", f"{_y3} 均值"], _RVG["EL_DESC"])
ar = _tbl(["题目", "中文", "自回归 B"], [(a, b, c) for a, b, c in _RVG["EL_AR"]])
top = _tbl(["从（T）", "中文", "到（T+1）", "中文", "样本 B", "2.5%", "97.5%", "被压成 0 的比例"],
           [r for r in _RVG["EL_TOP"]])
ei = _tbl(["节点", "中文", "出期望影响", "入期望影响"], _RVG["EL_EI"])

body = sec("what", "这一页是什么", f"""
<p>课文里的网络分析都用模拟数据，因为只有模拟数据才有已知的“真实结构”可供对照。这一页用一份公开的真实追踪面板数据走完<b>同一套流程</b>：智利社会纵向研究（ELSOC）里抑郁症状的 8 道题，从 {_y1} 预测 {_y2}。方法就是课程主线的“仅 LASSO”CLPN（{L("7.1", "7.1")}–{L("7.4", "7.4")}），外加 200 次的边权重 bootstrap（{L("8.2", "8.2")}）。</p>
<p>建议学完 7.4 和 8.2 再看。它不是新方法，而是一次对照：真实数据里没有“标准答案”，你只能说数据支持什么、不支持什么。</p>
<div class="box key"><b class="bt">数字从哪里来</b><p>下面所有人数、系数和区间都在构建网站时从 <code>R/output/data_elsoc_log.txt</code> 和 <code>case_elsoc_*.csv</code> 读入，对应脚本 <code>R/data_elsoc.R</code>、<code>R/case_elsoc.R</code>（种子 2026）。不要把这些数字抄进你自己的论文；你的样本、你的种子，数字会不同。</p></div>""")

body += sec("data", "数据", f"""
<p>来源：Reproducible Research, Centre for Social Conflict and Cohesion Studies COES (2022). <i>Estudio Longitudinal Social de Chile 2016-2021</i>. Harvard Dataverse, {{V:el_version}}. <a href="https://doi.org/{{V:el_doi}}">https://doi.org/{{V:el_doi}}</a>, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]。Dataverse 页面把这一版标为 CC0 1.0，可以再分发。</p>
<p>课程附带两份文件，仓库和 <code>clpn-course.zip</code> 里都有：原始文件 <code>data/elsoc/{{V:el_file}}</code>（与 Dataverse 上的 V1 逐字节相同，MD5 <code>{{V:el_md5}}</code>），以及由 <code>R/data_elsoc.R</code> 从它写出的分析文件 <code>data/elsoc_phq8_wide.csv</code>（原始样本，三波 PHQ-8 加性别、年龄，共 27 列）。做案例只需要：</p>
<div class="codeblk"><pre><code class="language-r">source("R/case_elsoc.R")   # CLPN 与 {{V:el_boot_n}} 次 bootstrap，约 1–2 分钟</code></pre></div>
<p>想核对预处理，可以运行 <code>source("R/data_elsoc.R")</code>：它读附带的原始文件（文件不在时才从 Dataverse 下载），重新写出分析文件，结果应与课程附带的文件相同。不需要联网。</p>
<h3>预处理做了什么</h3>
<ul>
<li>只用 2016 年招募的原始样本，不用 {{V:el_sup_when}} 才加入的补充样本（他们没有前两波）。</li>
<li>负数是缺失码（−999 / −888 / −777 / −666），全部改成 NA。不保留原始编号。</li>
<li>只保留 PHQ 的前 8 题，三波（{{V:el_y1}}、{{V:el_y2}}、{{V:el_y3}}）。</li>
</ul>
<div class="box warnbox"><b class="bt">为什么去掉第 9 题</b><p>第 9 题问的是“想到死亡或伤害自己”。这是需要临床跟进的高风险条目，不适合在教学练习里当成一个普通节点。研究中常用的 PHQ-8 就是去掉这一题的版本。脚本不导出第 9 题；请不要为了“凑齐 9 个节点”自己把它加回去。</p></div>
<p>另外两件读结果之前必须知道的事：</p>
<ul>
<li><b>计分不是临床常用的 0–3。</b>ELSOC 这 8 题是 1 = 从不 … 5 = 每天。8 题相加是 8–40，不是 PHQ-8 常见的 0–24。<b>不要用 10 分、20 分这类临床划界来解释这里的总分。</b></li>
<li><b>题号和标准 PHQ-9 不完全一样。</b>ELSOC 把标准卷的第 6 题（自我评价低）和第 7 题（注意力难集中）对调了。下表的中文按题目原文标注，不是按标准题号。节点叫 phq6 的，内容是注意力，不是“觉得自己很糟”。</li>
</ul>""")

body += sec("sample", "谁进了分析", f"""
<p>原始文件 {{V:el_n_raw}} 行 × {{V:el_n_col}} 列。原始样本 {{V:el_n_orig}} 人，补充样本 {{V:el_n_sup}} 人（不用）。原始样本中，PHQ-8 答完的人数：</p>
<div class="tablewrap"><table><thead><tr><th>波次</th><th>年份</th><th>这一波 8 题都答完</th></tr></thead><tbody>
<tr><td>1</td><td>{{V:el_y1}}</td><td>{{V:el_n_w1}}</td></tr>
<tr><td>2</td><td>{{V:el_y2}}</td><td>{{V:el_n_w2}}</td></tr>
<tr><td>3</td><td>{{V:el_y3}}</td><td>{{V:el_n_w3}}</td></tr>
</tbody></table></div>
<p>第 1–2 波都完整的有 {{V:el_n_w12}} 人。第 1–3 波都完整的有 <b>{{V:el_n}}</b> 人，案例的 CLPN 只用这 {{V:el_n}} 人（完整个案，不是多重插补）。其中女性 {{V:el_n_f}} 人（{{V:el_pct_f}}%），{{V:el_age_y}} 年年龄均值 {{V:el_age_m}}（标准差 {{V:el_age_sd}}，范围 {{V:el_age_lo}}–{{V:el_age_hi}}）。</p>
<p>从原始样本 {{V:el_n_orig}} 人收到三波都完整的 {{V:el_n}} 人，少掉的人未必和留下的人一样（{L("4.3", "4.3")}）。本页没有做流失比较。若写成论文，这一句必须补上：留下的人在第一波的症状上，和没有做完三波的人有没有差别。</p>""")

body += sec("desc", "症状有多常见", f"""
<p>下面是 {{V:el_n}} 名三波都完整者的题目均值（1–5 分）。疲乏最高，自我评价低最低；三年之间均值只挪了一点点。</p>
{desc}
<p>8 题相加（范围 8–40）：{{V:el_tot_y1}} 年均值 {{V:el_tot_m1}}，{{V:el_tot_y2}} 年 {{V:el_tot_m2}}，{{V:el_tot_y3}} 年 {{V:el_tot_m3}}。{{V:el_tot_y1}} 与 {{V:el_tot_y2}} 的总分相关 r = {{V:el_tot_r}}。间隔大约一年，总分只中等程度地稳定——题目层面的网络看的就是：这点稳定性具体落在哪几道题之间。</p>""")

body += sec("model", "估计的是哪一个模型", f"""
<p>和 {L("7.2", "7.2")} 的主分析相同，不是 7.5 的完整流程（没有 SEM 重估，没有跨时间等值约束）：</p>
<ul>
<li>每个 {{V:el_y2}} 的题目做一次 LASSO 回归，预测变量是全部 8 个 {{V:el_y1}} 的题目（{L("7.1", "7.1")} 的逐节点回归）。</li>
<li>进入回归前，题目在 <code>clpn_estimate()</code> 里做了 z 标准化。下面的 B 是<b>标准差单位</b>：0.10 意味着“T 的这道题高 1 个标准差，T+1 的那道题的预测值高 0.10 个标准差”，不是高 0.10 个原始分数点。</li>
<li>λ 用 10 折交叉验证的 <code>lambda.min</code>，种子 <code>set.seed(2026)</code>。这是课程的默认，也是假阳性较多的那一个（{L("7.2", "7.2")}、{L("7.5", "7.5")}）。</li>
<li>交叉滞后位置共 {{V:el_n_cell}} 个（8 × 7）。自回归另算，不画进图里。</li>
</ul>""")

if RV["el_top1_b"] == RV["el_top2_b"]:
    _top = "并列最强的两条是“{V:el_top1_from_zh}”→“{V:el_top1_to_zh}”，以及“{V:el_top2_from_zh}”→“{V:el_top2_to_zh}”，样本估计都是 {V:el_top1_b}。"
else:
    _top = "最强的是“{V:el_top1_from_zh}”→“{V:el_top1_to_zh}”（{V:el_top1_b}），其次是“{V:el_top2_from_zh}”→“{V:el_top2_to_zh}”（{V:el_top2_b}）。"
_neg_clause = "（这一次没有负边：非零的都是正的，其余被压成了 0）" if RV["el_n_neg"] == "0" else ""
_fig_neg = "这一次没有负的交叉滞后边，所以图上是蓝的。" if RV["el_n_neg"] == "0" else "红色的是负边。"
body += sec("edges", RV["el_y1"] + " → " + RV["el_y2"] + " 的边", f"""
<p>非零交叉滞后边 <b>{{V:el_n_cl}} / {{V:el_n_cell}}</b> 条，其中负边 {{V:el_n_neg}} 条{_neg_clause}。最大 |B| = {{V:el_max_b}}。边又多又小：lambda.min 在这个大样本上仍留下许多小边，与 7.5 课说的一致，交叉验证带来的假阳性不随 N 变大而消失。</p>
<p>{_top}读法与 {L("7.3", "7.3")} 相同：在 {{V:el_y1}} 年其余症状（包括“{{V:el_top1_to_zh}}”自己）都相同的人里，当年“{{V:el_top1_from_zh}}”高 1 个标准差的人，下一年“{{V:el_top1_to_zh}}”的预测值大约高 {{V:el_top1_b}} 个标准差。<b>这是预测，不是“{{V:el_top1_from_zh}}导致了{{V:el_top1_to_zh}}”。</b></p>
{top}
<p class="muted">上表是样本估计绝对值最大的 {{V:el_top_n}} 条。区间是 {{V:el_boot_n}} 次个案重抽样的 2.5% 与 97.5% 分位数；最后一列是这 {{V:el_boot_n}} 次里该系数被 LASSO 压成 0 的比例。正式报告不要用 {{V:el_boot_n}} 次，见下面“bootstrap”。</p>
<figure><img src="../R/output/case_elsoc_clpn.png" alt="ELSOC PHQ-8 的交叉滞后网络，蓝色箭头表示正向预测" loading="lazy"><figcaption>图：<code>R/output/case_elsoc_clpn.png</code>。只画交叉滞后边，自回归没有画。colorblind 主题，与全课一致：蓝色 = 正，红色 = 负。{_fig_neg}</figcaption></figure>
<h3>自回归：哪道题最“稳”</h3>
<p>对角线是“今年的这道题预测明年的同一道题”（已控制其他 7 题）。最高的是“{{V:el_ar_hi_zh}}”（{{V:el_ar_hi}}），最低的是“{{V:el_ar_lo_zh}}”（{{V:el_ar_lo}}）。最低的那一道几乎没有独特的自回归，下一年的高低更多是被其他症状预测的（下面的入期望影响会再看到这一点）。</p>
{ar}""")

body += sec("ei", "出 / 入期望影响", f"""
<p>只加交叉滞后边，不含自回归（与 {L("7.4", "7.4")} 相同）。出期望影响最高的是“{{V:el_out_top_zh}}”（{{V:el_out_top_v}}），入期望影响最高的是“{{V:el_in_top_zh}}”（{{V:el_in_top_v}}）。<b>最能预测别人的，和最容易被别人预测的，不是同一个节点。</b></p>
{ei}
<div class="box warnbox"><b class="bt">不要据此决定先干预谁</b><p>本案例<b>没有</b>做个案删除 bootstrap，<b>没有</b> CS 系数（{L("8.3", "8.3")}）。上表只是这一次样本上的加权出度 / 入度。不能说“情绪低落是核心症状”，也不能说“应优先干预情绪低落”。即便以后补上稳定性，排序第一也只是预测关系较强，干预是否有效要另做研究（{L("9.2", "9.2")}、{L("10.1", "10.1")}）。</p></div>""")

body += sec("again", "换一段时间、加两个协变量", f"""
<h3>用 {{V:el_rep_y1}} → {{V:el_rep_y2}} 再做一次</h3>
<p>同一批人、同一种设定。非零交叉滞后边 {{V:el_n_cl_rep}} / {{V:el_rep_den}} 条。与 {{V:el_y1}} → {{V:el_y2}} 在全部 {{V:el_rep_den}} 个交叉滞后位置上（含被压成 0 的）的相关 r = {{V:el_rep_r}}。样本里最强的 8 条里，有 {{V:el_rep_same}} 条在下一段仍为同方向且非零。</p>
<p>r = {{V:el_rep_r}} 是中等，不是“结构复现了”。一年后再看，大的方向有一部分还在，细的边换了很多。写的时候就写这个相关和这 {{V:el_rep_same}} 条，不要写“结果在两段时间上一致”。</p>
<h3>加上性别和年龄（不惩罚）</h3>
<p>在三波都完整、并且性别与年龄也不缺的 {{V:el_n_sens}} 人上，把这两项作为协变量放进每个回归，<code>penalty.factor = 0</code>（不参与收缩，系数本身不画进网络）。非零交叉滞后边 {{V:el_n_cl_sens}} / {{V:el_sens_den}} 条，与主分析在全部交叉滞后位置上的相关 r = {{V:el_r_sens}}。</p>
<p>边的<b>格局</b>几乎没变。这只能说明“在这个样本里，控制性别和年龄之后，题目之间的预测关系还在”，不能说明已经控制住了所有混杂（{L("5.4", "5.4")}）。没测的东西（收入、躯体疾病、社会支持）仍然可以同时推高今年的疲乏和明年的食欲改变。</p>""")

body += sec("boot", "这 200 次 bootstrap 说明什么、不说明什么", f"""
<p>第 6 步是非参数 bootstrap：有放回地抽取 {{V:el_n}} 人，重复 {{V:el_boot_n}} 次，每次都重新做 10 折 CV 的 LASSO。这是 {L("8.2", "8.2")} 的思路，但是<b>手写的、而且只有 {{V:el_boot_n}} 次</b>，不是课程主分析用的 bootnet 1000 次。脚本里把 <code>B_BOOT</code> 改成 1000，大约再要几分钟；写论文请用至少 1000 次。</p>
<p>最强 {{V:el_top_n}} 条里，区间不含 0 的有 {{V:el_top_excl0}} 条。读这句之前先记住三件限制：</p>
<ol>
<li>这 {{V:el_top_n}} 条是<b>先看了样本估计再挑出来的</b>，不是分析前登记的假设。挑完再报“{{V:el_top_excl0}} / {{V:el_top_n}} 不含 0”，比事先指定一条边更容易显得“都显著”。</li>
<li>{{V:el_boot_n}} 次重抽样时，“被压为 0 的比例”这类数只能以 1/{{V:el_boot_n}} 为单位变化。这是<b>分辨率</b>，不是精度。精度要看蒙特卡罗误差：用 B 次重抽样估计一个真实值为 p 的比例，标准误约为 √(p(1 − p) / B)，B = 200、p = 0.05 时约 0.015，是分辨率 0.005 的三倍。区间端点同样不稳：200 次时，2.5% 和 97.5% 分位数各只由最外侧约 5 个重抽样结果决定，换一次种子就可能明显挪动。它也没有做 {{V:el_n_cell}} 条边的多重比较校正（校正会怎样把 p 值抬上去，见 {L("7.7", "7.7")}）。</li>
<li>区间不含 0，只表示“这个预测系数没有被重抽样轻易压没”。它仍然不是因果，也不是 CS 系数。</li>
</ol>""")

body += sec("limits", "写成报告时，至少写上这些局限", """
<ul>
<li><b>标准 CLPN 把被试间和被试内混在一起</b>（""" + L("5.3", "5.3") + """、""" + L("7.5", "7.5") + """）。边里有一部分可能只是“长期更抑郁的人，每道题都更高”，不是“这个人今年比自己平时更情绪低落，所以明年兴趣更差”。</li>
<li><b>完整个案</b>。三波都答完的人和中途缺失的人可能不同，本页没有比较。</li>
<li><b>只有 lambda.min</b>，没有 SEM 重估。{{V:el_n_cl}} 条非零边里会有假阳性。</li>
<li><b>未检验测量不变性</b>（""" + L("7.6", "7.6") + """用课程模拟数据和教练数据演示了做法，本案例未对 ELSOC 检验）。不能默认 2016 年的“疲乏”和 2018 年的“疲乏”是同一把尺子。</li>
<li><b>间隔约一年</b>，看不到几周之内的起伏。量表是 1–5 的频率题，总分不能对临床划界。</li>
<li><b>一个国家、一个年代的社区样本</b>。不能写成“抑郁症状一般都是这样互相预测的”。</li>
</ul>
<p>可借用的句式在<a href="writing.html">写作工作坊</a>的“结果”和“局限”两节。想对照别人怎么写真实数据，见<a href="reading.html">论文阅读包</a>里的 Funkhouser 等（2021）和 Grygiel 等（2026）。</p>""")

body += sec("quiz", "读完检查", Q("""Q: 为什么这个案例不用 PHQ 的第 9 题？
- 第 9 题缺失太多，放进网络会让 LASSO 报错 || 脚本是因为内容把它排除的，不是因为缺失率。
+ 第 9 题问的是想到死亡或伤害自己，不适合当作教学里的普通节点；PHQ-8 本身也不含这一题 || 对。分析文件里也没有这一题，请不要自己从原始数据加回去。
- 第 9 题是反向计分，标准化之后符号会反 || 案例没有说它反向计分。
- 9 个节点太多，8 个才算得动 || 课程模拟数据就是 9 个节点。
H: 和临床风险、而不是和样本量有关。
E: 见本节“数据”。研究里常用的 PHQ-8 就是去掉这一题。""") + Q("""Q: “情绪低落 → 兴趣减退”的 B = {{V:el_top1_b}}，下面哪句可以说？
- 情绪低落导致了下一年的兴趣减退 || “导致”是因果语言。CLPN 没有排除未测量的混杂，也没有分开被试间和被试内。
- 兴趣减退是最应该优先干预的症状，因为它的入期望影响最高 || 入期望影响高只表示“易被其他题预测”。本页没有 CS 系数，也不能从中心性推出干预靶点。
+ 在控制了第一年其余症状之后，第一年情绪低落较高的人，下一年兴趣减退的预测值略高；这是预测关系 || 对。还要写上区间、标准化单位，以及这不是因果。
- 因为 bootstrap 区间不含 0，所以这条边在总体里一定不为 0 || {{V:el_boot_n}} 次、又是事后挑出的边，不能说“一定”。
H: 课程允许的动词是“预测”，不是“导致”或“应当干预”。
E: 见 """ + L("5.4", "5.4") + """、""" + L("7.3", "7.3") + """、""" + L("9.2", "9.2") + """。""") + Q(f"""Q: 三波 PHQ-8 都答完、进入这次 CLPN 的有多少人？（填整数）
N: {{{{V:el_n}}}} | 0
H: 不是原始文件的行数，也不是原始样本的人数。
E: {{V:el_n}} 人。原始样本有 {{V:el_n_orig}} 人，三波都完整的才进入网络。见“谁进了分析”。""") + Q(f"""Q: {{V:el_y1}} → {{V:el_y2}} 的非零交叉滞后边有多少条？（填整数）
N: {{{{V:el_n_cl}}}} | 0
H: 分母是 {{V:el_n_cell}} 个交叉滞后位置。自回归不算在内。
E: {{V:el_n_cl}} 条，其中负边 {{V:el_n_neg}} 条。边多而小，和 lambda.min 的假阳性有关，见 """ + L("7.5", "7.5") + """。"""))

body += sec("do", "你自己跑的时候", """
<ol>
<li>用 <code>clpn-course.Rproj</code> 打开项目，运行 <code>source("R/case_elsoc.R")</code>。</li>
<li>对照 <code>R/output/case_elsoc_log.txt</code> 和本页。同一 R、同一套包、种子 2026 时，系数应与本页一致；你若改了 <code>B_BOOT</code> 或 R 版本，区间可以略有不同。</li>
<li>用这份数据写东西时，按上面“数据”一节的格式引用 ELSOC。</li>
</ol>
<p>变量含义、许可和引用格式也写在<a href="../data/data_dictionary.html">数据字典</a>最后一节。</p>""")

page("case_elsoc.html", "真实数据案例：ELSOC 的抑郁症状网络",
     fill_all("<p>用公开的 ELSOC 抑郁症状追踪数据演示课程主线的“仅 LASSO”CLPN。配套分析文件随课程提供，运行 <code>R/case_elsoc.R</code> 即可复现本页结果。</p>"),
     fill_all(body))
