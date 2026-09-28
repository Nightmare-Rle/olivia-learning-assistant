// End-to-end DOM integration test of the OLIVIA mobile SPA using jsdom.
// Mocks window.fetch to read from the real www assets on disk.
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");

const ROOT = path.join(__dirname, "..", "..");
const WWW = path.join(ROOT, "web", "assets", "www");

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const settle = (ms) => sleep(ms || 80);

function loadApp() {
  const indexHtml = fs.readFileSync(path.join(WWW, "index.html"), "utf8");
  const scripts = ["js/store.js", "js/app.js", "js/quiz.js"]
    .map((p) => "<script>" + fs.readFileSync(path.join(WWW, p), "utf8") + "</script>")
    .join("");
  const mockFetch = `
    <script>
    (function(){
      var FILES = ${JSON.stringify(listFiles(""))};
      window.fetch = function(u){
        var key = String(u).split("?")[0];
        if (FILES.indexOf(key) === -1) {
          return Promise.resolve({ok:false, status:404, text:function(){return Promise.resolve("");}});
        }
        var fs = undefined, path = undefined;
        // read path is injected at real-module level via global.__readFile
        var txt = window.__readFile(key);
        return Promise.resolve({ok:true, status:200,
          text:function(){ return Promise.resolve(txt); },
          json:function(){ return Promise.resolve(JSON.parse(txt)); }});
      };
    })();
    </script>`;
  const finalHtml = indexHtml
    .replace(/<script src="js\/(store|app|quiz)\.js"><\/script>/g, "")
    .replace("</body>", mockFetch + scripts + "</body>");

  const dom = new JSDOM(finalHtml, {
    url: "http://localhost/",
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(window) {
      window.__readFile = (key) => {
        const p = path.join(WWW, decodeURIComponent(key));
        return fs.readFileSync(p, "utf8");
      };
    },
  });
  return dom;
}

function listFiles(dir) {
  const base = path.join(WWW, dir);
  const out = [];
  for (const e of fs.readdirSync(base, { withFileTypes: true })) {
    const rel = dir ? dir + "/" + e.name : e.name;
    const full = path.join(base, e.name);
    if (e.isDirectory()) out.push(...listFiles(rel));
    else out.push(rel);
  }
  return out;
}

let failures = 0;
function assert(cond, msg) {
  if (cond) console.log("  PASS:", msg);
  else { failures++; console.error("  FAIL:", msg); }
}

async function click(el) {
  el.dispatchEvent(new (el.ownerDocument.defaultView.Event)("click", { bubbles: true }));
}

async function run() {
  console.log("Loading app...");
  const dom = loadApp();
  const w = dom.window;
  const d = w.document;
  await settle(400); // let DOMContentLoaded + init run

  console.log("Step 1 - auth screen");
  const startBtn = d.getElementById("au-start");
  assert(!!startBtn, "auth screen renders (Start Learning button)");

  const nameInput = d.getElementById("au-name");
  nameInput.value = "Test User";
  await click(startBtn);
  await settle(300);
  const hero = d.querySelector(".hero-strip");
  assert(!!hero && hero.textContent.indexOf("Test User") !== -1, "home screen shows hero with user name");
  const stats = d.querySelectorAll(".stat");
  assert(stats.length === 3, "home shows 3 stat cards");

  console.log("Step 2 - K-12 browse");
  await click(d.querySelector("[data-go='k12']"));
  await sleep(400); // catalog fetch
  const gradeRows = d.querySelectorAll("#view .flat-row[data-grade]");
  assert(gradeRows.length >= 13, "K-12 grade list rendered: " + gradeRows.length + " grades");

  await click(gradeRows[1]); // Grade 1
  await sleep(150);
  const subRows = d.querySelectorAll("#view .flat-row[data-sub]");
  assert(subRows.length >= 1, "subject list rendered: " + subRows.length);

  await click(subRows[0]); // first subject
  await sleep(150);
  const lessonRows = d.querySelectorAll("#view .flat-row[data-lesson]");
  assert(lessonRows.length >= 1, "lesson list rendered: " + lessonRows.length);

  console.log("Step 3 - open a lesson (markdown, to exercise quiz)");
  await click(lessonRows[lessonRows.length - 1]); // topic lesson, not visual
  await sleep(400);
  const qbtn = d.getElementById("quiz-fab");
  const isMd = !!d.querySelector(".lesson-hero");
  assert(!!isMd, "markdown lesson content loaded");
  assert(qbtn && qbtn.style.display !== "none", "quiz button visible for markdown lesson");

  console.log("Step 4 - quiz flow");
  await click(d.getElementById("quiz-fab"));
  await sleep(600); // QUIZ.json fetch
  const q = w.Quiz;
  assert(q.qs && q.qs.length > 0, "quiz loaded with " + (q.qs && q.qs.length) + " questions");
  let guard = 0;
  while (d.getElementById("res-back") === null && guard < 30) {
    guard++;
    const qi = q.qs[q.idx];
    console.log("  [dbg] idx=" + q.idx + " type=" + qi.type +
      " opts=" + d.querySelectorAll(".quiz-opt").length +
      " in=" + !!d.getElementById("quiz-in") +
      " next=" + !!d.getElementById("quiz-next") +
      " quizscreen=" + !!d.querySelector(".quiz-q"));
    if (d.querySelector(".quiz-opt")) {
      const opts = d.querySelectorAll(".quiz-opt");
      let target = null;
      opts.forEach((o) => {
        if (o.dataset.opt === qi.correct) target = o;
      });
      if (!target) target = opts[0];
      await click(target);
    } else if (d.getElementById("quiz-in")) {
      d.getElementById("quiz-in").value = qi.correct;
      d.getElementById("quiz-in").dispatchEvent(new w.KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
    } else if (d.getElementById("quiz-next")) {
      await click(d.getElementById("quiz-next"));
      await sleep(120);
      continue;
    } else {
      console.log("  [dbg] stuck - no controls");
      break;
    }
    await sleep(950); // wait for Next button reveal
    const nxt = d.getElementById("quiz-next");
    if (nxt) await click(nxt);
    await sleep(120);
  }
  await sleep(300);
  const res = d.getElementById("res-back");
  assert(!!res, "quiz finished with result screen");
  const prog = w.Store.getProgress();
  const st = w.Store.stats();
  assert(st.completed >= 1 && st.points > 0, "progress recorded (completed=" + st.completed + ", points=" + st.points + ")");
  assert(Object.keys(prog.lessons).length === 1, "lesson completion stored");
  assert(prog.quizzes.length === 1 && prog.quizzes[0].lessonId, "quiz history stored");

  console.log("Step 5b - settings screen");
  await click(d.getElementById("top-gear"));
  await sleep(200);
  const setTitle = d.querySelector(".screen-title");
  assert(setTitle && setTitle.textContent === "Settings", "settings screen renders");
  const verRows = d.querySelectorAll(".set-ver");
  assert(verRows.length === 11, "11 Android versions listed");
  const detail = d.getElementById("ver-detail");
  assert(!!detail && detail.textContent.indexOf("Android") !== -1, "version detail card present");
  await click(d.querySelector(".set-ver[data-api='28']"));
  await sleep(200);
  const detail2 = d.getElementById("ver-detail");
  assert(detail2.textContent.indexOf("Android 9") !== -1, "selector updates detail to Android 9");
  assert(w.localStorage.getItem("olivia.settings.androidVer") === "28", "selection persisted");
  await click(d.getElementById("top-gear")); // back to obtaining progress view for step5 default
  await sleep(150);

  console.log("Step 5 - progress screen");
  await click(d.querySelector("[data-screen='progress']"));
  await sleep(200);
  const pTitle = d.querySelector(".screen-title");
  assert(!!pTitle && pTitle.textContent.indexOf("Progress") !== -1, "progress screen renders");
  const badges = d.querySelectorAll(".badge-card");
  assert(badges.length === 8, "8 badges displayed");
  const lb = d.querySelector(".lb-row");
  assert(!!lb, "leaderboard has rows");

  console.log("Step 6 - college browse");
  await click(d.querySelector("[data-screen='college']"));
  await sleep(200);
  const catRows = d.querySelectorAll("#view .flat-row[data-cat]");
  assert(catRows.length === 12, "12 college categories rendered");
  await click(catRows[0]);
  await sleep(150);
  const progRows = d.querySelectorAll("#view .flat-row[data-prog]");
  assert(progRows.length >= 1, "programs rendered: " + progRows.length);
  await click(progRows[0]);
  await sleep(150);
  const topicRows = d.querySelectorAll("#view .flat-row[data-lesson]");
  assert(topicRows.length >= 1, "topics rendered: " + topicRows.length);
  await click(topicRows[0]);
  await sleep(400);
  assert(!!d.querySelector(".lesson-hero"), "college lesson content loaded");

  console.log("\nRESULT: " + (failures === 0 ? "ALL TESTS PASSED" : failures + " FAILURES"));
  process.exit(failures === 0 ? 0 : 1);
}

run().catch((e) => { console.error("TEST CRASH:", e); process.exit(2); });