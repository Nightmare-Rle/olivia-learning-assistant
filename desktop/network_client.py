"""O.L.I.V.I.A Network Client — wrapper around TCP connections to a remote server.

Auto-reconnects on connection drop. Caches session id (sid) per server.
"""

import json
import logging
import socket
import time

from network_protocol import OP, DEFAULT_PORT, BUF_SIZE, TIMEOUT

logger = logging.getLogger(__name__)


class NetworkClient:
    def __init__(self, host="127.0.0.1", port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.sid = None
        self.username = None
        self.role = None
        self._sock = None
        self._buf = b""
        self._connected = False

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        try:
            sock.connect((self.host, self.port))
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            logger.warning("Could not connect to %s:%d: %s", self.host, self.port, e)
            return False
        self._sock = sock
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    @property
    def connected(self):
        return self._connected

    def login(self, username, password):
        resp = self._send({"op": "login", "data": {"username": username, "password": password}})
        if resp and resp.get("ok"):
            self.sid = resp["data"]["sid"]
            self.username = resp["data"]["username"]
            self.role = resp["data"]["role"]
            return True
        return False

    def get_role(self):
        resp = self._send({"op": "get_role", "sid": self.sid})
        if resp and resp.get("ok"):
            return resp["data"]["role"]
        return None

    # ---------- Auth ----------
    def is_first_run(self):
        resp = self._send({"op": "is_first_run"})
        return resp.get("data", {}).get("first_run", True) if resp else True

    def create_admin(self, username, password):
        resp = self._send({"op": "create_admin", "data": {"username": username, "password": password}})
        return resp.get("ok", False) if resp else False

    def add_user(self, username, password, role):
        resp = self._call("add_user", {"username": username, "password": password, "role": role})
        return resp.get("ok", False) if resp else False

    def remove_user(self, username):
        resp = self._call("remove_user", {"username": username})
        return resp.get("ok", False) if resp else False

    def list_users(self):
        resp = self._call("list_users", {})
        if resp and resp.get("ok"):
            d = resp["data"]
            return d["admin"], {"students": d["students"], "teachers": d["teachers"]}
        return None, {"students": [], "teachers": []}

    def get_admin_username(self):
        resp = self._call("get_admin_username", {})
        return resp.get("data", {}).get("admin") if resp else None

    def change_admin_password(self, username, old_pw, new_pw):
        resp = self._call("change_admin_pw", {"username": username, "old_pw": old_pw, "new_pw": new_pw})
        if resp and resp.get("ok"):
            return True, resp.get("message", "Password changed")
        return resp.get("message") if resp else (False, "Connection error")

    # ---------- Profile ----------
    def ensure_profile(self, username, role):
        self._call("ensure_profile", {"username": username, "role": role})

    def get_profile(self, username=None):
        resp = self._call("get_profile", {"username": username or self.username})
        return resp.get("data") if resp else None

    def update_display_name(self, name):
        self._call("update_display_name", {"name": name})

    # ---------- Progress ----------
    def record_access(self, path, label="", curriculum="", grade="", subject="", difficulty=""):
        self._call("record_access", {"path": path, "label": label, "curriculum": curriculum,
                                      "grade": grade, "subject": subject, "difficulty": difficulty})

    def mark_complete(self, path, time_spent=0, score=None, max_score=None):
        self._call("mark_complete", {"path": path, "time_spent": time_spent, "score": score, "max_score": max_score})

    def get_progress(self, username=None, path=None):
        data = {}
        if username:
            data["username"] = username
        if path:
            data["path"] = path
        resp = self._call("get_progress", data)
        return resp.get("data") if resp else []

    def get_subject_progress(self, username=None):
        resp = self._call("get_subject_progress", {"username": username or self.username})
        return resp.get("data", []) if resp else []

    def get_student_stats(self, username=None):
        resp = self._call("get_student_stats", {"username": username or self.username})
        return resp.get("data", {}) if resp else {}

    def get_teacher_dashboard(self):
        resp = self._call("get_teacher_dashboard", {})
        return resp.get("data", {"students": [], "enrolled": 0, "active_today": 0, "today_lessons": 0}) if resp else {"students": [], "enrolled": 0, "active_today": 0, "today_lessons": 0}

    def get_leaderboard(self, limit=50):
        resp = self._call("get_leaderboard", {"limit": limit})
        return resp.get("data", []) if resp else []

    # ---------- Quiz ----------
    def record_quiz_answer(self, path, question, correct, user_answer, is_correct, qtype="mcq"):
        self._call("record_quiz_answer", {"path": path, "question": question, "correct": correct,
                                           "user_answer": user_answer, "is_correct": is_correct, "qtype": qtype})

    def save_quiz_result(self, path, questions, user_answers, score, total):
        self._call("save_quiz_result", {"path": path, "questions": questions, "user_answers": user_answers,
                                         "score": score, "total": total})

    def get_quiz_results(self, username=None, path=None):
        data = {}
        if username:
            data["username"] = username
        if path:
            data["path"] = path
        resp = self._call("get_quiz_results", data)
        return resp.get("data", []) if resp else []

    # ---------- Gamification ----------
    def award_points(self, points):
        self._call("award_points", {"points": points})

    def get_gamification(self, username=None):
        resp = self._call("get_gamification", {"username": username or self.username})
        return resp.get("data", {}) if resp else {}

    # ---------- Notes ----------
    def add_note(self, student, note, path=""):
        self._call("add_note", {"student": student, "note": note, "path": path})

    def get_notes(self, student=None):
        data = {}
        if student:
            data["student"] = student
        resp = self._call("get_notes", data)
        return resp.get("data", []) if resp else []

    # ---------- Activity ----------
    def log_activity(self, atype, amount=1):
        self._call("log_activity", {"type": atype, "amount": amount})

    # ---------- Internal ----------
    def _call(self, op, data):
        return self._send({"op": op, "data": data, "sid": self.sid})

    def _send(self, msg):
        if not self._connected:
            if not self.connect():
                return None
        try:
            payload = json.dumps(msg) + "\n"
            self._sock.sendall(payload.encode())
            resp = self._recv()
            return resp
        except (ConnectionError, socket.timeout, OSError):
            self.disconnect()
            return None

    def _recv(self):
        while True:
            if "\n" in self._buf:
                line, self._buf = self._buf.split("\n", 1)
                return json.loads(line.decode())
            try:
                chunk = self._sock.recv(BUF_SIZE)
                if not chunk:
                    self.disconnect()
                    return None
                self._buf += chunk
            except (socket.timeout, ConnectionError, OSError):
                self.disconnect()
                return None
