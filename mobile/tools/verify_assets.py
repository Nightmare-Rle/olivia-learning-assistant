# Verify every catalog entry points to an existing asset and quiz coverage.
import json, io, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "assets", "www")
cat = json.load(io.open(os.path.join(ROOT, "data", "CATALOG.json"), encoding="utf-8"))
quiz = json.load(io.open(os.path.join(ROOT, "data", "QUIZ.json"), encoding="utf-8"))

missing = 0
checked = 0
lesson_ids = set()
visual_ids = set()

for g in cat["k12"]:
    for sub in g["subjects"]:
        for d in sub["difficulties"]:
            checked += 1
            lesson_ids.add(d["id"])
            p = os.path.join(ROOT, "lessons", d["file"])
            if not os.path.isfile(p):
                print("MISSING K12 LESSON:", d["file"]); missing += 1
        for v in sub.get("visual", []):
            checked += 1
            visual_ids.add(v["id"])
            p = os.path.join(ROOT, v["file"])
            if not os.path.isfile(p):
                print("MISSING VISUAL:", v["file"]); missing += 1

for c in cat["college"]:
    for prog in c["programs"]:
        for t in prog["topics"]:
            checked += 1
            lesson_ids.add(t["id"])
            p = os.path.join(ROOT, "lessons", t["file"])
            if not os.path.isfile(p):
                print("MISSING COLLEGE LESSON:", t["file"]); missing += 1

# quiz keys should be a subset of lesson ids
bad_keys = [k for k in quiz if k not in lesson_ids]
print("entries checked:", checked)
print("md lessons:", len(lesson_ids), "visual:", len(visual_ids))
print("quiz lessons:", len(quiz))
print("missing files:", missing)
print("quiz keys not in catalog:", len(bad_keys))
if bad_keys[:5]:
    print("  sample:", bad_keys[:5])

# sample quiz sanity
sample = next(iter(quiz.values()))
print("sample quiz qtype:", [q["type"] for q in sample])
assert not missing and not bad_keys, "verification failed"
print("VERIFICATION OK")