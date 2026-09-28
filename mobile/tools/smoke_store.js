// Smoke-test store.js gamification logic in Node with a mock localStorage + window.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const mem = new Map();
global.localStorage = {
  getItem: (k) => (mem.has(k) ? mem.get(k) : null),
  setItem: (k, v) => mem.set(k, String(v)),
  removeItem: (k) => mem.delete(k),
};
const sandbox = { localStorage, window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(__dirname, "..", "web", "assets", "www", "js", "store.js"), "utf8"), sandbox);
const Store = sandbox.window.Store;

const assert = (c, m) => { if (!c) { console.error("FAIL:", m); process.exit(1); } };

// scenario 1: new user stats
let s = Store.stats();
assert(s.completed === 0 && s.points === 0 && s.streak === 0, "fresh stats");

// scenario 2: record quiz, points += correct*2 (+10 perfect)
Store.recordLessonAccess("a");
const gained = Store.recordQuiz("k12/a", "Lesson A", 8, 10);
assert(gained === 8 * 2, "gained points for 8/10 = 16, got " + gained);
s = Store.stats();
assert(s.completed === 1 && s.points === 16, "one lesson, 16 points");

// scenario 3: perfect score bonus
const g2 = Store.recordQuiz("k12/b", "Lesson B", 5, 5);
assert(g2 === 10 + 10, "perfect bonus: 10 + 10, got " + g2);
onlyAwarded = Store.getProgress().badges;
assert(onlyAwarded.includes("first_lesson"), "first_lesson badge");
assert(onlyAwarded.includes("quiz_master"), "quiz_master badge");

// scenario 4: streak today then +1 tomorrow (simulate by forcing lastActive yesterday)
const p = Store.getProgress();
const d = new Date(); d.setDate(d.getDate() - 1);
p.lastActive = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
Store.saveProgress(p);
Store.recordQuiz("k12/c", "Lesson C", 3, 5);
s = Store.stats();
assert(s.streak === 2, "streak advanced to 2, got " + s.streak);

// scenario 5: reset
Store.resetProgress();
s = Store.stats();
assert(s.completed === 0 && s.points === 0, "reset clears progress");

console.log("STORE SMOKE TEST PASSED");