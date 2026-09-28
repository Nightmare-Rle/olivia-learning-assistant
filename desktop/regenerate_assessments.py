"""Regenerate all _Full_Assessment.md files with proper answer keys from quarter_curriculum.json."""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = os.path.dirname(BASE)
QJSON = os.path.join(BASE, "quarter_curriculum.json")
K12_DIR = os.path.join(APP_ROOT, "K-12_Philippine_Curriculum")

GRADE_FOLDERS = {
    "0": "00_Kindergarten",
    "1": "01_Grade_1", "2": "02_Grade_2", "3": "03_Grade_3",
    "4": "04_Grade_4", "5": "05_Grade_5", "6": "06_Grade_6",
    "7": "07_Grade_7", "8": "08_Grade_8", "9": "09_Grade_9",
    "10": "10_Grade_10",
}

QUARTER_NAMES = ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"]

def load_json():
    with open(QJSON, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_grade_assessments(data):
    total = 0
    for grade_key, subjects in data.items():
        if grade_key not in GRADE_FOLDERS:
            continue
        gnum = int(grade_key)
        folder = GRADE_FOLDERS[grade_key]
        grade_dir = os.path.join(K12_DIR, folder)
        if not os.path.isdir(grade_dir):
            print(f"  Skipping {folder} (not found)")
            continue

        for subject, quarters in subjects.items():
            if not isinstance(quarters, list):
                continue
            for qi, qdata in enumerate(quarters):
                if not isinstance(qdata, dict):
                    continue
                title = qdata.get("title", "")
                desc = qdata.get("description", "")
                assessment = qdata.get("assessment", [])
                answer_key = qdata.get("answer_key", [])
                melcs = qdata.get("melcs", [])
                weeks = qdata.get("weeks", [])
                subj_clean = subject.replace("_", " ").title()
                grade_label = f"Grade {gnum}" if gnum > 0 else "Kindergarten"

                lines = []
                lines.append(f"# {grade_label} {subj_clean} — {QUARTER_NAMES[qi]} (Full Assessment)\n")
                lines.append("## Instructions\n")
                lines.append("Read each question carefully. Write your answers on a separate sheet of paper.\n")

                mc_count = 0

                # Part I — Multiple Choice from assessment field
                if assessment:
                    lines.append("### PART I: MULTIPLE CHOICE\n")
                    for i, item in enumerate(assessment):
                        mc_count += 1
                        lines.append(f"{mc_count}. {item}\n")

                # Part II — Additional questions based on MELCs
                if melcs:
                    lines.append("### PART II: SHORT ANSWER\n")
                    for j, m in enumerate(melcs[:5]):
                        mc_count += 1
                        lines.append(f"{mc_count}. Explain or demonstrate: \"{m}\"\n")

                # Part III — Week topics identification
                if weeks:
                    lines.append("### PART III: IDENTIFICATION\n")
                    for k, w in enumerate(weeks[:5]):
                        mc_count += 1
                        lines.append(f"{mc_count}. What is the main topic covered in: \"{w}\"?\n")

                # Part IV — Open-ended
                lines.append("### PART IV: OPEN ENDED\n")
                mc_count += 1
                lines.append(f"{mc_count}. Write a short paragraph explaining the most important thing you learned in {subj_clean} this quarter.\n")
                mc_count += 1
                lines.append(f"{mc_count}. How can you apply what you learned in {subj_clean} to your daily life?\n")

                # --- ANSWER KEY ---
                lines.append("---\n")
                lines.append("## Answer Key\n\n")

                ans_idx = 0
                if answer_key:
                    lines.append("### Multiple Choice & Short Answer\n")
                    for a in answer_key:
                        ans_idx += 1
                        lines.append(f"{ans_idx}. {a}\n")
                else:
                    lines.append("*Answers will vary for open-ended questions. Discuss with your teacher.*\n")

                if assessment:
                    lines.append("\n### Open Ended\n")
                    lines.append("*Answers will vary. Award credit for reasonable, well-explained responses.*\n")

                lines.append("\n---\n")
                lines.append("> Keep practicing! Review any questions you got wrong and try again.\n")

                content = "".join(lines)
                fname = f"{subject}_Full_Assessment.md"
                fpath = os.path.join(grade_dir, fname)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                total += 1
                print(f"  {folder}/{fname} — {QUARTER_NAMES[qi]}")
    return total

def main():
    print("Loading quarter_curriculum.json...")
    data = load_json()
    print(f"Regenerating Full_Assessment.md files with answer keys...")
    total = generate_grade_assessments(data)
    print(f"\nDone! Regenerated {total} assessment files with answer keys.")

if __name__ == "__main__":
    main()
