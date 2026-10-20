/* 学习日志：在页面填写，留在本浏览器，并下载 Markdown 或打印。 */
(function () {
  "use strict";
  const KEY = "clpn-study-log-v1";
  const daysHost = document.getElementById("slogDays");
  if (!daysHost) return;

  const DAY = [
    ["date", "日期", "date"],
    ["lesson", "课程", "lesson"],
    ["time", "用时", "text"],
    ["learned", "今天学到的三件事", "area"],
    ["unclear", "还不懂的地方", "area"],
    ["error", "遇到的 R 报错及解决办法", "area"],
    ["ask", "下一步想弄清的问题", "area"]
  ];
  const WEEK = [
    ["week", "第几周", "text"],
    ["done", "本周完成的课程", "area"],
    ["quiz", "测验正确率 / 练习完成情况", "area"],
    ["concept", "最有收获的一个概念（用自己的话解释一遍）", "area"],
    ["stuck", "仍然困惑的地方，以及打算怎样解决", "area"],
    ["sent", "本周完成并归档的练习", "area"],
    ["plan", "下周计划（对照学习指南的周计划）", "area"]
  ];
  const FEYN = [
    ["concept", "概念", "text"],
    ["tell", "用一段话讲给没学过统计的社工同事听", "area"],
    ["stuck", "我卡住的地方（说明还没真正理解）", "area"]
  ];

  function blank(fields) {
    const o = {};
    fields.forEach(function (f) { o[f[0]] = ""; });
    return o;
  }
  function nonempty(o) {
    return Object.keys(o).some(function (k) { return String(o[k] || "").trim(); });
  }
  function load() {
    try {
      const s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (s && Array.isArray(s.sessions) && Array.isArray(s.weeks) && Array.isArray(s.feynman)) return s;
    } catch (e) {}
    return null;
  }

  let data = load() || {
    name: "",
    sessions: [blank(DAY)],
    weeks: [blank(WEEK)],
    feynman: [blank(FEYN)]
  };
  if (!data.sessions.length) data.sessions.push(blank(DAY));
  if (!data.weeks.length) data.weeks.push(blank(WEEK));
  if (!data.feynman.length) data.feynman.push(blank(FEYN));

  const nameEl = document.getElementById("slogName");
  const weeksHost = document.getElementById("slogWeeks");
  const feynHost = document.getElementById("slogFeyn");
  nameEl.value = data.name || "";

  function listFor(id) {
    if (id === "slogDays") return data.sessions;
    if (id === "slogWeeks") return data.weeks;
    return data.feynman;
  }

  function field(spec, value) {
    const key = spec[0], label = spec[1], kind = spec[2];
    const lab = document.createElement("label");
    if (kind === "lesson") lab.className = "lesson";
    const span = document.createElement("span");
    span.textContent = label;
    lab.appendChild(span);
    let input;
    if (kind === "area") {
      input = document.createElement("textarea");
      input.rows = 3;
    } else {
      input = document.createElement("input");
      input.type = kind === "date" ? "date" : "text";
      if (kind === "lesson") input.setAttribute("list", "slogLessons");
      if (key === "time") input.placeholder = "例如 40 分钟";
      if (key === "week") input.placeholder = "例如 3";
      if (kind === "lesson") input.placeholder = "课号或课名，例如 1.4";
    }
    input.dataset.key = key;
    input.value = value || "";
    lab.appendChild(input);
    return lab;
  }

  function renderList(host, items, fields, short) {
    host.replaceChildren();
    items.forEach(function (item, i) {
      const art = document.createElement("div");
      art.className = "entry";
      if (short) {
        const head = document.createElement("div");
        head.className = "slog-head" + (short.length === 1 ? " one" : "");
        short.forEach(function (key) {
          head.appendChild(field(fields.find(function (f) { return f[0] === key; }), item[key]));
        });
        art.appendChild(head);
      }
      fields.forEach(function (f) {
        if (short && short.indexOf(f[0]) >= 0) return;
        art.appendChild(field(f, item[f[0]]));
      });
      const bar = document.createElement("div");
      bar.className = "entry-bar nprint";
      const del = document.createElement("button");
      del.type = "button";
      del.className = "linkish quiet";
      del.textContent = "删除这条";
      del.addEventListener("click", function () {
        sync();
        const list = listFor(host.id);
        if (nonempty(list[i]) && !confirm("删除这条记录？")) return;
        list.splice(i, 1);
        if (!list.length) list.push(blank(fields));
        render();
        save();
      });
      bar.appendChild(del);
      art.appendChild(bar);
      host.appendChild(art);
    });
  }

  function render() {
    renderList(daysHost, data.sessions, DAY, ["date", "lesson", "time"]);
    renderList(weeksHost, data.weeks, WEEK, ["week"]);
    renderList(feynHost, data.feynman, FEYN, null);
    fit();
  }

  function collect(host) {
    return Array.prototype.map.call(host.querySelectorAll(":scope > .entry"), function (entry) {
      const o = {};
      entry.querySelectorAll("[data-key]").forEach(function (el) { o[el.dataset.key] = el.value; });
      return o;
    });
  }
  function sync() {
    data.name = nameEl.value;
    data.sessions = collect(daysHost);
    data.weeks = collect(weeksHost);
    data.feynman = collect(feynHost);
  }
  function save() {
    sync();
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {}
  }

  function focusLast(host) {
    const entries = host.querySelectorAll(":scope > .entry");
    const last = entries[entries.length - 1];
    const el = last && last.querySelector("input, textarea");
    if (el) el.focus();
  }
  function add(key, fields, host) {
    return function () {
      sync();
      data[key].push(blank(fields));
      render();
      save();
      focusLast(host);
    };
  }

  function fit(one) {
    const nodes = one ? [one] : document.querySelectorAll(".slog textarea");
    Array.prototype.forEach.call(nodes, function (t) {
      t.style.height = "auto";
      t.style.height = t.scrollHeight + "px";
    });
  }

  function mdText(s) { return String(s || "").replace(/\r\n/g, "\n").trim(); }
  function block(label, text) {
    const t = mdText(text);
    if (!t) return [];
    return ["**" + label + "**", "", t, ""];
  }
  function weekTitle(n) {
    n = mdText(n);
    if (!n) return "## 每周小结";
    if (n.indexOf("周") >= 0) return "## 每周小结（" + n + "）";
    return "## 每周小结（第 " + n + " 周）";
  }
  function toMarkdown(d) {
    const lines = ["# CLPN 自学课程 · 学习日志", ""];
    lines.push("## 每次学习记录", "");
    const sessions = d.sessions.filter(nonempty);
    if (!sessions.length) lines.push("（尚未填写）", "");
    sessions.forEach(function (s) {
      const head = [s.date, s.lesson, s.time].map(mdText).filter(Boolean).join(" · ");
      lines.push("### " + (head || "一条记录"), "");
      lines.push.apply(lines, block("今天学到的三件事", s.learned));
      lines.push.apply(lines, block("还不懂的地方", s.unclear));
      lines.push.apply(lines, block("遇到的 R 报错及解决办法", s.error));
      lines.push.apply(lines, block("下一步想弄清的问题", s.ask));
    });
    const weeks = d.weeks.filter(nonempty);
    if (!weeks.length) lines.push("## 每周小结", "", "（尚未填写）", "");
    weeks.forEach(function (w) {
      lines.push(weekTitle(w.week), "");
      [["done", "本周完成的课程"], ["quiz", "测验正确率 / 练习完成情况"], ["concept", "最有收获的一个概念（用自己的话解释）"], ["stuck", "仍然困惑的地方，以及打算怎样解决"], ["sent", "本周完成并归档的练习"], ["plan", "下周计划"]].forEach(function (pair) {
        const t = mdText(w[pair[0]]);
        if (t) lines.push("- **" + pair[1] + "**：" + t.replace(/\n+/g, " "), "");
      });
    });
    lines.push("## 费曼检查", "");
    const fs = d.feynman.filter(nonempty);
    if (!fs.length) lines.push("（尚未填写）", "");
    fs.forEach(function (f) {
      lines.push.apply(lines, block("概念", f.concept));
      lines.push.apply(lines, block("用一段话讲给没学过统计的社工同事听", f.tell));
      lines.push.apply(lines, block("我卡住的地方", f.stuck));
    });
    return lines.join("\n").replace(/\n{3,}/g, "\n\n").replace(/\n+$/, "\n");
  }

  function download(text) {
    const name = mdText(data.name).replace(/[\\/:*?"<>|]/g, "").slice(0, 40);
    const filename = name ? "study_log_" + name + ".md" : "study_log.md";
    const blob = new Blob(["﻿" + text], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1500);
  }

  document.querySelector("main").addEventListener("input", function (e) {
    if (!e.target.closest(".slog")) return;
    save();
    if (e.target.tagName === "TEXTAREA") fit(e.target);
  });
  document.getElementById("addDay").addEventListener("click", add("sessions", DAY, daysHost));
  document.getElementById("addWeek").addEventListener("click", add("weeks", WEEK, weeksHost));
  document.getElementById("addFeyn").addEventListener("click", add("feynman", FEYN, feynHost));
  document.getElementById("slogDownload").addEventListener("click", function () {
    save();
    download(toMarkdown(data));
  });
  document.getElementById("slogPrint").addEventListener("click", function () {
    fit();
    window.print();
  });
  document.getElementById("slogClear").addEventListener("click", function () {
    if (!confirm("确定清除本页填写的全部内容吗？已经下载的文件不会被删除。")) return;
    data = { name: "", sessions: [blank(DAY)], weeks: [blank(WEEK)], feynman: [blank(FEYN)] };
    nameEl.value = "";
    render();
    save();
  });
  window.addEventListener("beforeprint", function () { fit(); });

  render();
})();
