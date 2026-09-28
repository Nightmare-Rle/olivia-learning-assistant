"use strict";
/* OLIVIA Mobile - SPA shell, router, browse screens */

(() => {
  const catUrl = (p) => "data/CATALOG.json";
  let CATALOG = null;
  let quizLoading = null;

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function toast(msg) {
    const t = $("toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.classList.remove("show"), 2400);
  }
  function diffClass(d) {
    const m = (d || "").toLowerCase();
    if (m.includes("visual")) return "diff-visual";
    if (m.includes("easy")) return "diff-easy";
    if (m.includes("medium")) return "diff-medium";
    if (m.includes("hard")) return "diff-hard";
    if (m.includes("practice")) return "diff-practice";
    if (m.includes("assessment")) return "diff-practice";
    if (m.includes("full") || m === "") return "diff-full";
    return "diff-default";
  }
  function fetchText(u) {
    return fetch(u).then(r => { if (!r.ok) throw new Error(r.status); return r.text(); });
  }
  function ensureCatalog() {
    if (CATALOG) return Promise.resolve(CATALOG);
    if (ensureCatalog._p) return ensureCatalog._p;
    ensureCatalog._p = fetchText("data/CATALOG.json").then(t => {
      CATALOG = JSON.parse(t);
      window.CATALOG = CATALOG;
      return CATALOG;
    }).catch(() => { CATALOG = { k12: [], college: [] }; window.CATALOG = CATALOG; return CATALOG; });
    return ensureCatalog._p;
  }
  function loadQuizMap() {
    if (quizLoading) return quizLoading;
    quizLoading = fetchText("data/QUIZ.json").then(t => JSON.parse(t)).catch(() => ({}));
    return quizLoading;
  }

  /* ---------- router ---------- */
  const App = {
    stack: [],

    push(screen, params) {
      this.stack.push({ screen, params: params || {} });
      history.pushState({ idx: this.stack.length - 1 }, "");
      this._show(screen, params);
      $("view").scrollTop = 0;
    },
    replace(screen, params) {
      if (this.stack.length) this.stack[this.stack.length - 1] = { screen, params: params || {} };
      else this.stack.push({ screen, params: params || {} });
      history.replaceState({ idx: this.stack.length - 1 }, "");
      this._show(screen, params);
      $("view").scrollTop = 0;
    },
    gotoRoot(screen) {
      this.stack = [{ screen, params: {} }];
      history.replaceState({ idx: 0 }, "");
      this._show(screen, {});
      $("view").scrollTop = 0;
    },
    back() {
      if (this.stack.length <= 1) {
        if (confirm("Sign out of OLIVIA?")) { Store.signOut(); location.reload(); }
        return;
      }
      history.back();
    },
    _show(screen, params) {
      const v = $("view");
      this._cur = screen;
      setNav(screen);
      if (screen === "home" || screen === "progress" || screen === "settings") {
        // informational screens render immediately
        if (screen === "home") renderHome(v, params);
        else if (screen === "progress") renderProgress(v, params);
        else renderSettings(v, params);
        return;
      }
      if (screen === "lesson") { renderLesson(v, params); return; }
      if (screen === "quiz") { Quiz.render(v, params); return; }
      // catalog-backed screens
      if (!CATALOG) {
        v.innerHTML = "<div class='empty'><span class='ei'>\u23F3</span>Loading content\u2026</div>";
        ensureCatalog().then(() => {
          if (this._cur === screen) this._show(screen, params);
        });
        return;
      }
      if (screen === "k12") renderK12(v, params);
      else if (screen === "college") renderCollege(v, params);
    },
  };

  window.addEventListener("popstate", () => {
    if (App.stack.length > 1) {
      App.stack.pop();
      const st = App.stack[App.stack.length - 1];
      App._show(st.screen, st.params);
      $("view").scrollTop = 0;
    }
  });

  function setNav(screen) {
    const tabs = ["home", "k12", "college", "progress"];
    document.querySelectorAll(".bottomnav button").forEach(b => {
      b.classList.toggle("active", b.dataset.screen === screen);
    });
  }

  /* ---------- auth ---------- */
  function renderAuth() {
    const user = Store.getUser();
    if (user) return;
    const v = $("view");
    v.innerHTML =
      "<div id='screen-auth'><div class='card auth-card'>" +
      "<div class='auth-logo'>\u{1F393}</div>" +
      "<div class='auth-title'>O.L.I.V.I.A.</div>" +
      "<div class='auth-sub'>Online Learning Intelligent Virtual Interactive Assistant</div>" +
      "<input id='au-name' class='auth-input' placeholder='Your name' maxlength='24' value='" + esc(Store.getDefaultName()) + "'>" +
      "<div class='role-row' id='au-roles'>" +
      ["student", "teacher", "admin"].map(r =>
        "<div class='role-chip' data-role='" + r + "'>" + r.charAt(0).toUpperCase() + r.slice(1) + "</div>").join("") +
      "</div>" +
      "<button id='au-start' class='btn btn-primary'>Start Learning</button>" +
      "</div></div>";
    let role = "student";
    v.querySelectorAll(".role-chip").forEach(chip => {
      chip.classList.toggle("active", chip.dataset.role === role);
      chip.addEventListener("click", () => {
        role = chip.dataset.role;
        v.querySelectorAll(".role-chip").forEach(c => c.classList.toggle("active", c.dataset.role === role));
      });
    });
    $("au-start").addEventListener("click", () => {
      const name = $("au-name").value.trim();
      if (!name) { toast("Please enter your name"); return; }
      storeUserAndStart(name, role);
    });
  }

  function storeUserAndStart(name, role) {
    Store.saveUser({
      name, role,
      color: ["#2E86C1", "#27AE60", "#E67E22", "#8E44AD", "#C0392B"][Math.floor(Math.random() * 5)],
      created: Date.now(),
    });
    toast("Welcome, " + name + "!");
    renderTopbar();
    App.gotoRoot("home");
  }

  function renderTopbar() {
    const u = Store.getUser();
    $("top-title").textContent = "O.L.I.V.I.A.";
    $("top-user").innerHTML = u ? "<b>" + esc(u.name) + "</b><br><small>" + esc(u.role) + "</small>" : "";
  }

  /* ---------- home ---------- */
  function renderHome(v, params) {
    const u = Store.getUser();
    const s = Store.stats();
    const recent = Store.getProgress().quizzes.slice(0, 4);
    v.innerHTML =
      "<div class='hero-strip'><div class='hi'>Hi, " + esc(u.name) + " \u{1F44B}</div>" +
      "<div class='sub'>" + esc(u.role.charAt(0).toUpperCase() + u.role.slice(1)) +
      " \u2022 K-12 + College \u2022 MATATAG / CHED curriculum</div></div>" +
      "<div class='stats-3'>" +
      "<div class='stat'><div class='num'>" + s.completed + "</div><div class='lab'>Lessons</div></div>" +
      "<div class='stat'><div class='num'>" + s.points + "</div><div class='lab'>Points</div></div>" +
      "<div class='stat'><div class='num'>" + s.streak + "\u{1F525}</div><div class='lab'>Day Streak</div></div>" +
      "</div>" +
      "<div class='tiles'>" +
      "<div class='tile' data-go='k12' style='background:linear-gradient(135deg,#1565C0,#42A5F5)'><div class='ti'>\u{1F4D6}</div><div class='tt'>K-12 Learning</div></div>" +
      "<div class='tile' data-go='college' style='background:linear-gradient(135deg,#6A1B9A,#AB47BC)'><div class='ti'>\u{1F3DB}\uFE0F</div><div class='tt'>College Programs</div></div>" +
      "<div class='tile' data-go='progress' style='background:linear-gradient(135deg,#2E7D32,#66BB6A)'><div class='ti'>\u{1F4C8}</div><div class='tt'>My Progress</div></div>" +
      "</div>" +
      (recent.length ?
        "<div class='sec-label'>Recent Quizzes</div>" +
        recent.map(r =>
          "<div class='card recent-item' data-lesson='" + esc(r.lessonId) + "'>" +
          "<div class='rt'>" + esc(r.title) + "</div>" +
          "<div class='rs'>" + r.score + "/" + r.total + " \u2022 " + new Date(r.ts).toLocaleDateString() + "</div></div>").join("")
        : "<div class='card empty' style='margin-top:12px'><span class='ei'>\u{1F4D4}</span>Finish a quiz to see recent activity here.</div>");
    v.querySelectorAll(".tile").forEach(t => t.addEventListener("click", () => App.gotoRoot(t.dataset.go)));
    v.querySelectorAll(".recent-item").forEach(r => r.addEventListener("click", () => openLessonById(r.dataset.lesson)));
  }

  /* ---------- K-12 ---------- */
  function renderK12(v, params) {
    if (params.level === "subject") return renderSubjects(v, params);
    if (params.level === "lessons") return renderLessons(v, params);
    // grade list
    v.innerHTML = "<div class='screen-title'>K-12 Learning</div>" +
      "<div class='muted' style='margin-bottom:10px;font-size:12px'>Philippine MATATAG Curriculum</div>" +
      CATALOG.k12.map(g =>
        "<div class='flat-row' data-grade='" + esc(g.code) + "'><div class='av' style='background:linear-gradient(135deg,#34495E,#5D6D7E)'>" +
        (g.code === "00" ? "\u{1F476}" : g.code === "99" ? "\u{1F4DA}" : "\u{1F4D6}") + "</div>" +
        "<div class='tx'><div class='t1'>" + esc(g.grade) + "</div><div class='t2'>" + g.subjects.length + " subjects</div></div>" +
        "<div class='chev'>\u25B8</div></div>").join("");
    v.querySelectorAll(".flat-row").forEach(r => r.addEventListener("click", () =>
      App.push("k12", { level: "subject", grade: r.dataset.grade })));
  }

  function renderSubjects(v, params) {
    const g = CATALOG.k12.find(x => x.code === params.grade);
    if (!g) { v.innerHTML = "<div class='empty'>Grade not found</div>"; return; }
    v.innerHTML =
      "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>" + esc(g.grade) + "</div></div>" +
      g.subjects.map(s =>
        "<div class='flat-row' data-sub='" + esc(s.name) + "'>" +
        "<div class='av' style='background:linear-gradient(135deg," + s.color + ",-webkit-linear-gradient,#5DADE2);background:" + s.color + "'>" + s.emoji + "</div>" +
        "<div class='tx'><div class='t1'>" + esc(s.name) + "</div><div class='t2'>" +
        (s.difficulties.length + (s.visual ? s.visual.length : 0)) + " lessons</div></div>" +
        "<div class='chev'>\u25B8</div></div>").join("");
    wireBack();
    v.querySelectorAll(".flat-row").forEach(r => r.addEventListener("click", () =>
      App.push("k12", { level: "lessons", grade: params.grade, subject: r.dataset.sub })));
  }

  function renderLessons(v, params) {
    const g = CATALOG.k12.find(x => x.code === params.grade);
    const s = g && g.subjects.find(x => x.name === params.subject);
    if (!s) { v.innerHTML = "<div class='empty'>Subject not found</div>"; return; }
    const vis = s.visual || [];
    const diffs = s.difficulties;
    const item = (e, label, d) =>
      "<div class='flat-row' data-lesson='" + esc(e.id) + "'><div class='av' style='background:" + s.color + "'>" + s.emoji + "</div>" +
      "<div class='tx'><div class='t1'>" + esc(e.title) + "</div>" +
      "<div style='margin-top:4px'><span class='diff-badge " + diffClass(d) + "'>" + esc(d) + "</span></div></div>" +
      "<div class='chev'>\u25B8</div></div>";
    let html = "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>" + esc(s.name) + "</div></div>";
    if (vis.length) {
      html += "<div class='sec-label'>Visual Lessons</div>" +
        vis.map(x => item(x, x.title, "Visual")).join("");
    }
    if (diffs.length) {
      html += "<div class='sec-label'>Topic Lessons</div>" +
        diffs.map(d => item(d, d.difficulty === "Full Lesson" ? d.title : d.title + " (" + d.difficulty + ")", d.difficulty)).join("");
    }
    html += "<div class='card muted' style='font-size:11px;text-align:center'>Aligned with DepEd MATATAG Curriculum \u2022 " + esc(g.grade) + "</div>";
    v.innerHTML = html;
    wireBack();
    v.querySelectorAll("[data-lesson]").forEach(r => r.addEventListener("click", () => openLessonById(r.dataset.lesson)));
  }

  /* ---------- College ---------- */
  function renderCollege(v, params) {
    if (params.level === "program") return renderPrograms(v, params);
    if (params.level === "topics") return renderTopics(v, params);
    v.innerHTML = "<div class='screen-title'>College Programs</div>" +
      "<div class='muted' style='margin-bottom:10px;font-size:12px'>CHED-aligned program lessons</div>" +
      CATALOG.college.map(c =>
        "<div class='flat-row' data-cat='" + esc(c.category) + "'><div class='av' style='background:" + c.color + "'>" + c.emoji + "</div>" +
        "<div class='tx'><div class='t1'>" + esc(c.category) + "</div><div class='t2'>" + c.programs.length + " programs</div></div>" +
        "<div class='chev'>\u25B8</div></div>").join("");
    v.querySelectorAll(".flat-row").forEach(r => r.addEventListener("click", () =>
      App.push("college", { level: "program", cat: r.dataset.cat })));
  }

  function renderPrograms(v, params) {
    const c = CATALOG.college.find(x => x.category === params.cat);
    if (!c) { v.innerHTML = "<div class='empty'>Not found</div>"; return; }
    v.innerHTML =
      "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>" + esc(c.category) + "</div></div>" +
      c.programs.map(p =>
        "<div class='flat-row' data-prog='" + esc(p.name) + "'><div class='av' style='background:" + c.color + "'>" + c.emoji + "</div>" +
        "<div class='tx'><div class='t1'>" + esc(p.name) + "</div><div class='t2'>" + p.topics.length + " topics</div></div>" +
        "<div class='chev'>\u25B8</div></div>").join("");
    wireBack();
    v.querySelectorAll(".flat-row").forEach(r => r.addEventListener("click", () =>
      App.push("college", { level: "topics", cat: params.cat, prog: r.dataset.prog })));
  }

  function renderTopics(v, params) {
    const c = CATALOG.college.find(x => x.category === params.cat);
    const p = c && c.programs.find(x => x.name === params.prog);
    if (!p) { v.innerHTML = "<div class='empty'>Not found</div>"; return; }
    v.innerHTML =
      "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>" + esc(p.name) + "</div></div>" +
      p.topics.map(t =>
        "<div class='flat-row' data-lesson='" + esc(t.id) + "'><div class='av' style='background:" + c.color + "'>" + c.emoji + "</div>" +
        "<div class='tx'><div class='t1'>" + esc(t.title) + "</div>" +
        "<div style='margin-top:4px'><span class='diff-badge diff-full'>Full Lesson</span></div></div>" +
        "<div class='chev'>\u25B8</div></div>").join("");
    wireBack();
    v.querySelectorAll("[data-lesson]").forEach(r => r.addEventListener("click", () => openLessonById(r.dataset.lesson)));
  }

  /* ---------- progress ---------- */
  function renderProgress(v, params) {
    const s = Store.stats();
    const week = Store.last7();
    const badges = Store.BADGES;
    const maxBar = Math.max(1, ...week.map(w => w.quizzes));
    const u = Store.getUser();
    const others = Store.getAllUsers();
    const entries = Object.keys(others).map(n => ({
      name: n, role: others[n].role, color: others[n].color,
      points: n === u.name ? s.points : Math.round(others[n].points || 0),
    })).sort((a, b) => b.points - a.points);
    const rank = (i) => i === 0 ? "gold" : i === 1 ? "silver" : i === 2 ? "bronze" : "";
    v.innerHTML =
      "<div class='screen-title'>My Progress</div>" +
      "<div class='stats-3'>" +
      "<div class='stat'><div class='num'>" + s.completed + "</div><div class='lab'>Completed</div></div>" +
      "<div class='stat'><div class='num'>" + (s.completed ? s.avg.toFixed(1) : "0") + "%</div><div class='lab'>Avg Score</div></div>" +
      "<div class='stat'><div class='num'>" + s.points + "</div><div class='lab'>Points</div></div>" +
      "</div>" +
      "<div class='card'><h3>Weekly Activity</h3>" +
      "<div class='week-bars'>" + week.map(w =>
        "<div class='week-col'><div class='bar' style='height:" + Math.round((w.quizzes / maxBar) * 100) + "%'></div>" +
        "<div class='bday'>" + ["S", "M", "T", "W", "T", "F", "S"][new Date(w.key).getDay()] + "</div></div>").join("") +
      "</div><div class='muted' style='font-size:11px;text-align:center;margin-top:6px'>Quizzes taken in the last 7 days</div></div>" +
      "<div class='card'><h3>Badges (" + s.badges.length + ")</h3>" +
      badges.map(b => {
        const got = s.badges.includes(b.id);
        return "<div class='badge-card" + (got ? "" : " locked") + "'><div class='bi'>" + b.icon + "</div>" +
          "<div><div class='bn'>" + esc(b.name) + "</div><div class='bd'>" + esc(b.desc) + "</div></div></div>";
      }).join("") + "</div>" +
      "<div class='card'><h3>Leaderboard</h3>" +
      entries.map((e, i) =>
        "<div class='lb-row'><div class='rk " + rank(i) + "'>" + (i + 1) + "</div>" +
        "<div class='av' style='width:30px;height:30px;border-radius:50%;background:" + e.color + ";color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px'>" + esc(e.name.charAt(0).toUpperCase()) + "</div>" +
        "<div class='nm'>" + esc(e.name) + " <small class='muted'>(" + esc(e.role) + ")</small></div>" +
        "<div class='pt'>" + e.points + "</div></div>").join("") +
      "</div>" +
      "<button id='reset-prog' class='btn btn-ghost' style='width:100%'>Reset my progress</button>";
    $("reset-prog").addEventListener("click", () => {
      if (confirm("Reset all progress, points and badges?")) { Store.resetProgress(); alert("Progress reset."); App.replace("progress"); }
    });
  }

  /* ---------- lesson viewer ---------- */
  const screenLessonInit = () => {
    const el = $("lesson-back");
    if (el) el.addEventListener("click", () => App.back());
    const fab = $("quiz-fab");
    if (fab) fab.addEventListener("click", () => {
      App.push("quiz", { lessonId: fab.dataset.lesson });
    });
  };

  function openLessonById(id) {
    App.push("lesson", { lessonId: id });
  }

  function renderLesson(v, params) {
    const id = params.lessonId;
    Store.recordLessonAccess(id);
    const isVisual = /^v\//.test(id);
    v.innerHTML =
      "<div class='lesson-toolbar'><button class='tbtn' id='lesson-back'>\u2039</button>" +
      "<div class='tt' id='lesson-tt'>Loading\u2026</div></div>" +
      "<div class='lesson-content' id='lesson-body'><div class='empty'><span class='ei'>\u23F3</span>Loading lesson\u2026</div></div>";
    if (isVisual) {
      fetchVisual(id).then(html => {
        $("lesson-tt").textContent = id.split("/").pop();
        $("lesson-body").innerHTML =
          "<iframe id='vis-frame' style='width:100%;min-height:70vh;border:none;background:#fff;border-radius:12px'></iframe>";
        $("vis-frame").srcdoc = html;
        const doc = $("vis-frame").contentDocument;
        if (doc) {
          const t = doc.querySelector("title");
          if (t) $("lesson-tt").textContent = t.textContent;
        }
      }).catch(() => {
        $("lesson-body").innerHTML = "<div class='empty'>Failed to load visual lesson.</div>";
      });
    } else {
      fetchText("lessons/" + id + ".html").then(html => {
        $("lesson-body").innerHTML = html;
        findLessonMeta(id, (meta) => {
          $("lesson-tt").textContent = meta ? meta.title : id.split("/").pop();
        });
        hideFabIfNoQuiz(id);
      }).catch(() => {
        $("lesson-body").innerHTML = "<div class='empty'>Failed to load lesson.</div>";
      });
    }
    // "Take Quiz" button (hidden for visual lessons)
    const fab = document.createElement("button");
    fab.className = "quiz-fab";
    fab.id = "quiz-fab";
    fab.dataset.lesson = id;
    fab.innerHTML = "<span class='plus'>\u{1F9EA}</span>&nbsp; Take Quiz";
    if (isVisual) fab.style.display = "none";
    v.appendChild(fab);
    screenLessonInit();
  }

  function hideFabIfNoQuiz(id) {
    loadQuizMap().then(map => {
      if (!map[id]) { const f = $("quiz-fab"); if (f) f.style.display = "none"; }
    });
  }

  function findLessonMeta(id, cb) {
    (CATALOG ? Promise.resolve(CATALOG) : legacyCatalog()).then(cat => {
      let meta = null;
      for (const g of cat.k12) for (const s of g.subjects) {
        for (const d of s.difficulties) if (d.id === id) meta = { title: d.title, sub: s.name + " \u2022 " + g.grade };
        for (const vis of s.visual || []) if (vis.id === id) meta = { title: vis.title, sub: s.name + " \u2022 " + g.grade };
      }
      for (const c of cat.college) for (const p of c.programs) for (const t of p.topics)
        if (t.id === id) meta = { title: t.title, sub: p.name + " \u2022 " + c.category };
      cb(meta);
    });
  }

  function legacyCatalog() { return Promise.resolve({ k12: [], college: [] }); }

  function fetchVisual(id) {
    const entry = findVisualEntry(id);
    if (!entry) return Promise.reject(new Error("no visual file for " + id));
    return fetchText("visual/" + entry.file.slice("visual/".length));
  }

  function findVisualEntry(id) {
    if (!CATALOG) return null;
    for (const g of CATALOG.k12) for (const s of g.subjects)
      for (const v of s.visual || []) if (v.id === id) return v;
    return null;
  }

  /* ---------- settings ---------- */
  const APP_VERSION = "1.0.0";
  const ANDROID_VERSIONS = [
    { ver: "7.0", api: 24, name: "Nougat", tag: "MINIMUM" },
    { ver: "7.1", api: 25, name: "Nougat", tag: "" },
    { ver: "8.0", api: 26, name: "Oreo", tag: "" },
    { ver: "8.1", api: 27, name: "Oreo", tag: "" },
    { ver: "9", api: 28, name: "Pie", tag: "BEST VALUE" },
    { ver: "10", api: 29, name: "Q", tag: "" },
    { ver: "11", api: 30, name: "R", tag: "" },
    { ver: "12", api: 31, name: "S", tag: "" },
    { ver: "12L", api: 32, name: "S v2", tag: "" },
    { ver: "13", api: 33, name: "Tiramisu", tag: "" },
    { ver: "14", api: 34, name: "Upside Down Cake", tag: "TESTED" },
  ];
  const SEL_KEY = "olivia.settings.androidVer";

  function detectAndroid() {
    const ua = navigator.userAgent || "";
    const m = ua.match(/Android[ \/](\d+(?:\.\d+)?)/);
    return m ? m[1] : null;
  }

  function apiFromVer(ver) {
    if (!ver) return null;
    const n = Number(ver);
    if (n === 7.0) return 24;
    if (n === 7.1) return 25;
    if (n === 8.0) return 26;
    if (n === 8.1) return 27;
    if (n === 9) return 28;
    if (n === 10) return 29;
    if (n === 11) return 30;
    if (n === 12) return 31;
    if (n === 13) return 33;
    if (n === 14) return 34;
    if (n >= 7) return Math.floor(n) + 17;
    return null;
  }

  function renderSettings(v, params) {
    const u = Store.getUser();
    const dev = detectAndroid();
    const api = apiFromVer(dev);
    const sel = localStorage.getItem(SEL_KEY) || "24";
    const cur = ANDROID_VERSIONS.find(x => x.api === Number(sel)) || ANDROID_VERSIONS[0];
    v.innerHTML =
      "<div class='screen-title'>Settings</div>" +
      "<div class='card'><h3>Device</h3>" +
      "<div class='set-row'><span>Model</span><b>" + esc(navigator.userAgentData && navigator.userAgentData.platform ? navigator.userAgentData.platform : (navigator.platform || "Android")) + "</b></div>" +
      "<div class='set-row'><span>Android</span><b>" + (dev ? "Android " + esc(dev) : "detected\u2026") + (api ? " \u2022 API " + api : "") + "</b></div>" +
      "<div class='set-row'><span>App version</span><b>O.L.I.V.I.A. v" + APP_VERSION + "</b></div>" +
      "<div class='set-row'><span>Signed in</span><b>" + esc(u.name) + " (" + esc(u.role) + ")</b></div>" +
      "</div>" +
      "<div class='card'><h3>Android version selector</h3>" +
      "<div class='muted' style='font-size:11px;margin-bottom:10px'>Tells OLIVIA which Android you compare against. The app supports Android 7.0 (API 24) and newer.</div>" +
      ANDROID_VERSIONS.map(x => {
        const active = x.api === cur.api;
        const isThis = dev && x.ver === dev;
        return "<div class='set-ver" + (active ? " on" : "") + "' data-api='" + x.api + "'>" +
          "<div><div class='sv'>Android " + x.ver + " <span class='muted' style='font-size:11px'>API " + x.api + "</span>" +
          (x.tag ? " <span class='diff-badge " + (x.tag === "MINIMUM" ? "diff-medium" : "diff-full") + "'>" + x.tag + "</span>" : "") +
          (isThis ? " <span class='diff-badge diff-visual'>THIS DEVICE</span>" : "") +
          "</div><div class='sn'>" + x.name + "</div></div><div class='chev'>" + (active ? "\u2713" : "\u25B8") + "</div></div>";
      }).join("") +
      "</div>" +
      "<div class='card' id='ver-detail'><h3>Android " + cur.ver + " \u2022 " + cur.name + " \u2022 API " + cur.api + "</h3>" +
      "<p class='muted' style='font-size:12px;line-height:1.5'>" + notesFor(cur.api, dev, cur) + "</p></div>" +
      "<div class='card'><h3>About</h3><p class='muted' style='font-size:12px;line-height:1.5'>" +
      "O.L.I.V.I.A. \u2014 Online Learning Intelligent Virtual Interactive Assistant. " +
      "Philippine MATATAG K-12 + CHED College curriculum, quizzes, progress and badges. " +
      "Everything runs offline on your device.</p></div>" +
      "<button id='set-reset' class='btn btn-ghost' style='width:100%'>Reset my progress</button>" +
      "<button id='set-out' class='btn btn-ghost' style='width:100%;margin-top:8px'>Sign out</button>";
    v.querySelectorAll(".set-ver").forEach(r => r.addEventListener("click", () => {
      localStorage.setItem(SEL_KEY, r.dataset.api);
      App.replace("settings");
    }));
    $("set-reset").addEventListener("click", () => {
      if (confirm("Reset all progress, points and badges?")) { Store.resetProgress(); App.replace("settings"); }
    });
    $("set-out").addEventListener("click", () => {
      if (confirm("Sign out of OLIVIA?")) { Store.signOut(); location.reload(); }
    });
  }

  function notesFor(api, dev, cur) {
    const base = "OLIVIA runs on Android " + cur.ver + " (API " + api + ").";
    let body;
    if (api === 24) body = base + " This is the minimum. Lessons, quizzes, progress, badges and offline storage all work. Update tip: updating to Android 9+ improves WebView security and rendering speed.";
    else if (api === 25) body = base + " Fully supported (Nougat 7.1 refresh). No known differences from API 24 for this app.";
    else if (api === 26 || api === 27) body = base + " Oreo adds background limits and autofill. OLIVIA is unaffected.";
    else if (api === 28) body = base + " Pie is the best value: modern WebView, adaptive battery, faster rendering. A great target for old hardware.";
    else if (api === 29) body = base + " Android 10 adds dark mode support and scoped storage (OLIVIA keeps data locally, no files needed).";
    else if (api === 30) body = base + " Android 11 strengthens package visibility; OLIVIA needs no external apps.";
    else if (api === 31) body = base + " Android 12 brings material-you and WebView updates; fully supported.";
    else if (api === 32) body = base + " Android 12L optimizes for large screens and tablets. OLIVIA scales to two-pane layouts.";
    else if (api === 33) body = base + " Android 13 refines per-app language settings. OLIVIA content is English.";
    else body = base + " Android 14 (API 34) is the version this APK was built against (targetSdk 34). No known issues.";
    if (!dev) return body;
    const dNum = Number(dev);
    return body + " Your device reports Android " + dev + " \u2014 " +
      (dNum >= 24 ? "compatible and verified. " : "older than the minimum; update to Android 7.0+. ");
  }

  /* ---------- boot ---------- */
  function wireBack() {
    const b = document.querySelector("[data-back]");
    if (b) b.addEventListener("click", () => App.back());
  }

  function nav() {
    document.querySelectorAll(".bottomnav button").forEach(b =>
      b.addEventListener("click", () => App.gotoRoot(b.dataset.screen)));
  }

  function init() {
    renderTopbar();
    nav();
    $("top-gear").addEventListener("click", () => App.push("settings"));
    if (!Store.getUser()) { renderAuth(); return; }
    App.gotoRoot("home");
    loadQuizMap();
  }

  document.addEventListener("DOMContentLoaded", init);

  window.OLIVIA = { App, loadQuizMap, toast };
})();