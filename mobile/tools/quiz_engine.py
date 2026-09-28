# Portable copy of OLIVIA quiz_engine.py (stdlib only), made deterministic
# by accepting a random.Random instance for shuffling.

import re


QUESTION_TYPES = ["mcq", "true_false", "fill_blank"]


def parse_lesson_content(content):
    lines = content.split("\n")
    paragraphs = []
    bullet_points = []
    definitions = []
    headings = []
    current_section = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            current_section = stripped.lstrip("#").strip()
            headings.append(current_section)
        elif stripped and not stripped.startswith("!") and not stripped.startswith("["):
            if stripped.startswith("- ") or stripped.startswith("* "):
                bullet_points.append(stripped[2:])
            elif ":" in stripped and len(stripped) < 120:
                definitions.append(stripped)
            else:
                paragraphs.append(stripped)
    return {
        "paragraphs": paragraphs,
        "bullet_points": bullet_points,
        "definitions": definitions,
        "headings": headings,
        "raw": content,
    }


def generate_mcq(parsed, rng=None, num_options=4):
    random = rng or __import__("random")
    questions = []
    candidates = []
    for p in parsed["paragraphs"]:
        sentences = re.split(r"(?<=[.!?])\s+", p)
        for s in sentences:
            s = s.strip()
            if len(s) > 30 and "?" not in s and "!" not in s:
                candidates.append(s)
    random.shuffle(candidates)
    for sentence in candidates[:5]:
        words = re.findall(r"\b[A-Z][a-z]{2,}\b", sentence)
        if not words:
            words = re.findall(r"\b[a-z]{3,}\b", sentence)
        if len(words) < 3:
            continue
        random.shuffle(words)
        blank_word = words[0]
        question_stem = sentence.replace(blank_word, "_____", 1)
        distractors = _generate_distractors(blank_word, candidates, rng=random)
        if not distractors:
            continue
        options = [blank_word] + distractors[: num_options - 1]
        random.shuffle(options)
        questions.append({
            "type": "mcq",
            "question": 'What word completes: "%s"?' % question_stem,
            "options": options,
            "correct": blank_word,
            "context": sentence,
        })
        if len(questions) >= 3:
            break
    if not questions and parsed["bullet_points"]:
        for bp in parsed["bullet_points"][:5]:
            words = re.findall(r"\b[A-Z][a-z]{2,}\b", bp)
            if not words:
                words = re.findall(r"\b[a-z]{4,}\b", bp)
            if len(words) < 3:
                continue
            blank_word = random.choice(words)
            stem = bp.replace(blank_word, "_____", 1)
            distractors = _generate_distractors(blank_word, parsed["bullet_points"] + parsed["paragraphs"], rng=random)
            if not distractors:
                continue
            options = [blank_word] + distractors[:3]
            random.shuffle(options)
            questions.append({
                "type": "mcq",
                "question": 'Complete: "%s"?' % stem,
                "options": options,
                "correct": blank_word,
                "context": bp,
            })
            if len(questions) >= 3:
                break
    return questions


def _generate_distractors(word, candidates, rng=None):
    random = rng or __import__("random")
    distractors = []
    seen = {word.lower()}
    for c in candidates:
        for w in re.findall(r"\b[a-zA-Z]{3,}\b", c):
            lw = w.lower()
            if lw not in seen and len(distractors) < 6:
                seen.add(lw)
                distractors.append(w)
    random.shuffle(distractors)
    return distractors[:5]


def generate_true_false(parsed, rng=None):
    random = rng or __import__("random")
    questions = []
    sentences = []
    for p in parsed["paragraphs"]:
        sentences.extend(re.split(r"(?<=[.!?])\s+", p))
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20 and "?" not in s]
    random.shuffle(sentences)
    for s in sentences[:4]:
        q_text = s
        correct = True
        if random.random() < 0.5:
            q_text = _flip_statement(s)
            correct = False
        questions.append({
            "type": "true_false",
            "question": q_text[:200],
            "options": ["True", "False"],
            "correct": "True" if correct else "False",
            "context": s,
        })
    return questions


def _flip_statement(s):
    words = s.split()
    if len(words) < 4:
        return s
    negations = {"is": "is not", "are": "are not", "was": "was not", "were": "were not",
                 "has": "has not", "have": "have not", "do": "do not", "does": "does not",
                 "can": "cannot", "will": "will not", "would": "would not", "should": "should not",
                 "must": "must not", "may": "may not"}
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in negations:
            words[i] = negations[lw]
            return " ".join(words)
        if lw.startswith("not "):
            words[i] = w[4:]
            return " ".join(words)
    if len(words) > 2:
        words.insert(1, "not")
    return " ".join(words)


def generate_fill_blank(parsed, rng=None):
    random = rng or __import__("random")
    questions = []
    sentences = []
    for p in parsed["paragraphs"]:
        sentences.extend(re.split(r"(?<=[.!?])\s+", p))
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    random.shuffle(sentences)
    for s in sentences[:5]:
        words = re.findall(r"\b[a-zA-Z]{4,}\b", s)
        if len(words) < 4:
            continue
        key_word = None
        for w in sorted(words, key=len, reverse=True):
            if w not in ("this", "that", "these", "those", "with", "from", "have", "been", "they", "them"):
                key_word = w
                break
        if not key_word:
            continue
        stem = s.replace(key_word, "_____", 1)
        questions.append({
            "type": "fill_blank",
            "question": stem[:200],
            "options": [],
            "correct": key_word,
            "context": s,
        })
        if len(questions) >= 3:
            break
    return questions


def generate_combined_quiz(content, rng=None):
    random = rng or __import__("random")
    parsed = parse_lesson_content(content)
    mcq = generate_mcq(parsed, rng=random)
    tf = generate_true_false(parsed, rng=random)
    fb = generate_fill_blank(parsed, rng=random)
    all_questions = mcq + tf + fb
    random.shuffle(all_questions)
    return all_questions[:10]