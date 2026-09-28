"""O.L.I.V.I.A Network Server — threaded TCP server with role-based auth.

Hierarchy: King (4) > Admin (3) > Teacher (2) > Student (1)
King = the first admin to start the server; their instance is the master.
Others connect as clients and get access based on their role relative to
the target user's progress data.
"""

import json
import logging
import socket
import threading
import time
import uuid

import lesson_db as db
from network_protocol import OP, ERR_OK, ERR_AUTH, ERR_DENIED, ERR_NOT_FOUND, ERR_INTERNAL, ROLE_HIERARCHY, DEFAULT_PORT, BUF_SIZE

logger = logging.getLogger(__name__)


class Session:
    __slots__ = ("sid", "username", "role", "addr", "created")
    def __init__(self, sid, username, role, addr):
        self.sid = sid
        self.username = username
        self.role = role
        self.addr = addr
        self.created = time.time()


class NetworkServer:
    def __init__(self, host="0.0.0.0", port=DEFAULT_PORT, auth_manager=None):
        self.host = host
        self.port = port
        self.auth = auth_manager
        self.sessions = {}
        self._lock = threading.Lock()
        self._running = False
        self._sock = None
        self._thread = None

    def start(self):
        if self._running:
            return
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(1.0)
        try:
            self._sock.bind((self.host, self.port))
            self._sock.listen(16)
        except OSError as e:
            logger.error("Server bind failed on %s:%d: %s", self.host, self.port, e)
            self._sock = None
            return
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()
        logger.info("Network server listening on %s:%d", self.host, self.port)

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
        logger.info("Network server stopped")

    @property
    def is_running(self):
        return self._running

    @property
    def peer_info(self):
        return {"host": self.host, "port": self.port}

    def _serve(self):
        while self._running:
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            t = threading.Thread(target=self._handle, args=(conn, addr), daemon=True)
            t.start()

    def _handle(self, conn, addr):
        buf = b""
        conn.settimeout(30)
        try:
            while True:
                chunk = conn.recv(BUF_SIZE)
                if not chunk:
                    break
                buf += chunk
                if len(buf) > 1048576:
                    logger.warning("Buffer overflow from %s, closing", addr)
                    break
                try:
                    msg = json.loads(buf.decode())
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                resp = self._dispatch(msg, addr)
                try:
                    conn.sendall((json.dumps(resp) + "\n").encode())
                except OSError:
                    pass
                buf = b""
        except (socket.timeout, ConnectionError, OSError):
            pass
        finally:
            self._cleanup_session(addr)
            try:
                conn.close()
            except OSError:
                pass

    def _dispatch(self, msg, addr):
        op = msg.get("op", "")
        data = msg.get("data", {})
        sid = msg.get("sid")

        if op == "ping":
            return {"ok": True, "op": op}
        if op == "login":
            return self._cmd_login(data, addr)
        if op == "is_first_run":
            return {"ok": True, "op": op, "data": {"first_run": self.auth.is_first_run() if self.auth else True}}
        if op == "get_role":
            return self._cmd_get_role(sid)

        if not self._require_auth(op):
            return self._exec_cmd(op, data, None, None)

        session = self._get_session(sid, addr)
        if not session:
            return {"ok": False, "op": op, "error": ERR_AUTH}
        return self._exec_cmd(op, data, session.username, session.role)

    _NO_AUTH_OPS = {"is_first_run", "ping", "login", "get_role"}

    def _require_auth(self, op):
        return op not in self._NO_AUTH_OPS

    def _cmd_login(self, data, addr):
        username = data.get("username", "")
        password = data.get("password", "")
        if self.auth:
            role, uname = self.auth.login(username, password)
        else:
            return {"ok": False, "op": "login", "error": ERR_INTERNAL}
        if role and uname:
            sid = str(uuid.uuid4())
            with self._lock:
                self.sessions[sid] = Session(sid, uname, role, addr)
            return {"ok": True, "op": "login", "data": {"sid": sid, "username": uname, "role": role}}
        return {"ok": False, "op": "login", "error": ERR_AUTH}

    def _cmd_get_role(self, sid):
        with self._lock:
            s = self.sessions.get(sid)
        if s:
            return {"ok": True, "op": "get_role", "data": {"username": s.username, "role": s.role}}
        return {"ok": False, "op": "get_role", "error": ERR_AUTH}

    def _get_session(self, sid, addr):
        if not sid:
            return None
        with self._lock:
            return self.sessions.get(sid)

    def _cleanup_session(self, addr):
        with self._lock:
            to_del = [sid for sid, s in self.sessions.items() if s.addr == addr]
            for sid in to_del:
                del self.sessions[sid]

    def _exec_cmd(self, op, data, username, role):
        try:
            handler = getattr(self, f"_h_{op}", None)
            if handler is None:
                return {"ok": False, "op": op, "error": "unknown_op"}
            return handler(data, username, role)
        except Exception as e:
            logger.exception("Error handling op=%s: %s", op, e)
            return {"ok": False, "op": op, "error": ERR_INTERNAL, "message": str(e)}

    # ---------- Role check helper ----------
    def _check(self, role, minimum):
        return ROLE_HIERARCHY.get(role, 0) >= ROLE_HIERARCHY.get(minimum, 0)

    def _check_target(self, viewer_role, viewer_user, target_user, data):
        if viewer_role == "king":
            return True
        if viewer_user == target_user:
            return True
        if viewer_role == "admin":
            return True
        if viewer_role == "teacher":
            viewer_role_data = data
            target_roles = None
            return True
        return False

    # ========== HANDLERS ==========

    def _h_create_admin(self, data, user, role):
        if self.auth is None:
            return {"ok": False, "op": "create_admin", "error": ERR_INTERNAL, "message": "no auth manager"}
        self.auth.create_admin(data.get("username", ""), data.get("password", ""))
        return {"ok": True, "op": "create_admin"}

    def _h_add_user(self, data, user, role):
        if not self._check(role, "king"):
            return {"ok": False, "op": "add_user", "error": ERR_DENIED}
        self.auth.add_user(data["username"], data["password"], data["role"])
        return {"ok": True, "op": "add_user"}

    def _h_remove_user(self, data, user, role):
        if not self._check(role, "king"):
            return {"ok": False, "op": "remove_user", "error": ERR_DENIED}
        self.auth.remove_user(data.get("username", ""))
        return {"ok": True, "op": "remove_user"}

    def _h_list_users(self, data, user, role):
        if not self._check(role, "king"):
            return {"ok": False, "op": "list_users", "error": ERR_DENIED}
        aname, users = self.auth.list_users()
        return {"ok": True, "op": "list_users", "data": {"admin": aname, "students": users.get("students", []), "teachers": users.get("teachers", [])}}

    def _h_get_admin_username(self, data, user, role):
        return {"ok": True, "op": "get_admin_username", "data": {"admin": self.auth.get_admin_username() if self.auth else None}}

    def _h_change_admin_pw(self, data, user, role):
        if not self._check(role, "king"):
            return {"ok": False, "op": "change_admin_pw", "error": ERR_DENIED}
        ok, msg = self.auth.change_admin_password(data.get("username", user), data.get("old_pw", ""), data.get("new_pw", ""))
        if isinstance(ok, tuple):
            ok, msg = ok
        return {"ok": ok, "op": "change_admin_pw", "message": msg if not ok else ""}

    def _h_ensure_profile(self, data, user, role):
        db.ensure_profile(data.get("username", user), data.get("role", role))
        return {"ok": True, "op": "ensure_profile"}

    def _h_get_profile(self, data, user, role):
        target = data.get("username", user)
        if not self._check_target(role, user, target, data):
            return {"ok": False, "op": "get_profile", "error": ERR_DENIED}
        p = db.get_profile(target)
        return {"ok": True, "op": "get_profile", "data": p}

    def _h_update_display_name(self, data, user, role):
        db.update_display_name(data.get("username", user), data.get("name", ""))
        return {"ok": True, "op": "update_display_name"}

    def _h_record_access(self, data, user, role):
        db.record_lesson_access(user, data.get("path", ""), data.get("label", ""),
                                 data.get("curriculum", ""), data.get("grade", ""),
                                 data.get("subject", ""), data.get("difficulty", ""))
        return {"ok": True, "op": "record_access"}

    def _h_mark_complete(self, data, user, role):
        db.mark_lesson_complete(user, data.get("path", ""),
                                 data.get("time_spent", 0), data.get("score"), data.get("max_score"))
        return {"ok": True, "op": "mark_complete"}

    def _h_get_progress(self, data, user, role):
        target = data.get("username", user)
        if not self._check(role, "teacher"):
            if target != user:
                return {"ok": False, "op": "get_progress", "error": ERR_DENIED}
        path = data.get("path")
        prog = db.get_lesson_progress(target if self._check(role, "teacher") else user, path)
        return {"ok": True, "op": "get_progress", "data": prog}

    def _h_get_subject_progress(self, data, user, role):
        target = data.get("username", user)
        if not self._check(role, "teacher") and target != user:
            return {"ok": False, "op": "get_subject_progress", "error": ERR_DENIED}
        sp = db.get_subject_progress(target)
        return {"ok": True, "op": "get_subject_progress", "data": sp}

    def _h_get_student_stats(self, data, user, role):
        target = data.get("username", user)
        if target != user and not self._check(role, "teacher"):
            return {"ok": False, "op": "get_student_stats", "error": ERR_DENIED}
        stats = db.get_student_stats(target)
        return {"ok": True, "op": "get_student_stats", "data": stats}

    def _h_get_teacher_dashboard(self, data, user, role):
        if not self._check(role, "teacher"):
            return {"ok": False, "op": "get_teacher_dashboard", "error": ERR_DENIED}
        dash = db.get_teacher_dashboard(user)
        return {"ok": True, "op": "get_teacher_dashboard", "data": dash}

    def _h_get_leaderboard(self, data, user, role):
        lb = db.get_leaderboard(data.get("limit", 50))
        return {"ok": True, "op": "get_leaderboard", "data": lb}

    def _h_record_quiz_answer(self, data, user, role):
        db.record_quiz_answer(user, data.get("path", ""), data.get("question", ""),
                               data.get("correct", ""), data.get("user_answer", ""),
                               data.get("is_correct", False), data.get("qtype", "mcq"))
        return {"ok": True, "op": "record_quiz_answer"}

    def _h_save_quiz_result(self, data, user, role):
        db.save_quiz_result(user, data.get("path", ""), data.get("questions", []),
                             data.get("user_answers", []), data.get("score", 0), data.get("total", 0))
        return {"ok": True, "op": "save_quiz_result"}

    def _h_get_quiz_results(self, data, user, role):
        target = data.get("username", user)
        if target != user and not self._check(role, "teacher"):
            return {"ok": False, "op": "get_quiz_results", "error": ERR_DENIED}
        results = db.get_quiz_results(target, data.get("path"))
        return {"ok": True, "op": "get_quiz_results", "data": results}

    def _h_award_points(self, data, user, role):
        db.award_points(user, data.get("points", 0))
        return {"ok": True, "op": "award_points"}

    def _h_get_gamification(self, data, user, role):
        target = data.get("username", user)
        if target != user and not self._check(role, "teacher"):
            return {"ok": False, "op": "get_gamification", "error": ERR_DENIED}
        gam = db.get_gamification(target)
        return {"ok": True, "op": "get_gamification", "data": gam}

    def _h_add_note(self, data, user, role):
        if not self._check(role, "teacher"):
            return {"ok": False, "op": "add_note", "error": ERR_DENIED}
        db.add_teacher_note(user, data.get("student", ""), data.get("note", ""), data.get("path", ""))
        return {"ok": True, "op": "add_note"}

    def _h_get_notes(self, data, user, role):
        if not self._check(role, "teacher"):
            return {"ok": False, "op": "get_notes", "error": ERR_DENIED}
        notes = db.get_teacher_notes(user, data.get("student"))
        return {"ok": True, "op": "get_notes", "data": notes}

    def _h_log_activity(self, data, user, role):
        db.log_daily_activity(user, data.get("type", ""), data.get("amount", 1))
        return {"ok": True, "op": "log_activity"}

    def _h_get_all_users(self, data, user, role):
        if not self._check(role, "king"):
            return {"ok": False, "op": "get_all_users", "error": ERR_DENIED}
        aname, users = self.auth.list_users()
        return {"ok": True, "op": "get_all_users", "data": {"admin": aname, "students": users.get("students", []), "teachers": users.get("teachers", [])}}
