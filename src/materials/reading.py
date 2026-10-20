# -*- coding: utf-8 -*-
# 论文阅读包 materials/reading.html。只放链接（DOI），不放 PDF。
# 每条 DOI 于 2026-10-18 用 api.crossref.org/works/<doi> 核对过题名、期刊、卷期页和作者；更换条目时请重新核对。
# 例外：Wysocki et al. (2025) 的 Crossref 记录漏了第 5 作者 Rhemtulla（期刊网页上有，且是通讯作者），按期刊网页写。
READING = [
 ("入门：CLPN 是什么", [
  ("Wysocki, A., McCarthy, I., van Bork, R., Cramer, A. O. J., &amp; Rhemtulla, M. (2025). Cross-lagged panel networks. <i>advances.in/psychology, 2</i>, e739621.", "10.56296/aip00037", "CC BY 4.0，开放获取",
   "作者为什么说 CLPN 的边是“回归系数”而不是“相关”？自回归边和交叉滞后边分别回答什么问题？", ["7.1", "7.2"]),
  ("Epskamp, S., Borsboom, D., &amp; Fried, E. I. (2018). Estimating psychological networks and their accuracy: A tutorial paper. <i>Behavior Research Methods, 50</i>(1), 195–212.", "10.3758/s13428-017-0862-1", "CC BY 4.0，开放获取",
   "边权重 bootstrap 和个案删除 bootstrap 各回答什么问题？CS 系数 0.25 和 0.5 这两条线是怎么来的？", ["8.2", "8.3"]),
 ]),
 ("实证范例：怎样把 CLPN 写成论文", [
  ("Funkhouser, C. J., Chacko, A. A., Correa, K. A., Kaiser, A. J. E., &amp; Shankman, S. A. (2021). Unique longitudinal relationships between symptoms of psychopathology in youth: A cross-lagged panel network analysis in the ABCD study. <i>Journal of Child Psychology and Psychiatry, 62</i>(2), 184–194.", "10.1111/jcpp.13256", "订阅期刊（可通过学校图书馆获取）",
   "作者怎样处理 T1→T2 与 T2→T3 两段的复现？他们用了哪些稳定性指标？结论部分有没有避免因果语言？", ["9.1"]),
  ("Grygiel, P., Opozda-Suder, S., &amp; Dolata, R. (2026). The longitudinal interplay between loneliness and depressive symptoms during late childhood: Cross-lagged panel network analyses. <i>European Journal of Investigation in Health, Psychology and Education, 16</i>(6), 78.", "10.3390/ejihpe16060078", "CC BY 4.0，开放获取",
   "样本来自 NLSY79 儿童与青年调查（NLSY79-CY），N = 4,333 名 10–12 岁儿童，只有两个时间点。孤独与抑郁的题目层面关系，和课程模拟数据的结构有什么相同和不同？只有两波数据，作者能检验和不能检验什么（比如能否做 T2→T3 复现）？样本年龄段会怎样影响结论的推广？", ["9.1", "10.3"]),
  ("Fried, E. I., Papanikolaou, F., &amp; Epskamp, S. (2022). Mental health and social contact during the COVID-19 pandemic: An ecological momentary assessment study. <i>Clinical Psychological Science, 10</i>(2), 340–354.", "10.1177/21677026211017839", "CC BY 4.0，开放获取",
   "密集追踪（EMA）数据和三波面板数据回答的问题有什么不同？“被试内”的含义在这里怎样体现？", ["5.3", "7.5"]),
 ]),
 ("模型批评：被试内与被试间", [
  ("Hamaker, E. L., Kuiper, R. M., &amp; Grasman, R. P. P. P. (2015). A critique of the cross-lagged panel model. <i>Psychological Methods, 20</i>(1), 102–116.", "10.1037/a0038889", "订阅期刊",
   "为什么稳定的个人差异会让交叉滞后系数“看起来”有效应？RI-CLPM 加了什么？这对 CLPN 的解释意味着什么？", ["5.3", "7.5"]),
 ]),
 ("测量不变性（选修 7.6）", [
  ("Putnick, D. L., &amp; Bornstein, M. H. (2016). Measurement invariance conventions and reporting: The state of the art and future directions for psychological research. <i>Developmental Review, 41</i>, 71–90.", "10.1016/j.dr.2016.06.004", "订阅期刊",
   "形态、弱、强不变性分别约束什么？论文里通常怎样报告比较结果？", ["7.6"]),
  ("Cheung, G. W., &amp; Rensvold, R. B. (2002). Evaluating goodness-of-fit indexes for testing measurement invariance. <i>Structural Equation Modeling, 9</i>(2), 233–255.", "10.1207/S15328007SEM0902_5", "订阅期刊",
   "为什么不用卡方差异检验，而看 ΔCFI？ΔCFI ≤ 0.01 这条线的依据是什么？", ["7.6"]),
  ("Chen, F. F. (2007). Sensitivity of goodness of fit indexes to lack of measurement invariance. <i>Structural Equation Modeling, 14</i>(3), 464–504.", "10.1080/10705510701301834", "订阅期刊",
   "ΔRMSEA 和 ΔSRMR 的建议界值是多少？样本量会怎样影响这些界值？", ["7.6"]),
 ]),
 ("组间比较与样本量（选修 7.7、进阶）", [
  ("van Borkulo, C. D., van Bork, R., Boschloo, L., Kossakowski, J. J., Tio, P., Schoevers, R. A., Borsboom, D., &amp; Waldorp, L. J. (2023). Comparing network structures on three aspects: A permutation test. <i>Psychological Methods, 28</i>(6), 1273–1285.", "10.1037/met0000476", "订阅期刊",
   "网络比较检验（NCT）检验了哪三个方面？置换次数和多重比较校正应怎样设置？", ["7.7"]),
  ("Constantin, M. A., Schuurman, N. K., &amp; Vermunt, J. K. (2026). A general Monte Carlo method for sample size analysis in the context of network models. <i>Psychological Methods, 31</i>(3), 385–405.", "10.1037/met0000555", "APA 开放获取",
   "为什么网络模型的样本量要靠重复模拟来估计？“功效”在这里是怎样定义的？", ["7.6", "7.7"]),
 ]),
 ("报告规范", [
  ("Burger, J., Isvoranu, A.-M., Lunansky, G., Haslbeck, J. M. B., Epskamp, S., Hoekstra, R. H. A., Fried, E. I., Borsboom, D., &amp; Blanken, T. F. (2023). Reporting standards for psychological network analyses in cross-sectional data. <i>Psychological Methods, 28</i>(4), 806–824.", "10.1037/met0000471", "订阅期刊",
   "这份规范针对横断面网络；哪些条目可以直接用于 CLPN，哪些需要补充（例如时间间隔、自回归）？", ["9.3", "10.3"]),
 ]),
]
def _reading_body():
    out = sec("how", "怎么读", """<ul><li>本页<b>只给链接</b>（DOI），不提供 PDF。标“开放获取”的可直接下载；订阅期刊可通过学校图书馆获取，或在作者主页、预印本平台查找作者自存版本。</li>
<li>每篇附一个<b>阅读问题</b>和配套课程。先学完配套的课，再带着问题读；不需要读懂每一个公式，能用自己的话回答问题就够了。</li>
<li>读完在<a href="study_log.html">学习日志</a>里写三句话：这篇回答了什么问题、用了什么方法、对我的毕业项目有什么启发。</li></ul>""")
    n = 0
    for gi, (h, items) in enumerate(READING):
        lis = ""
        for cite, doi, acc, q, les in items:
            n += 1
            lis += (f'<li><p>{cite} <a href="https://doi.org/{doi}">https://doi.org/{doi}</a>（{acc}）</p>'
                    f'<p><b>阅读问题：</b>{q}</p><p><b>配套课程：</b>{"、".join(L(i) for i in les)}</p></li>')
        out += sec(f"g{gi + 1}", h, f"<ol>{lis}</ol>")
    out += sec("more", "写论文时", '<p>写作练习见<a href="writing.html">写作工作坊</a>；课程引用的全部文献见<a href="../index.html#readings">课程大纲 · 参考文献</a>。</p>')
    return n, out
_n_read, _rb = _reading_body()
page("reading.html", "论文阅读包", f"<p>{_n_read} 篇精选论文，按主题分组，每篇附阅读问题和配套课程（提供 DOI 链接，标“开放获取”的可直接下载）。</p>", _rb)
