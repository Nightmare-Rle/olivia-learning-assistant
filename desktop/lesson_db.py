import sqlite3
import os, json, time, logging, threading
from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

DB_PATH = None
_local = threading.local()

def _get_db_path():
    global DB_PATH
    if DB_PATH is None:
        if getattr(__import__("sys"), "frozen", False):
            base = __import__("os").path.dirname(__import__("sys").executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(base, "olivia_data.db")
    return DB_PATH

def get_conn():
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = sqlite3.connect(_get_db_path())
        _local.conn.row_factory = sqlite3.Row
        _local.conn.execute("PRAGMA journal_mode=WAL")
        _local.conn.execute("PRAGMA foreign_keys=ON")
    return _local.conn

def init_db():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS profiles (
                username TEXT PRIMARY KEY,
                role TEXT NOT NULL CHECK(role IN ('student','teacher','admin')),
                display_name TEXT NOT NULL DEFAULT '',
                avatar TEXT DEFAULT '',
                created_at REAL NOT NULL,
                last_login REAL
            );

            CREATE TABLE IF NOT EXISTS lesson_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                lesson_path TEXT NOT NULL,
                lesson_label TEXT NOT NULL DEFAULT '',
                curriculum TEXT NOT NULL DEFAULT '',
                grade TEXT NOT NULL DEFAULT '',
                subject TEXT NOT NULL DEFAULT '',
                difficulty TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0,
                score REAL,
                max_score REAL,
                time_spent REAL DEFAULT 0,
                attempts INTEGER NOT NULL DEFAULT 1,
                last_accessed REAL NOT NULL,
                UNIQUE(username, lesson_path)
            );

            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                lesson_path TEXT NOT NULL,
                question TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                user_answer TEXT NOT NULL,
                is_correct INTEGER NOT NULL DEFAULT 0,
                question_type TEXT NOT NULL DEFAULT 'mcq',
                attempted_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS gamification (
                username TEXT PRIMARY KEY,
                total_points INTEGER NOT NULL DEFAULT 0,
                lessons_completed INTEGER NOT NULL DEFAULT 0,
                quizzes_taken INTEGER NOT NULL DEFAULT 0,
                quiz_streak INTEGER NOT NULL DEFAULT 0,
                last_quiz_date TEXT DEFAULT '',
                current_streak INTEGER NOT NULL DEFAULT 0,
                longest_streak INTEGER NOT NULL DEFAULT 0,
                badges TEXT NOT NULL DEFAULT '[]'
            );

            CREATE TABLE IF NOT EXISTS daily_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                activity_date TEXT NOT NULL,
                actions INTEGER NOT NULL DEFAULT 0,
                points_earned INTEGER NOT NULL DEFAULT 0,
                lessons_viewed INTEGER NOT NULL DEFAULT 0,
                quizzes_taken INTEGER NOT NULL DEFAULT 0,
                UNIQUE(username, activity_date)
            );

            CREATE TABLE IF NOT EXISTS teacher_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher TEXT NOT NULL,
                student TEXT NOT NULL,
                lesson_path TEXT DEFAULT '',
                note TEXT NOT NULL,
                created_at REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_lesson_progress_username ON lesson_progress(username);
            CREATE INDEX IF NOT EXISTS idx_lesson_progress_path ON lesson_progress(lesson_path);
            CREATE INDEX IF NOT EXISTS idx_quiz_results_username ON quiz_results(username);
            CREATE INDEX IF NOT EXISTS idx_quiz_results_path ON quiz_results(lesson_path);
            CREATE INDEX IF NOT EXISTS idx_daily_activity_date ON daily_activity(activity_date);
            CREATE INDEX IF NOT EXISTS idx_daily_activity_user_date ON daily_activity(username, activity_date);
            CREATE INDEX IF NOT EXISTS idx_teacher_notes_teacher ON teacher_notes(teacher);
            CREATE INDEX IF NOT EXISTS idx_teacher_notes_student ON teacher_notes(student);
        """)
        conn.commit()
    except Exception as e:
        logger.error("Failed to initialize database: %s", e)
    finally:
        conn.close()

def ensure_profile(username, role):
    conn = get_conn()
    try:
        cur = conn.cursor()
        now = time.time()
        cur.execute("INSERT OR IGNORE INTO profiles (username, role, created_at) VALUES (?, ?, ?)", (username, role, now))
        cur.execute("UPDATE profiles SET last_login = ? WHERE username = ?", (now, username))
        cur.execute("INSERT OR IGNORE INTO gamification (username) VALUES (?)", (username,))
        conn.commit()
    except Exception as e:
        logger.error("ensure_profile failed: %s", e)
    finally:
        conn.close()

def get_profile(username):
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM profiles WHERE username = ?", (username,)).fetchone()
        return dict(row) if row else None
    except Exception as e:
        logger.error("get_profile failed: %s", e)
        return None
    finally:
        conn.close()

def update_display_name(username, name):
    conn = get_conn()
    try:
        conn.execute("UPDATE profiles SET display_name = ? WHERE username = ?", (name, username))
        conn.commit()
    except Exception as e:
        logger.error("update_display_name failed: %s", e)
    finally:
        conn.close()

def record_lesson_access(username, lesson_path, lesson_label="", curriculum="", grade="", subject="", difficulty=""):
    conn = get_conn()
    try:
        now = time.time()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO lesson_progress (username, lesson_path, lesson_label, curriculum, grade, subject, difficulty, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(username, lesson_path) DO UPDATE SET
                last_accessed = excluded.last_accessed,
                lesson_label = COALESCE(NULLIF(excluded.lesson_label, ''), lesson_label),
                curriculum = COALESCE(NULLIF(excluded.curriculum, ''), curriculum),
                grade = COALESCE(NULLIF(excluded.grade, ''), grade),
                subject = COALESCE(NULLIF(excluded.subject, ''), subject),
                difficulty = COALESCE(NULLIF(excluded.difficulty, ''), difficulty)
        """, (username, lesson_path, lesson_label, curriculum, grade, subject, difficulty, now))
        conn.commit()
    except Exception as e:
        logger.error("record_lesson_access failed: %s", e)
    finally:
        conn.close()
    log_daily_activity(username, "lessons_viewed", 1)

def mark_lesson_complete(username, lesson_path, time_spent=0, score=None, max_score=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        row = cur.execute(
            "SELECT attempts, completed FROM lesson_progress WHERE username = ? AND lesson_path = ?",
            (username, lesson_path)
        ).fetchone()
        attempts = 1
        if row:
            attempts = row["attempts"] + 1 if not row["completed"] else row["attempts"]
        now = time.time()
        cur.execute("""
            INSERT INTO lesson_progress (username, lesson_path, completed, score, max_score, time_spent, attempts, last_accessed)
            VALUES (?, ?, 1, ?, ?, ?, ?, ?)
            ON CONFLICT(username, lesson_path) DO UPDATE SET
                completed = 1,
                score = COALESCE(?, score),
                max_score = COALESCE(?, max_score),
                time_spent = lesson_progress.time_spent + ?,
                attempts = ?,
                last_accessed = ?
        """, (username, lesson_path, score, max_score, time_spent, attempts, now,
              score, max_score, time_spent, attempts, now))
        conn.commit()
    except Exception as e:
        logger.error("mark_lesson_complete failed: %s", e)
    finally:
        conn.close()
    log_daily_activity(username, "lessons_viewed", 1)
    award_points(username, 10)

def get_lesson_progress(username, lesson_path=None):
    conn = get_conn()
    try:
        if lesson_path:
            row = conn.execute(
                "SELECT * FROM lesson_progress WHERE username = ? AND lesson_path = ?",
                (username, lesson_path)
            ).fetchone()
            return dict(row) if row else None
        rows = conn.execute(
            "SELECT * FROM lesson_progress WHERE username = ? ORDER BY last_accessed DESC",
            (username,)
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("get_lesson_progress failed: %s", e)
        return [] if lesson_path is None else None
    finally:
        conn.close()

def record_quiz_answer(username, lesson_path, question, correct_answer, user_answer, is_correct, question_type="mcq"):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO quiz_results (username, lesson_path, question, correct_answer, user_answer, is_correct, question_type, attempted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, lesson_path, question, correct_answer, user_answer, int(is_correct), question_type, time.time()))
        conn.commit()
    except Exception as e:
        logger.error("record_quiz_answer failed: %s", e)
    finally:
        conn.close()

def save_quiz_result(username, lesson_path, questions, user_answers, score, total):
    conn = get_conn()
    try:
        cur = conn.cursor()
        now = time.time()
        for q, user_ans in zip(questions, user_answers):
            cur.execute("""
                INSERT INTO quiz_results (username, lesson_path, question, correct_answer, user_answer, is_correct, question_type, attempted_at)
                VALUES (?, ?, ?, ?, ?, ?, 'mcq', ?)
            """, (username, lesson_path, q, q, user_ans, 0, now))
        cur.execute("""
            INSERT INTO lesson_progress (username, lesson_path, completed, score, max_score, time_spent, attempts, last_accessed)
            VALUES (?, ?, 1, ?, ?, 0, 1, ?)
            ON CONFLICT(username, lesson_path) DO UPDATE SET
                completed = 1,
                score = COALESCE(?, score),
                max_score = COALESCE(?, max_score),
                attempts = attempts + 1,
                last_accessed = ?
        """, (username, lesson_path, score, total, now, score, total, now))
        conn.commit()
    except Exception as e:
        logger.error("save_quiz_result failed: %s", e)
    finally:
        conn.close()
    log_daily_activity(username, "quizzes_taken", 1)
    update_quiz_streak(username)
    award_points(username, score * 2)
    if score == total:
        award_points(username, 20)

def get_quiz_results(username, lesson_path=None):
    conn = get_conn()
    try:
        if lesson_path:
            rows = conn.execute(
                "SELECT * FROM quiz_results WHERE username = ? AND lesson_path = ? ORDER BY attempted_at DESC",
                (username, lesson_path)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM quiz_results WHERE username = ? ORDER BY attempted_at DESC LIMIT 500",
                (username,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("get_quiz_results failed: %s", e)
        return []
    finally:
        conn.close()

def award_points(username, points):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE gamification SET total_points = total_points + ? WHERE username = ?", (points, username))
        conn.commit()
    except Exception as e:
        logger.error("award_points failed: %s", e)
    finally:
        conn.close()
    log_daily_activity(username, "points_earned", points)

def update_quiz_streak(username):
    conn = get_conn()
    try:
        cur = conn.cursor()
        row = cur.execute("SELECT last_quiz_date, current_streak, longest_streak FROM gamification WHERE username = ?", (username,)).fetchone()
        if not row:
            return
        today = date.today().isoformat()
        last = row["last_quiz_date"]
        streak = row["current_streak"]
        longest = row["longest_streak"]
        if last == today:
            pass
        elif last == (date.fromisoformat(today) - timedelta(days=1)).isoformat():
            streak += 1
        else:
            streak = 1
        longest = max(longest, streak)
        cur.execute("UPDATE gamification SET last_quiz_date = ?, current_streak = ?, longest_streak = ?, quizzes_taken = quizzes_taken + 1 WHERE username = ?",
                    (today, streak, longest, username))
        if streak > 1 and streak % 5 == 0:
            award_points(username, 50)
            add_badge(username, f"{streak}-Day Streak")
        conn.commit()
    except Exception as e:
        logger.error("update_quiz_streak failed: %s", e)
    finally:
        conn.close()

def add_badge(username, badge_name):
    conn = get_conn()
    try:
        row = conn.execute("SELECT badges FROM gamification WHERE username = ?", (username,)).fetchone()
        if not row:
            return
        badges = json.loads(row["badges"])
        if badge_name not in badges:
            badges.append(badge_name)
            conn.execute("UPDATE gamification SET badges = ? WHERE username = ?", (json.dumps(badges), username))
            conn.commit()
    except Exception as e:
        logger.error("add_badge failed: %s", e)
    finally:
        conn.close()

def get_gamification(username):
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM gamification WHERE username = ?", (username,)).fetchone()
        result = dict(row) if row else {
            "total_points": 0, "lessons_completed": 0, "quizzes_taken": 0,
            "quiz_streak": 0, "last_quiz_date": "", "current_streak": 0,
            "longest_streak": 0, "badges": "[]"
        }
        if isinstance(result.get("badges"), str):
            result["badges"] = json.loads(result["badges"])
        return result
    except Exception as e:
        logger.error("get_gamification failed: %s", e)
        return {"total_points": 0, "lessons_completed": 0, "quizzes_taken": 0, "badges": []}
    finally:
        conn.close()

def get_leaderboard(limit=20):
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT g.username, p.display_name, g.total_points, g.lessons_completed,
                   g.quizzes_taken, g.current_streak, g.badges
            FROM gamification g
            JOIN profiles p ON g.username = p.username
            WHERE p.role = 'student'
            ORDER BY g.total_points DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("get_leaderboard failed: %s", e)
        return []
    finally:
        conn.close()

def log_daily_activity(username, action_type, amount=1):
    conn = get_conn()
    try:
        today = date.today().isoformat()
        cur = conn.cursor()
        if action_type == "lessons_viewed":
            cur.execute("""
                INSERT INTO daily_activity (username, activity_date, lessons_viewed)
                VALUES (?, ?, ?)
                ON CONFLICT(username, activity_date) DO UPDATE SET
                    lessons_viewed = lessons_viewed + ?,
                    actions = actions + 1
            """, (username, today, amount, amount))
        elif action_type == "quizzes_taken":
            cur.execute("""
                INSERT INTO daily_activity (username, activity_date, quizzes_taken)
                VALUES (?, ?, ?)
                ON CONFLICT(username, activity_date) DO UPDATE SET
                    quizzes_taken = quizzes_taken + ?,
                    actions = actions + 1
            """, (username, today, amount, amount))
        elif action_type == "points_earned":
            cur.execute("""
                INSERT INTO daily_activity (username, activity_date, points_earned)
                VALUES (?, ?, ?)
                ON CONFLICT(username, activity_date) DO UPDATE SET
                    points_earned = points_earned + ?,
                    actions = actions + 1
            """, (username, today, amount, amount))
        conn.commit()
    except Exception as e:
        logger.error("log_daily_activity failed: %s", e)
    finally:
        conn.close()

def get_student_stats(username):
    conn = get_conn()
    try:
        today = date.today().isoformat()
        week_ago = (date.today() - timedelta(days=7)).isoformat()
        total_lessons = conn.execute(
            "SELECT COUNT(*) as c FROM lesson_progress WHERE username = ? AND completed = 1", (username,)
        ).fetchone()["c"]
        avg_score = conn.execute(
            "SELECT AVG(score * 1.0 / max_score) as avg FROM lesson_progress WHERE username = ? AND completed = 1 AND max_score > 0",
            (username,)
        ).fetchone()["avg"]
        total_quizzes = conn.execute(
            "SELECT COUNT(DISTINCT lesson_path) as c FROM quiz_results WHERE username = ?", (username,)
        ).fetchone()["c"]
        weekly_activity = conn.execute(
            "SELECT SUM(actions) as a FROM daily_activity WHERE username = ? AND activity_date >= ?",
            (username, week_ago)
        ).fetchone()["a"]
        gam = get_gamification(username)
        return {
            "total_lessons": total_lessons or 0,
            "avg_score": round((avg_score or 0) * 100, 1),
            "total_quizzes": total_quizzes or 0,
            "weekly_activity": weekly_activity or 0,
            "total_points": gam["total_points"],
            "current_streak": gam["current_streak"],
            "longest_streak": gam["longest_streak"],
            "badges": gam["badges"],
        }
    except Exception as e:
        logger.error("get_student_stats failed: %s", e)
        return {}
    finally:
        conn.close()

def get_teacher_dashboard(teacher):
    conn = get_conn()
    try:
        students = conn.execute(
            "SELECT username, display_name FROM profiles WHERE role = 'student' ORDER BY username"
        ).fetchall()
        student_stats = []
        for s in students:
            stats = get_student_stats(s["username"])
            stats["username"] = s["username"]
            stats["display_name"] = s["display_name"] or s["username"]
            student_stats.append(stats)
        enrolled = conn.execute("SELECT COUNT(*) as c FROM profiles WHERE role = 'student'").fetchone()["c"]
        active_today = conn.execute(
            "SELECT COUNT(DISTINCT username) as c FROM daily_activity WHERE activity_date = ?",
            (date.today().isoformat(),)
        ).fetchone()["c"]
        today_lessons = conn.execute(
            "SELECT SUM(lessons_viewed) as c FROM daily_activity WHERE activity_date = ?",
            (date.today().isoformat(),)
        ).fetchone()["c"]
        return {
            "students": student_stats,
            "enrolled": enrolled,
            "active_today": active_today or 0,
            "today_lessons": today_lessons or 0,
        }
    except Exception as e:
        logger.error("get_teacher_dashboard failed: %s", e)
        return {"students": [], "enrolled": 0, "active_today": 0, "today_lessons": 0}
    finally:
        conn.close()

def get_subject_progress(username):
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT curriculum, grade, subject, COUNT(*) as total, SUM(completed) as done FROM lesson_progress WHERE username = ? GROUP BY curriculum, grade, subject",
            (username,)
        ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("get_subject_progress failed: %s", e)
        return []
    finally:
        conn.close()

def add_teacher_note(teacher, student, note, lesson_path=""):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO teacher_notes (teacher, student, lesson_path, note, created_at) VALUES (?, ?, ?, ?, ?)",
            (teacher, student, lesson_path, note, time.time())
        )
        conn.commit()
    except Exception as e:
        logger.error("add_teacher_note failed: %s", e)
    finally:
        conn.close()

def get_teacher_notes(teacher, student=None):
    conn = get_conn()
    try:
        if student:
            rows = conn.execute(
                "SELECT * FROM teacher_notes WHERE teacher = ? AND student = ? ORDER BY created_at DESC",
                (teacher, student)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM teacher_notes WHERE teacher = ? ORDER BY created_at DESC",
                (teacher,)
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("get_teacher_notes failed: %s", e)
        return []
    finally:
        conn.close()
