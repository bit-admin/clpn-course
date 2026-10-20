/* Study Log: fill in your browser, stored in localStorage, download as Markdown or print. */
(function () {
  "use strict";
  const KEY = "clpn-study-log-v1";
  const daysHost = document.getElementById("slogDays");
  if (!daysHost) return;

  const DAY = [
    ["date", "Date", "date"],
    ["lesson", "Lesson", "lesson"],
    ["time", "Time Spent", "text"],
    ["learned", "Three things I learned today", "area"],
    ["unclear", "What still feels unclear", "area"],
    ["error", "R errors encountered & how I fixed them", "area"],
    ["ask", "Questions to figure out next", "area"]
  ];
  const WEEK = [
    ["week", "Week #", "text"],
    ["done", "Lessons completed this week", "area"],
    ["quiz", "Quiz accuracy / exercises completed", "area"],
    ["concept", "Most valuable concept (explained in my own words)", "area"],
    ["stuck", "Remaining confusion & my plan to resolve it", "area"],
    ["sent", "Exercises completed & archived this week", "area"],
    ["plan", "Plan for next week (vs. Study Guide schedule)", "area"]
  ];
  const FEYN = [
    ["concept", "Concept", "text"],
    ["tell", "Explain in one paragraph to a colleague with no statistics background", "area"],
    ["stuck", "Where I got stuck (shows what I don't fully understand yet)", "area"]
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
      if (key === "time") input.placeholder = "e.g., 40 min";
      if (key === "week") input.placeholder = "e.g., 3";
      if (kind === "lesson") input.placeholder = "Lesson ID or title, e.g., 1.4";
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
      del.textContent = "Delete entry";
      del.addEventListener("click", function () {
        sync();
        const list = listFor(host.id);
        if (nonempty(list[i]) && !confirm("Delete this entry?")) return;
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
    if (!n) return "## Weekly Summary";
    if (/week/i.test(n)) return "## Weekly Summary (" + n + ")";
    return "## Weekly Summary (Week " + n + ")";
  }
  function toMarkdown(d) {
    const lines = ["# CLPN Self-Paced Course · Study Log", ""];
    lines.push("## Session Logs", "");
    const sessions = d.sessions.filter(nonempty);
    if (!sessions.length) lines.push("(Not filled in yet)", "");
    sessions.forEach(function (s) {
      const head = [s.date, s.lesson, s.time].map(mdText).filter(Boolean).join(" · ");
      lines.push("### " + (head || "Session"), "");
      lines.push.apply(lines, block("Three things I learned today", s.learned));
      lines.push.apply(lines, block("What still feels unclear", s.unclear));
      lines.push.apply(lines, block("R errors encountered & how I fixed them", s.error));
      lines.push.apply(lines, block("Questions to figure out next", s.ask));
    });
    const weeks = d.weeks.filter(nonempty);
    if (!weeks.length) lines.push("## Weekly Summary", "", "(Not filled in yet)", "");
    weeks.forEach(function (w) {
      lines.push(weekTitle(w.week), "");
      [["done", "Lessons completed this week"], ["quiz", "Quiz accuracy / exercises completed"], ["concept", "Most valuable concept (in my own words)"], ["stuck", "Remaining confusion & plan to resolve"], ["sent", "Exercises completed & archived"], ["plan", "Plan for next week"]].forEach(function (pair) {
        const t = mdText(w[pair[0]]);
        if (t) lines.push("- **" + pair[1] + "**: " + t.replace(/\n+/g, " "), "");
      });
    });
    lines.push("## Feynman Check", "");
    const fs = d.feynman.filter(nonempty);
    if (!fs.length) lines.push("(Not filled in yet)", "");
    fs.forEach(function (f) {
      lines.push.apply(lines, block("Concept", f.concept));
      lines.push.apply(lines, block("Explain in one paragraph to a colleague with no statistics background", f.tell));
      lines.push.apply(lines, block("Where I got stuck", f.stuck));
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
    if (!confirm("Clear all entries on this page? Previously downloaded files will not be affected.")) return;
    data = { name: "", sessions: [blank(DAY)], weeks: [blank(WEEK)], feynman: [blank(FEYN)] };
    nameEl.value = "";
    render();
    save();
  });
  window.addEventListener("beforeprint", function () { fit(); });

  render();
})();
