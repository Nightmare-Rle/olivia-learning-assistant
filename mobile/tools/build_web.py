# Build OLIVIA-Mobile web assets from the desktop OLIVIA content corpus.
# Generates:
#   web/assets/data/CATALOG.json    - browse structure (k12 + college)
#   web/assets/data/QUIZ.json       - per-lesson precomputed quizzes
#   web/assets/lessons/<id>.html    - pre-rendered markdown lessons
#   web/assets/visual/<...>.html    - Visual_Lessons_Student copies
import html
import hashlib
import io
import json
import os
import random
import re
import shutil
import sys

import quiz_engine

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(os.path.dirname(ROOT), "O.L.I.V.I.A")

K12_EN = os.path.join(CONTENT, "K-12_Philippine_Curriculum_EN")
COLLEGE_EN = os.path.join(CONTENT, "College_Programs_EN")
VISUAL = os.path.join(CONTENT, "Visual_Lessons_Student")

OUT = os.path.join(ROOT, "web", "assets", "www")
LESSONS_OUT = os.path.join(OUT, "lessons")
VISUAL_OUT = os.path.join(OUT, "visual")

DIFF_SUFFIXES = ["_Full_Assessment", "_Practice", "_Medium", "_Hard", "_Easy"]
DIFF_LABELS = {"_Full_Assessment": "Full Assessment", "_Practice": "Practice",
               "_Medium": "Medium", "_Hard": "Hard", "_Easy": "Easy", "": "Full Lesson"}

GRADE_LABELS = {
    "00": "Kindergarten", "01": "Grade 1", "02": "Grade 2", "03": "Grade 3",
    "04": "Grade 4", "05": "Grade 5", "06": "Grade 6", "07": "Grade 7",
    "08": "Grade 8", "09": "Grade 9", "10": "Grade 10", "11": "Grade 11 SHS",
    "12": "Grade 12 SHS", "99": "Reference Materials",
}

QUARTER_WORDS = ["First", "Second", "Third", "Fourth"]

SUBJECT_META = {k.lower(): v for k, v in {
    "GMRC": ("\U0001F49A", "#AD1457"),
    "Language": ("\U0001F5E3\uFE0F", "#6A1B9A"),
    "Reading and Literacy": ("\U0001F4D6", "#8E24AA"),
    "Makabansa": ("\U0001F1F5\U0001F1ED", "#E65100"),
    "Mathematics": ("\U0001F4D0", "#1565C0"),
    "English": ("\U0001F1EC\U0001F1E7", "#0D47A1"),
    "Filipino": ("\U0001F1F5\U0001F1ED", "#4527A0"),
    "Science": ("\U0001F52C", "#2E7D32"),
    "Araling Panlipunan": ("\U0001F3DB\uFE0F", "#C62828"),
    "EPP_TLE": ("\U0001F527", "#EF6C00"),
    "TLE": ("\U0001F527", "#EF6C00"),
    "Music and Arts": ("\U0001F3A8", "#D81B60"),
    "MAPEH": ("\U0001F3A8", "#D81B60"),
    "PE and Health": ("\u26BD", "#00838F"),
    "Values Education": ("\U0001F49B", "#F9A825"),
    "Cognitive Development": ("\U0001F9E0", "#5E35B1"),
    "Aesthetic Creative Development": ("\U0001F3A8", "#EC407A"),
    "Socio-Emotional Development": ("\U0001F91D", "#00897B"),
    "Physical Health and Motor Development": ("\U0001F3C3", "#F4511E"),
    "Values Development": ("\U0001F49B", "#F9A825"),
    "Reference Materials": ("\U0001F4DA", "#546E7A"),
}.items()}

COLLEGE_COLORS = {
    "01_Business_and_Finance": ("\U0001F4BC", "#0D47A1"),
    "02_Engineering": ("\u2699\uFE0F", "#B71C1C"),
    "03_IT_and_Computing": ("\U0001F4BB", "#01579B"),
    "04_Health_Sciences": ("\U0001FA7A", "#1B5E20"),
    "05_Education": ("\U0001F393", "#6A1B9A"),
    "06_Social_Sciences": ("\U0001F30D", "#4E342E"),
    "07_Communication_and_Arts": ("\U0001F3AD", "#AD1457"),
    "08_Hospitality_and_Tourism": ("\U0001F37D\uFE0F", "#E65100"),
    "09_Criminal_Justice_and_Law": ("\u2696\uFE0F", "#37474F"),
    "10_Agriculture_and_Environment": ("\U0001F331", "#33691E"),
    "11_Maritime": ("\U0001F6A2", "#006064"),
    "12_Sciences": ("\U0001F52C", "#2E7D32"),
}

DEFAULT_META = ("\U0001F4D6", "#455A64")


def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(re.compile(r"!\[([^\]]*)\]\(([^)]+)\)"), r'<img alt="\1" src="\2" class="md-img">', s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" class="md-link">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", s)
    return s


class MdRenderer:
    def __init__(self):
        self.out = None
        self.list_stack = None

    def _close_lists(self, depth, inclusive=False):
        while self.list_stack:
            d = self.list_stack[-1][1]
            if d > depth or (inclusive and d == depth):
                self.out.append("</%s>" % self.list_stack.pop()[0])
            else:
                break

    def _open_list(self, ltype, depth):
        while self.list_stack:
            lt, d = self.list_stack[-1]
            if d > depth or (d == depth and lt != ltype):
                self.out.append("</%s>" % self.list_stack.pop()[0])
            else:
                break
        if not self.list_stack or self.list_stack[-1][0] != ltype or self.list_stack[-1][1] != depth:
            self.list_stack.append((ltype, depth))
            self.out.append("<%s>" % ltype)

    def _render_table(self, header, rows):
        p = ["<div class='md-table-wrap'><table class='md-table'>"]
        if header:
            p.append("<thead><tr>" + "".join("<th>%s</th>" % inline(h) for h in header) + "</tr></thead>")
        if rows:
            p.append("<tbody>")
            for r in rows:
                p.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
            p.append("</tbody>")
        p.append("</table></div>")
        return "".join(p)

    def render(self, text):
        self.out = []
        self.list_stack = []
        lines = text.split("\n")
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            if stripped.startswith("```"):
                buf = []
                i += 1
                while i < n and not lines[i].strip().startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1
                self._close_lists(0)
                self.out.append("<pre class='md-pre'><code>%s</code></pre>" % esc("\n".join(buf)))
                continue

            m = re.match(r"^(#{1,6})\s+(.*)", line)
            if m:
                lvl = len(m.group(1))
                self._close_lists(0)
                self.out.append("<h%d class='md-h%d'>%s</h%d>" % (lvl, lvl, inline(m.group(2)), lvl))
                i += 1
                continue

            if re.match(r"^(-{3,}|\*{3,})$", stripped):
                self._close_lists(0)
                self.out.append("<hr class='md-hr'>")
                i += 1
                continue

            if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]):
                header = [c.strip() for c in line.strip().strip("|").split("|")]
                i += 2
                rows = []
                while i < n and "|" in lines[i] and not lines[i].strip().startswith("#"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                self._close_lists(0)
                self.out.append(self._render_table(header, rows))
                continue

            if stripped.startswith(">"):
                buf = []
                while i < n and lines[i].strip().startswith(">"):
                    buf.append(lines[i].strip().lstrip(">").strip())
                    i += 1
                self._close_lists(0)
                self.out.append("<blockquote class='md-quote'>%s</blockquote>" % inline(" ".join(buf)))
                continue

            lm = re.match(r"^(\s*)((?:[-*]\s)|(?:\d+\.\s+))(.*)$", line)
            if lm:
                indent = len(lm.group(1))
                marker = lm.group(2)
                depth = indent // 2
                ltype = "ol" if re.match(r"\d+\.\s", marker) else "ul"
                item = lm.group(3)
                cm = re.match(r"^\[( |x|X)\]\s*(.*)$", item)
                chk = ""
                if cm:
                    chk = " checked" if cm.group(1).lower() == "x" else ""
                    item = cm.group(2)
                self._open_list(ltype, depth)
                pad = "<input type='checkbox'%s disabled> " % chk if chk else ""
                self.out.append("<li class='md-li'>%s%s</li>" % (pad, inline(item)))
                i += 1
                continue

            buf = [stripped]
            i += 1
            while i < n:
                s2 = lines[i].strip()
                if not s2 or re.match(r"^(#{1,6}\s|```|>|[-*]\s|\d+\.\s|(-{3,}|\*{3,})$)", s2) or (
                        "|" in s2 and i + 1 < n and "-" in lines[i + 1]):
                    break
                buf.append(s2)
                i += 1
            self._close_lists(0)
            self.out.append("<p class='md-p'>%s</p>" % inline("<br>".join(buf)))

        self._close_lists(0)
        return "\n".join(self.out)


MD_RENDERER = MdRenderer()


def lesson_html_skin(title, subtitle, emoji, color, body_inner):
    return (
        "<div class='lesson-hero' style='background:linear-gradient(135deg,%s,#5C9DFF);'>"
        "<div class='lesson-hero-emoji'>%s</div>"
        "<h1 class='lesson-hero-title'>%s</h1>"
        "<div class='lesson-hero-sub'>%s</div>"
        "</div>%s"
    ) % (color, emoji, esc(title), esc(subtitle), body_inner)


def split_difficulty(name):
    for suf in DIFF_SUFFIXES:
        if name.endswith(suf):
            return name[:-len(suf)], suf
    return name, ""


def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "x"


def stable_seed(s):
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest()[:8], 16)


def build_quiz(lesson_id, md_text):
    rng = random.Random(stable_seed(lesson_id))
    return quiz_engine.generate_combined_quiz(md_text, rng=rng)


def scan_k12():
    grades = []
    if not os.path.isdir(K12_EN):
        print("  !! K-12 dir missing:", K12_EN)
        return grades
    for folder in sorted(os.listdir(K12_EN)):
        fdir = os.path.join(K12_EN, folder)
        if not os.path.isdir(fdir) or not re.match(r"^\d{2}_", folder):
            continue
        gcode = folder[:2]
        grade_label = GRADE_LABELS.get(gcode, folder[3:].replace("_", " "))
        subjects = {}
        for fname in os.listdir(fdir):
            if not fname.endswith(".md"):
                continue
            stem, _ = os.path.splitext(fname)
            topic, dif = split_difficulty(stem)
            subjects.setdefault(topic, []).append((dif, fname))
        subject_list = []
        for topic in sorted(subjects):
            meta = SUBJECT_META.get(topic.lower(), DEFAULT_META)
            emoji, color = meta
            sub = {"name": topic, "emoji": emoji, "color": color, "difficulties": [], "visual": []}
            for dif, fname in subjects[topic]:
                lesson_id = "k12/%s/%s/%s" % (folder, slug(topic), slug(fname[:-3]))
                sub["difficulties"].append({
                    "id": lesson_id, "file": lesson_id + ".html",
                    "title": topic, "difficulty": DIFF_LABELS.get(dif, "Full Lesson"),
                })
            subject_list.append(sub)
        grades.append({"code": gcode, "grade": grade_label, "subjects": subject_list})
    return grades


def scan_college():
    cats = []
    if not os.path.isdir(COLLEGE_EN):
        print("  !! College dir missing:", COLLEGE_EN)
        return cats
    for folder in sorted(os.listdir(COLLEGE_EN)):
        cdir = os.path.join(COLLEGE_EN, folder)
        if not os.path.isdir(cdir):
            continue
        pretty = re.sub(r"^\d{2}_", "", folder).replace("_", " ")
        emoji, color = COLLEGE_COLORS.get(folder, DEFAULT_META)
        programs = []
        for pdir_name in sorted(os.listdir(cdir)):
            pdir = os.path.join(cdir, pdir_name)
            if not os.path.isdir(pdir):
                continue
            topics = []
            for fname in sorted(os.listdir(pdir)):
                if not fname.endswith(".md"):
                    continue
                stem, _ = os.path.splitext(fname)
                lesson_id = "college/%s/%s/%s" % (folder, slug(pdir_name), slug(stem))
                topics.append({"id": lesson_id, "file": lesson_id + ".html", "title": stem, "difficulty": "Full Lesson"})
            programs.append({"name": pdir_name.replace("_", " "), "topics": topics})
        cats.append({"category": pretty, "emoji": emoji, "color": color, "programs": programs})
    return cats


def _k12_folder(grade):
    return os.path.join(K12_EN, grade["code"] + "_" + grade["grade"].replace(" ", "_"))


def _subject_md_path(grade, subject, suffix):
    leaf = subject["name"] + suffix + ".md"
    return os.path.join(_k12_folder(grade), leaf)


def _college_folder(cat):
    for f in os.listdir(COLLEGE_EN):
        if os.path.isdir(os.path.join(COLLEGE_EN, f)) and \
                re.sub(r"^\d{2}_", "", f).replace("_", " ") == cat["category"]:
            return f
    return cat["category"].replace(" ", "_")


def main():
    os.makedirs(LESSONS_OUT, exist_ok=True)
    os.makedirs(VISUAL_OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)

    print("Scanning K-12...")
    k12 = scan_k12()
    print("Scanning College...")
    college = scan_college()

    print("Rendering markdown lessons + quizzes...")
    quizzes = {}
    total_md = 0
    skipped = []

    def render_entry(e, emoji, color, subtitle):
        nonlocal total_md
        if not os.path.isfile(e["src"]):
            skipped.append(e["src"])
            return None
        with io.open(e["src"], "r", encoding="utf-8", errors="replace") as f:
            md_text = f.read()
        eid = e["id"]
        out_html = lesson_html_skin(e["title"], subtitle, emoji, color,
                                    MD_RENDERER.render(md_text))
        out_path = os.path.join(LESSONS_OUT, eid + ".html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with io.open(out_path, "w", encoding="utf-8") as f:
            f.write(out_html)
        qs = build_quiz(eid, md_text)
        if len(qs) >= 3:
            quizzes[eid] = qs
        total_md += 1

    for grade in k12:
        for sub in grade["subjects"]:
            for d in sub["difficulties"]:
                suf = d["difficulty"]
                if suf == "Full Lesson":
                    suf = ""
                else:
                    suf = "_" + suf.replace(" ", "_")
                d["src"] = _subject_md_path(grade, sub, suf)
                render_entry(d, sub["emoji"], sub["color"], "%s \u2022 %s" % (grade["grade"], sub["name"]))

    for cat in college:
        cfolder = _college_folder(cat)
        for prog in cat["programs"]:
            for t in prog["topics"]:
                t["src"] = os.path.join(COLLEGE_EN, cfolder, prog["name"].replace(" ", "_"), t["title"] + ".md")
                render_entry(t, cat["emoji"], cat["color"], "%s \u2022 %s" % (cat["category"], prog["name"]))

    print("Copying visual lessons...")
    visual_map = {}
    if os.path.isdir(VISUAL):
        for folder in sorted(os.listdir(VISUAL)):
            fdir = os.path.join(VISUAL, folder)
            if not os.path.isdir(fdir):
                continue
            gcode = folder[:2]
            for fname in os.listdir(fdir):
                if not fname.endswith(".html"):
                    continue
                stem = fname[:-5]
                m = re.match(r"^(.*)_(?:First|Second|Third|Fourth)_Quarter$", stem)
                if not m:
                    continue
                subject = m.group(1)
                rel = os.path.join(folder, fname)
                dst = os.path.join(VISUAL_OUT, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(fdir, fname), dst)
                visual_map.setdefault((gcode, subject), []).append({
                    "subject": subject, "file": "visual/" + rel.replace("\\", "/"),
                    "title": _quarter_title(find_quarter(fname))})
        for k, v in visual_map.items():
            visual_map[k] = sorted(v, key=lambda x: QUARTER_WORDS.index(x["title"].split()[0]) if x["title"].split() else 99)

    print("Attaching visual lessons to K-12 subjects...")
    for grade in k12:
        gcode = grade["code"]
        for sub in grade["subjects"]:
            vis = visual_map.get((gcode, sub["name"])) or visual_map.get((gcode, sub["name"].split()[0]))
            if vis:
                sub["visual"] = [{"id": "v/" + sha(v["file"]), "file": v["file"], "title": v["title"],
                                  "difficulty": "Visual"} for v in vis]

    print("Writing catalog...")
    catalog = {"k12": k12, "college": college}
    with io.open(os.path.join(OUT, "data", "CATALOG.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, separators=(",", ":"))

    print("Writing quizzes...")
    with io.open(os.path.join(OUT, "data", "QUIZ.json"), "w", encoding="utf-8") as f:
        json.dump(quizzes, f, ensure_ascii=False, separators=(",", ":"))

    print("DONE  md_lessons=%d  quizzes=%d  visual=%d  skipped=%d"
          % (total_md, len(quizzes), sum(len(v) for v in visual_map.values()), len(skipped)))
    for s in skipped[:10]:
        print("  skipped:", s)


def find_quarter(fname):
    for q in QUARTER_WORDS:
        if q + "_Quarter" in fname:
            return q
    return ""


def _quarter_title(qword):
    return "%s Quarter" % qword if qword else "Quarter"


def sha(s):
    return hashlib.sha1(s.encode()).hexdigest()[:10]


if __name__ == "__main__":
    main()