import hashlib, json, os, sys, secrets, time, threading

PBKDF2_ITERATIONS = 600000
MAX_ATTEMPTS = 5
ATTEMPT_WINDOW = 300
LOCKOUT_DURATION = 30

_lock = threading.Lock()
_login_cache = {}

def _get_cred_path():
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "credentials.json")

def _hash_pw(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERATIONS).hex()
    return h, salt

def _verify_pw(password, stored_hash, salt):
    h, _ = _hash_pw(password, salt)
    return secrets.compare_digest(h.encode(), stored_hash.encode())

def _get_lockout_status(username):
    now = time.time()
    entry = _login_cache.get(username)
    if not entry:
        return "ok", 0
    if now - entry["start"] > ATTEMPT_WINDOW:
        _login_cache.pop(username, None)
        return "ok", 0
    if entry["count"] >= MAX_ATTEMPTS:
        remaining = int(entry.get("locked_until", 0) - now)
        if remaining > 0:
            return "locked", remaining
        _login_cache.pop(username, None)
        return "ok", 0
    return "ok", 0

def _record_attempt(username):
    now = time.time()
    entry = _login_cache.get(username)
    if not entry:
        _login_cache[username] = {"start": now, "count": 1, "locked_until": 0}
    else:
        if now - entry["start"] > ATTEMPT_WINDOW:
            _login_cache[username] = {"start": now, "count": 1, "locked_until": 0}
        else:
            entry["count"] += 1
            if entry["count"] >= MAX_ATTEMPTS:
                entry["locked_until"] = now + LOCKOUT_DURATION

def _lock_and_load():
    with _lock:
        path = _get_cred_path()
        if not os.path.exists(path):
            return {"admin": None, "users": {}}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def _lock_and_save(data):
    with _lock:
        path = _get_cred_path()
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)

def is_first_run():
    data = _lock_and_load()
    return data["admin"] is None

def create_admin(username, password):
    data = _lock_and_load()
    if data["admin"] is not None:
        return False
    h, salt = _hash_pw(password)
    data["admin"] = {"username": username, "password": h, "salt": salt, "role": "admin"}
    _lock_and_save(data)
    _login_cache.clear()
    return True

def login(username, password):
    status, remaining = _get_lockout_status(username)
    if status == "locked":
        return None, f"Try again in {remaining} seconds."
    data = _lock_and_load()
    if data.get("admin") and data["admin"]["username"] == username:
        if _verify_pw(password, data["admin"]["password"], data["admin"]["salt"]):
            _login_cache.pop(username, None)
            return "admin", data["admin"]["username"]
    for uid, uinfo in data.get("users", {}).items():
        if uinfo.get("username") == username:
            if _verify_pw(password, uinfo["password"], uinfo["salt"]):
                _login_cache.pop(username, None)
                return uinfo["role"], uinfo["username"]
    _record_attempt(username)
    status, remaining = _get_lockout_status(username)
    if status == "locked":
        return None, f"Try again in {remaining} seconds."
    return None, "Invalid username or password"

def add_user(username, password, role):
    data = _lock_and_load()
    h, salt = _hash_pw(password)
    uid = f"{role}_{username}"
    data["users"][uid] = {"username": username, "password": h, "salt": salt, "role": role}
    _lock_and_save(data)
    return True

def remove_user(username):
    data = _lock_and_load()
    to_del = None
    for uid, uinfo in data.get("users", {}).items():
        if uinfo.get("username") == username:
            to_del = uid
            break
    if to_del:
        del data["users"][to_del]
        _lock_and_save(data)
        return True
    return False

def list_users():
    data = _lock_and_load()
    result = {"students": [], "teachers": []}
    for uid, uinfo in data.get("users", {}).items():
        role = uinfo["role"]
        if role == "student":
            result["students"].append(uinfo["username"])
        elif role == "teacher":
            result["teachers"].append(uinfo["username"])
    admin_name = data["admin"]["username"] if data.get("admin") else None
    return admin_name, result

def change_admin_password(username, old_pw, new_pw):
    data = _lock_and_load()
    if not data.get("admin"):
        return False, "No admin account"
    if not _verify_pw(old_pw, data["admin"]["password"], data["admin"]["salt"]):
        return False, "Current password is incorrect"
    h, salt = _hash_pw(new_pw)
    data["admin"] = {"username": username, "password": h, "salt": salt, "role": "admin"}
    _lock_and_save(data)
    return True, "Password changed"

def get_admin_username():
    data = _lock_and_load()
    if data.get("admin"):
        return data["admin"]["username"]
    return None

def get_user_role(username):
    data = _lock_and_load()
    if data.get("admin") and data["admin"]["username"] == username:
        return "admin"
    for uid, uinfo in data.get("users", {}).items():
        if uinfo.get("username") == username:
            return uinfo["role"]
    return None
