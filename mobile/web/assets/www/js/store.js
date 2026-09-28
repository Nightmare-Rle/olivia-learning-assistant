"use strict";
/* OLIVIA Mobile - local storage + gamification (mirrors desktop behavior) */
(function (global) {
  const KEY_USER = "olivia_user";
  const KEY_PROG = "olivia_progress";
  const KEY_USERS = "olivia_users";

  const todayStr = () => {
    const d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  };

  const defaultProgress = () => ({
    lessons: {},            // lessonId -> {done:true, score, max, ts}
    quizzes: [],            // recent [{lessonId, title, score, total, ts}]
    points: 0,
    streak: 0,
    streakBest: 0,
    lastActive: "",
    badges: [],             // awarded badge ids
    daily: {},              // 'YYYY-MM-DD' -> {viewed, quizzes, points}
  });

  const Store = {
    getDefaultName() {
      return "Student";
    },

    getUser() {
      try { return JSON.parse(localStorage.getItem(KEY_USER)) || null; } catch (e) { return null; }
    },
    saveUser(u) {
      localStorage.setItem(KEY_USER, JSON.stringify(u));
      const users = this.getAllUsers();
      users[u.name] = { role: u.role, color: u.color || "#2E86C1", created: u.created || Date.now() };
      localStorage.setItem(KEY_USERS, JSON.stringify(users));
    },
    hasUser() { return !!this.getUser(); },
    signOut() { localStorage.removeItem(KEY_USER); },

    getAllUsers() {
      try { return JSON.parse(localStorage.getItem(KEY_USERS)) || {}; } catch (e) { return {}; }
    },

    getProgress() {
      try {
        const p = JSON.parse(localStorage.getItem(KEY_PROG));
        if (p && typeof p === "object") return p;
      } catch (e) {}
      return defaultProgress();
    },
    saveProgress(p) {
      localStorage.setItem(KEY_PROG, JSON.stringify(p));
    },

    _touchDay(p, deltaPoints) {
      const t = todayStr();
      const day = p.daily[t] || { viewed: 0, quizzes: 0, points: 0 };
      if (deltaPoints) day.points += deltaPoints;
      p.daily[t] = day;
      return day;
    },

    recordLessonAccess(lessonId) {
      const p = this.getProgress();
      this._touchDay(p, 0).viewed += 1;
      this.saveProgress(p);
    },

    recordQuiz(lessonId, title, score, total) {
      const p = this.getProgress();
      const t = todayStr();
      const day = this._touchDay(p, 0);
      day.quizzes += 1;
      const correct = score;
      const gained = correct * 2 + (score === total ? 10 : 0);
      p.points += gained;
      day.points += gained;
      p.quizzes.unshift({ lessonId, title, score, total, ts: Date.now() });
      p.quizzes = p.quizzes.slice(0, 30);
      // lesson completion
      if (!p.lessons[lessonId] || !p.lessons[lessonId].done) {
        p.lessons[lessonId] = { done: true, score, max: total, ts: Date.now() };
      }
      // streak
      if (p.lastActive !== t) {
        p.streak = (p.lastActive === this._yesterday()) ? p.streak + 1 : 1;
        p.lastActive = t;
      } else {
        p.streak = Math.max(1, p.streak);
      }
      if (p.streak > p.streakBest) p.streakBest = p.streak;
      this._awardBadges(p);
      this.saveProgress(p);
      return gained;
    },

    _yesterday() {
      const d = new Date();
      d.setDate(d.getDate() - 1);
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    },

    last7() {
      const out = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const k = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
        const day = this.getProgress().daily[k] || { viewed: 0, quizzes: 0, points: 0 };
        out.push({ key: k, quizzes: day.quizzes, viewed: day.viewed, points: day.points });
      }
      return out;
    },

    stats() {
      const p = this.getProgress();
      const lessons = Object.keys(p.lessons);
      let scoreSum = 0, scoreCount = 0;
      lessons.forEach(id => {
        const l = p.lessons[id];
        if (l.score !== undefined) { scoreSum += l.score; scoreCount += 1; }
      });
      return {
        completed: lessons.length,
        avg: scoreCount ? Math.round((scoreSum / scoreCount) * 100) / 100 : 0,
        points: p.points,
        streak: p.streak,
        streakBest: p.streakBest,
        badges: p.badges,
      };
    },

    BADGES: [
      { id: "first_lesson", icon: "\u2655", name: "First Steps", desc: "Complete your first lesson" },
      { id: "quiz_master", icon: "\u{1F3C6}", name: "Quiz Master", desc: "Score 100% on a quiz" },
      { id: "streak_5", icon: "\u{1F525}", name: "On Fire", desc: "5-day streak" },
      { id: "streak_10", icon: "\u{1F31F}", name: "Unstoppable", desc: "10-day streak" },
      { id: "lessons_10", icon: "\u{1F4DA}", name: "Bookworm", desc: "Complete 10 lessons" },
      { id: "lessons_50", icon: "\u{1F393}", name: "Scholar", desc: "Complete 50 lessons" },
      { id: "points_100", icon: "\u2B50", name: "Rising Star", desc: "Earn 100 points" },
      { id: "points_500", icon: "\u{1F451}", name: "Crown", desc: "Earn 500 points" },
    ],

    _awardBadges(p) {
      const s = this.stats();
      let changed = false;
      const have = (id) => p.badges.some(b => b === id);
      const check = (cond, id) => {
        if (cond && !have(id)) { p.badges.push(id); changed = true; }
      };
      check(Object.keys(p.lessons).length >= 1, "first_lesson");
      check(p.quizzes.some(q => q.score === q.total && q.total > 0), "quiz_master");
      check(p.streak >= 5, "streak_5");
      check(p.streak >= 10, "streak_10");
      check(Object.keys(p.lessons).length >= 10, "lessons_10");
      check(Object.keys(p.lessons).length >= 50, "lessons_50");
      check(p.points >= 100, "points_100");
      check(p.points >= 500, "points_500");
      return changed;
    },

    resetProgress() {
      const p = this.getProgress();
      const kp = Object.keys(p);
      kp.forEach(k => delete p[k]);
      Object.assign(p, defaultProgress());
      this.saveProgress(p);
    },
  };

  global.Store = Store;
})(window);