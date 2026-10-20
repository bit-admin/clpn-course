# -*- coding: utf-8 -*-
# M2 阶段测验：R 基础（第 5 周，与 M1 一起做）。不需要现场运行 R，读代码作答即可。
LEAD = "<p>学完 2.1–2.6 后做（标准节奏第 5 周，与 M1 阶段测验一起）。8 道自动判分题 + 1 道简答，约 15 分钟。题目只需要读代码，不需要运行 R；做完可以在 RStudio 里自己验证。</p>"
ITEMS = [
dict(obj="2.1-3", q="""Q: 在 R 里依次运行 <code>x &lt;- 5</code> 和 <code>x &lt;- x * 2 + 1</code>，现在 <code>x</code> 的值是多少？
N: 11 | 0
H: <code>&lt;-</code> 把右边算出来的结果存进左边的名字。第二行用的是 x 原来的值 5。
E: 5 × 2 + 1 = 11，结果再存回 x。赋值与对象见 <a href="../lessons/L2-1.html">2.1</a>。"""),
dict(obj="2.2-1", q="""Q: <code>scores &lt;- c(3, 8, 5, 10)</code>，那么 <code>scores[3]</code> 是多少？
N: 5 | 0
H: R 的位置从 1 开始数。
E: 第 3 个元素是 5。R 从 1 开始计数（有些语言从 0 开始），见 <a href="../lessons/L2-2.html">2.2</a>。"""),
dict(obj="2.2-3", q="""Q: <code>dep &lt;- c(2, NA, 4)</code>。运行 <code>mean(dep)</code> 的结果是什么？
- 3 || 默认情况下，R 不会自动跳过缺失值。
+ NA || 对。只要有一个 NA，默认的平均数就是 NA；要用 <code>mean(dep, na.rm = TRUE)</code> 才会得到 3。
- 2 || 不是。
- 报错，程序停止 || 不会报错，只会返回 NA。
E: NA 表示缺失，<code>na.rm = TRUE</code> 告诉函数先去掉缺失值再计算，见 <a href="../lessons/L2-2.html">2.2</a>。"""),
dict(obj="2.2-2", q="""Q: 数据里性别存成了 <code>"男"</code>、<code>"女"</code> 两种文字。在 R 里，最适合用哪种数据类型表示这种分类变量？
- 数值（numeric） || 文字不是数值。
- 逻辑（logical） || 逻辑型只有 TRUE / FALSE。
+ 因子（factor） || 对。因子专门用来存“有固定几个类别”的变量。
- 函数（function） || 函数不是数据类型的选择。
E: 数值、字符、逻辑、因子等类型见 <a href="../lessons/L2-2.html">2.2</a>。"""),
dict(obj="2.3-1", q="""Q: 课程数据 <code>clpn_sim_wide.csv</code> 读进 R 后，<code>dim(dat)</code> 显示 <code>800 34</code>。这两个数分别表示什么？
+ 800 行（800 个人）、34 列（34 个变量） || 对。数据框是“行 = 个案、列 = 变量”。
- 800 个变量、34 个人 || 方向反了。
- 800 道题、34 个波次 || 不是。
- 平均分 800、标准差 34 || dim() 给的是维度，不是统计量。
E: 数据框的结构见 <a href="../lessons/L2-3.html">2.3</a>。"""),
dict(obj="2.3-2", q="""Q: 想从数据框 <code>dat</code> 中只保留女性（<code>gender == 1</code>）。用 dplyr 应该写哪一个？
- <code>dat |&gt; select(gender == 1)</code> || select() 是选“列”，不是选“行”。
+ <code>dat |&gt; filter(gender == 1)</code> || 对。filter() 按条件选“行”。
- <code>dat |&gt; mutate(gender = 1)</code> || 这会把所有人的性别都改成 1。
- <code>dat |&gt; summarise(gender == 1)</code> || summarise() 用来汇总统计量。
E: select 选列、filter 选行、mutate 新建或修改列、summarise 汇总，见 <a href="../lessons/L2-3.html">2.3</a>。注意判断“等于”要用两个等号 <code>==</code>。"""),
dict(obj="2.4-1", q="""Q: 你昨天已经运行过 <code>install.packages("glmnet")</code>。今天重新打开 RStudio，要使用 glmnet，应该运行哪一行？
- 再运行一次 <code>install.packages("glmnet")</code> || 安装只需要一次，重复安装浪费时间。
+ <code>library(glmnet)</code> || 对。每次新开 R 都要加载一次。
- 什么都不用做，昨天的已经加载好了 || 关掉 R 以后，加载的包就失效了。
- <code>source("glmnet")</code> || source() 是运行一个脚本文件。
E: install.packages() 安装一次，library() 每次加载，见 <a href="../lessons/L2-4.html">2.4</a>。"""),
dict(obj="2.4-3", q="""Q: 同学把你的课程文件夹拷到自己电脑上，脚本里的 <code>read.csv("C:/Users/小张/Desktop/data/clpn_sim_wide.csv")</code> 就报错了。最好的改法是？
- 让同学也把用户名改成“小张” || 不现实。
+ 打开 <code>clpn-course.Rproj</code>，用相对路径 <code>read.csv("data/clpn_sim_wide.csv")</code> || 对。项目会把工作目录设在课程文件夹，相对路径在任何电脑上都能用。
- 把数据复制到桌面 || 下次换电脑还会出问题。
- 不用 CSV，改用截图 || 不行。
E: RStudio Project 与相对路径，是“别人拿到也能运行”的前提，见 <a href="../lessons/L2-4.html">2.4</a>。"""),
]
SHORT = [
dict(obj="2.1-4", q="<p>你运行 <code>read.csv(\"data/my_survey.csv\")</code> 时出现报错：<code>cannot open file 'data/my_survey.csv': No such file or directory</code>。请写一条发到 R 论坛或学习群里的求助消息（4–6 句），要让从没见过你电脑的人不用来回追问就能帮你找到问题。</p>",
     answer="<p>示例：“你好，我在运行 R/L2-4.R 第 12 行 <code>read.csv(\"data/my_survey.csv\")</code> 时报错：cannot open file 'data/my_survey.csv': No such file or directory。我是双击 clpn-course.Rproj 打开的项目，<code>getwd()</code> 显示 ……/clpn-course。data 文件夹里有 clpn_sim_wide.csv，但我刚刚发现 my_survey.csv 放在了下载文件夹里。我已经试过把文件名重新输入一遍。请问应该把文件放在哪里？我的 R 版本是 4.5.0（下面贴了 <code>sessionInfo()</code> 的文字输出）。”</p><p>要点：说清楚运行的是哪一行代码、完整的报错原文、自己已经检查过什么（工作目录、文件是否在那个位置）、软件版本。</p>",
     rubric=[(3, "包含运行的代码、完整报错原文、已做过的检查（如 getwd()、文件位置）和软件版本，读者可以直接定位问题"),
             (2, "有代码和报错，但缺少已做过的检查或环境信息"),
             (1, "只说“读数据报错了怎么办”，没有代码或报错原文"),
             (0, "没有作答")]),
]
