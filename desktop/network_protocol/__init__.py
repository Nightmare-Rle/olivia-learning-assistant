"""Shared protocol definitions for O.L.I.V.I.A network layer."""

ROLE_HIERARCHY = {"king": 4, "admin": 3, "teacher": 2, "student": 1}
DEFAULT_PORT = 9876
DISCOVERY_PORT = 9877
DISCOVERY_MSG = b"OLIVIA_DISCOVER"
DISCOVERY_RESP = b"OLIVIA_HERE"
BUF_SIZE = 8192
TIMEOUT = 5.0

OP = {
    # Auth
    "LOGIN": "login",
    "IS_FIRST_RUN": "is_first_run",
    "CREATE_ADMIN": "create_admin",
    "ADD_USER": "add_user",
    "REMOVE_USER": "remove_user",
    "LIST_USERS": "list_users",
    "GET_ADMIN_USERNAME": "get_admin_username",
    "CHANGE_ADMIN_PW": "change_admin_pw",
    # Profiles
    "ENSURE_PROFILE": "ensure_profile",
    "GET_PROFILE": "get_profile",
    "UPDATE_DISPLAY_NAME": "update_display_name",
    # Progress
    "RECORD_ACCESS": "record_access",
    "MARK_COMPLETE": "mark_complete",
    "GET_PROGRESS": "get_progress",
    "GET_SUBJECT_PROGRESS": "get_subject_progress",
    "GET_STUDENT_STATS": "get_student_stats",
    "GET_TEACHER_DASHBOARD": "get_teacher_dashboard",
    "GET_LEADERBOARD": "get_leaderboard",
    # Quiz
    "RECORD_QUIZ_ANSWER": "record_quiz_answer",
    "SAVE_QUIZ_RESULT": "save_quiz_result",
    "GET_QUIZ_RESULTS": "get_quiz_results",
    # Gamification
    "AWARD_POINTS": "award_points",
    "GET_GAMIFICATION": "get_gamification",
    # Notes
    "ADD_NOTE": "add_note",
    "GET_NOTES": "get_notes",
    # Activity
    "LOG_ACTIVITY": "log_activity",
    # Discovery / meta
    "PING": "ping",
    "GET_ROLE": "get_role",
    "GET_ALL_USERS": "get_all_users",
}

ERR_OK = "ok"
ERR_AUTH = "auth_required"
ERR_DENIED = "permission_denied"
ERR_NOT_FOUND = "not_found"
ERR_INTERNAL = "internal_error"
