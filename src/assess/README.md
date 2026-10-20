# src/assess/：测评题库

每个文件对应一个测评页，由 `src/build_materials.py` 经 `src/common/assess.py` 生成 `materials/assess_<slug>.html`。
文件名（slug）和题数在 `src/common/assess.py` 的 `SPECS` 里：`pre`、`m0` … `m10`、`final`。题库文件不存在时，不生成对应页面。

```python
LEAD = "<p>页首导语（HTML）</p>"
INTRO = "<p>页首说明（HTML，可选）</p>"
ITEMS = [   # 自动判分题，正文格式与 ```quiz 宏相同（Q: / - / + / N: / T: / H: / E:）
  dict(obj="1.4-2", q="""Q: 题干
- 错误选项 || 反馈
+ 正确选项 || 反馈
E: 解释，用 <a href="../lessons/L1-4.html">1.4</a> 链回讲解的课"""),
  dict(obj="7.6-1", adv=True, q="""..."""),   # 进阶选学题（只在 m7），不计入 SPECS 的题数
]
SHORT = [   # 简答题：参考答案 + 0–3 级评分标准
  dict(obj="1.6-3", q="<p>题干</p>", answer="<p>参考答案</p>",
       rubric=[(3, "…"), (2, "…"), (1, "…"), (0, "…")]),
]
```

- `obj` 是“课号-目标序号”，对应 `src/data1–3.py` 里该课 `obj` 列表的第几条（从 1 数起）。
- 题目要新写，不要复制课内测验；`src/test/check_assess.py` 会查重。
- 不在这里写考核比重。比重只在 `src/template.html` 的 `#assessment` 表里。
- 按 `src/README.md` 的构建顺序重建，然后运行 `python3 src/test/check_assess.py --complete`（它读生成的课件页和 materials/，所以要在重建之后运行；13 个题库都已写完，所以总是加 `--complete`）。
- 题库文件不存在时不生成对应页面；删掉题库后重建会删除旧页面。测评总页 `materials/assessment.html` 自动列出全部测评，只链接已生成的页面。
- 可选的 `OUTRO`（HTML）放在题目之后，例如前测的“选择学习节奏”表。
- 期末 `final.py` 的额外写法：
  - `PARTS = [(part, 标题, 说明 HTML), ...]`：页面按部分分节；每道自动题写 `part="A"` 或 `part="C"`；`part == "short"` 的一节放 `SHORT`。
  - B 部分的简答用 `dims=[(维度, 分值, 本题要点), ...]`（4 个维度，合计 10 分）代替 `rubric`。
  - 引用课程运行结果时写 `{{V:键}}`（键在 `src/common/rvals.py`，期末专用的以 `fx_` 开头），不要手抄数字。
  - C 部分的答案用 `ANS["C1"]` … `ANS["C5"]`：来自 `R/output/assess_answers.csv`（由 `R/assess_answers.R` 生成）。题库执行时还可以用 `ROOT`。
