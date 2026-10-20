# 数据字典与生成模型说明 Data dictionary & data-generating model

文件：`clpn_sim_wide.csv`（同内容 `clpn_sim_wide.sav`）。由 `data/simulate_data.R` 生成（种子 `set.seed(20261016)`），**纯模拟数据，不含任何真实个人信息**。

- 样本：N = 800 名成人（18–85 岁社区样本），3 波（T1/T2/T3），**波次间隔 6 个月**（T1 → T2 → T3 共一年），宽格式（每人一行），无缺失（缺失/流失练习见 `R/L4-3.R`）
- 节点（9 题）：孤独 `lone1–lone4`（1–4 分，仿 UCLA-3）；抑郁 `dep1–dep5`（0–3 分，仿 PHQ-9，右偏）
- 列名规则：`题目_t波次`，例如 `dep3_t2` = 第 2 波的“睡眠问题”
- 变量逐一说明见 `data_dictionary.csv`（中英双语）

| 变量 | 中文 | English | 取值 |
|---|---|---|---|
| lone1 | 缺少陪伴 | lack companionship | 1 从不 – 4 经常 |
| lone2 | 被冷落 | feel left out | 1–4 |
| lone3 | 与人隔绝 | feel isolated | 1–4 |
| lone4 | 无人理解 | no one understands me | 1–4 |
| dep1 | 情绪低落 | depressed mood | 0 完全不会 – 3 几乎每天 |
| dep2 | 兴趣丧失 | anhedonia | 0–3 |
| dep3 | 睡眠问题 | sleep problems | 0–3 |
| dep4 | 疲乏 | fatigue | 0–3 |
| dep5 | 无价值感 | worthlessness | 0–3 |
| gender | 性别 | gender | 0 男 / 1 女 |
| age | 年龄 | age | 18–85 |
| social_support_t1 | 社会支持 | social support | 1–5 |
| sleep_hours_t1 | 睡眠时长 | sleep hours | 3–11 |
| life_sat_t1 | 生活满意度 | life satisfaction | 0–100 |
| help_seek_t2 | T2 是否求助 | sought help at T2 | 0/1 |

## 生成模型（“真实答案”）

1. **被试内滞后结构** `true_B_within.csv`：`B[k, j]` = T 时刻题目 k → T+1 时刻题目 j。自回归 0.35（孤独）/0.30（抑郁）。交叉滞后边：
   - 孤独 → 抑郁：lone3→dep1 0.18，lone1→dep2 0.14，lone4→dep5 0.12
   - 抑郁 → 孤独：dep2→lone3 0.12，dep4→lone2 −0.15（负边，用于 EI 与强度对比）
   - 构念内：dep3→dep4 0.16，dep1→dep5 0.10，lone2→lone4 0.10
2. 同期残差相关：同构念内 0.35，跨构念 0.15；T1 取自平稳分布。
3. **稳定特质（随机截距）**：孤独特质与抑郁特质相关 0.50，每题特质方差 ≈ 0.45（被试内方差 = 1）；女性抑郁题 +0.2。
4. 连续得分按阈值切分为李克特等级。

**CLPN 应该找回什么？** 由于特质与等级化，观测数据上的 CLPN 目标不是被试内 B，而是 `true_B_population.csv`：在 20 万人的同模型大样本中，用标准化 T1 题目对每个 T2 题目做 OLS 得到的总体系数。其中构念内约 0.05–0.07 的小边来自稳定特质（被试间混淆），这正是 7.5 / 5.3 课讨论的局限。

## 附：真实数据 `coaches_mhc_raw.csv`（7.6 课的测量不变性练习）

这一份**不是**模拟数据，而是公开的真实研究数据，按原样收录（没有改动任何字节）。只用于 7.6 课的测量不变性练习，参考答案见 `R/solutions/L7-6_solution.R`，下面的核对数字都来自它的日志 `R/output/sol_L7-6_log.txt`。

- **来源**：Ackeret, N., Röthlin, P., Horvath, S., & Allemand, M. (2023). *Positive mental health among sports coaches: A six-month longitudinal study* [数据集，第 3 版]. Dryad. https://doi.org/10.5061/dryad.8931zcrws 。原文件名 `PMH_Coaches_data.csv`（63,813 字节，MD5 `c89921f505a473ab4084b761fb5567e6`）。相关论文：*Sport, Exercise, and Performance Psychology*, 13(1), 76–88（2024），https://doi.org/10.1037/spy0000335 。
- **许可**：CC0 1.0（公共领域贡献），可以自由再分发；课程照常注明出处。见 `LICENSE` 与 `THIRD_PARTY_NOTICES.md`。
- **样本**：瑞士的体育教练，3 波。第 1 波 422 人，第 2 波 301 人，第 3 波 259 人（后两波是流失，不是抽样）。数据里**没有**人口学变量（作者为了匿名删去了），所以不能做性别等分组比较。
- **读入**：分号分隔，小数点是“.”，缺失是空格子。R 里用 `read.csv2("data/coaches_mhc_raw.csv", dec = ".")`，得到 422 行 × 60 列。

### 变量

| 变量 | 含义 |
|---|---|
| `t1w1` … `t1w14`、`t2w1` … `t2w14`、`t3w1` … `t3w14` | 第 1、2、3 波的 MHC-SF 14 题（心理健康连续体简版 Mental Health Continuum–Short Form；Keyes, 2009）。**只用这些列** |
| `t1emowb`、`t1socwb`、`t1psywb`、`t1wbtot`（t2、t3 同理） | 原作者算好的情绪 / 社会 / 心理幸福感均值和总均值。**与题目列对不上，不要用**（见下文“已知问题”） |
| `t1_WB_cont`、`t2_WB_cont`、`t3_WB_cont` | 原作者算好的连续总分（按 0–5 计分求和，范围 0–70） |
| `dropout` | 是否流失：0 = 否，1 = 是 |
| `t2_missing`、`t3_missing` | 这一波是否缺失：FALSE = 有数据，TRUE = 缺失 |

题目问的是“过去一个月里，你有多常感到……”，计分 1 = 从不，2 = 一两次，3 = 大约每周一次，4 = 每周两三次，5 = 几乎每天，6 = 每天。

| 分量表 | 题号 | 内容（意译） |
|---|---|---|
| 情绪幸福感 emotional well-being | w1–w3 | 快乐、对生活感兴趣、对生活满意 |
| **社会幸福感 social well-being**（7.6 练习用） | **w4–w8** | 觉得自己能为社会做出重要贡献、属于某个社群（如邻里、社团）、社会正在变好、人基本上是善良的、社会的运作方式说得通 |
| 心理幸福感 psychological well-being | w9–w14 | 喜欢自己的性格、能处理日常责任、有温暖信任的人际关系、经历促使自己成长、敢于表达自己的想法、生活有方向和意义 |

社会幸福感和社会工作关系最密切：社区归属、社会贡献、对他人的信任，正是社区工作和社会融入服务关心的内容。

### 已知问题（请如实写进你的练习报告）

1. **波次间隔前后矛盾。** 数据集的摘要和说明文件都写“基线、3 个月后、6 个月后”，但 Methods 一节又写“baseline, month 6 and month 12”。我们没有联系作者核实，所以**只用这份数据检验“前后测的是不是同一个东西”（测量不变性），不解读变化的快慢**，也不把它用来做 CLPN。
2. **自带的分量表列和题目列对不上。** 用题目重新计算的均值与自带列的相关（应接近 1）：

   | 波次 | 情绪（w1–3） | 社会（w4–8） | 心理（w9–14） | `*_WB_cont` 与 14 题之和 |
   |---|---|---|---|---|
   | T1 | 0.90 | 0.15 | 0.18 | 0.97 |
   | T2 | 0.35 | 0.22 | 0.25 | 1.00 |
   | T3 | 0.30 | 0.09 | 0.22 | 1.00 |

   T2、T3 的 `*_WB_cont` 对所有人都恰好等于“14 题之和 − 14”，T1 只有 89 / 420 人如此。题目列本身是前后一致的：14 题总分的跨波相关 T1–T2 = 0.73，T2–T3 = 0.76，T1–T3 = 0.73。原因不明，所以课程**只用题目列自己计算**。这也是一个真实的教训：拿到别人的数据，先核对汇总列能不能从原始题目算出来。
3. **说明文件写“只收录完整作答的人”**，但第 1 波有 2 人没有答完 14 题（14 题全部作答：T1 420 人，T2 301 人，T3 259 人）。练习用 FIML（`missing = "ml"`）处理缺失，422 人全部进入模型。

## 附：ELSOC（真实数据案例）

[真实数据案例](../materials/case_elsoc.html) 用智利社会纵向研究（ELSOC）2016–2018 年的抑郁症状，做课程主线的“仅 LASSO”CLPN。分析文件 `data/elsoc_phq8_wide.csv` 随课程提供（仓库和 `clpn-course.zip` 里都有）。人数、系数和区间写在案例页上，构建时从 `R/output/data_elsoc_log.txt` 与 `case_elsoc_*.csv` 读取，这里不手抄。

- **来源**（Harvard Dataverse 推荐的引用格式）：Reproducible Research, Centre for Social Conflict and Cohesion Studies COES, 2022, "Estudio Longitudinal Social de Chile 2016-2021", https://doi.org/10.7910/DVN/LQMURF , Harvard Dataverse, V1, UNF:6:z/vWFguq9fg03YaOLWFddA== [fileUNF]。用到这份数据时请照此引用。
- **许可**：Dataverse 将这一版标为 CC0 1.0，可以再分发。课程同时附带原始文件和预处理后的子集，下载 Dataverse 出问题时也能离线完成案例。
- **原始文件**：`data/elsoc/ELSOC_Wide_2016_2021_v1.00_R.RData`（V1，4.8 MB，1848 列），与 Dataverse 上的文件逐字节相同（MD5 `a5a45571d39cf9db12e1949fdcb6fff2`）。它含有全部问卷变量，也包括本案例不用的 PHQ 第 9 题（见下文“使用前要知道的三件事”第 1 条）。
- **怎么来的**：`R/data_elsoc.R` 读原始文件（不在时从 Dataverse 下载，并用 MD5 校验），写出 `data/elsoc_phq8_wide.csv`。做案例不需要运行它，想核对预处理时再运行。
- **怎么跑**：`source("R/case_elsoc.R")`，约 1–2 分钟。`run_all.R` 会依次运行这两个脚本。

### 分析文件 `data/elsoc_phq8_wide.csv`

只含原始样本（2016 年招募）。列是脚本规定的，不是原始问卷的全部变量：

| 列 | 含义 |
|---|---|
| `id` | 新编号（1, 2, …）。**不是** ELSOC 的原始编号 |
| `female` | 1 = 女，0 = 男（由第一波性别题转来；缺失为 NA） |
| `age` | 2016 年的年龄 |
| `phq1_t1` … `phq8_t3` | 三波各 8 题。1 = 从不 … 5 = 每天。负数缺失码已改成 NA |

### 使用前要知道的三件事

1. **没有第 9 题。** 标准 PHQ-9 的第 9 题问“想到死亡或伤害自己”，需要临床跟进，不适合当作教学里的普通节点。研究中常用的 PHQ-8 也不含这一题。脚本不导出它，请不要自己加回去。
2. **计分不是 0–3。** 这里是 1–5 的频率题，8 题相加是 8–40，不是临床 PHQ-8 常见的 0–24。不要用 10 分、20 分这类划界来解释总分。
3. **题号与标准 PHQ-9 有一处对调。** ELSOC 把标准卷的第 6 题（自我评价低）和第 7 题（注意力难集中）对调了。案例页和脚本里的中文按题目原文标注：`phq6` 是注意力，`phq7` 是自我评价低。
