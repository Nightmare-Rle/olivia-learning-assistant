"use strict";
/* OLIVIA Mobile - quiz screen using precomputed questions from QUIZ.json */

(() => {
  const $ = (id) => document.getElementById(id);

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function typeIcon(t) {
    return t === "mcq" ? "\u{1F4AC}" : t === "true_false" ? "\u2696\uFE0F" : "\u270F\uFE0F";
  }
  const typeLabel = (t) => t === "mcq" ? "Multiple Choice" : t === "true_false" ? "True or False" : "Fill in the Blank";

  const Quiz = {
    qs: null,
    idx: 0,
    correct: 0,
    lessonId: null,
    lessonTitle: "",

    render(v, params) {
      const id = params.lessonId;
      this.lessonId = id;
      this.idx = 0;
      this.correct = 0;
      OLIVIA.loadQuizMap().then(map => {
        this.qs = map[id] || [];
        if (!this.qs.length) {
          v.innerHTML =
            "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>Quiz</div></div>" +
            "<div class='empty'><span class='ei'>\u{1F937}</span>No questions available for this lesson.</div>";
          document.querySelector("[data-back]").addEventListener("click", () => OLIVIA.App.back());
          return;
        }
        findTitle(id, (t) => { this.lessonTitle = t || "Quiz"; this._draw(v); });
      });
    },

    _draw(v) {
      const q = this.qs[this.idx];
      const pct = Math.round((this.idx / this.qs.length) * 100);
      let html =
        "<div class='lesson-toolbar'><button class='tbtn' data-back>\u2039</button><div class='tt'>" + esc(this.lessonTitle) + " \u2022 Quiz</div></div>" +
        "<div class='quiz-head'><div class='muted' style='font-size:12px'>Question " + (this.idx + 1) + " of " + this.qs.length +
        " \u2022 Score " + this.correct + "</div>" +
        "<div class='quiz-progress'><div class='fill' style='width:" + pct + "%'></div></div></div>" +
        "<div class='quiz-type'>" + typeLabel(q.type) + " " + typeIcon(q.type) + "</div>" +
        "<div class='quiz-q'>" + esc(q.question) + "</div>";
      if (q.type === "mcq") {
        html += "<div class='quiz-opts'>" + q.options.map((o) =>
          "<button class='quiz-opt' data-opt='" + esc(o) + "'>\u{1F5C2}  " + esc(o) + "</button>").join("") + "</div>";
      } else if (q.type === "true_false") {
        html += "<div class='quiz-opts'>" +
          ["True", "False"].map(o => "<button class='quiz-opt' data-opt='" + o + "'>" + o + "</button>").join("") + "</div>";
      } else {
        html += "<div class='quiz-opts'><input id='quiz-in' class='quiz-input' placeholder='Type your answer' autocomplete='off' autofocus></div>";
      }
      html += "<div class='quiz-footer' id='quiz-foot'></div>";
      v.innerHTML = html;
      if (q.type === "mcq" || q.type === "true_false") {
        v.querySelectorAll(".quiz-opt").forEach(b => b.addEventListener("click", () => this._answer(b.dataset.opt, v)));
      } else {
        const trySubmit = () => {
          const val = $("quiz-in") ? $("quiz-in").value.trim() : "";
          if (val) this._answer(val, v);
        };
        $("quiz-in").addEventListener("keydown", (e) => { if (e.key === "Enter") trySubmit(); });
        $("quiz-in").focus();
      }
      document.querySelector("[data-back]").addEventListener("click", () => OLIVIA.App.back());
    },

    _answer(ans, v) {
      const q = this.qs[this.idx];
      const ok = q.type === "fill_blank"
        ? String(ans).trim().toLowerCase() === String(q.correct).trim().toLowerCase()
        : ans === q.correct;
      if (ok) this.correct++;
      const opts = v.querySelectorAll(".quiz-opt");
      opts.forEach(b => {
        if (b.dataset.opt === q.correct) b.classList.add("correct-show");
        if (b.dataset.opt === ans && !ok) b.classList.add("wrong");
        if (ok && b.dataset.opt === ans) b.classList.add("right");
        b.disabled = true;
      });
      const inp = $("quiz-in");
      if (inp) inp.disabled = true;
      const fb = document.createElement("div");
      fb.className = "quiz-feedback " + (ok ? "ok" : "no");
      fb.textContent = ok ? "\u2713  Correct! (+2 points)" : "\u2717  Incorrect. Answer: " + q.correct;
      v.insertBefore(fb, $("quiz-foot"));
      window.setTimeout(() => {
        const foot = $("quiz-foot");
        if (!foot) return;
        foot.innerHTML = "<button id='quiz-next' class='btn " +
          (this.idx + 1 >= this.qs.length ? "btn-primary" : "btn-ghost") + "'>" +
          (this.idx + 1 >= this.qs.length ? "Finish \u2713" : "Next \u2192") + "</button>";
        $("quiz-next").addEventListener("click", () => this._next(v));
      }, 800);
    },

    _next(v) {
      if (this.idx + 1 < this.qs.length) {
        this.idx++;
        this._draw(v);
      } else {
        this._finish(v);
      }
    },

    _finish(v) {
      const total = this.qs.length;
      const gained = Store.recordQuiz(this.lessonId, this.lessonTitle, this.correct, total);
      const pct = Math.round((this.correct / total) * 100);
      const cls = pct >= 70 ? "good" : pct >= 40 ? "mid" : "bad";
      const model = Store.BADGES;
      const prog = Store.getProgress();
      const newBadges = model.filter(b => prog.badges.includes(b.id));
      v.innerHTML =
        "<div class='result-hero'>" +
        "<div class='result-score " + cls + "'>" + pct + "%</div>" +
        "<div class='result-sub'>" + this.correct + " of " + total + " correct \u2022+" + gained + " points</div>" +
        (pct >= 70 ? "<div class='result-sub' style='color:#27AE60'>\u{1F389} Great job! Keep it up.</div>" : "") +
        "</div>" +
        "<div class='card'><h3>Your Answers</h3>" +
        this.qs.map((q, i) => {
          return "<div style='padding:8px 0;border-bottom:1px solid #f0f2f4;font-size:13px'>" +
            "<b>" + (i + 1) + ".</b> " + esc(q.question) +
            " <span class='diff-badge diff-full' style='margin-left:6px'>" + esc(q.correct) + "</span></div>";
        }).join("") + "</div>" +
        (newBadges.length ? "<div class='badge-grid'>" + newBadges.map(b => "<div class='badge-chip'>" + b.icon + " " + esc(b.name) + "</div>").join("") + "</div>" : "") +
        "<div style='padding:6px 16px 16px;display:flex;gap:10px'>" +
        "<button id='res-back' class='btn btn-ghost' style='flex:1'>Back to Lesson</button>" +
        "<button id='res-again' class='btn btn-primary' style='flex:1'>Take Again</button></div>";
      $("res-back").addEventListener("click", () => OLIVIA.App.back());
      $("res-again").addEventListener("click", () => OLIVIA.App.replace("quiz", { lessonId: this.lessonId }));
    },
  };

  function findTitle(id, cb) {
    const short = () => cb(id.split("/").pop().replace(/_/g, " "));
    const c = window.CATALOG; // may be undefined
    if (!c) return short();
    for (const g of c.k12) for (const s of g.subjects) {
      for (const d of s.difficulties) if (d.id === id) return cb(d.title);
      for (const vis of s.visual || []) if (vis.id === id) return cb(vis.title);
    }
    for (const cat of c.college) for (const p of cat.programs) for (const t of p.topics)
      if (t.id === id) return cb(t.title);
    short();
  }

  window.Quiz = Quiz;
})();