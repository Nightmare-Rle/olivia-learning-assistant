import os
import sys

# Resolve the app root directory regardless of whether running
# as a frozen .exe (PyInstaller) or as a plain .py script.
def _get_app_root():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    base = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        if any(os.path.isdir(os.path.join(base, d))
               for d in ["K-12_Philippine_Curriculum", "College_Programs"]):
            return base
        base = os.path.dirname(base)
    return os.path.dirname(os.path.abspath(__file__))

APP_ROOT = _get_app_root()

def _resolve_dir(name):
    path = os.path.join(APP_ROOT, name)
    return path if os.path.isdir(path) else None

# Source directories for learning materials — resolved relative to app root
SOURCE_K12 = _resolve_dir("K-12_Philippine_Curriculum") or os.path.join(APP_ROOT, "K-12_Philippine_Curriculum")
SOURCE_COLLEGE = _resolve_dir("College_Programs") or os.path.join(APP_ROOT, "College_Programs")
SOURCE_STUDY = _resolve_dir("Study_Materials")

DIFFICULTIES = ["Full Lesson", "Easy", "Medium", "Hard", "Practice", "Full Assessment"]

# Order matters: check longer suffixes first
DIFF_SUFFIXES = [
    ("Full Assessment", "_Full_Assessment"),
    ("Practice",        "_Practice"),
    ("Medium",          "_Medium"),
    ("Hard",            "_Hard"),
    ("Easy",            "_Easy"),
    ("Full Lesson",     ""),
]

def _files_to_topics(files):
    topics = {}
    for f in files:
        name = f["name"] if isinstance(f, dict) else f.name
        path = f["path"] if isinstance(f, dict) else f.path
        base = name[:-3] if name.endswith(".md") else name
        matched = False
        for diff, suffix in DIFF_SUFFIXES:
            if suffix and base.endswith(suffix):
                topic_name = base[: -len(suffix)]
                topics.setdefault(topic_name, {})[diff] = path
                matched = True
                break
        if not matched:
            topics.setdefault(base, {})["Full Lesson"] = path
    return topics

def scan_k12():
    data = {}
    if not os.path.isdir(SOURCE_K12):
        return {}

    for grade_name in sorted(os.listdir(SOURCE_K12)):
        grade_path = os.path.join(SOURCE_K12, grade_name)
        if not os.path.isdir(grade_path):
            continue

        # Build a human-readable label
        if grade_name == "00_Kindergarten":
            label = "Kindergarten"
        elif grade_name == "11_Grade_11_SHS":
            label = "Grade 11 SHS"
        elif grade_name == "12_Grade_12_SHS":
            label = "Grade 12 SHS"
        elif grade_name == "99_Reference_Materials":
            label = "Reference Materials"
        elif "_Grade_" in grade_name:
            parts = grade_name.split("_", 1)
            label = parts[1].replace("_", " ") if len(parts) > 1 else grade_name
        else:
            label = grade_name.replace("_", " ")

        subjects = {}
        items = os.listdir(grade_path)
        subdirs = sorted(d for d in items if os.path.isdir(os.path.join(grade_path, d)))

        if subdirs:
            # SHS strands / sub-folders
            for sd in subdirs:
                sd_path = os.path.join(grade_path, sd)
                md_files = [
                    {"name": f, "path": os.path.join(sd_path, f)}
                    for f in os.listdir(sd_path) if f.endswith(".md")
                ]
                topics = _files_to_topics(md_files)
                for t, diffs in topics.items():
                    subj_name = f"{sd.replace('_', ' ')} - {t.replace('_', ' ')}"
                    subjects[subj_name] = diffs
        else:
            md_files = [
                {"name": f, "path": os.path.join(grade_path, f)}
                for f in items if f.endswith(".md")
            ]
            topics = _files_to_topics(md_files)
            for t, diffs in topics.items():
                subjects[t.replace("_", " ")] = diffs

        if subjects:
            data[label] = subjects

    return data

def scan_college():
    data = {}
    if not os.path.isdir(SOURCE_COLLEGE):
        return {}

    for cat_name in sorted(os.listdir(SOURCE_COLLEGE)):
        cat_path = os.path.join(SOURCE_COLLEGE, cat_name)
        if not os.path.isdir(cat_path):
            continue

        # Strip leading "01_" etc.
        cat_label = cat_name.lstrip("0123456789").lstrip("_").replace("_", " ")

        programs = {}
        for prog_name in sorted(os.listdir(cat_path)):
            prog_path = os.path.join(cat_path, prog_name)
            if not os.path.isdir(prog_path):
                continue

            md_files = [
                {"name": f, "path": os.path.join(prog_path, f)}
                for f in os.listdir(prog_path) if f.endswith(".md")
            ]
            topics = _files_to_topics(md_files)
            prog_topics = {t.replace("_", " "): diffs for t, diffs in topics.items()}

            if prog_topics:
                programs[prog_name.replace("_", " ")] = prog_topics

        if programs:
            data[cat_label] = programs

    return data


def _extract_answer_key(content):
    """Extract answer key section from markdown content."""
    answer_key = ""
    in_key = False
    key_lines = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## Answer Key") or stripped.startswith("## Susing Sagot") or stripped.startswith("## Susi sa Pagwawasto"):
            in_key = True
            continue
        if in_key:
            if stripped.startswith("---") or stripped.startswith("*Study") or stripped.startswith("*Pag"):
                break
            key_lines.append(line)
    if key_lines:
        answer_key = "\n".join(key_lines).strip()
    return answer_key


def _get_lang_path(filepath, suffix):
    """Get corresponding language file path (e.g., _EN or _TL)"""
    for src_dir in ["K-12_Philippine_Curriculum", "College_Programs"]:
        lang_dir = src_dir + suffix
        if src_dir in filepath and lang_dir not in filepath:
            return filepath.replace(src_dir, lang_dir)
    return None


def scan_answer_sheets():
    """Scan all Full_Assessment files from source directories and extract their Answer Key sections.
    Also checks for _EN and _TL versions for language switching support."""
    sheets = []
    
    def scan_dir(source_dir, prefix):
        if not os.path.isdir(source_dir):
            return
        for root, dirs, files in os.walk(source_dir):
            for f in sorted(files):
                if not f.endswith("_Full_Assessment.md"):
                    continue
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, source_dir)
                label = f"{prefix} {rel.replace('\\', ' / ').replace('.md', '')}"
                try:
                    with open(fp, "r", encoding="utf-8") as fh:
                        content = fh.read()
                    answer_key = _extract_answer_key(content)
                    
                    # Check for English version
                    en_path = _get_lang_path(fp, "_EN")
                    answer_key_en = ""
                    if en_path and os.path.exists(en_path):
                        try:
                            with open(en_path, "r", encoding="utf-8") as fh:
                                en_content = fh.read()
                            answer_key_en = _extract_answer_key(en_content)
                        except Exception:
                            pass
                    
                    # Check for Tagalog version
                    tl_path = _get_lang_path(fp, "_TL")
                    answer_key_tl = ""
                    if tl_path and os.path.exists(tl_path):
                        try:
                            with open(tl_path, "r", encoding="utf-8") as fh:
                                tl_content = fh.read()
                            answer_key_tl = _extract_answer_key(tl_content)
                        except Exception:
                            pass
                    
                    sheets.append({
                        "path": fp,
                        "label": label,
                        "answer_key": answer_key,
                        "answer_key_en": answer_key_en,
                        "answer_key_tl": answer_key_tl,
                        "full_content": content,
                    })
                except Exception:
                    sheets.append({"path": fp, "label": label, "answer_key": "", "full_content": ""})
    
    scan_dir(SOURCE_K12, "K-12")
    scan_dir(SOURCE_COLLEGE, "College")
    
    return sheets
