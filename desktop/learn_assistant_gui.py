import socket
import os
import webbrowser
import random
import json
import logging
import threading
import re
from urllib.parse import quote_plus
from tkinter import messagebox, filedialog
import learning_data
import auth_manager
import lesson_db
import quiz_engine
import backup_manager
import network_server
import network_client
import discovery
import lesson_renderer
from network_protocol import ROLE_HIERARCHY, DEFAULT_PORT

_PIL_AVAIL = True
_TRANSLATOR_AVAIL = True

logger = logging.getLogger(__name__)

UI_TR = {
    "english": {
        "select_role": "Select your role to sign in",
        "welcome_back": "Welcome back",
        "welcome_status": "Welcome back, {user}!  |  {role}  |  {language}",
        "signed_in_as": "Signed in as",
        "language": "Language / Wika:",
        "k12_learning": "K-12 Learning",
        "college_programs": "College Programs",
        "web_search": "Web Search",
        "markdown_reader": "Markdown Reader",
        "answer_sheets": "Answer Sheets",
        "admin_panel": "Admin Panel",
        "home": "Home",
        "click_to_open": "Click to open",
        "internet": "Internet:",
        "connected": "Connected",
        "offline": "Offline",
        "open_md_file": "Open .md File",
        "no_file_opened": "No file opened",
        "search_placeholder": "Search Google or enter URL...",
        "search": "Search",
        "official_portals": "Official Education Portals:",
        "general_search": "General Search:",
        "answer_keys_on": "Answer Keys: ON",
        "grade_levels": "Grade Levels",
        "subjects_difficulties": "Subjects & Difficulties",
        "select_grade": "Select a grade from the left",
        "categories": "Categories",
        "programs_difficulties": "Programs & Difficulties",
        "select_category": "Select a category from the left",
        "my_progress": "My Progress",
        "leaderboard": "Leaderboard",
        "analytics": "Analytics",
        "admin_title": "Admin Panel",
        "click_student_for_details": "Click student for details",
        "new_badge": "New Badge Earned!",
        "perfect_score_bonus": "Perfect Score Bonus!",
        "rank": "Rank",
        "role": "Role:",
        "share_lesson": "Share",
        "streak_bonus": "Streak Bonus!",
        "student_analytics": "Student Analytics",
        "king_view": "King View",
        "quiz": "Quiz",
        "take_quiz": "Take Quiz",
        "submit_quiz": "Submit Quiz",
        "quiz_result": "Quiz Result",
        "your_score": "Your Score",
        "correct": "Correct",
        "incorrect": "Incorrect",
        "next_question": "Next",
        "question_of": "Question {n} of {total}",
        "points_earned": "Points Earned",
        "total_points": "Total Points",
        "streak": "Streak",
        "badges": "Badges",
        "lessons_completed": "Lessons Completed",
        "quizzes_taken": "Quizzes Taken",
        "avg_score": "Average Score",
        "weekly_activity": "Weekly Activity",
        "enrolled_students": "Enrolled Students",
        "active_today": "Active Today",
        "back_to_lesson": "Back to Lesson",
        "select_lesson_first": "Open a lesson first, then take a quiz",
        "student": "Student",
        "teacher": "Teacher",
        "admin": "Admin",
        "progress_overview": "Progress Overview",
        "sign_in": "Sign In",
        "first_run_title": "First-Time Setup \u2014 Create Admin Account",
        "confirm": "Confirm:",
        "create_admin": "Create Admin Account",
        "sign_in_title": "Sign In",
        "no_results": "No results found",
        "visit_lrmds": "Visit LRMDS",
        "visit_ched": "Visit CHED",
        "official_deped": "Official DepEd Portal",
        "official_ched": "Official CHED Portal",
        "log_out": "Log Out",
        # ?? Main tabs ??
        "k12_learning_materials": "K-12 Learning Materials",
        "college_learning_materials": "College Learning Materials",
        "imported_files": "Imported Files",
        "create_documents": "Create",
        "my_content": "My Content",
        # ?? Web Search ??
        "enter_url_or_search": "Enter URL or search...",
        "open_in_browser": "Open in Browser",
        "quick_links": "Quick Links  \u2014  Opens in your default browser",
        # ?? K-12 details ??
        "subjects_info": "{subjects} subjects from {grades} grade levels + LRMDS Portal",
        "select_grade_level": "Select a grade level",
        "back_to_grade_levels": "< Back to Grade Levels",
        # ?? College details ??
        "programs_info": "programs from {count} categories + CHED Portal",
        "select_category_short": "Select a category",
        "back_to_categories": "< Back to Categories",
        # ?? Markdown Reader ??
        "language_label": "Language:",
        "could_not_open_file": "Could not open file:\n{error}",
        # ?? Imported Files ??
        "import_folder": "Import Folder",
        "save": "Save",
        "history": "History",
        "open_externally": "Open Externally",
        "filter_all": "All",
        "filter_images": "Images",
        "filter_pdfs": "PDFs",
        "filter_videos": "Videos",
        "filter_text": "Text",
        "filter_other": "Other",
        "imported_empty_hint": "Click \'Import Folder\' to add files",
        "no_files_imported": "No files imported yet",
        "no_category_found": "No {category} found",
        "open": "Open",
        "play": "Play",
        "pause": "Pause",
        "stop": "Stop",
        "saved": "Saved!",
        "edit": "Edit",
        "cancel": "Cancel",
        "save_copy": "Save Copy",
        "file_saved": "File saved",
        "save_failed": "Save failed: {error}",
        "version_restored": "Version restored!",
        "version_history": "Version History",
        "no_previous_versions": "No previous versions found.",
        "restore": "Restore",
        "restore_version_confirm": "Replace current file with this version?",
        # ?? Document Editor ??
        "upload_tab": "Upload",
        "create_label": "Create:",
        "create_document": "+ Document",
        "create_slide": "+ Slide",
        "save_as": "Save As",
        "close": "Close",
        "ready": "Ready",
        "add_user": "Add User",
        "answer_sheets_title": "Answer Sheets \u2014 All Assessments",
        "back": "< Back",
        "backup_restore": "Backup & Restore",
        "change_password": "Change Password",
        "confirm_new": "Confirm New:",
        "create_backup": "Create Backup",
        "current_password": "Current Password:",
        "manage_users": "Manage Users",
        "new_password": "New Password:",
        "no_answer_sheets": "No answer sheets found",
        "no_data_yet": "No data yet. Start learning!",
        "no_programs": "No programs found",
        "no_students_yet": "No students enrolled yet",
        "no_subjects": "No subjects found",
        "password": "Password:",
        "refresh": "Refresh",
        "remove": "Remove",
        "restore_backup": "Restore Backup",
        "search_answer": "Search by subject, grade, or program...",
        "subject_progress": "Subject Progress",
        "username": "Username:",
        "username_leaderboard": "Username",
        "new_document": "New document",
        "insert_image": "Insert Image",
        "open_file": "Open File",
        "resize_image": "Resize Image",
        "width": "Width:",
        "height": "Height:",
        "keep_aspect_ratio": "Keep aspect ratio",
        "resize": "Resize",
        "file_error": "Error: {error}",
        # ?? Slide Editor ??
        "slides": "Slides",
        "add_slide": "+ Add Slide",
        "delete_selected": "\u2715 Delete Selected",
        "close_tab": "Close Tab",
        "background": "Background",
        "image": "Image",
        "slide_nav": "Slide {current} of {total}",
        "slide_added": "Slide added",
        "slide_background_title": "Slide Background",
        "open_presentation": "Open Presentation",
        # ?? Create Upload ??
        "upload_file": "Upload File",
        "uploaded_will_appear": "Uploaded files will appear here",
        "no_files_uploaded": "No files uploaded yet",
        "select_file_upload": "Select file to upload",
        "uploaded": "Uploaded: {filename}",
        # ?? Answer Sheets ??
        "show_all_answers": "Show All Answers",
        "no_answer_key": "No answer key found in this file.",
        "no_answer_key_available": "  No answer key available",
        "all_answer_keys": "ALL ANSWER KEYS",
        "full_content_label": "Full content:",
        # ?? Admin - Manage Users ??
        "students_label": "Students",
        "teachers_label": "Teachers",
        "fill_all_fields": "Fill all fields",
        "password_too_short": "Password too short (min 4)",
        "user_added": "{role} \'{user}\' added!",
        "user_removed": "\'{username}\' removed",
        "confirm_remove_user": "Remove user \'{username}\'?",
        "change_admin_password": "Change Admin Password",
        "new_passwords_no_match": "New passwords do not match",
        # ?? Admin - Backup ??
        "backup_created": "Backup created: {path} ({size})",
        "select_backup_restore": "Select backup to restore",
        "confirm_restore": "This will restore credentials and study materials.\nContinue?",
        "restored_to": "Restored to: {directory}",
        # ?? Admin - Generate Curriculum ??
        "full_generate": "Full Generate",
        "prompt_lesson": "Prompt Lesson",
        "generate_all_curriculum": "Generate All Curriculum",
        "generate_now": "Generate Now",
        "generating": "Generating...",
        "running": "Running...",
        "complete": "Complete!",
        "gen_success": "Curriculum generation complete!\nYou may need to restart the app to see new content.",
        "gen_error": "Error",
        # ?? Prompt Lesson ??
        "create_lesson_with_prompt": "Create a Lesson with a Prompt",
        "level": "Level:",
        "grade_category": "Grade / Category:",
        "subject_course": "Subject / Course:",
        "lesson_title": "Lesson Title:",
        "lesson_content": "Lesson Content (write in markdown, use ### for headings):",
        "lesson_content_placeholder": "Enter your lesson content here...\\n\\n### Topic 1\\nDetails about topic 1.\\n\\n### Topic 2\\nDetails about topic 2.",
        "generate_lesson": "Generate Lesson",
        "no_options": "No options",
        "missing_title": "Missing Title",
        "missing_title_msg": "Please enter a lesson title.",
        "missing_content": "Missing Content",
        "missing_content_msg": "Please write meaningful lesson content (at least 20 characters).",
        "saved_to_custom": "Saved to Custom_Lessons",
        "success": "Success",
        "lesson_saved": "Lesson \'{title}\' saved!\nLocation: Custom_Lessons/{level_key}_{subject_key}/\n\nView it in the \'My Content\' tab.",
        # ?? My Content ??
        "my_created_lessons": "My Created Lessons & Worksheets",
        "new_lesson": "+ New Lesson",
        "no_custom_lessons": "No custom lessons yet.",
        # ?? General ??
        "error": "Error",
        "confirm_title": "Confirm",
        "log_out_confirm": "Are you sure you want to log out?",
        "invalid_usr_pw": "Invalid username or password",
        "enter_usr_pw": "Enter username and password",
        "usr_pw_required": "Username and password required",
        "pw_no_match": "Passwords do not match",
        "pw_too_short": "Password must be at least 4 characters",
        "no_role_account": "No {role} account with that username",
        "keys_on": "  |  Keys: ON",
        "student_performance": "Student Performance",
        # ?? Home Cards ??
        "k12_card_subtitle": "{grades} grade levels\n{subjects} subjects",
        "college_card_subtitle": "{cats} categories\n{progs} programs",
        "search_subtitle": "Google search, URL browsing",
        "reader_subtitle": "Read, edit & practice",
        "create_subtitle": "Create lessons, quizzes & practice materials",
        "imported_subtitle": "Import external lesson files",
        "content_subtitle": "My created content library",
        "analytics_subtitle": "Performance & activity trends",
        "admin_subtitle": "User management, system settings",
        "explore_lessons": "Explore K-12",
        "explore_programs": "Explore College",
        "browse_label": "Browse Web",
        "read_label": "Open Files",
        "create_label": "Create Materials",
        "import_label": "Import Lessons",
        "assess_label": "Answer Sheets",
        "content_label": "My Content",
        "analytics_label": "View Analytics",
        "progress_label": "Track Progress",
        "admin_label": "Manage System",
        # ?? Login ??
        "sign_in_title_extra": "Sign In - {role}",
        # ?? K-12/College ??
        "grade_title": "{grade} - Subjects",
        "cat_title": "{cat} - Programs",
        "college_info": "{progs} programs from {cats} categories + CHED Portal",
        "grade_btn": "{grade}  ({count} subjects)",
        "cat_btn": "{cat}  ({count} programs)",
        # ?? Import ??
        "select_folder_import": "Select folder to import",
        "no_category_items": "No {cat} found",
        # ?? Version History ??
        "version_history_title": "Version History - {name}",
        "version_history_label": "Version History: {name}",
        # ?? Slide viewer ??
        "slide_page": "Slide {current} of {total}",
        "slide_number": "Slide {n}",
        # ?? Answer sheets ??
        "ans_count": "     {count} answers",
        "ans_summary": "  {with_key}/{total} assessments have answer keys\n\n",
        # ?? General UI ??
        "no_categories": "No categories found",
        "untitled": "Untitled",
        "error_status": "Error: {err}",
        "saved_file": "Saved: {fname}",
        "opened_file": "Opened: {fname}",
        "uploaded_file": "Uploaded: {fname}",
        "doc_tab": "Doc {n}",
        "slide_tab": "Slide {n}",
    },
    "tagalog": {
        "select_role": "Pumili ng iyong tungkulin upang mag-sign in",
        "welcome_back": "Maligayang pagbabalik",
        "welcome_status": "Maligayang pagbabalik, {user}!  |  {role}  |  {language}",
        "signed_in_as": "Naka-sign in bilang",
        "language": "Wika / Language:",
        "k12_learning": "Pag-aaral ng K-12",
        "college_programs": "Programang Kolehiyo",
        "web_search": "Paghahanap sa Web",
        "markdown_reader": "Pagbasa ng Markdown",
        "answer_sheets": "Sagutang Papel",
        "admin_panel": "Panel ng Admin",
        "home": "Tahanan",
        "click_to_open": "Pindutin upang buksan",
        "internet": "Internet:",
        "connected": "Konektado",
        "offline": "Offline",
        "open_md_file": "Buksan ang .md File",
        "no_file_opened": "Walang bukas na file",
        "search_placeholder": "Maghanap sa Google o maglagay ng URL...",
        "search": "Maghanap",
        "official_portals": "Opisyal na Portal ng Edukasyon:",
        "general_search": "Pangkalahatang Paghahanap:",
        "answer_keys_on": "Sagutang Papel: NAKA-ON",
        "grade_levels": "Antas ng Baitang",
        "subjects_difficulties": "Asignatura at Antas ng Hirap",
        "select_grade": "Pumili ng baitang mula sa kaliwa",
        "categories": "Mga Kategorya",
        "programs_difficulties": "Programa at Antas ng Hirap",
        "select_category": "Pumili ng kategorya mula sa kaliwa",
        "answer_sheets_title": "Sagutang Papel \u2014 Lahat ng Assessment",
        "search_answer": "Maghanap ayon sa asignatura, baitang, o programa...",
        "refresh": "I-refresh",
        "admin_title": "Panel ng Admin",
        "manage_users": "Pamahalaan ang mga User",
        "backup_restore": "Backup at Restore",
        "change_password": "Palitan ang Password",
        "no_answer_sheets": "Walang nakitang sagutang papel",
        "no_subjects": "Walang nakitang asignatura",
        "no_programs": "Walang nakitang programa",
        "create_backup": "Gumawa ng Backup",
        "restore_backup": "I-restore ang Backup",
        "add_user": "Magdagdag ng User",
        "remove": "Tanggalin",
        "username": "Username:",
        "password": "Password:",
        "role": "Tungkulin:",
        "current_password": "Kasalukuyang Password:",
        "new_password": "Bagong Password:",
        "confirm_new": "Kumpirmahin ang Bago:",
        "back": "< Bumalik",
        "admin": "Admin",
        "teacher": "Guro",
        "student": "Mag-aaral",
        "sign_in": "Mag-sign In",
        "first_run_title": "Unang Pag-setup \u2014 Gumawa ng Admin Account",
        "confirm": "Kumpirmahin:",
        "create_admin": "Gumawa ng Admin Account",
        "sign_in_title": "Mag-sign In",
        "no_results": "Walang nakitang resulta",
        "visit_lrmds": "Bisitahin ang LRMDS",
        "visit_ched": "Bisitahin ang CHED",
        "official_deped": "Opisyal na Portal ng DepEd",
        "official_ched": "Opisyal na Portal ng CHED",
        "log_out": "Mag-log Out",
        # ?? Main tabs ??
        "k12_learning_materials": "Mga Materyales ng Pag-aaral ng K-12",
        "college_learning_materials": "Mga Materyales ng Pag-aaral ng Kolehiyo",
        "imported_files": "Mga Na-import na File",
        "create_documents": "Lumikha",
        "my_content": "Aking Nilalaman",
        # ?? Web Search ??
        "enter_url_or_search": "Magpasok ng URL o maghanap...",
        "open_in_browser": "Buksan sa Browser",
        "quick_links": "Mabilis na Link  \u2014  Bubuksan sa iyong default na browser",
        # ?? K-12 details ??
        "subjects_info": "{subjects} asignatura mula sa {grades} baitang + LRMDS Portal",
        "select_grade_level": "Pumili ng baitang",
        "back_to_grade_levels": "< Bumalik sa mga Baitang",
        # ?? College details ??
        "programs_info": "{count} programa mula sa mga kategorya + CHED Portal",
        "select_category_short": "Pumili ng kategorya",
        "back_to_categories": "< Bumalik sa mga Kategorya",
        # ?? Markdown Reader ??
        "language_label": "Wika:",
        "could_not_open_file": "Hindi mabuksan ang file:\n{error}",
        # ?? Imported Files ??
        "import_folder": "Mag-import ng Folder",
        "save": "I-save",
        "history": "Kasaysayan",
        "open_externally": "Buksan sa Labas",
        "filter_all": "Lahat",
        "filter_images": "Mga Larawan",
        "filter_pdfs": "Mga PDF",
        "filter_videos": "Mga Video",
        "filter_text": "Teksto",
        "filter_other": "Iba Pa",
        "imported_empty_hint": "Pindutin ang \'Mag-import ng Folder\' upang magdagdag ng mga file",
        "no_files_imported": "Wala pang na-import na file",
        "no_category_found": "Walang nakitang {category}",
        "open": "Buksan",
        "play": "I-play",
        "pause": "I-pause",
        "stop": "Ihinto",
        "saved": "Nai-save!",
        "edit": "I-edit",
        "cancel": "Kanselahin",
        "save_copy": "I-save ang Kopya",
        "file_saved": "Nai-save ang file",
        "save_failed": "Hindi nai-save: {error}",
        "version_restored": "Na-restore ang bersyon!",
        "version_history": "Kasaysayan ng Bersyon",
        "no_previous_versions": "Walang nakitang nakaraang bersyon.",
        "restore": "I-restore",
        "restore_version_confirm": "Palitan ang kasalukuyang file ng bersyong ito?",
        # ?? Document Editor ??
        "upload_tab": "Mag-upload",
        "create_label": "Lumikha:",
        "create_document": "+ Dokumento",
        "create_slide": "+ Slide",
        "save_as": "I-save Bilang",
        "close": "Isara",
        "ready": "Handa",
        "new_document": "Bagong dokumento",
        "insert_image": "Magsingit ng Larawan",
        "open_file": "Buksan ang File",
        "resize_image": "Baguhin ang Laki ng Larawan",
        "width": "Lapad:",
        "height": "Taas:",
        "keep_aspect_ratio": "Panatilihin ang aspect ratio",
        "resize": "Baguhin ang Laki",
        "file_error": "Error: {error}",
        # ?? Slide Editor ??
        "slides": "Mga Slide",
        "add_slide": "+ Magdagdag ng Slide",
        "delete_selected": "\u2715 Burahin ang Napili",
        "close_tab": "Isara ang Tab",
        "background": "Background",
        "image": "Larawan",
        "slide_nav": "Slide {current} ng {total}",
        "slide_added": "Idinagdag ang slide",
        "slide_background_title": "Background ng Slide",
        "open_presentation": "Buksan ang Presentation",
        # ?? Create Upload ??
        "upload_file": "Mag-upload ng File",
        "uploaded_will_appear": "Lilitaw dito ang mga na-upload na file",
        "no_files_uploaded": "Wala pang na-upload na file",
        "select_file_upload": "Pumili ng file na i-upload",
        "uploaded": "Na-upload: {filename}",
        # ?? Answer Sheets ??
        "show_all_answers": "Ipakita Lahat ng Sagot",
        "no_answer_key": "Walang nakitang sagot sa file na ito.",
        "no_answer_key_available": "  Walang available na sagot",
        "all_answer_keys": "LAHAT NG SAGOT",
        "full_content_label": "Buong nilalaman:",
        # ?? Admin - Manage Users ??
        "students_label": "Mga Mag-aaral",
        "teachers_label": "Mga Guro",
        "fill_all_fields": "Punan ang lahat ng field",
        "password_too_short": "Masyadong maikli ang password (min 4)",
        "user_added": "Idinagdag si {role} \'{user}\'!",
        "user_removed": "Tinanggal si \'{username}\'",
        "confirm_remove_user": "Tanggalin ang user na \'{username}\'?",
        "change_admin_password": "Palitan ang Admin Password",
        "new_passwords_no_match": "Hindi tugma ang mga bagong password",
        # ?? Admin - Backup ??
        "backup_created": "Backup na ginawa: {path} ({size})",
        "select_backup_restore": "Pumili ng backup na i-restore",
        "confirm_restore": "Ire-restore nito ang credentials at study materials.\nMagpatuloy?",
        "restored_to": "Na-restore sa: {directory}",
        # ?? Admin - Generate Curriculum ??
        "full_generate": "Buong Pag-generate",
        "prompt_lesson": "Aralin sa Prompt",
        "generate_all_curriculum": "I-generate Lahat ng Kurikulum",
        "generate_now": "I-generate Ngayon",
        "generating": "Ginenera...",
        "running": "Tumatakbo...",
        "complete": "Tapos!",
        "gen_success": "Kumpleto ang pag-generate ng kurikulum!\nMaaaring kailanganin mong i-restart ang app upang makita ang bagong nilalaman.",
        "gen_error": "Error",
        # ?? Prompt Lesson ??
        "create_lesson_with_prompt": "Gumawa ng Aralin gamit ang Prompt",
        "level": "Antas:",
        "grade_category": "Baitang / Kategorya:",
        "subject_course": "Asignatura / Kurso:",
        "lesson_title": "Pamagat ng Aralin:",
        "lesson_content": "Nilalaman ng Aralin (isulat sa markdown, gamitin ang ### para sa mga heading):",
        "lesson_content_placeholder": "Ilagay ang nilalaman ng iyong aralin dito...\\n\\n### Paksa 1\\nMga detalye tungkol sa paksa 1.\\n\\n### Paksa 2\\nMga detalye tungkol sa paksa 2.",
        "generate_lesson": "Gumawa ng Aralin",
        "no_options": "Walang opsyon",
        "missing_title": "Kulang ang Pamagat",
        "missing_title_msg": "Mangyaring magpasok ng pamagat ng aralin.",
        "missing_content": "Kulang ang Nilalaman",
        "missing_content_msg": "Mangyaring sumulat ng makabuluhang nilalaman ng aralin (hindi bababa sa 20 karakter).",
        "saved_to_custom": "Nai-save sa Custom_Lessons",
        "success": "Tagumpay",
        "lesson_saved": "Ang aralin na \'{title}\' ay nai-save!\nLokasyon: Custom_Lessons/{level_key}_{subject_key}/\n\nTingnan ito sa tab na \'My Content\'.",
        # ?? My Content ??
        "my_created_lessons": "Aking mga Ginawang Aralin at Worksheets",
        "new_lesson": "+ Bagong Aralin",
        "no_custom_lessons": "Wala pang custom na aralin.",
        # ?? General ??
        "error": "Error",
        "confirm_title": "Kumpirmahin",
        "log_out_confirm": "Sigurado ka bang gusto mong mag-log out?",
        "invalid_usr_pw": "Maling username o password",
        "enter_usr_pw": "Ilagay ang username at password",
        "usr_pw_required": "Kinakailangan ang username at password",
        "pw_no_match": "Hindi tugma ang mga password",
        "pw_too_short": "Ang password ay dapat na hindi bababa sa 4 na karakter",
        "no_role_account": "Walang {role} account na may username na iyon",
        "keys_on": "  |  Keys: NAKA-ON",
        # ?? Home Cards ??
        "k12_card_subtitle": "{grades} baitang\n{subjects} asignatura",
        "college_card_subtitle": "{cats} kategorya\n{progs} programa",
        "search_subtitle": "Google search, pag-browse URL",
        "reader_subtitle": "Magbasa, mag-edit at magsanay",
        "create_subtitle": "Gumawa ng aralin, pagsusulit at materyal",
        "imported_subtitle": "Mag-import ng lesson files",
        "content_subtitle": "Aking nilikhang content library",
        "analytics_subtitle": "Pagganap at trend ng aktibidad",
        "admin_subtitle": "Pamamahala ng user, system settings",
        "explore_lessons": "Galugarin K-12",
        "explore_programs": "Galugarin Kolehiyo",
        "browse_label": "Mag-browse Web",
        "read_label": "Buksan File",
        "create_label": "Gumawa ng Materyal",
        "import_label": "Mag-import Aralin",
        "assess_label": "Sagutang Papel",
        "content_label": "Aking Nilalaman",
        "analytics_label": "Tingnan Analytics",
        "progress_label": "Subaybayan Pag-unlad",
        "admin_label": "Pamahalaan Sistema",
        # ?? Login ??
        "sign_in_title_extra": "Sign In - {role}",
        # ?? K-12/College ??
        "grade_title": "{grade} - Mga Asignatura",
        "cat_title": "{cat} - Mga Programa",
        "college_info": "{progs} programa mula sa {cats} kategorya + CHED Portal",
        "grade_btn": "{grade}  ({count} asignatura)",
        "cat_btn": "{cat}  ({count} programa)",
        # ?? Import ??
        "select_folder_import": "Pumili ng folder upang i-import",
        "no_category_items": "Walang nakitang {cat}",
        # ?? Version History ??
        "version_history_title": "Kasaysayan ng Bersyon - {name}",
        "version_history_label": "Kasaysayan ng Bersyon: {name}",
        # ?? Slide viewer ??
        "slide_page": "Slide {current} ng {total}",
        "slide_number": "Slide {n}",
        # ?? Answer sheets ??
        "ans_count": "     {count} sagot",
        "ans_summary": "  {with_key}/{total} assessments ay may answer key\n\n",
        # ?? General UI ??
        "no_categories": "Walang nakitang kategorya",
        "untitled": "Walang Pamagat",
        "error_status": "Error: {err}",
        "saved_file": "Na-save: {fname}",
        "opened_file": "Binuksan: {fname}",
        "uploaded_file": "Na-upload: {fname}",
        "doc_tab": "Doc {n}",
        "slide_tab": "Slide {n}",
        "my_progress": "Aking Progress",
        "leaderboard": "Ranggo",
        "analytics": "Analytics",
        "quiz": "Pagsusulit",
        "take_quiz": "Kumuha ng Pagsusulit",
        "submit_quiz": "Ipasa ang Pagsusulit",
        "quiz_result": "Resulta ng Pagsusulit",
        "your_score": "Iyong Iskor",
        "correct": "Tama",
        "incorrect": "Mali",
        "next_question": "Susunod",
        "question_of": "Tanong {n} ng {total}",
        "points_earned": "Nakuhang Puntos",
        "total_points": "Kabuuang Puntos",
        "streak": "Sunod-sunod",
        "badges": "Mga Badge",
        "lessons_completed": "Natapos na Aralin",
        "quizzes_taken": "Kinuhang Pagsusulit",
        "avg_score": "Katamtamang Iskor",
        "weekly_activity": "Aktibidad ng Linggo",
        "enrolled_students": "Mga Naka-enroll na Mag-aaral",
        "active_today": "Aktibo Ngayon",
        "back_to_lesson": "Bumalik sa Aralin",
        "select_lesson_first": "Magbukas muna ng aralin bago kumuha ng pagsusulit",
        "student": "Mag-aaral",
        "teacher": "Guro",
        "admin": "Admin",
        "progress_overview": "Pangkalahatang Progress",
        "no_data_yet": "Wala pang data. Magsimulang matuto!",
        "student_performance": "Student Performance",
        "student_analytics": "Analytics ng Mag-aaral",
        "subject_progress": "Progress sa Asignatura",
        "click_student_for_details": "Pindutin ang mag-aaral para sa detalye",
        "no_students_yet": "Wala pang naka-enroll na mag-aaral",
        "rank": "Ranggo",
        "username_leaderboard": "Username",
        "perfect_score_bonus": "Bonus sa Perpektong Iskor!",
        "streak_bonus": "Bonus sa Sunod-sunod!",
        "new_badge": "Bagong Badge Nakuha!",
        "share_lesson": "I-share",
    },
}

import customtkinter as ctk
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

SUBJECT_EMOJI_MAP = [
    ("mathematics", "📐"), ("math", "📐"), ("algebra", "📐"), ("geometry", "📐"), ("calculus", "∫"),
    ("trigonometry", "📐"), ("statistics", "📊"), ("probability", "📊"),
    ("science", "🔬"), ("biology", "🧬"), ("chemistry", "🧪"), ("physics", "⚛️"),
    ("earth and life", "🌍"), ("earth science", "🌍"), ("physical science", "⚛️"),
    ("english", "📖"), ("reading and literacy", "📚"), ("reading", "📚"), ("writing", "✍️"),
    ("literacy", "📚"), ("language", "🗣️"),
    ("filipino", "🇵🇭"),
    ("araling panlipunan", "🌏"), ("social studies", "🌏"),
    ("edukasyon sa pagpapakatao", "💛"), ("esp", "💛"), ("values education", "💎"),
    ("mapeh", "🎨"), ("music", "🎵"), ("arts", "🎭"), ("pe ", "🏃"), ("health", "💪"),
    ("physical education", "🏃"),
    ("tle", "🔧"), ("technology and livelihood", "🔧"),
    ("computer", "💻"), ("ict", "💻"), ("it ", "💻"), ("information technology", "💻"),
    ("computer science", "💻"), ("programming", "👨‍💻"),
    ("engineering", "⚙️"),
    ("business", "💼"), ("accounting", "💰"), ("accountancy", "💰"), ("economics", "📈"),
    ("education", "📝"), ("teaching", "📝"),
    ("nursing", "🩺"),
    ("psychology", "🧠"),
    ("criminology", "🔍"),
    ("hospitality", "🏨"), ("tourism", "🗺️"),
    ("agriculture", "🌾"),
    ("history", "📜"),
    ("grammar", "📝"),
    ("media and information", "📺"), ("media", "📺"),
    ("personal development", "🌱"),
    ("philosophy", "🤔"),
    ("religion", "⛪"),
    ("cookery", "🍳"), ("drafting", "📏"),
    ("electronics", "⚡"), ("welding", "🔩"),
    ("dressmaking", "🧵"),
    ("homeroom guidance", "🏠"),
    ("catch-up", "📅"),
    ("reference", "📋"),
]

SUBJECT_COLOR_MAP = [
    ("mathematics", "#64B5F6"), ("math", "#64B5F6"), ("algebra", "#64B5F6"), ("calculus", "#42A5F5"),
    ("statistics", "#42A5F5"), ("probability", "#42A5F5"),
    ("science", "#81C784"), ("biology", "#66BB6A"), ("chemistry", "#FFB74D"), ("physics", "#BA68C8"),
    ("earth and life", "#4DB6AC"), ("earth science", "#4DB6AC"), ("physical science", "#BA68C8"),
    ("english", "#5C6BC0"), ("reading and literacy", "#BA68C8"), ("reading", "#BA68C8"),
    ("writing", "#BA68C8"), ("literacy", "#BA68C8"), ("language", "#5C6BC0"),
    ("filipino", "#EF9A9A"),
    ("araling panlipunan", "#4DB6AC"), ("social studies", "#4DB6AC"),
    ("edukasyon sa pagpapakatao", "#FFD54F"), ("esp", "#FFD54F"), ("values education", "#FFD54F"),
    ("mapeh", "#FFB74D"), ("music", "#BA68C8"), ("arts", "#E57373"),
    ("pe ", "#64B5F6"), ("health", "#81C784"), ("physical education", "#64B5F6"),
    ("tle", "#78909C"), ("technology and livelihood", "#78909C"),
    ("computer", "#4DB6AC"), ("ict", "#4DB6AC"), ("it ", "#4DB6AC"), ("information technology", "#4DB6AC"),
    ("computer science", "#4DB6AC"), ("programming", "#4DB6AC"),
    ("engineering", "#FFB74D"),
    ("business", "#64B5F6"), ("accounting", "#64B5F6"), ("accountancy", "#64B5F6"), ("economics", "#64B5F6"),
    ("education", "#BA68C8"), ("teaching", "#BA68C8"),
    ("nursing", "#EF9A9A"),
    ("psychology", "#CE93D8"),
    ("criminology", "#78909C"),
    ("hospitality", "#FFB74D"), ("tourism", "#4DB6AC"),
    ("agriculture", "#81C784"),
    ("media and information", "#64B5F6"), ("media", "#64B5F6"),
    ("personal development", "#CE93D8"),
    ("philosophy", "#BA68C8"),
    ("homeroom guidance", "#FFD54F"),
    ("reference", "#B0BEC5"),
]

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False

k12_data = learning_data.scan_k12()
college_data = learning_data.scan_college()

class LearnAssistantGUI:
    def __init__(self):
        lesson_db.init_db()
        self.window = ctk.CTk()
        self.window.title("O.L.I.V.I.A: Online Learning Intelligent Interactive Assistant")
        self.window.geometry("1200x800")
        self.window.minsize(1000, 700)
        self.online = is_connected()
        self.current_role = None
        self.current_user = None
        self._selected_role = None
        self.answer_sheets_data = []
        self.language = "english"
        self._translation_cache = {}
        self._current_filepath = None
        self._current_raw_content = None
        self._current_answer_sheet = None
        self._current_md_label = ""
        self.imported_files = []
        self.imported_folder = None
        self._editing_path = None
        self._editing_md = False
        self._active_image = None
        self._drag_data = None
        # Networking
        self.net_server = network_server.NetworkServer(auth_manager=auth_manager)
        self.net_discovery = discovery.DiscoveryListener()
        self.net_clients = {}
        self._net_lock = threading.Lock()
        self._king_mode = False
        self._start_networking()
        self._show_login()

    def _start_networking(self):
        try:
            self.net_server.start()
            self.net_discovery.start()
        except Exception as e:
            logger.warning("Network startup: %s", e)

    def _discover_peers(self):
        """Returns list of (NetworkClient, dict) for discovered peers."""
        peers = []
        try:
            found = discovery.discover_peers(timeout=2.0)
        except Exception as e:
            logger.warning("Peer discovery error: %s", e)
            return peers
        for info in found:
            key = f"{info['host']}:{info['port']}"
            with self._net_lock:
                if key not in self.net_clients:
                    cl = network_client.NetworkClient(info["host"], info["port"])
                    if cl.connect():
                        self.net_clients[key] = cl
                        peers.append((cl, info))
                    else:
                        try:
                            cl.disconnect()
                        except Exception:
                            pass
                else:
                    peers.append((self.net_clients[key], info))
        return peers

    def _get_remote_students(self, clients):
        """Collect student stats from all connected peers (for teacher/admin/king)."""
        all_students = []
        for cl, _ in clients:
            try:
                dash = cl.get_teacher_dashboard()
                all_students.extend(dash.get("students", []))
                admin_name = cl.get_admin_username()
                if admin_name:
                    role_info = cl.get_role()
                    if role_info:
                        all_students.append({
                            "username": admin_name,
                            "display_name": admin_name,
                            "total_points": 0, "total_lessons": 0,
                            "total_quizzes": 0, "avg_score": 0,
                            "current_streak": 0, "badges": [],
                            "weekly_activity": 0, "_remote": True,
                            "_host": cl.host,
                        })
            except Exception as e:
                logger.warning("Remote fetch error from %s: %s", cl.host, e)
        return all_students

    def _show_login(self):
        self.login_frame = ctk.CTkFrame(self.window, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.login_frame.pack(fill="both", expand=True)
        container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.40, anchor="center")
        ctk.CTkLabel(container, text="O.L.I.V.I.A.", font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#2C3E50").pack(pady=(0, 2))
        ctk.CTkLabel(container, text="Online Learning Intelligent Virtual Interactive Assistant",
                     font=ctk.CTkFont(size=14), text_color="#5D6D7E").pack()
        ctk.CTkLabel(container, text="Created by NightmareRLE  |  Rights reserved to N_RLE group",
                     font=ctk.CTkFont(size=10), text_color="#95A5A6").pack(pady=(0, 10))
        k12_count = sum(len(subj) for subj in k12_data.values())
        college_count = sum(len(prog) for prog in college_data.values())
        ctk.CTkLabel(container, text=f"K-12 ({k12_count} subjects)  |  College ({college_count} programs)",
                     font=ctk.CTkFont(size=12), text_color="#7F8C8D").pack(pady=(0, 15))
        ctk.CTkLabel(container, text=self._tr("select_role"), font=ctk.CTkFont(size=16, weight="bold"), text_color="#2C3E50").pack(pady=(0, 10))
        self._show_role_selection(container)

    def _show_role_selection(self, container):
        role_frame = ctk.CTkFrame(container, fg_color="transparent")
        role_frame.pack()
        roles = [
            ("\U0001F393  " + self._tr("student"), "student"),
            ("\U0001F4DA  " + self._tr("teacher"), "teacher"),
            ("\u2699\uFE0F  " + self._tr("admin"), "admin"),
        ]
        for i, (text, role) in enumerate(roles):
            ctk.CTkButton(role_frame, text=text, width=200, height=55,
                           font=ctk.CTkFont(size=16, weight="bold"),
                           fg_color="#EBF5FB", text_color="#2C3E50", hover_color="#D4E6F1",
                           border_width=2, border_color="#A9CCE3",
                           command=lambda r=role: self._on_role_selected(r)).grid(row=0, column=i, padx=10, pady=10)

    def _on_role_selected(self, role):
        for w in self.login_frame.winfo_children():
            w.destroy()
        container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.40, anchor="center")
        ctk.CTkLabel(container, text="O.L.I.V.I.A.", font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#2C3E50").pack(pady=(0, 2))
        ctk.CTkLabel(container, text="Online Learning Intelligent Virtual Interactive Assistant",
                     font=ctk.CTkFont(size=14), text_color="#5D6D7E").pack()
        ctk.CTkLabel(container, text="Created by NightmareRLE  |  Rights reserved to N_RLE group",
                     font=ctk.CTkFont(size=10), text_color="#95A5A6").pack(pady=(0, 10))
        back_btn = ctk.CTkButton(container, text=self._tr("back"), width=80, height=28, font=ctk.CTkFont(size=12),
                                  command=lambda: self._back_to_role_selection())
        back_btn.pack(anchor="w", pady=(0, 5))
        self._selected_role = role
        if role == "admin" and auth_manager.is_first_run():
            self._show_first_run_form(container, role)
        else:
            self._show_login_form(container, role)

    def _back_to_role_selection(self):
        for w in self.login_frame.winfo_children():
            w.destroy()
        container = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        container.place(relx=0.5, rely=0.40, anchor="center")
        ctk.CTkLabel(container, text="O.L.I.V.I.A.", font=ctk.CTkFont(size=36, weight="bold"),
                     text_color="#2C3E50").pack(pady=(0, 2))
        ctk.CTkLabel(container, text="Online Learning Intelligent Virtual Interactive Assistant",
                     font=ctk.CTkFont(size=14), text_color="#5D6D7E").pack()
        ctk.CTkLabel(container, text="Created by NightmareRLE  |  Rights reserved to N_RLE group",
                     font=ctk.CTkFont(size=10), text_color="#95A5A6").pack(pady=(0, 10))
        k12_count = sum(len(subj) for subj in k12_data.values())
        college_count = sum(len(prog) for prog in college_data.values())
        ctk.CTkLabel(container, text=f"K-12 ({k12_count} subjects)  |  College ({college_count} programs)",
                     font=ctk.CTkFont(size=12), text_color="#7F8C8D").pack(pady=(0, 15))
        ctk.CTkLabel(container, text=self._tr("select_role"), font=ctk.CTkFont(size=16, weight="bold"), text_color="#2C3E50").pack(pady=(0, 10))
        self._show_role_selection(container)

    def _show_first_run_form(self, container, role):
        ctk.CTkLabel(container, text="First-Time Setup \u2014 Create Admin Account",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#2C3E50").pack(pady=(0, 10))
        form = ctk.CTkFrame(container, fg_color="transparent")
        form.pack()
        ctk.CTkLabel(form, text=self._tr("username"), font=ctk.CTkFont(size=14), text_color="#2C3E50").grid(row=0, column=0, sticky="w", pady=8)
        self.fr_username = ctk.CTkEntry(form, width=260, font=ctk.CTkFont(size=13))
        self.fr_username.grid(row=0, column=1, pady=8, padx=(10, 0))
        ctk.CTkLabel(form, text=self._tr("password"), font=ctk.CTkFont(size=14), text_color="#2C3E50").grid(row=1, column=0, sticky="w", pady=8)
        self.fr_password = ctk.CTkEntry(form, width=260, font=ctk.CTkFont(size=13), show="*")
        self.fr_password.grid(row=1, column=1, pady=8, padx=(10, 0))
        ctk.CTkLabel(form, text=self._tr("confirm"), font=ctk.CTkFont(size=14), text_color="#2C3E50").grid(row=2, column=0, sticky="w", pady=8)
        self.fr_confirm = ctk.CTkEntry(form, width=260, font=ctk.CTkFont(size=13), show="*")
        self.fr_confirm.grid(row=2, column=1, pady=8, padx=(10, 0))
        self.fr_status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=12), text_color="#7F8C8D")
        self.fr_status.grid(row=3, column=0, columnspan=2, pady=8)
        ctk.CTkButton(form, text=self._tr("create_admin"), command=self._do_first_run,
                      width=200, height=40, font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#2E86C1", hover_color="#1B4F72").grid(row=4, column=0, columnspan=2, pady=(15, 0))

    def _do_first_run(self):
        u = self.fr_username.get().strip()
        p = self.fr_password.get()
        c = self.fr_confirm.get()
        if not u or not p:
            self.fr_status.configure(text=self._tr("usr_pw_required"))
            return
        if p != c:
            self.fr_status.configure(text=self._tr("pw_no_match"))
            return
        if len(p) < 4:
            self.fr_status.configure(text=self._tr("pw_too_short"))
            return
        auth_manager.create_admin(u, p)
        self.current_role = "admin"
        self.current_user = u
        lesson_db.ensure_profile(u, "admin")
        self.login_frame.destroy()
        self._build_main_ui()

    def _show_login_form(self, container, role):
        role_label = {"student": self._tr("student"), "teacher": self._tr("teacher"), "admin": self._tr("admin")}
        ctk.CTkLabel(container, text=f"Sign In \u2014 {role_label.get(role, role.title())}",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#2C3E50").pack(pady=(0, 10))
        form = ctk.CTkFrame(container, fg_color="transparent")
        form.pack()
        ctk.CTkLabel(form, text=self._tr("username"), font=ctk.CTkFont(size=14), text_color="#2C3E50").grid(row=0, column=0, sticky="w", pady=8)
        self.login_username = ctk.CTkEntry(form, width=260, font=ctk.CTkFont(size=13))
        self.login_username.grid(row=0, column=1, pady=8, padx=(10, 0))
        self.login_username.bind("<Return>", lambda e: self.login_password.focus())
        ctk.CTkLabel(form, text=self._tr("password"), font=ctk.CTkFont(size=14), text_color="#2C3E50").grid(row=1, column=0, sticky="w", pady=8)
        self.login_password = ctk.CTkEntry(form, width=260, font=ctk.CTkFont(size=13), show="*")
        self.login_password.grid(row=1, column=1, pady=8, padx=(10, 0))
        self.login_password.bind("<Return>", lambda e: self._do_login())
        self.login_status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=12), text_color="#7F8C8D")
        self.login_status.grid(row=2, column=0, columnspan=2, pady=8)
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(15, 0))
        ctk.CTkButton(btn_frame, text=self._tr("sign_in"), command=self._do_login, width=120,
                      height=38, font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#2E86C1", hover_color="#1B4F72").pack(side="left", padx=5)

    def _do_login(self):
        u = self.login_username.get().strip()
        p = self.login_password.get()
        if not u or not p:
            self.login_status.configure(text=self._tr("enter_usr_pw"))
            return
        result = auth_manager.login(u, p)
        if isinstance(result, tuple) and len(result) == 2:
            role, uname = result
        else:
            role, uname = None, None
        if role is None:
            if isinstance(uname, str) and "Too many" in uname:
                self.login_status.configure(text=uname)
                m = re.search(r"in (\d+)", uname)
                self._start_lockout_timer(int(m.group(1)) if m else 30)
            elif isinstance(uname, str):
                self.login_status.configure(text=uname)
            else:
                self.login_status.configure(text=self._tr("invalid_usr_pw"))
            return
        if role != self._selected_role:
            self.login_status.configure(text=f"No {self._selected_role} account with that username")
            return
        self.current_role = role
        self.current_user = uname
        lesson_db.ensure_profile(uname, role)
        # Network peer discovery
        self._king_mode = False
        clients = self._discover_peers()
        if role == "admin" and clients:
            self._king_mode = True
        elif role == "admin":
            self._king_mode = True
        for cl, info in clients:
            try:
                cl.login(u, p)
            except Exception:
                pass
        self.login_frame.destroy()
        self._build_main_ui()

    def _build_main_ui(self):
        net_emoji = "\U0001f60a" if self.online else "\U0001f634"
        net_text = self._tr("connected") if self.online else self._tr("offline")
        net_color = "#000000"
        self.tab_view = ctk.CTkTabview(self.window, width=1100, height=650)
        self.tab_view.pack(pady=(5, 0), padx=5, fill="both", expand=True)
        self.tab_home = self.tab_view.add(self._tr("home"))
        self.tab_k12 = self.tab_view.add(self._tr("k12_learning"))
        self.tab_college = self.tab_view.add(self._tr("college_programs"))
        self.tab_search = self.tab_view.add(self._tr("web_search"))
        self.tab_md = self.tab_view.add(self._tr("markdown_reader"))
        if self.current_role == "student":
            self.tab_progress = self.tab_view.add(self._tr("my_progress"))
        self.tab_leaderboard = self.tab_view.add(self._tr("leaderboard"))
        if self.current_role in ("teacher", "admin"):
            self.tab_answer = self.tab_view.add(self._tr("answer_sheets"))
            self.tab_imported = self.tab_view.add(self._tr("imported_files"))
            self.tab_create = self.tab_view.add(self._tr("create_documents"))
            self.tab_mycontent = self.tab_view.add(self._tr("my_content"))
            self.tab_analytics = self.tab_view.add(self._tr("analytics"))
        if self.current_role == "admin":
            self.tab_admin = self.tab_view.add(self._tr("admin_panel"))
        if self._king_mode:
            self.tab_network = self.tab_view.add(self._tr("king_view"))
        self.setup_home_tab()
        self.setup_k12_tab()
        self.setup_college_tab()
        self.setup_search_tab()
        self.setup_md_tab()
        if self.current_role == "student":
            self.setup_progress_tab()
        self.setup_leaderboard_tab()
        if self.current_role in ("teacher", "admin"):
            self.setup_answer_sheets_tab()
            self.setup_imported_tab()
            self.setup_create_tab()
            self.setup_mycontent_tab()
            self.setup_analytics_tab()
        if self.current_role == "admin":
            self.setup_admin_tab()
        if self._king_mode:
            self.setup_king_tab()
        self.status_frame = ctk.CTkFrame(self.window, fg_color="transparent", height=28)
        self.status_frame.pack(fill="x", padx=10, pady=(2, 5))
        ctk.CTkLabel(self.status_frame, text=f"{net_emoji} {net_text}",
                     font=ctk.CTkFont(size=10), text_color=net_color).pack(side="left")
        ctk.CTkLabel(self.status_frame, text=f"  |  {self.current_user} ({self.current_role})",
                     font=ctk.CTkFont(size=10), text_color="#5D6D7E").pack(side="left")
        k12_count = sum(len(subj) for subj in k12_data.values())
        college_count = sum(len(prog) for prog in college_data.values())
        ctk.CTkLabel(self.status_frame, text=f"  |  K-12: {k12_count}  |  College: {college_count}",
                     font=ctk.CTkFont(size=10), text_color="#5D6D7E").pack(side="left")
        if self.current_role in ("teacher", "admin"):
            ctk.CTkLabel(self.status_frame, text=self._tr("keys_on"), font=ctk.CTkFont(size=10),
                         text_color="#5D6D7E").pack(side="left")
        ctk.CTkLabel(self.status_frame, text=f"  |  {self.language.title()}", font=ctk.CTkFont(size=10),
                     text_color="#5D6D7E").pack(side="left")
        if self._king_mode:
            peer_count = len(self.net_clients)
            ctk.CTkLabel(self.status_frame, text=f"  |  King ({peer_count} peers)", font=ctk.CTkFont(size=10),
                         text_color="#E67E22").pack(side="left")
        self.logout_btn = ctk.CTkButton(self.status_frame, text=self._tr("log_out"), width=60, height=22,
                                        font=ctk.CTkFont(size=9), fg_color="#E74C3C", hover_color="#C0392B",
                                        command=self._logout)
        self.logout_btn.pack(side="right", padx=(0, 5))

    def _logout(self):
        if messagebox.askyesno(self._tr("log_out"), self._tr("log_out_confirm")):
            self.current_role = None
            self.current_user = None
            self._selected_role = None
            for w in (self.tab_view, self.status_frame):
                w.destroy()
            self._show_login()

    def setup_home_tab(self):
        main_frame = ctk.CTkFrame(self.tab_home)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        header_area = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_area.grid(row=0, column=0, sticky="ew", pady=(25, 5))
        header_area.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header_area, text="O.L.I.V.I.A.", font=ctk.CTkFont(size=32, weight="bold"),
                     text_color="#2C3E50", anchor="w").pack(anchor="w")
        ctk.CTkLabel(header_area, text="Online Learning Intelligent Virtual Interactive Assistant",
                     font=ctk.CTkFont(size=14), text_color="#5D6D7E", anchor="w").pack(anchor="w")
        ctk.CTkLabel(header_area, text=self._tr("welcome_status").format(user=self.current_user, role=self.current_role.title(), language=self.language.title()),
                     font=ctk.CTkFont(size=14), text_color="#7F8C8D", anchor="w").pack(anchor="w")
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=20)
        k12_count = sum(len(subj) for subj in k12_data.values())
        college_count = sum(len(prog) for prog in college_data.values())
        cards_data = [
            ("\U0001F4DA", self._tr("k12_learning"), self._tr("k12_card_subtitle").format(grades=len(k12_data), subjects=k12_count), "#E8F0FE", self._tr("k12_learning"), self._tr("explore_lessons")),
            ("\U0001F393", self._tr("college_programs"), self._tr("college_card_subtitle").format(cats=len(college_data), progs=college_count), "#E6F4EA", self._tr("college_programs"), self._tr("explore_programs")),
            ("\U0001F50D", self._tr("web_search"), "", "#FEF7E0", self._tr("web_search"), self._tr("browse_label")),
            ("\U0001F4DD", self._tr("markdown_reader"), "", "#F3E8FD", self._tr("markdown_reader"), self._tr("read_label")),
        ]
        if self.current_role in ("teacher", "admin"):
            cards_data.append(("\u270F\uFE0F", self._tr("create_documents"), "", "#FCE8E6", self._tr("create_documents"), self._tr("create_label")))
            cards_data.append(("\U0001F4C2", self._tr("imported_files"), "", "#E1F5FE", self._tr("imported_files"), self._tr("import_label")))
            sheets = learning_data.scan_answer_sheets()
            cards_data.append(("\u2705", self._tr("answer_sheets"), f"{len(sheets)} assessments\nwith answer keys", "#FCE4EC", self._tr("answer_sheets"), self._tr("assess_label")))
            cards_data.append(("\U0001F4C1", self._tr("my_content"), "", "#F3E8FD", self._tr("my_content"), self._tr("content_label")))
            cards_data.append(("\U0001F4CA", self._tr("analytics"), "", "#FFF3E0", self._tr("analytics"), self._tr("analytics_label")))
        if self.current_role == "student":
            try:
                stats = lesson_db.get_student_stats(self.current_user)
            except Exception:
                stats = {"total_points": 0, "total_lessons": 0, "current_streak": 0}
            cards_data.append(("\U0001F4C8", self._tr("my_progress"), f"{stats.get('total_points', 0)} pts | {stats.get('total_lessons', 0)} lessons | Streak: {stats.get('current_streak', 0)}", "#E8F5E9", self._tr("my_progress"), self._tr("progress_label")))
        if self.current_role == "admin":
            cards_data.append(("\u2699\uFE0F", self._tr("admin_panel"), "", "#ECEFF1", self._tr("admin_panel"), self._tr("admin_label")))
        cols = 3 if len(cards_data) >= 6 else 2
        for i in range(cols):
            content_frame.grid_columnconfigure(i, weight=1)
        rows_needed = (len(cards_data) + cols - 1) // cols
        for i in range(rows_needed):
            content_frame.grid_rowconfigure(i, weight=1)
        for i, (emoji, title, desc, color, tab_name, label) in enumerate(cards_data):
            r, c = divmod(i, cols)
            try:
                card = ctk.CTkFrame(content_frame, fg_color=color, corner_radius=15, border_width=1, border_color="#E0E0E0", height=110)
                card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
                card.grid_propagate(False)
                card.grid_columnconfigure(1, weight=1)
                card.grid_rowconfigure(0, weight=1)
                emoji_lbl = ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=36), text_color="#2C3E50")
                emoji_lbl.grid(row=0, column=0, padx=(15, 6), pady=8, sticky="ns")
                text_frame = ctk.CTkFrame(card, fg_color="transparent")
                text_frame.grid(row=0, column=1, padx=(0, 10), pady=8, sticky="nsew")
                text_frame.grid_columnconfigure(0, weight=1)
                text_frame.grid_rowconfigure(0, weight=0)
                text_frame.grid_rowconfigure(1, weight=0)
                text_frame.grid_rowconfigure(2, weight=1)
                ctk.CTkLabel(text_frame, text=label, font=ctk.CTkFont(size=11, weight="normal"), text_color="#5D6D7E", anchor="sw").grid(row=0, column=0, sticky="sw")
                ttl_lbl = ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color="#2C3E50", wraplength=200, justify="left", anchor="nw")
                ttl_lbl.grid(row=1, column=0, sticky="nw", pady=(2, 2))
                if desc:
                    ctk.CTkLabel(text_frame, text=desc, font=ctk.CTkFont(size=10), text_color="#5D6D7E", justify="left", wraplength=220, anchor="nw").grid(row=2, column=0, padx=(0, 4), sticky="nw")
                ctk.CTkLabel(text_frame, text=self._tr("click_to_open"), font=ctk.CTkFont(size=10), text_color="#7F8C8D", anchor="se").grid(row=2, column=0, sticky="se")
                for w in (card, emoji_lbl, text_frame):
                    w.configure(cursor="hand2")
                    w.bind("<Button-1>", lambda e, t=tab_name: self.tab_view.set(t), add="+")
                for child in text_frame.winfo_children():
                    child.configure(cursor="hand2")
                    child.bind("<Button-1>", lambda e, t=tab_name: self.tab_view.set(t), add="+")
            except Exception as ex:
                print(f"Card render error: {ex}")
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.grid(row=2, column=0, sticky="ew", pady=(10, 15))
        online_color = "#000000"
        online_text = self._tr("connected") if self.online else self._tr("offline")
        ctk.CTkLabel(info_frame, text=self._tr("internet"), font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
        ctk.CTkLabel(info_frame, text=online_text, font=ctk.CTkFont(size=13), text_color=online_color).pack(side="left")

    def _on_k12_lang_change(self, *args):
        if getattr(self, "_lang_changing", False):
            return
        self._lang_changing = True
        self.language = "tagalog" if self.k12_lang_var.get() == "Tagalog" else "english"
        if hasattr(self, "college_lang_var"):
            self.college_lang_var.set(self.k12_lang_var.get())
        if hasattr(self, "md_lang_var"):
            self.md_lang_var.set(self.k12_lang_var.get())
        if self._current_raw_content:
            self._render_current_material()
        self._lang_changing = False

    def _on_college_lang_change(self, *args):
        if getattr(self, "_lang_changing", False):
            return
        self._lang_changing = True
        self.language = "tagalog" if self.college_lang_var.get() == "Tagalog" else "english"
        if hasattr(self, "k12_lang_var"):
            self.k12_lang_var.set(self.college_lang_var.get())
        if hasattr(self, "md_lang_var"):
            self.md_lang_var.set(self.college_lang_var.get())
        if self._current_raw_content:
            self._render_current_material()
        self._lang_changing = False

    def _on_ans_lang_change(self, *args):
        if getattr(self, "_lang_changing", False):
            return
        self._lang_changing = True
        self.language = "tagalog" if self.ans_lang_var.get() == "Tagalog" else "english"
        if hasattr(self, "k12_lang_var"):
            self.k12_lang_var.set(self.ans_lang_var.get())
        if hasattr(self, "college_lang_var"):
            self.college_lang_var.set(self.ans_lang_var.get())
        if hasattr(self, "md_lang_var"):
            self.md_lang_var.set(self.ans_lang_var.get())
        if self._current_raw_content:
            self._render_current_material()
        if hasattr(self, "_current_answer_sheet") and self._current_answer_sheet:
            self._show_answer(self._current_answer_sheet)
        self._lang_changing = False

    def setup_k12_tab(self):
        main_frame = ctk.CTkFrame(self.tab_k12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        header_frame.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(header_frame, text=self._tr("k12_learning_materials"), font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#2C3E50").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.k12_lang_var = ctk.StringVar(value="English" if self.language == "english" else "Tagalog")
        self.k12_lang_var.trace_add("write", self._on_k12_lang_change)
        ctk.CTkOptionMenu(header_frame, variable=self.k12_lang_var, values=["English", "Tagalog"],
                          width=110, font=ctk.CTkFont(size=13)).grid(row=0, column=1, padx=(0, 10), sticky="e")
        k12_count = sum(len(subj) for subj in k12_data.values())
        ctk.CTkLabel(header_frame, text=self._tr("subjects_info").format(subjects=k12_count, grades=len(k12_data)),
                     font=ctk.CTkFont(size=13), text_color="#5D6D7E").grid(row=1, column=0, sticky="w")
        official_frame = ctk.CTkFrame(header_frame, fg_color="#EBF5FB", corner_radius=12)
        official_frame.grid(row=0, column=2, rowspan=2, sticky="ne", padx=(15, 0), pady=(0, 5))
        official_frame.grid_propagate(False)
        official_frame.configure(width=200, height=90)
        ctk.CTkLabel(official_frame, text=self._tr("official_deped"), font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#000000").pack(pady=(10, 5))
        ctk.CTkButton(official_frame, text=self._tr("visit_lrmds"), width=150, height=35,
                      command=lambda: webbrowser.open("https://lrmds.deped.gov.ph/k_to_12"),
                       fg_color="#2E86C1", hover_color="#1B4F72").pack(pady=5)
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        self.k12_label = ctk.CTkLabel(content_frame, text=self._tr("select_grade_level"),
                                      font=ctk.CTkFont(size=18, weight="bold"), text_color="#2C3E50")
        self.k12_label.grid(row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=15)
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=5)
        ctk.CTkLabel(left_frame, text=self._tr("grade_levels"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#2C3E50").pack(anchor="w", padx=10, pady=(10, 5))
        self.k12_grade_list = ctk.CTkScrollableFrame(left_frame)
        self.k12_grade_list.pack(fill="both", expand=True, padx=10, pady=5)
        for grade in k12_data:
            subj_count = len(k12_data[grade])
            btn = ctk.CTkButton(self.k12_grade_list, text=self._tr("grade_btn").format(grade=grade, count=subj_count), anchor="w", height=38,
                                font=ctk.CTkFont(size=13),
                                command=lambda g=grade: self._k12_show_subjects(g))
            btn.pack(fill="x", pady=3)
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 15), pady=5)
        ctk.CTkLabel(right_frame, text=self._tr("subjects_difficulties"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#2C3E50").pack(anchor="w", padx=10, pady=(10, 5))
        self.k12_subject_list = ctk.CTkScrollableFrame(right_frame)
        self.k12_subject_list.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(self.k12_subject_list, text=self._tr("select_grade"),
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _k12_back_to_grades(self):
        self.k12_label.configure(text=self._tr("select_grade_level"))
        for w in self.k12_subject_list.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.k12_subject_list, text=self._tr("select_grade"),
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _k12_show_subjects(self, grade):
        self.k12_label.configure(text=f"{grade} \u2014 Subjects")
        self._k12_current_grade = grade
        self._k12_current_quarter = 0
        for w in self.k12_subject_list.winfo_children():
            w.destroy()
        back_btn = ctk.CTkButton(self.k12_subject_list, text=self._tr("back_to_grade_levels"), width=120, height=28,
                                 font=ctk.CTkFont(size=11), fg_color="#7F8C8D", hover_color="#5D6D7E",
                                 command=self._k12_back_to_grades)
        back_btn.pack(anchor="w", pady=(5, 5), padx=5)

        q_frame = ctk.CTkFrame(self.k12_subject_list, fg_color="transparent")
        q_frame.pack(fill="x", pady=(0, 8), padx=5)
        ctk.CTkLabel(q_frame, text="Quarter:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#2C3E50").pack(side="left", padx=(0, 8))
        self._k12_quarter_var = ctk.IntVar(value=0)
        for qi, qname in enumerate(["1st", "2nd", "3rd", "4th"]):
            rb = ctk.CTkRadioButton(q_frame, text=qname, variable=self._k12_quarter_var,
                                    value=qi, font=ctk.CTkFont(size=12), text_color="#000000")
            rb.pack(side="left", padx=4)

        subjects = k12_data.get(grade, {})
        if not subjects:
            ctk.CTkLabel(self.k12_subject_list, text=self._tr("no_subjects"),
                         font=ctk.CTkFont(size=14), text_color="#7F8C8D").pack(pady=20)
            return
        for subject_name, diffs in subjects.items():
            card = ctk.CTkFrame(self.k12_subject_list, fg_color="#F8F9FA", corner_radius=10, border_width=1, border_color="#E9ECEF")
            card.pack(fill="x", pady=5, padx=5)
            emoji = ""
            for kw, e in SUBJECT_EMOJI_MAP:
                if kw in subject_name.lower():
                    emoji = e
                    break
            ctk.CTkLabel(card, text=f"{emoji}  {subject_name}", font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#2C3E50", anchor="w").pack(anchor="w", padx=12, pady=(8, 2))
            diff_frame = ctk.CTkFrame(card, fg_color="transparent")
            diff_frame.pack(fill="x", padx=12, pady=(0, 8))
            for diff_name in learning_data.DIFFICULTIES:
                if diff_name in diffs:
                    filepath = diffs[diff_name]
                    btn = ctk.CTkButton(diff_frame, text=diff_name, width=75, height=30,
                                        font=ctk.CTkFont(size=10),
                                        fg_color="#27AE60" if diff_name == "Full Lesson" else "#2ECC71" if diff_name == "Easy" else "#F39C12" if diff_name == "Medium" else "#E74C3C" if diff_name == "Hard" else "#8E44AD" if diff_name == "Practice" else "#E91E63",
                                        text_color="white",
                                        hover_color="#1E8449" if diff_name == "Full Lesson" else "#239B56" if diff_name == "Easy" else "#D68910" if diff_name == "Medium" else "#CB4335" if diff_name == "Hard" else "#6C3483" if diff_name == "Practice" else "#C2185B",
                                        command=lambda p=filepath, l=f"{grade} - {subject_name} ({diff_name})": self._open_material(p, l, self._k12_quarter_var.get()))
                    btn.pack(side="left", padx=3)

    def _k12_refresh_subjects(self):
        if hasattr(self, '_k12_current_grade') and self._k12_current_grade:
            self._k12_show_subjects(self._k12_current_grade)

    def setup_college_tab(self):
        main_frame = ctk.CTkFrame(self.tab_college)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=0)
        header_frame.grid_columnconfigure(2, weight=1)
        ctk.CTkLabel(header_frame, text=self._tr("college_learning_materials"), font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="#2C3E50").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.college_lang_var = ctk.StringVar(value="English" if self.language == "english" else "Tagalog")
        self.college_lang_var.trace_add("write", self._on_college_lang_change)
        ctk.CTkOptionMenu(header_frame, variable=self.college_lang_var, values=["English", "Tagalog"],
                          width=110, font=ctk.CTkFont(size=13)).grid(row=0, column=1, padx=(0, 10), sticky="e")
        college_count = sum(len(prog) for prog in college_data.values())
        ctk.CTkLabel(header_frame, text=self._tr("college_info").format(progs=college_count, cats=len(college_data)),
                     font=ctk.CTkFont(size=13), text_color="#5D6D7E").grid(row=1, column=0, sticky="w")
        official_frame = ctk.CTkFrame(header_frame, fg_color="#EBF5FB", corner_radius=12)
        official_frame.grid(row=0, column=2, rowspan=2, sticky="ne", padx=(15, 0), pady=(0, 5))
        official_frame.grid_propagate(False)
        official_frame.configure(width=200, height=90)
        ctk.CTkLabel(official_frame, text=self._tr("official_ched"), font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#000000").pack(pady=(10, 5))
        ctk.CTkButton(official_frame, text=self._tr("visit_ched"), width=150, height=35,
                      command=lambda: webbrowser.open("https://ched.gov.ph"),
                       fg_color="#2E86C1", hover_color="#1B4F72").pack(pady=5)
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        self.college_label = ctk.CTkLabel(content_frame, text=self._tr("select_category_short"),
                                          font=ctk.CTkFont(size=18, weight="bold"))
        self.college_label.grid(row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=15)
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(15, 5), pady=5)
        ctk.CTkLabel(left_frame, text=self._tr("categories"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").pack(anchor="w", padx=10, pady=(10, 5))
        self.college_cat_list = ctk.CTkScrollableFrame(left_frame)
        self.college_cat_list.pack(fill="both", expand=True, padx=10, pady=5)
        for cat in college_data:
            prog_count = sum(len(progs) for progs in college_data[cat].values())
            btn = ctk.CTkButton(self.college_cat_list, text=self._tr("cat_btn").format(cat=cat, count=prog_count), anchor="w", height=38,
                                font=ctk.CTkFont(size=13),
                                command=lambda c=cat: self._college_show_programs(c))
            btn.pack(fill="x", pady=3)
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 15), pady=5)
        ctk.CTkLabel(right_frame, text=self._tr("programs_difficulties"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").pack(anchor="w", padx=10, pady=(10, 5))
        self.college_prog_list = ctk.CTkScrollableFrame(right_frame)
        self.college_prog_list.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(self.college_prog_list, text=self._tr("select_category"),
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _college_back_to_categories(self):
        self.college_label.configure(text=self._tr("select_category_short"))
        for w in self.college_prog_list.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.college_prog_list, text=self._tr("select_category"),
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _college_show_programs(self, cat):
        self.college_label.configure(text=f"{cat} — Programs")
        self._college_current_cat = cat
        for w in self.college_prog_list.winfo_children():
            w.destroy()
        back_btn = ctk.CTkButton(self.college_prog_list, text=self._tr("back_to_categories"), width=120, height=28,
                                 font=ctk.CTkFont(size=11), command=self._college_back_to_categories)
        back_btn.pack(anchor="w", pady=(5, 10), padx=5)
        programs = college_data.get(cat, {})
        if not programs:
            ctk.CTkLabel(self.college_prog_list, text=self._tr("no_programs"),
                         font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=20)
            return
        for prog_name, topics in programs.items():
            card = ctk.CTkFrame(self.college_prog_list, fg_color="#FFF8F0", corner_radius=10)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=prog_name, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#000000", anchor="w").pack(anchor="w", padx=10, pady=(8, 2))
            topic_frame = ctk.CTkFrame(card, fg_color="transparent")
            topic_frame.pack(fill="x", padx=10, pady=(0, 8))
            topic_btns_frame = ctk.CTkFrame(topic_frame, fg_color="transparent")
            topic_btns_frame.pack(fill="x")
            for topic_name, diffs in topics.items():
                for diff_name in learning_data.DIFFICULTIES:
                    if diff_name in diffs:
                        filepath = diffs[diff_name]
                        btn = ctk.CTkButton(topic_btns_frame, text=diff_name, width=75, height=28,
                                            font=ctk.CTkFont(size=10),
                                            fg_color="#81C784" if diff_name == "Full Lesson" else "#A5D6A7" if diff_name == "Easy" else "#FFE082" if diff_name == "Medium" else "#EF9A9A" if diff_name == "Hard" else "#CE93D8" if diff_name == "Practice" else "#F48FB1",
                                            command=lambda p=filepath, l=f"{cat} - {prog_name} - {topic_name} ({diff_name})": self._open_material(p, l))
                        btn.pack(side="left", padx=3, pady=2)
            ctk.CTkLabel(card, text=f"  {topic_name}", font=ctk.CTkFont(size=11), text_color="#000000", anchor="w").pack(anchor="w", padx=15)

    def setup_search_tab(self):
        main = ctk.CTkFrame(self.tab_search)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=0)
        main.grid_rowconfigure(1, weight=1)
        nav_frame = ctk.CTkFrame(main, fg_color="transparent")
        nav_frame.grid(row=0, column=0, pady=(15, 5), sticky="ew")
        nav_frame.grid_columnconfigure(0, weight=1)
        self.browser_url_entry = ctk.CTkEntry(nav_frame, placeholder_text=self._tr("enter_url_or_search"),
                                              font=ctk.CTkFont(size=14))
        self.browser_url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.browser_url_entry.bind("<Return>", lambda e: self._browser_open())
        ctk.CTkButton(nav_frame, text=self._tr("open_in_browser"), width=140, height=36,
                      command=self._browser_open, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=1)
        shortcuts = ctk.CTkFrame(main, fg_color="transparent")
        shortcuts.grid(row=1, column=0, sticky="nsew", pady=10)
        shortcuts.grid_columnconfigure(0, weight=1)
        info = ctk.CTkLabel(shortcuts, text=self._tr("quick_links"),
                            font=ctk.CTkFont(size=13), text_color="#000000")
        info.grid(row=0, column=0, pady=(0, 15))
        btn_frame = ctk.CTkFrame(shortcuts, fg_color="transparent")
        btn_frame.grid(row=1, column=0)
        quick_links = [
            ("YouTube", "https://youtube.com"),
            ("Google", "https://google.com"),
            ("DepEd", "https://deped.gov.ph"),
            ("CHED", "https://ched.gov.ph"),
            ("Scholar", "https://scholar.google.com"),
            ("Wikipedia", "https://en.wikipedia.org"),
        ]
        for label, url in quick_links:
            ctk.CTkButton(btn_frame, text=label, width=130, height=44,
                          command=lambda u=url: webbrowser.open(u),
                          font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=6)

    def _browser_open(self):
        text = self.browser_url_entry.get().strip()
        if not text:
            text = "https://www.google.com"
        if not text.startswith("http"):
            if "." in text and " " not in text:
                text = "https://" + text
            else:
                text = f"https://www.google.com/search?q={quote_plus(text)}"
        webbrowser.open(text)

    def setup_md_tab(self):
        main = ctk.CTkFrame(self.tab_md)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        top.grid_columnconfigure(3, weight=1)
        ctk.CTkButton(top, text="\u2190 " + self._tr("home"), width=80, height=38,
                      font=ctk.CTkFont(size=13), fg_color="#546E7A", hover_color="#37474F",
                      command=lambda: self.tab_view.set(self._tr("home"))).grid(row=0, column=0, padx=(0, 5))
        ctk.CTkButton(top, text=self._tr("open_md_file"), width=120, height=38,
                      command=self.open_md_file, font=ctk.CTkFont(size=14)).grid(row=0, column=1, padx=(0, 5))
        ctk.CTkLabel(top, text=self._tr("language_label"), font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(5, 5))
        self.md_lang_var = ctk.StringVar(value="English" if self.language == "english" else "Tagalog")
        self.md_lang_var.trace_add("write", self._on_md_lang_change)
        ctk.CTkOptionMenu(top, variable=self.md_lang_var, values=["English", "Tagalog"],
                          width=110, font=ctk.CTkFont(size=13)).grid(row=0, column=2, padx=(0, 10))
        self.md_filename = ctk.CTkLabel(top, text=self._tr("no_file_opened"), font=ctk.CTkFont(size=14), text_color="#5D6D7E")
        self.md_filename.grid(row=0, column=4, sticky="w", padx=(5, 0))
        self.quiz_btn = ctk.CTkButton(top, text=self._tr("take_quiz"), width=100, height=32,
                                        font=ctk.CTkFont(size=13), fg_color="#E67E22", hover_color="#D35400",
                                        command=self._open_quiz_dialog)
        self.quiz_btn.grid(row=0, column=5, padx=(10, 0))
        ctk.CTkButton(top, text=self._tr("leaderboard"), width=100, height=32,
                        font=ctk.CTkFont(size=13), fg_color="#2E86C1", hover_color="#1B4F72",
                        command=lambda: self.tab_view.set(self._tr("leaderboard"))).grid(row=0, column=6, padx=(5, 0))
        self.edit_btn = ctk.CTkButton(top, text=self._tr("edit"), width=70, height=32,
                                        font=ctk.CTkFont(size=13), fg_color="#F39C12", hover_color="#D68910",
                                        command=self._toggle_edit_mode)
        self.edit_btn.grid(row=0, column=7, padx=(5, 0))
        self.save_btn = ctk.CTkButton(top, text=self._tr("save"), width=70, height=32,
                                       font=ctk.CTkFont(size=13), fg_color="#27AE60", hover_color="#1E8449",
                                       command=self._save_md_file)
        self.save_btn.grid(row=0, column=8, padx=(5, 0))
        text_frame = ctk.CTkFrame(main)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        self.md_text = ctk.CTkTextbox(text_frame, wrap="word", font=ctk.CTkFont(size=13), text_color="#2C3E50", fg_color="#FEF9E7")
        self.md_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.visual_viewer = lesson_renderer.LessonRenderer(text_frame, self._tr, self.current_user)
        self.visual_viewer.grid(row=0, column=0, sticky="nsew")
        self.visual_viewer.grid_remove()
        self.html_editor = ctk.CTkTextbox(text_frame, wrap="word", font=ctk.CTkFont(size=12), text_color="#FFFFFF", fg_color="#1E1E1E")
        self.html_editor.grid(row=0, column=0, sticky="nsew")
        self.html_editor.grid_remove()

    def open_md_file(self):
        path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md"), ("All files", "*.*")])
        if not path:
            return
        self._open_material(path, os.path.basename(path))

    def _toggle_edit_mode(self):
        if self._editing_md:
            self._editing_md = False
            self.edit_btn.configure(text=self._tr("edit"))
            if self.html_editor.winfo_ismapped():
                self.html_editor.grid_remove()
                self.visual_viewer.grid()
                if self._current_filepath:
                    try:
                        with open(self._current_filepath, encoding="utf-8") as f:
                            self.visual_viewer.html_frame.load_html(f.read())
                    except Exception:
                        pass
            else:
                self.md_text.configure(state="disabled")
                self._render_current_material()
            return
        self._editing_md = True
        self.edit_btn.configure(text=self._tr("cancel"))
        if self.visual_viewer.winfo_ismapped():
            self.visual_viewer.grid_remove()
            self.html_editor.grid()
            if self._current_filepath:
                try:
                    with open(self._current_filepath, encoding="utf-8") as f:
                        content = f.read()
                    self.html_editor.delete("0.0", "end")
                    self.html_editor.insert("0.0", content)
                except Exception:
                    pass
        else:
            self.md_text.configure(state="normal")

    def _save_md_file(self):
        if not self._current_filepath:
            messagebox.showinfo(self._tr("gen_error"), self._tr("no_file_opened"))
            return
        if not self._editing_md and not self.html_editor.winfo_ismapped():
            self._save_md_copy()
            return
        try:
            if self.html_editor.winfo_ismapped():
                content = self.html_editor.get("0.0", "end-1c")
            else:
                content = self.md_text.get("0.0", "end-1c")
            with open(self._current_filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self._current_raw_content = content
            if self.html_editor.winfo_ismapped():
                self.html_editor.grid_remove()
                self.visual_viewer.grid()
                self.visual_viewer.html_frame.load_html(content)
            else:
                self._render_current_material()
            self._editing_md = False
            self.edit_btn.configure(text=self._tr("edit"))
            self.md_text.configure(state="disabled")
            messagebox.showinfo(self._tr("saved"), self._tr("file_saved"))
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Save failed:\n{e}")

    def _save_md_copy(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=os.path.join(learning_data.APP_ROOT, "Custom_Lessons")
        )
        if not path:
            return
        try:
            content = self.md_text.get("0.0", "end-1c") if self.md_text.winfo_ismapped() else ""
            if not content and self._current_raw_content:
                content = self._current_raw_content
            if not content:
                return
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo(self._tr("saved"), self._tr("file_saved"))
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Save failed:\n{e}")

    def _get_lang_path(self, filepath, lang="english"):
        """Get corresponding language file path in _EN or _TL directory, or None"""
        suffix = "_EN" if lang == "english" else "_TL"
        for src_dir in ["K-12_Philippine_Curriculum", "College_Programs"]:
            lang_dir = src_dir + suffix
            if src_dir in filepath and lang_dir not in filepath:
                return filepath.replace(src_dir, lang_dir)
        return None

    def _get_visual_path(self, filepath, quarter_idx=0):
        """Map a K-12 markdown path to the HTML equivalent.
        Uses quarter_idx (0-3) to select First through Fourth Quarter.
        Students are routed to Visual_Lessons_Student/ (green theme),
        admin/teacher use Visual_Lessons/ (original)."""
        qnames = ["First_Quarter", "Second_Quarter", "Third_Quarter", "Fourth_Quarter"]
        qn = qnames[quarter_idx] if 0 <= quarter_idx < 4 else "First_Quarter"
        is_student = self.current_role == "student"
        for src_dir in ["K-12_Philippine_Curriculum", "College_Programs"]:
            if src_dir not in filepath:
                continue
            rel = filepath.split(src_dir, 1)[1].lstrip("\\/")
            base, ext = os.path.splitext(rel)
            visual_subdir = os.path.dirname(base)
            fname_stem = os.path.basename(base)

            # Strip difficulty suffixes from fname_stem for clean subject name
            clean_stem = fname_stem
            for diff_sfx in ["_Full_Assessment", "_Practice", "_Hard", "_Medium", "_Easy"]:
                if clean_stem.endswith(diff_sfx):
                    clean_stem = clean_stem[:-len(diff_sfx)]
                    break

            # Student route — files are named {Subject}_{Quarter}.html (no diff suffix)
            if is_student:
                student_dir = os.path.join(learning_data.APP_ROOT, "Visual_Lessons_Student", visual_subdir)
                candidate = os.path.join(student_dir, f"{clean_stem}_{qn}.html")
                if os.path.exists(candidate):
                    return candidate

            # Admin/teacher route — try quarter-specific file with difficulty suffixes
            visual_dir = os.path.join(learning_data.APP_ROOT, "Visual_Lessons", visual_subdir)
            for sfx in ["", "_Full_Assessment", "_Practice", "_Hard", "_Medium", "_Easy"]:
                candidate = os.path.join(visual_dir, f"{fname_stem}_{qn}{sfx}.html")
                if os.path.exists(candidate):
                    return candidate

            # Fall back to legacy plain name
            visual_path = os.path.join(learning_data.APP_ROOT, "Visual_Lessons", rel.replace(ext, ".html"))
            if os.path.exists(visual_path):
                return visual_path
            return None
        return None

    def _open_material(self, filepath, label, quarter_idx=0):
        try:
            visual_path = self._get_visual_path(filepath, quarter_idx)
            if visual_path:
                self._open_visual_material(visual_path, label, filepath)
                return

            with open(filepath, encoding="utf-8") as f:
                content = f.read()
            self._editing_md = False
            self.edit_btn.configure(text=self._tr("edit"))
            self.html_editor.grid_remove()
            self.visual_viewer.grid_remove()
            self.md_text.grid()
            self._current_filepath = filepath
            self._current_raw_content = content
            self._current_md_label = label
            self._translation_cache.clear()
            en_path = self._get_lang_path(filepath, "english")
            self._current_en_content = None
            if en_path and os.path.exists(en_path):
                with open(en_path, encoding="utf-8") as f:
                    self._current_en_content = f.read()
            tl_path = self._get_lang_path(filepath, "tagalog")
            self._current_tl_content = None
            if tl_path and os.path.exists(tl_path):
                with open(tl_path, encoding="utf-8") as f:
                    self._current_tl_content = f.read()
            parts = label.split(" - ")
            grade = parts[0] if len(parts) > 0 else ""
            subject = parts[1].split(" (")[0] if len(parts) > 1 else ""
            diff = parts[1].split("(")[-1].rstrip(")") if len(parts) > 1 and "(" in parts[1] else ""
            lesson_db.record_lesson_access(
                self.current_user, filepath, label,
                curriculum="K12" if "K-12" in filepath else "College",
                grade=grade, subject=subject, difficulty=diff
            )
            self._render_current_material()
            self.tab_view.set(self._tr("markdown_reader"))
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Could not open file:\n{e}")

    def _open_visual_material(self, visual_path, label, orig_path):
        self._editing_md = False
        self.edit_btn.configure(text=self._tr("edit"))
        self.html_editor.grid_remove()
        self.md_text.grid_remove()
        self.visual_viewer.grid()
        try:
            with open(visual_path, encoding="utf-8") as f:
                html_content = f.read()
            self.visual_viewer.load_lesson_content(html_content, filepath=orig_path, label=label)
            self.md_filename.configure(text=label, text_color="#000000")
            parts = label.split(" - ")
            grade = parts[0] if len(parts) > 0 else ""
            subject = parts[1].split(" (")[0] if len(parts) > 1 else ""
            diff = parts[1].split("(")[-1].rstrip(")") if len(parts) > 1 and "(" in parts[1] else ""
            lesson_db.record_lesson_access(
                self.current_user, orig_path, label,
                curriculum="K12" if "K12" in visual_path else "College",
                grade=grade, subject=subject, difficulty=diff
            )
            self.tab_view.set(self._tr("markdown_reader"))
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Could not open visual lesson:\n{e}")

    def _render_current_material(self):
        if self.visual_viewer.winfo_ismapped():
            return
        if not self._current_raw_content:
            return
        lang = self.md_lang_var.get().lower() if hasattr(self, "md_lang_var") else self.language
        self.language = lang
        if self.language == "english" and self._current_en_content:
            content = self._current_en_content
            lang_tag = " (EN)"
        elif self.language == "tagalog" and self._current_tl_content:
            content = self._current_tl_content
            lang_tag = " (TL)"
        else:
            content = self._current_raw_content
            lang_tag = ""
        display_label = (self._current_md_label or self._tr("untitled")) + lang_tag
        self.md_filename.configure(text=display_label, text_color="#000000")
        self._render_md(content)

    def _on_md_lang_change(self, *args):
        if getattr(self, "_lang_changing", False):
            return
        self._lang_changing = True
        self.language = "tagalog" if self.md_lang_var.get() == "Tagalog" else "english"
        if hasattr(self, "k12_lang_var"):
            self.k12_lang_var.set(self.md_lang_var.get())
        if hasattr(self, "college_lang_var"):
            self.college_lang_var.set(self.md_lang_var.get())
        self._render_current_material()
        self._lang_changing = False

    TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".xml", ".html", ".htm", ".css", ".js", ".py",
                  ".yaml", ".yml", ".ini", ".cfg", ".log", ".bat", ".ps1", ".sh", ".env", ".cfg",
                  ".java", ".cpp", ".c", ".h", ".hpp", ".rb", ".php", ".pl", ".rs", ".go", ".ts",
                  ".jsx", ".tsx", ".vue", ".svelte", ".sql", ".r", ".lua", ".dart", ".kt", ".swift"}

    def _is_text_file(self, ext):
        return ext in self.TEXT_EXTS

    def setup_imported_tab(self):
        main = ctk.CTkFrame(self.tab_imported)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(header, text=self._tr("imported_files"), font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, sticky="w")
        self.imported_path_label = ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=11), text_color="#000000")
        self.imported_path_label.grid(row=0, column=1, sticky="w", padx=(15, 0))
        ctk.CTkButton(header, text=self._tr("import_folder"), width=130, height=36,
                      command=self._import_folder, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=2, padx=(10, 0))
        filter_frame = ctk.CTkFrame(main, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        for f in [self._tr("filter_all"), self._tr("filter_images"), self._tr("filter_pdfs"), self._tr("filter_videos"), self._tr("filter_text"), self._tr("filter_other")]:
            ctk.CTkButton(filter_frame, text=f, width=90, height=30,
                         font=ctk.CTkFont(size=12),
                         command=lambda c=f: self._show_imported_category(c)).pack(side="left", padx=3)
        self.imported_list = ctk.CTkScrollableFrame(main)
        self.imported_list.grid(row=2, column=0, sticky="nsew")
        self.editor_frame = ctk.CTkFrame(main)
        self.editor_frame.grid(row=2, column=0, sticky="nsew")
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        self.editor_top = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
        self.editor_top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.editor_top.grid_columnconfigure(1, weight=1)
        self.editor_back_btn = ctk.CTkButton(self.editor_top, text=self._tr("back"), width=70, height=30,
                                              font=ctk.CTkFont(size=12), command=self._back_to_imported_list)
        self.editor_back_btn.grid(row=0, column=0, padx=(0, 10))
        self.editor_filename_label = ctk.CTkLabel(self.editor_top, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.editor_filename_label.grid(row=0, column=1, sticky="w")
        self.editor_save_btn = ctk.CTkButton(self.editor_top, text=self._tr("save"), width=70, height=30,
                                              font=ctk.CTkFont(size=12, weight="bold"),
                                              fg_color="#81C784", hover_color="#66BB6A", command=self._save_imported_file)
        self.editor_save_btn.grid(row=0, column=2, padx=5)
        self.editor_history_btn = ctk.CTkButton(self.editor_top, text=self._tr("history"), width=80, height=30,
                                                 font=ctk.CTkFont(size=12), command=self._show_file_history)
        self.editor_history_btn.grid(row=0, column=3, padx=5)
        self.editor_external_btn = ctk.CTkButton(self.editor_top, text=self._tr("open_externally"), width=120, height=30,
                                                  font=ctk.CTkFont(size=12),
                                                  command=self._open_imported_external)
        self.editor_external_btn.grid(row=0, column=4, padx=5)
        self.editor_status = ctk.CTkLabel(self.editor_top, text="", font=ctk.CTkFont(size=11))
        self.editor_status.grid(row=0, column=5, padx=(5, 0))
        self.editor_text = ctk.CTkTextbox(self.editor_frame, wrap="word", font=ctk.CTkFont(size=13),
                                          text_color="#000000", fg_color="#FFF0D0")
        self.editor_text.grid(row=1, column=0, sticky="nsew")
        self.editor_frame.grid_remove()
        ctk.CTkLabel(self.imported_list, text="Click 'Import Folder' to add files",
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _import_folder(self):
        folder = filedialog.askdirectory(title=self._tr("select_folder_import"))
        if not folder:
            return
        self.imported_folder = folder
        self.imported_path_label.configure(text=folder)
        self.imported_files = self._scan_folder(folder)
        self._back_to_imported_list()
        self._show_imported_category(self._tr("filter_all"))

    def _scan_folder(self, folder):
        IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".ico"}
        PDF_EXTS = {".pdf"}
        VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"}
        files = []
        for root, dirs, fnames in os.walk(folder):
            for fname in sorted(fnames):
                ext = os.path.splitext(fname)[1].lower()
                fpath = os.path.join(root, fname)
                if ext in IMAGE_EXTS:
                    category = self._tr("filter_images")
                elif ext in PDF_EXTS:
                    category = self._tr("filter_pdfs")
                elif ext in VIDEO_EXTS:
                    category = self._tr("filter_videos")
                elif self._is_text_file(ext):
                    category = self._tr("filter_text")
                else:
                    category = self._tr("filter_other")
                files.append({"name": fname, "path": fpath, "ext": ext, "category": category})
        return files

    def _show_imported_category(self, category):
        for w in self.imported_list.winfo_children():
            w.destroy()
        if not self.imported_files:
            ctk.CTkLabel(self.imported_list, text=self._tr("no_files_imported"),
                         font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)
            return
        filtered = self.imported_files if category == self._tr("filter_all") else [f for f in self.imported_files if f["category"] == category]
        if not filtered:
            ctk.CTkLabel(self.imported_list, text=self._tr("no_category_items").format(cat=category.lower()),
                         font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)
            return
        for f in filtered:
            card = ctk.CTkFrame(self.imported_list, fg_color="#FFF8F0", corner_radius=8)
            card.pack(fill="x", pady=3, padx=5)
            emoji = {self._tr("filter_images"): "🖼️", self._tr("filter_pdfs"): "📄", self._tr("filter_videos"): "🎬", self._tr("filter_text"): "📝", self._tr("filter_other"): "📁"}.get(f["category"], "📁")
            ctk.CTkLabel(card, text=f"{emoji}  {f['name']}", font=ctk.CTkFont(size=13),
                         anchor="w").pack(side="left", padx=10, pady=6)
            try:
                size_kb = os.path.getsize(f["path"]) // 1024
                ctk.CTkLabel(card, text=f"({size_kb} KB)", font=ctk.CTkFont(size=10),
                             text_color="#000000").pack(side="left", padx=5)
            except OSError:
                pass
            ctk.CTkButton(card, text=self._tr("open"), width=60, height=26, font=ctk.CTkFont(size=11),
                         command=lambda p=f["path"], c=f["category"]: self._open_imported_file(p, c)).pack(side="right", padx=10)

    def _open_imported_file(self, path, category):
        self._open_imported_viewer(path)

    def _open_imported_viewer(self, path):
        self._editing_path = path
        self.editor_filename_label.configure(text=os.path.basename(path))
        self.editor_status.configure(text="")
        self.editor_text.configure(state="normal")
        self.editor_text.delete("0.0", "end")
        ext = os.path.splitext(path)[1].lower()
        size = os.path.getsize(path)
        fname = os.path.basename(path)
        IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".ico", ".svg", ".heic", ".avif"}
        VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm"}
        PDF_EXTS = {".pdf"}
        if ext in IMAGE_EXTS and _PIL_AVAIL:
            try:
                from PIL import Image, ImageTk
                img = Image.open(path)
                max_w = self.editor_text.winfo_width() - 40 or 700
                max_h = self.editor_text.winfo_height() - 40 or 500
                if max_w < 100: max_w = 700
                if max_h < 100: max_h = 500
                if img.width > max_w or img.height > max_h:
                    ratio = min(max_w / img.width, max_h / img.height)
                    img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                if not hasattr(self, "_imported_images"):
                    self._imported_images = []
                self._imported_images.append(photo)
                self.editor_text._textbox.image_create("end", image=photo)
                self.editor_text.insert("end", f"\n\n{fname}  ({img.width}x{img.height})")
            except Exception as e:
                self.editor_text.insert("0.0", f"Could not display image: {e}\n\n")
                self.editor_text.insert("end", f"File: {fname}\nSize: {size:,} bytes\nPath: {path}")
        elif ext in VIDEO_EXTS:
            import subprocess, json, os, tempfile, math
            info = f"File: {fname}\nSize: {size:,} bytes\nType: Video ({ext.upper()})\nPath: {path}"
            try:
                result = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                                         "-show_format", "-show_streams", path],
                                        capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    fmt = data.get("format", {})
                    dur = float(fmt.get("duration", 0))
                    info += f"\nDuration: {dur:.1f}s\nBitrate: {fmt.get('bit_rate', '?')} bps"
                    for s in data.get("streams", []):
                        codec = s.get("codec_name", "?")
                        stype = s.get("codec_type", "?")
                        if stype == "video":
                            w, h = s.get("width", "?"), s.get("height", "?")
                            fps_str = s.get("r_frame_rate", "0/1")
                            if "/" in fps_str:
                                try:
                                    num, den = fps_str.split("/")
                                    fps_val = float(num) / float(den)
                                except Exception: fps_val = 0
                            else: fps_val = 0
                            info += f"\nVideo: {codec} | {w}x{h} | {fps_val:.1f} fps"
                        elif stype == "audio":
                            info += f"\nAudio: {codec} | {s.get('sample_rate','?')} Hz | {s.get('channels','?')} ch"
            except Exception: pass  # video metadata parsing failed, continue with limited info
            self.editor_text.insert("0.0", info)
            self.editor_text.insert("end", "\n\n--- Video player ---\n")
            self.editor_text._textbox.mark_set("_video_frame", "end")
            self._video_state = {"path": path, "playing": False, "idx": 0, "frames": [],
                                 "tmpdir": None, "after_id": None, "fps": 10, "display": None}
            max_w = self.editor_text.winfo_width() - 60 or 640
            if max_w < 100: max_w = 640
            try:
                dur = dur if dur > 0 else 10
                fps_play = 10
                total_frames = min(int(dur * fps_play) + 1, 300)
                self._video_state["total"] = total_frames
                self._video_state["fps"] = fps_play
                self._video_state["max_w"] = max_w
                tmpdir = tempfile.mkdtemp()
                self._video_state["tmpdir"] = tmpdir
                pattern = os.path.join(tmpdir, "frame%05d.png").replace("\\", "/")
                subprocess.Popen(["ffmpeg", "-i", path, "-vf", f"fps={fps_play},scale={max_w}:-2",
                                  "-frames:v", str(total_frames), "-loglevel", "error",
                                  pattern, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._video_state["extracting"] = True
                self._schedule_video_update()
            except Exception as e:
                self.editor_text.insert("end", f"(Player init error: {e})")
        elif ext in PDF_EXTS:
            import zlib, re
            info = f"File: {fname}\nSize: {size:,} bytes\nType: PDF\nPath: {path}\n"
            try:
                with open(path, "rb") as f:
                    raw = f.read()
                texts = []
                for m in re.finditer(rb'stream\s(.+?)\s*endstream', raw, re.DOTALL):
                    data = m.group(1).strip()
                    try:
                        data = zlib.decompress(data)
                    except Exception: pass  # skip non-compressed PDF stream
                    for t in re.finditer(rb'\(([^)]*)\)', data):
                        t = t.group(1).decode("latin-1", errors="replace")
                        if len(t.strip()) > 1:
                            texts.append(t.strip())
                    for t in re.finditer(rb'BT\s*(.+?)\s*ET', data, re.DOTALL):
                        block = t.group(1)
                        for line in re.finditer(rb"T[dw]?\s*", block):
                            pass
                        for txt in re.finditer(rb'\(([^)]*)\)\s*Tj', block):
                            t = txt.group(1).decode("latin-1", errors="replace").strip()
                            if t: texts.append(t)
                seen = set()
                unique = []
                for t in texts:
                    if t not in seen:
                        seen.add(t)
                        unique.append(t)
                if unique:
                    info += f"\n--- Extracted text ---\n\n" + "\n".join(unique[:500])
                    if len(unique) > 500:
                        info += f"\n... ({len(unique) - 500} more lines)"
                else:
                    info += "\n(No extractable text found in PDF)"
            except Exception as e:
                info += f"\n(PDF read error: {e})"
            self.editor_text.insert("0.0", info)
        else:
            try:
                with open(path, "rb") as f:
                    raw = f.read(100000)
                is_binary = bool(raw) and sum(32 <= b < 127 or b in (9, 10, 13) for b in raw) < len(raw) * 0.7
                if is_binary:
                    strings_list = []
                    current = []
                    for b in raw:
                        if 32 <= b < 127:
                            current.append(chr(b))
                        else:
                            if len(current) >= 4:
                                strings_list.append("".join(current))
                            current = []
                    if len(current) >= 4:
                        strings_list.append("".join(current))
                    hex_lines = []
                    for i in range(0, min(len(raw), 2048), 16):
                        chunk = raw[i:i+16]
                        hex_lines.append(f"{i:08x}  {' '.join(f'{b:02x}' for b in chunk):48s}  {''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)}")
                    hex_dump = "\n".join(hex_lines)
                    info = f"File: {fname}\nSize: {size:,} bytes\nType: {ext.upper() if ext else 'Unknown'}\nPath: {path}\n"
                    if strings_list:
                        info += f"\n--- Readable text ---\n\n{chr(10).join(strings_list[:200])}"
                        if len(strings_list) > 200:
                            info += f"\n... ({len(strings_list) - 200} more strings)"
                    info += f"\n\n--- Hex dump (first {min(len(raw), 2048)} bytes) ---\n\n{hex_dump}"
                    if len(raw) > 2048:
                        info += f"\n... ({len(raw) - 2048} more bytes)"
                else:
                    with open(path, encoding="utf-8", errors="replace") as f:
                        content = f.read(100000)
                    info = f"File: {fname}\nSize: {size:,} bytes\nType: {ext.upper() if ext else 'Unknown'}\nPath: {path}\n\n--- Content ---\n\n{content}"
            except Exception as e:
                info = f"File: {fname}\nSize: {size:,} bytes\nType: {ext.upper() if ext else 'Unknown'}\nPath: {path}\n\nError reading file: {e}"
            self.editor_text.insert("0.0", info)
        self.editor_text.configure(state="normal")
        self.imported_list.grid_remove()
        self.editor_frame.grid()
        if ext in VIDEO_EXTS:
            self._create_video_controls()

    def _create_video_controls(self):
        for b in getattr(self, "_video_controls", []):
            try: b.destroy()
            except Exception: pass  # widget may already be destroyed
        self._video_controls = []
        play_btn = ctk.CTkButton(self.editor_top, text=self._tr("play"), width=60, height=28,
                                 font=ctk.CTkFont(size=11, weight="bold"),
                                 fg_color="#81C784", hover_color="#66BB6A",
                                 command=self._video_play)
        play_btn.grid(row=0, column=6, padx=2)
        pause_btn = ctk.CTkButton(self.editor_top, text=self._tr("pause"), width=60, height=28,
                                  font=ctk.CTkFont(size=11),
                                  fg_color="#FFD54F", hover_color="#FFCA28",
                                  command=self._video_pause)
        pause_btn.grid(row=0, column=7, padx=2)
        stop_btn = ctk.CTkButton(self.editor_top, text=self._tr("stop"), width=60, height=28,
                                 font=ctk.CTkFont(size=11),
                                 fg_color="#E57373", hover_color="#EF5350",
                                 command=self._video_stop)
        stop_btn.grid(row=0, column=8, padx=2)
        self._video_controls = [play_btn, pause_btn, stop_btn]

    def _schedule_video_update(self):
        vs = getattr(self, "_video_state", None)
        if not vs: return
        if vs.get("extracting"):
            tmpdir = vs.get("tmpdir", "")
            if tmpdir and os.path.isdir(tmpdir):
                existing = sorted([f for f in os.listdir(tmpdir) if f.endswith(".png")])
                if existing:
                    vs["frames"] = [os.path.join(tmpdir, f) for f in existing]
                    vs["total"] = len(existing)
            if vs.get("total", 0) > 0:
                total_frames = vs["total"]
                tmpdir = vs.get("tmpdir", "")
                expected = total_frames
                if tmpdir and os.path.isdir(tmpdir):
                    actual = len([f for f in os.listdir(tmpdir) if f.endswith(".png")])
                    if actual >= expected or actual >= 10:
                        vs["extracting"] = False
                        vs["frames"] = sorted([os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".png")],
                                             key=lambda x: int(os.path.splitext(os.path.basename(x))[0].replace("frame","")))
                        vs["total"] = len(vs["frames"])
                    if not vs.get("playing") and not vs.get("display"):
                        self._video_show_frame(vs, 0)
        if not vs.get("playing"):
            self.window.after(200, self._schedule_video_update)
            return
        idx = vs.get("idx", 0)
        frames = vs.get("frames", [])
        if frames and idx < len(frames):
            self._video_show_frame(vs, idx)
            fps = vs.get("fps", 10)
            vs["idx"] = (idx + 1) % len(frames)
            aid = self.window.after(int(1000 / fps), self._schedule_video_update)
            vs["after_id"] = aid
        else:
            vs["playing"] = False

    def _video_show_frame(self, vs, idx):
        frames = vs.get("frames", [])
        if not frames or idx >= len(frames): return
        try:
            from PIL import Image, ImageTk
            fpath = frames[idx]
            if not os.path.isfile(fpath): return
            img = Image.open(fpath)
            photo = ImageTk.PhotoImage(img)
            if not hasattr(self, "_imported_images"):
                self._imported_images = []
            self._imported_images.append(photo)
            ed = self.editor_text._textbox
            pos = ed.index("_video_frame")
            ed.delete(pos, f"{pos} + 1 lines" if not vs.get("display") else f"{pos} + 1 char")
            ed.image_create("_video_frame", image=photo)
            ed.insert("_video_frame + 1 char", "\n")
            vs["display"] = True
        except Exception: pass  # frame display failed, skip this update

    def _video_play(self):
        vs = getattr(self, "_video_state", None)
        if not vs: return
        vs["playing"] = True
        self._schedule_video_update()

    def _video_pause(self):
        vs = getattr(self, "_video_state", None)
        if not vs: return
        vs["playing"] = False
        if vs.get("after_id"):
            try: self.window.after_cancel(vs["after_id"])
            except Exception: pass  # timer already fired or invalid
        vs["playing"] = False
        vs = getattr(self, "_video_state", None)
        if not vs: return
        vs["playing"] = False
        if vs.get("after_id"):
            try: self.window.after_cancel(vs["after_id"])
            except Exception: pass  # timer already fired or invalid
        vs["idx"] = 0

    def _open_imported_external(self):
        path = getattr(self, "_editing_path", None)
        if not path: return
        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Could not open file externally:\n{e}")

    def _save_imported_file(self):
        path = getattr(self, "_editing_path", None)
        if not path:
            return
        content = self.editor_text.get("0.0", "end-1c")
        try:
            self._save_version_backup(path)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.editor_status.configure(text=self._tr("saved"), text_color="#000000")
        except Exception as e:
            self.editor_status.configure(text=f"Save failed: {e}", text_color="#000000")

    def _save_version_backup(self, path):
        if not os.path.isfile(path):
            return
        base = os.path.dirname(path)
        name = os.path.basename(path)
        ver_dir = os.path.join(base, ".versions")
        os.makedirs(ver_dir, exist_ok=True)
        ts = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        ver_path = os.path.join(ver_dir, f"{name}.{ts}")
        import shutil
        shutil.copy2(path, ver_path)

    def _back_to_imported_list(self):
        self._video_pause()
        vs = getattr(self, "_video_state", None)
        if vs and vs.get("tmpdir"):
            import shutil
            try: shutil.rmtree(vs["tmpdir"], ignore_errors=True)
            except Exception: pass  # temp dir cleanup failed, safe to ignore
        self._video_state = None
        for b in getattr(self, "_video_controls", []):
            try: b.destroy()
            except Exception: pass  # widget may already be destroyed
        self._video_controls = []
        self.editor_frame.grid_remove()
        self.imported_list.grid()
        self._editing_path = None

    def _show_file_history(self):
        path = getattr(self, "_editing_path", None)
        if not path:
            return
        base = os.path.dirname(path)
        name = os.path.basename(path)
        ver_dir = os.path.join(base, ".versions")
        if not os.path.isdir(ver_dir):
            messagebox.showinfo(self._tr("version_history"), self._tr("no_previous_versions"))
            return
        versions = sorted(
            [os.path.join(ver_dir, f) for f in os.listdir(ver_dir) if f.startswith(name + ".")],
            reverse=True
        )
        if not versions:
            messagebox.showinfo(self._tr("version_history"), self._tr("no_previous_versions"))
            return
        win = ctk.CTkToplevel(self.window)
        win.title(f"Version History — {name}")
        win.geometry("600x400")
        win.transient(self.window)
        ctk.CTkLabel(win, text=self._tr("version_history_label").format(name=name), font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        list_frame = ctk.CTkScrollableFrame(win)
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        for vp in versions:
            vname = os.path.basename(vp)
            ts_part = vname.split(".")[-1] if "." in vname else ""
            size_kb = os.path.getsize(vp) // 1024
            card = ctk.CTkFrame(list_frame, fg_color="#FFF8F0", corner_radius=6)
            card.pack(fill="x", pady=3)
            ctk.CTkLabel(card, text=f"  {ts_part}  ({size_kb} KB)", font=ctk.CTkFont(size=12),
                         anchor="w").pack(side="left", padx=10, pady=6)
            ctk.CTkButton(card, text=self._tr("restore"), width=70, height=26, font=ctk.CTkFont(size=11),
                         command=lambda v=vp: self._restore_version(v, win)).pack(side="right", padx=10)

    def _restore_version(self, version_path, win):
        if not messagebox.askyesno(self._tr("confirm_title"), self._tr("restore_version_confirm")):
            return
        try:
            import shutil
            path = getattr(self, "_editing_path", None)
            if path:
                self._save_version_backup(path)
                shutil.copy2(version_path, path)
                self._open_imported_viewer(path)
                self.editor_status.configure(text=self._tr("version_restored"), text_color="#000000")
                win.destroy()
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Could not restore:\n{e}")

    def _show_image_preview(self, path):
        try:
            from PIL import Image
            img = Image.open(path)
            img.thumbnail((800, 600))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            win = ctk.CTkToplevel(self.window)
            win.title(os.path.basename(path))
            win.geometry(f"{img.width + 60}x{img.height + 100}")
            ctk.CTkLabel(win, text=os.path.basename(path), font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
            lbl = ctk.CTkLabel(win, image=ctk_img, text="")
            lbl.pack(pady=10)
            lbl.image = ctk_img
        except Exception as e:
            messagebox.showerror(self._tr("gen_error"), f"Could not open image:\n{e}")

    def setup_create_tab(self):
        main = ctk.CTkFrame(self.tab_create, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=0, pady=0)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)
        self.create_tabview = ctk.CTkTabview(main, corner_radius=4)
        self.create_tabview.grid(row=0, column=0, sticky="nsew")
        self._scratch_count = 0
        upload_tab = self.create_tabview.add(self._tr("upload_tab"))
        upload_tab.grid_columnconfigure(0, weight=1)
        upload_tab.grid_rowconfigure(1, weight=1)
        top_bar = ctk.CTkFrame(upload_tab, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(8, 8))
        ctk.CTkLabel(top_bar, text=self._tr("create_label"), font=ctk.CTkFont(size=13, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(top_bar, text="＋ Document", width=105, height=30,
                      font=ctk.CTkFont(size=12, weight="bold"), fg_color="#FFB74D", hover_color="#FFA726",
                      command=self._create_scratch_doc).pack(side="left", padx=3)
        ctk.CTkButton(top_bar, text="＋ Slide", width=90, height=30,
                      font=ctk.CTkFont(size=12, weight="bold"), fg_color="#FF8A65", hover_color="#FF7043",
                      command=self._create_scratch_slide).pack(side="left", padx=3)
        content_frame = ctk.CTkFrame(upload_tab)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        self._setup_create_upload(content_frame)

    def _create_scratch_doc(self):
        self._scratch_count += 1
        name = self._tr("doc_tab").format(n=self._scratch_count)
        tab = self.create_tabview.add(name)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        s = {"content": "", "filename": name, "filepath": None}
        outer = ctk.CTkFrame(tab, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_rowconfigure(2, weight=1)
        toolbar = ctk.CTkFrame(outer, fg_color="#FFB74D", height=38, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)
        tf = ctk.CTkFrame(toolbar, fg_color="transparent")
        tf.pack(fill="x", padx=4, pady=3)
        def tb(text, cmd, w=30, **kw):
            opts = {"width": w, "height": 28, "font": ctk.CTkFont(size=12, weight="bold"),
                    "fg_color": "transparent", "hover_color": "#3B86E8", "text_color": "white",
                    "border_width": 0, "corner_radius": 3}
            opts.update(kw)
            ctk.CTkButton(tf, text=text, command=cmd, **opts).pack(side="left", padx=1)
        tb("\u21A9", lambda: self._doc_undo(s))
        tb("\u21AA", lambda: self._doc_redo(s))
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        s["font_var"] = ctk.StringVar(value="Arial")
        fm = ctk.CTkOptionMenu(tf, variable=s["font_var"],
                               values=["Arial","Calibri","Courier New","Georgia","Tahoma","Times New Roman","Verdana"],
                               width=85, height=28, font=ctk.CTkFont(size=10), dropdown_font=ctk.CTkFont(size=10),
                               fg_color="white", button_color="#FFF0D0", text_color="#000000",
                               command=lambda v,s=s: self._doc_change_font(s))
        fm.pack(side="left", padx=1)
        s["size_var"] = ctk.StringVar(value="12")
        sz = ctk.CTkOptionMenu(tf, variable=s["size_var"],
                               values=["8","9","10","11","12","14","16","18","20","22","24","28","36","48"],
                               width=45, height=28, font=ctk.CTkFont(size=10), dropdown_font=ctk.CTkFont(size=10),
                               fg_color="white", button_color="#FFF0D0", text_color="#000000",
                               command=lambda v,s=s: self._doc_change_font(s))
        sz.pack(side="left", padx=1)
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb("B", lambda: self._doc_bold(s), fg_color="#7986CB", hover_color="#64B5F6")
        tb("I", lambda: self._doc_italic(s), fg_color="#7986CB", hover_color="#64B5F6")
        tb("U", lambda: self._doc_underline(s), fg_color="#7986CB", hover_color="#64B5F6")
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb("\u2261", lambda: self._doc_bullet(s))
        tb("1.", lambda: self._doc_numbered(s), w=32)
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb("\u25C0", lambda: self._doc_align(s, "left"))
        tb("\u25A0", lambda: self._doc_align(s, "center"))
        tb("\u25B6", lambda: self._doc_align(s, "right"))
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb("\uD83D\uDD17", lambda: self._doc_link(s))
        tb("\uD83D\uDCF7", lambda: self._doc_insert_image(s), w=36)
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb(self._tr("open"), lambda: self._doc_open_file(s), w=50, font=ctk.CTkFont(size=10))
        tb(self._tr("save"), lambda: self._doc_save_file(s), w=48, fg_color="#81C784", hover_color="#66BB6A",
           font=ctk.CTkFont(size=10, weight="bold"))
        tb(self._tr("save_as"), lambda: self._doc_save_as(s), w=60, font=ctk.CTkFont(size=10))
        tb(self._tr("close"), lambda n=name: self.create_tabview.delete(n), w=50, fg_color="#E57373", hover_color="#EF5350",
           font=ctk.CTkFont(size=10))
        canvas_frame = ctk.CTkFrame(outer, fg_color="#FFF0D0")
        canvas_frame.grid(row=2, column=0, sticky="nsew")
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        doc_page = ctk.CTkFrame(canvas_frame, fg_color="white", corner_radius=2,
                                border_width=1, border_color="#E0C9A6")
        doc_page.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        doc_page.grid_columnconfigure(0, weight=1)
        doc_page.grid_rowconfigure(0, weight=1)
        s["editor"] = ctk.CTkTextbox(doc_page, wrap="word", font=ctk.CTkFont(size=12, family="Arial"),
                                      text_color="#000000", fg_color="white", border_width=0)
        s["editor"].grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        s["editor"].bind("<KeyRelease>", lambda e, s=s: self._doc_update_undo(s))
        s["undo_stack"] = [""]
        s["redo_stack"] = []
        s["undo_locked"] = False
        status_bar = ctk.CTkFrame(outer, fg_color="#FFF5EB", height=24, corner_radius=0)
        status_bar.grid(row=3, column=0, sticky="ew")
        status_bar.grid_propagate(False)
        s["status"] = ctk.CTkLabel(status_bar, text=self._tr("ready"), font=ctk.CTkFont(size=11), text_color="#000000")
        s["status"].pack(side="left", padx=12)
        ctk.CTkLabel(status_bar, text=self._tr("new_document"), font=ctk.CTkFont(size=11), text_color="#000000").pack(side="right", padx=12)
        self.create_tabview.set(name)

    def _doc_change_font(self, s):
        try:
            fn = s["font_var"].get()
            fs = int(s["size_var"].get())
            s["editor"].configure(font=ctk.CTkFont(size=fs, family=fn))
        except Exception: pass

    def _doc_bold(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            fn = s["font_var"].get()
            fs = int(s["size_var"].get())
            if "bold" in ed.tag_names(a): ed.tag_remove("bold", a, b)
            else: ed.tag_add("bold", a, b); ed.tag_config("bold", font=(fn, fs, "bold"))
        except Exception: pass

    def _doc_italic(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            fn = s["font_var"].get()
            fs = int(s["size_var"].get())
            if "italic" in ed.tag_names(a): ed.tag_remove("italic", a, b)
            else: ed.tag_add("italic", a, b); ed.tag_config("italic", font=(fn, fs, "italic"))
        except Exception: pass

    def _doc_underline(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            if "underline" in ed.tag_names(a): ed.tag_remove("underline", a, b)
            else: ed.tag_add("underline", a, b); ed.tag_config("underline", underline=True)
        except Exception: pass

    def _doc_align(self, s, al):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            ed.tag_add(f"al_{al}", a, b)
            ed.tag_config(f"al_{al}", justify=al, lmargin1=20, lmargin2=20)
        except Exception: pass

    def _doc_bullet(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if sel: ed.insert(sel[0], "\u2022 ")
        except Exception: pass

    def _doc_numbered(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if sel: ed.insert(sel[0], "1. ")
        except Exception: pass

    def _doc_link(self, s):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            ed.tag_add("link", a, b)
            ed.tag_config("link", foreground="#1a73e8", underline=True)
        except Exception: pass

    def _insert_image_common(self, s, status_label=None):
        path = filedialog.askopenfilename(title=self._tr("insert_image"), filetypes=[("All files", "*.*"), (self._tr("filter_images"), "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp *.svg *.ico *.heic *.avif")])
        if not path: return
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            photo = ImageTk.PhotoImage(img)
            ed = s["editor"]._textbox
            if "_images" not in s: s["_images"] = []
            idx = len(s["_images"])
            tag = f"_img_{id(s)}_{idx}"
            mark = f"_img_mark_{id(s)}_{idx}"
            ed.mark_set(mark, "insert")
            pos = ed.image_create("insert", image=photo)
            ed.mark_set(mark, pos)
            ed.tag_add(tag, pos)
            ed.tag_bind(tag, "<Button-1>",
                        lambda e, s=s, idx=idx: self._show_image_handles(s, idx))
            ed.tag_bind(tag, "<Double-Button-1>",
                        lambda e, s=s, idx=idx: self._resize_image_dialog(s, idx))
            s["_images"].append({
                "photo": photo, "path": path,
                "width": img.width, "height": img.height,
                "mark": mark, "tag": tag
            })
            ed.insert("insert", "\n")
            msg = f"Image inserted: {os.path.basename(path)}"
            if status_label:
                try: status_label.configure(text=msg)
                except Exception: pass  # status label destroyed or unavailable
        except Exception as e:
            msg = self._tr("error_status").format(err=e)
            if status_label:
                try: status_label.configure(text=msg)
                except Exception: pass  # status label destroyed or unavailable

    def _resize_image_dialog(self, s, idx):
        if idx >= len(s["_images"]): return
        entry = s["_images"][idx]
        from PIL import Image, ImageTk
        orig = Image.open(entry["path"])
        top = ctk.CTkToplevel(self.window)
        top.title(self._tr("resize_image"))
        top.geometry("300x180")
        top.transient(self.window)
        top.grab_set()
        ctk.CTkLabel(top, text=self._tr("width"), font=ctk.CTkFont(size=12)).pack(pady=(15, 2))
        w_var = ctk.StringVar(value=str(entry["width"]))
        h_var = ctk.StringVar(value=str(entry["height"]))
        w_spin = ctk.CTkEntry(top, textvariable=w_var, width=100, justify="center")
        w_spin.pack()
        ctk.CTkLabel(top, text=self._tr("height"), font=ctk.CTkFont(size=12)).pack(pady=(10, 2))
        h_spin = ctk.CTkEntry(top, textvariable=h_var, width=100, justify="center")
        h_spin.pack()
        lock_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(top, text=self._tr("keep_aspect_ratio"), variable=lock_var,
                        font=ctk.CTkFont(size=11)).pack(pady=8)
        ed = s["editor"]._textbox
        def do_resize():
            try:
                nw = int(w_var.get())
                nh = int(h_var.get())
                if nw < 1 or nh < 1: return
                resized = orig.resize((nw, nh), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized)
                tag = entry["tag"]
                mark = entry["mark"]
                img_pos = ed.index(mark)
                ed.tag_delete(tag)
                ed.delete(img_pos)
                new_pos = ed.image_create(img_pos, image=photo)
                ed.mark_set(mark, new_pos)
                ed.tag_add(tag, new_pos)
                ed.tag_bind(tag, "<Button-1>",
                            lambda e, s=s, idx=idx: self._show_image_handles(s, idx))
                ed.tag_bind(tag, "<Double-Button-1>",
                            lambda e, s=s, idx=idx: self._resize_image_dialog(s, idx))
                entry["photo"] = photo
                entry["width"] = nw
                entry["height"] = nh
                top.destroy()
            except Exception: pass  # resize apply failed, dialog still usable
        ctk.CTkButton(top, text=self._tr("resize"), command=do_resize,
                      fg_color="#FFB74D", hover_color="#FFA726",
                      font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)
        def on_w_change(*_):
            if lock_var.get():
                try:
                    nw = int(w_var.get())
                    ratio = orig.height / orig.width
                    h_var.set(str(int(nw * ratio)))
                except Exception: pass  # non-numeric input, skip ratio update
        w_var.trace_add("write", on_w_change)

    def _show_image_handles(self, s, idx):
        self._hide_image_handles()
        if idx >= len(s["_images"]): return
        entry = s["_images"][idx]
        ed = s["editor"]._textbox
        pos = ed.index(entry["mark"])
        bbox = ed.bbox(pos)
        if not bbox: return
        x, y, w, h = bbox
        import tkinter as tk
        handles = []
        for dx, dy, cur in [(0, 0, "nw-resize"), (w, 0, "ne-resize"),
                            (0, h, "sw-resize"), (w, h, "se-resize")]:
            hdl = tk.Frame(ed, width=8, height=8, bg="#1a73e8",
                           highlightthickness=1, highlightbackground="white",
                           cursor=cur)
            hdl.place(x=x + dx - 4, y=y + dy - 4)
            hdl.bind("<Button-1>", lambda e, s=s, idx=idx, corner=(dx, dy):
                     self._start_resize_drag(e, s, idx, corner))
            hdl.bind("<B1-Motion>", lambda e, s=s, idx=idx:
                     self._do_resize_drag(e, s, idx))
            handles.append(hdl)
        entry["_handles"] = handles
        self._active_image = (s, idx)
        ed.bind("<Button-1>", self._hide_image_handles_on_click, add=True)
        ed.bind("<MouseWheel>", lambda e: self._hide_image_handles(), add=True)

    def _hide_image_handles_on_click(self, e):
        try:
            if not self._active_image: return
            ed = self._active_image[0]["editor"]._textbox
            if e.widget == ed:
                clicked_tag = ed.tag_names(f"@{e.x},{e.y}")
                if not any(t.startswith("_img_") for t in clicked_tag):
                    self._hide_image_handles()
        except Exception: pass  # image handle state already cleared

    def _hide_image_handles(self):
        try:
            for h in getattr(self, "_active_image_handles", []):
                try: h.destroy()
                except Exception: pass  # handle already destroyed
            if self._active_image:
                s, idx = self._active_image
                entry = s["_images"][idx] if idx < len(s["_images"]) else None
                if entry and "_handles" in entry:
                    for h in entry["_handles"]:
                        try: h.destroy()
                        except Exception: pass  # handle already destroyed
                    entry["_handles"] = []
                    try: entry["photo"] = entry.get("photo")
                    except Exception: pass  # no-op, safe to ignore
        except Exception: pass  # image handle state already cleared
        self._active_image = None

    def _start_resize_drag(self, e, s, idx, corner):
        if idx >= len(s["_images"]): return
        entry = s["_images"][idx]
        self._drag_data = {
            "s": s, "idx": idx, "corner": corner,
            "start_x": e.x_root, "start_y": e.y_root,
            "start_w": entry["width"], "start_h": entry["height"]
        }

    def _do_resize_drag(self, e, s, idx):
        d = getattr(self, "_drag_data", None)
        if not d or d["idx"] != idx: return
        entry = s["_images"][idx]
        from PIL import Image, ImageTk
        dx = e.x_root - d["start_x"]
        dy = e.y_root - d["start_y"]
        cx, cy = d["corner"]
        nw = max(20, d["start_w"] + (dx if cx > 0 else -dx))
        nh = max(20, d["start_h"] + (dy if cy > 0 else -dy))
        ratio = Image.open(entry["path"]).width / Image.open(entry["path"]).height
        nw = int(nh * ratio)
        if idx >= len(s["_images"]): return
        ed = s["editor"]._textbox
        try:
            orig = Image.open(entry["path"])
            resized = orig.resize((nw, nh), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            tag = entry["tag"]
            mark = entry["mark"]
            self._hide_image_handles()
            img_pos = ed.index(mark)
            ed.tag_delete(tag)
            ed.delete(img_pos)
            new_pos = ed.image_create(img_pos, image=photo)
            ed.mark_set(mark, new_pos)
            ed.tag_add(tag, new_pos)
            ed.tag_bind(tag, "<Button-1>",
                        lambda e, s=s, idx=idx: self._show_image_handles(s, idx))
            ed.tag_bind(tag, "<Double-Button-1>",
                        lambda e, s=s, idx=idx: self._resize_image_dialog(s, idx))
            entry["photo"] = photo
            entry["width"] = nw
            entry["height"] = nh
            self._show_image_handles(s, idx)
        except Exception: pass  # resize drag update failed, skip frame

    def _doc_insert_image(self, s):
        self._insert_image_common(s, s.get("status"))

    def _doc_open_file(self, s):
        path = filedialog.askopenfilename(title=self._tr("open_file"),
            filetypes=[("Text files", "*.md *.txt *.csv *.json *.xml *.html *.css *.js *.py *.yaml *.yml *.ini *.cfg *.log *.bat *.ps1 *.sh *.env *.java *.cpp *.c *.h *.rb *.php *.rs *.go *.ts *.sql *.r *.lua *.dart *.kt *.swift"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            s["editor"].delete("0.0", "end")
            s["editor"].insert("0.0", content)
            s["filepath"] = path
            s["status"].configure(text=self._tr("opened_file").format(fname=os.path.basename(path)))
        except Exception as e:
            s["status"].configure(text=self._tr("error_status").format(err=e))

    def _doc_save_file(self, s):
        content = s["editor"].get("0.0", "end-1c")
        path = s.get("filepath")
        if not path:
            path = filedialog.asksaveasfilename(defaultextension=".md",
                filetypes=[("Markdown", "*.md"), (self._tr("filter_text"), "*.txt"), ("All files", "*.*")],
                initialdir=os.path.join(learning_data.APP_ROOT, "Created"))
            if not path: return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            s["filepath"] = path
            s["status"].configure(text=self._tr("saved_file").format(fname=os.path.basename(path)))
        except Exception as e:
            s["status"].configure(text=self._tr("error_status").format(err=e))

    def _doc_save_as(self, s):
        path = filedialog.asksaveasfilename(defaultextension=".md",
            filetypes=[("Markdown", "*.md"), (self._tr("filter_text"), "*.txt"), ("All files", "*.*")],
            initialdir=os.path.join(learning_data.APP_ROOT, "Created"))
        if not path: return
        content = s["editor"].get("0.0", "end-1c")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            s["filepath"] = path
            s["status"].configure(text=self._tr("saved_file").format(fname=os.path.basename(path)))
        except Exception as e:
            s["status"].configure(text=self._tr("error_status").format(err=e))

    def _doc_undo(self, s):
        if len(s["undo_stack"]) <= 1: return
        s["redo_stack"].append(s["editor"].get("0.0", "end-1c"))
        s["undo_stack"].pop()
        s["undo_locked"] = True
        s["editor"].delete("0.0", "end")
        s["editor"].insert("0.0", s["undo_stack"][-1])
        s["undo_locked"] = False

    def _doc_redo(self, s):
        if not s["redo_stack"]: return
        s["undo_stack"].append(s["redo_stack"].pop())
        s["undo_locked"] = True
        s["editor"].delete("0.0", "end")
        s["editor"].insert("0.0", s["undo_stack"][-1])
        s["undo_locked"] = False

    def _doc_update_undo(self, s):
        if s.get("undo_locked"): return
        s["undo_stack"].append(s["editor"].get("0.0", "end-1c"))
        if len(s["undo_stack"]) > 50: s["undo_stack"].pop(0)
        s["redo_stack"].clear()

    def _create_scratch_slide(self):
        self._scratch_count += 1
        name = self._tr("slide_tab").format(n=self._scratch_count)
        tab = self.create_tabview.add(name)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        s = {"slides": [{"bg": "#ffffff", "text": ""}], "current": 0, "filename": name, "filepath": None}
        left_panel = ctk.CTkFrame(tab, width=180, corner_radius=6)
        left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 5), pady=5)
        left_panel.grid_propagate(False)
        ctk.CTkLabel(left_panel, text=self._tr("slides"), font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#000000").pack(pady=(10, 6))
        s["slide_list"] = ctk.CTkScrollableFrame(left_panel, height=320)
        s["slide_list"].pack(fill="both", expand=True, padx=6, pady=(0, 6))
        ctk.CTkButton(left_panel, text=self._tr("add_slide"), height=32,
                      font=ctk.CTkFont(size=12, weight="bold"), fg_color="#FF8A65", hover_color="#FF7043",
                      command=lambda s=s: self._pres_add_slide(s)).pack(fill="x", padx=8, pady=(0, 3))
        ctk.CTkButton(left_panel, text=self._tr("delete_selected"), height=32,
                      font=ctk.CTkFont(size=12), fg_color="#E57373", hover_color="#EF5350",
                      command=lambda s=s: self._pres_delete_slide(s)).pack(fill="x", padx=8, pady=(0, 3))
        ctk.CTkButton(left_panel, text=self._tr("close_tab"), height=30,
                      font=ctk.CTkFont(size=11), fg_color="#90A4AE", hover_color="#78909C",
                      command=lambda n=name: self.create_tabview.delete(n)).pack(fill="x", padx=8, pady=(5, 8))
        editor_area = ctk.CTkFrame(tab, corner_radius=6)
        editor_area.grid(row=0, column=1, sticky="nsew", pady=5, padx=(0, 5))
        editor_area.grid_columnconfigure(0, weight=1)
        editor_area.grid_rowconfigure(3, weight=1)
        toolbar = ctk.CTkFrame(editor_area, fg_color="#FF8A65", height=38, corner_radius=0)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)
        tf = ctk.CTkFrame(toolbar, fg_color="transparent")
        tf.pack(fill="x", padx=4, pady=3)
        def tb(text, cmd, w=30, **kw):
            opts = {"width": w, "height": 28, "font": ctk.CTkFont(size=12, weight="bold"),
                    "fg_color": "transparent", "hover_color": "#D95A3A", "text_color": "white",
                    "border_width": 0, "corner_radius": 3}
            opts.update(kw)
            ctk.CTkButton(tf, text=text, command=cmd, **opts).pack(side="left", padx=1)
        tb("B", lambda: self._pres_bold(s))
        tb("I", lambda: self._pres_italic(s))
        tb("U", lambda: self._pres_underline(s))
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        s["font_size"] = ctk.StringVar(value="18")
        sz = ctk.CTkOptionMenu(tf, variable=s["font_size"],
                               values=["12","14","16","18","20","24","28","32","36","48"],
                               width=45, height=28, font=ctk.CTkFont(size=10), dropdown_font=ctk.CTkFont(size=10),
                               fg_color="white", button_color="#FFF0D0", text_color="#000000")
        sz.pack(side="left", padx=1)
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb(self._tr("background"), lambda: self._pres_bg_color(s), w=85, font=ctk.CTkFont(size=10))
        tb(self._tr("image"), lambda: self._pres_insert_image(s), w=60, font=ctk.CTkFont(size=10))
        ctk.CTkLabel(tf, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        tb(self._tr("open"), lambda: self._pres_open_file(s), w=55, font=ctk.CTkFont(size=10))
        tb(self._tr("save"), lambda: self._pres_save(s), w=50, fg_color="#81C784", hover_color="#66BB6A",
           font=ctk.CTkFont(size=10, weight="bold"))
        tb(self._tr("save_as"), lambda: self._pres_save_as(s), w=60, font=ctk.CTkFont(size=10))
        nav_bar = ctk.CTkFrame(editor_area, fg_color="#FFF5EB", height=30, corner_radius=0)
        nav_bar.grid(row=1, column=0, sticky="ew")
        nav_bar.grid_propagate(False)
        ctk.CTkButton(nav_bar, text="\u25C0", width=26, height=22, font=ctk.CTkFont(size=11),
                      fg_color="#FFE0B2", hover_color="#E0C9A6", text_color="#000",
                      command=lambda s=s: self._pres_prev(s)).pack(side="left", padx=4, pady=4)
        s["page_label"] = ctk.CTkLabel(nav_bar, text=self._tr("slide_page").format(current=1, total=1), font=ctk.CTkFont(size=11, weight="bold"),
                                       text_color="#000")
        s["page_label"].pack(side="left", padx=6)
        ctk.CTkButton(nav_bar, text="\u25B6", width=26, height=22, font=ctk.CTkFont(size=11),
                      fg_color="#FFE0B2", hover_color="#E0C9A6", text_color="#000",
                      command=lambda s=s: self._pres_next(s)).pack(side="left", padx=4, pady=4)
        ctk.CTkLabel(nav_bar, text="|", text_color="#000000", font=ctk.CTkFont(size=14)).pack(side="left", padx=4)
        s["pres_status"] = ctk.CTkLabel(nav_bar, text=self._tr("ready"), font=ctk.CTkFont(size=10), text_color="#000000")
        s["pres_status"].pack(side="left", padx=6)
        slide_frame = ctk.CTkFrame(editor_area, fg_color="#FFF5EB", corner_radius=4)
        slide_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(6, 8))
        slide_frame.grid_columnconfigure(0, weight=1)
        slide_frame.grid_rowconfigure(0, weight=1)
        slide_inner = ctk.CTkFrame(slide_frame, fg_color="#ffffff", corner_radius=2,
                                   border_width=1, border_color="#E0C9A6")
        slide_inner.grid(row=0, column=0, sticky="nsew", padx=30, pady=20)
        slide_inner.grid_columnconfigure(0, weight=1)
        slide_inner.grid_rowconfigure(0, weight=1)
        s["editor"] = ctk.CTkTextbox(slide_inner, wrap="word", font=ctk.CTkFont(size=18, family="Arial"),
                                      text_color="#000000", fg_color="white", border_width=0)
        s["editor"].grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self._pres_build_all_thumbs(s)
        self._pres_update_label(s)
        self.create_tabview.set(name)

    def _pres_tag_apply(self, s, tag, config):
        ed = s["editor"]
        try:
            sel = ed.tag_ranges("sel")
            if not sel: return
            a, b = sel[0], sel[1]
            if tag in ed.tag_names(a): ed.tag_remove(tag, a, b)
            else: ed.tag_add(tag, a, b); ed.tag_config(tag, **config)
        except Exception: pass

    def _pres_bold(self, s):
        sz = int(s["font_size"].get())
        self._pres_tag_apply(s, "bold", {"font": ("Arial", sz, "bold")})

    def _pres_italic(self, s):
        sz = int(s["font_size"].get())
        self._pres_tag_apply(s, "italic", {"font": ("Arial", sz, "italic")})

    def _pres_underline(self, s):
        self._pres_tag_apply(s, "underline", {"underline": True})

    def _pres_add_slide(self, s):
        idx = len(s["slides"])
        s["slides"].append({"bg": "#ffffff", "text": ""})
        self._pres_build_all_thumbs(s)
        self._pres_select_slide(s, idx)
        self._pres_update_label(s)
        try: s["pres_status"].configure(text=self._tr("slide_added"))
        except Exception: pass  # status label destroyed or unavailable

    def _pres_delete_slide(self, s):
        if len(s["slides"]) <= 1: return
        idx = s["current"]
        s["slides"].pop(idx)
        self._pres_build_all_thumbs(s)
        self._pres_select_slide(s, min(idx, len(s["slides"]) - 1))

    def _pres_build_all_thumbs(self, s):
        for w in s["slide_list"].winfo_children(): w.destroy()
        for i in range(len(s["slides"])):
            sel = i == s.get("current", 0)
            thumb = ctk.CTkFrame(s["slide_list"], fg_color="#FFF0D0" if sel else "transparent",
                                corner_radius=4, height=38, border_width=1,
                                border_color="#FFAB91" if sel else "#ccc")
            thumb.pack(fill="x", pady=2)
            thumb._idx = i
            thumb.bind("<Button-1>", lambda e, idx=i, s=s: self._pres_select_slide(s, idx))
            ctk.CTkLabel(thumb, text=self._tr("slide_number").format(n=i+1), font=ctk.CTkFont(size=11), text_color="#000").pack(side="left", padx=8)

    def _pres_select_slide(self, s, idx):
        if 0 <= s["current"] < len(s["slides"]):
            s["slides"][s["current"]]["text"] = s["editor"].get("0.0", "end-1c")
        s["current"] = idx
        for w in s["slide_list"].winfo_children():
            is_sel = getattr(w, "_idx", -1) == idx
            w.configure(fg_color="#FFF0D0" if is_sel else "transparent", border_color="#FFAB91" if is_sel else "#ccc")
        s["editor"].delete("0.0", "end")
        s["editor"].insert("0.0", s["slides"][idx]["text"])
        self._pres_update_label(s)

    def _pres_update_label(self, s):
        try: s["page_label"].configure(text=self._tr("slide_page").format(current=s["current"]+1, total=len(s["slides"])))
        except Exception: pass  # label destroyed or unavailable

    def _pres_prev(self, s):
        if s["current"] > 0:
            s["slides"][s["current"]]["text"] = s["editor"].get("0.0", "end-1c")
            self._pres_select_slide(s, s["current"] - 1)

    def _pres_next(self, s):
        if s["current"] < len(s["slides"]) - 1:
            s["slides"][s["current"]]["text"] = s["editor"].get("0.0", "end-1c")
            self._pres_select_slide(s, s["current"] + 1)

    def _pres_bg_color(self, s):
        from tkinter import colorchooser
        c = colorchooser.askcolor(title=self._tr("slide_background_title"),
                                  initialcolor=s["slides"][s["current"]].get("bg", "#ffffff"))
        if c and c[1]:
            s["slides"][s["current"]]["bg"] = c[1]

    def _pres_insert_image(self, s):
        self._insert_image_common(s, s.get("pres_status"))

    def _pres_open_file(self, s):
        path = filedialog.askopenfilename(title=self._tr("open_presentation"),
            filetypes=[("Markdown", "*.md"), (self._tr("filter_text"), "*.txt"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                content = f.read()
            s["filepath"] = path
            slides_raw = content.split("---")
            s["slides"] = []
            for i, chunk in enumerate(slides_raw):
                lines = chunk.strip().split("\n")
                text_lines = [l for l in lines if not l.startswith("## ") and not l.startswith("# ")]
                s["slides"].append({"bg": "#ffffff", "text": "\n".join(text_lines).strip()})
            if not s["slides"]: s["slides"] = [{"bg": "#ffffff", "text": ""}]
            s["current"] = 0
            self._pres_build_all_thumbs(s)
            self._pres_select_slide(s, 0)
            try: s["pres_status"].configure(text=self._tr("opened_file").format(fname=os.path.basename(path)))
            except Exception: pass  # status label destroyed or unavailable
        except Exception as e:
            try: s["pres_status"].configure(text=self._tr("error_status").format(err=e))
            except Exception: pass  # status label destroyed or unavailable

    def _pres_save(self, s):
        if 0 <= s["current"] < len(s["slides"]):
            s["slides"][s["current"]]["text"] = s["editor"].get("0.0", "end-1c")
        path = s.get("filepath")
        if not path:
            path = filedialog.asksaveasfilename(defaultextension=".md",
                filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
                initialdir=os.path.join(learning_data.APP_ROOT, "Created"))
            if not path: return
        try:
            parts = [f"# {os.path.basename(path).replace('.md','')}"]
            for i, slide in enumerate(s["slides"]):
                parts.append(f"## Slide {i + 1}")
                txt = slide.get("text", "").strip()
                if txt: parts.append(txt)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n\n---\n\n".join(parts))
            s["filepath"] = path
            try: s["pres_status"].configure(text=self._tr("saved_file").format(fname=os.path.basename(path)))
            except Exception: pass  # status label destroyed or unavailable
        except Exception as e:
            try: s["pres_status"].configure(text=self._tr("error_status").format(err=e))
            except Exception: pass  # status label destroyed or unavailable

    def _pres_save_as(self, s):
        if 0 <= s["current"] < len(s["slides"]):
            s["slides"][s["current"]]["text"] = s["editor"].get("0.0", "end-1c")
        path = filedialog.asksaveasfilename(defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("All files", "*.*")],
            initialdir=os.path.join(learning_data.APP_ROOT, "Created"))
        if not path: return
        parts = [f"# {os.path.basename(path).replace('.md','')}"]
        for i, slide in enumerate(s["slides"]):
            parts.append(f"## Slide {i + 1}")
            txt = slide.get("text", "").strip()
            if txt: parts.append(txt)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n\n---\n\n".join(parts))
            s["filepath"] = path
            try: s["pres_status"].configure(text=self._tr("saved_file").format(fname=os.path.basename(path)))
            except Exception: pass  # status label destroyed or unavailable
        except Exception as e:
            try: s["pres_status"].configure(text=self._tr("error_status").format(err=e))
            except Exception: pass  # status label destroyed or unavailable

    def _setup_create_upload(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(5, 10))
        ctk.CTkButton(top, text=self._tr("import_folder"), width=120, height=32,
                      command=self._import_folder, font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
        ctk.CTkButton(top, text=self._tr("upload_file"), width=120, height=32,
                      command=self._create_upload_single, font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        self.create_upload_status = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=11))
        self.create_upload_status.pack(side="left", padx=15)
        list_frame = ctk.CTkFrame(parent)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        self.create_upload_list = ctk.CTkScrollableFrame(list_frame)
        self.create_upload_list.pack(fill="both", expand=True)
        ctk.CTkLabel(self.create_upload_list, text=self._tr("uploaded_will_appear"),
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)

    def _create_upload_single(self):
        path = filedialog.askopenfilename(title=self._tr("select_file_upload"))
        if not path:
            return
        save_dir = os.path.join(learning_data.APP_ROOT, "Created")
        os.makedirs(save_dir, exist_ok=True)
        try:
            import shutil
            dst = os.path.join(save_dir, os.path.basename(path))
            shutil.copy2(path, dst)
            self.create_upload_status.configure(text=self._tr("uploaded_file").format(fname=os.path.basename(path)), text_color="#000000")
            self._create_refresh_upload_list(save_dir)
        except Exception as e:
            self.create_upload_status.configure(text=self._tr("error_status").format(err=e), text_color="#000000")

    def _create_refresh_upload_list(self, directory):
        for w in self.create_upload_list.winfo_children():
            w.destroy()
        try:
            items = sorted(os.listdir(directory))
        except Exception:
            items = []
        if not items:
            ctk.CTkLabel(self.create_upload_list, text=self._tr("no_files_uploaded"),
                         font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=40)
            return
        for name in items:
            fpath = os.path.join(directory, name)
            if os.path.isfile(fpath):
                card = ctk.CTkFrame(self.create_upload_list, fg_color="#FFF8F0", corner_radius=6)
                card.pack(fill="x", pady=2, padx=5)
                ctk.CTkLabel(card, text=f"  {name}", font=ctk.CTkFont(size=12),
                             anchor="w").pack(side="left", padx=10, pady=4)
                ctk.CTkButton(card, text=self._tr("open"), width=50, height=24, font=ctk.CTkFont(size=10),
                             command=lambda p=fpath: os.startfile(p)).pack(side="right", padx=10)

    def _render_md(self, content):
        self.md_text.configure(state="normal")
        self.md_text.delete("0.0", "end")
        for tag in self.md_text.tag_names():
            if tag != "sel":
                self.md_text.tag_delete(tag)

        label = getattr(self, "_current_md_label", "")
        subject_emoji, subject_color, diff_name = self._parse_md_label(label)

        self.md_text.tag_config("h1", foreground=subject_color, spacing3=10, spacing2=8)
        self.md_text.tag_config("h2", foreground=subject_color, spacing3=8, spacing2=5)
        self.md_text.tag_config("h3", foreground=subject_color, spacing3=6, spacing2=4)
        self.md_text.tag_config("h4", spacing3=4, spacing2=3)
        self.md_text.tag_config("h5", spacing3=4, spacing2=2)
        self.md_text.tag_config("h6", spacing3=4, spacing2=2)
        self.md_text.tag_config("code", background="#f5f5f5", lmargin1=15, lmargin2=15, spacing3=2, spacing2=2)
        self.md_text.tag_config("quote", foreground="#666666", lmargin1=30, lmargin2=30, spacing3=2)
        self.md_text.tag_config("hr", foreground="#cccccc")
        self.md_text.tag_config("bullet", lmargin1=20, lmargin2=35)

        if label:
            banner = f" {subject_emoji}  {label}\n"
            self.md_text.insert("end", banner, "h1")
            if diff_name:
                diff_colors = {"Full Lesson": "#81C784", "Easy": "#A5D6A7", "Medium": "#FFE082", "Hard": "#EF9A9A", "Practice": "#CE93D8", "Full Assessment": "#F48FB1"}
                dc = diff_colors.get(diff_name, "#888888")
                self.md_text.tag_config("diff_badge", foreground=dc)
                self.md_text.insert("end", f"  [{diff_name}]\n", "diff_badge")
            self.md_text.insert("end", "─" * 70 + "\n\n", "hr")

        inside_code = False
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("```"):
                inside_code = not inside_code
                continue
            if inside_code:
                self.md_text.insert("end", line + "\n", "code")
                continue
            if stripped.startswith("###### "):
                self.md_text.insert("end", stripped[7:] + "\n", "h6")
            elif stripped.startswith("##### "):
                self.md_text.insert("end", stripped[6:] + "\n", "h5")
            elif stripped.startswith("#### "):
                self.md_text.insert("end", stripped[5:] + "\n", "h4")
            elif stripped.startswith("### "):
                self.md_text.insert("end", stripped[4:] + "\n", "h3")
            elif stripped.startswith("## "):
                self.md_text.insert("end", stripped[3:] + "\n", "h2")
            elif stripped.startswith("# "):
                self.md_text.insert("end", stripped[2:] + "\n", "h1")
            elif stripped.startswith("---") or stripped.startswith("***"):
                self.md_text.insert("end", "─" * 70 + "\n", "hr")
            elif stripped.startswith("- ") or stripped.startswith("* "):
                self.md_text.insert("end", "  \u2022  " + stripped[2:] + "\n", "bullet")
            elif stripped.startswith("> "):
                self.md_text.insert("end", "  \u2502  " + stripped[2:] + "\n", "quote")
            elif not stripped:
                self.md_text.insert("end", "\n")
            else:
                self.md_text.insert("end", line + "\n")
        self.md_text.configure(state="disabled")

    def _parse_md_label(self, label):
        if not label:
            return "\U0001f4c4", "#1a73e8", ""
        diff_name = ""
        for d in ["Full Assessment", "Full Lesson", "Practice", "Hard", "Medium", "Easy"]:
            if label.endswith(f"({d})"):
                diff_name = d
                break
        label_lower = label.lower()
        emoji = "\U0001f4c4"
        for keyword, e in SUBJECT_EMOJI_MAP:
            if keyword in label_lower:
                emoji = e
                break
        color = "#1a73e8"
        for keyword, c in SUBJECT_COLOR_MAP:
            if keyword in label_lower:
                color = c
                break
        return emoji, color, diff_name

    def _tr(self, key):
        lang_dict = UI_TR.get(self.language, UI_TR["english"])
        return lang_dict.get(key, UI_TR["english"].get(key, key))

    def _translate_content(self, content):
        if not _TRANSLATOR_AVAIL or not content.strip():
            return content
        cache_key = (self.language, hash(content[:200]))
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        try:
            if self.language == "english":
                t = GoogleTranslator(source="tl", target="en")
                MAX_CHUNK = 5000
                if len(content) > MAX_CHUNK:
                    chunks = [content[i:i+MAX_CHUNK] for i in range(0, len(content), MAX_CHUNK)]
                    translated = "".join(t.translate(c) for c in chunks)
                else:
                    translated = t.translate(content)
            else:
                return content
            self._translation_cache[cache_key] = translated
            return translated
        except Exception:
            return content

    def setup_answer_sheets_tab(self):
        main = ctk.CTkFrame(self.tab_answer)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)
        top_bar = ctk.CTkFrame(main, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", pady=(10, 5))
        top_bar.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(top_bar, text=self._tr("answer_sheets_title"),
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", anchor="w")
        self.ans_lang_var = ctk.StringVar(value="English" if self.language == "english" else "Tagalog")
        self.ans_lang_var.trace_add("write", self._on_ans_lang_change)
        ctk.CTkOptionMenu(top_bar, variable=self.ans_lang_var, values=["English", "Tagalog"],
                          width=110, font=ctk.CTkFont(size=13)).pack(side="right", padx=(10, 0))
        search_frame = ctk.CTkFrame(main, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)
        self.ans_search = ctk.CTkEntry(search_frame, placeholder_text=self._tr("search_answer"))
        self.ans_search.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.ans_search.bind("<KeyRelease>", lambda e: self._filter_answer_sheets())
        ctk.CTkButton(search_frame, text=self._tr("refresh"), width=80, command=self._load_answer_sheets).grid(row=0, column=1, padx=(0, 5))
        ctk.CTkButton(search_frame, text=self._tr("show_all_answers"), width=130,
                      command=self._show_all_answers, font=ctk.CTkFont(size=12)).grid(row=0, column=2)
        display_frame = ctk.CTkFrame(main)
        display_frame.grid(row=2, column=0, sticky="nsew")
        display_frame.grid_columnconfigure(0, weight=0)
        display_frame.grid_columnconfigure(1, weight=1)
        display_frame.grid_rowconfigure(0, weight=1)
        self.ans_list = ctk.CTkScrollableFrame(display_frame, width=320)
        self.ans_list.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        self.ans_view = ctk.CTkTextbox(display_frame, wrap="word", font=ctk.CTkFont(size=13), text_color="#000000", fg_color="#FFF0D0")
        self.ans_view.grid(row=0, column=1, sticky="nsew")
        self._load_answer_sheets()

    def _load_answer_sheets(self):
        self.answer_sheets_data = learning_data.scan_answer_sheets()
        self._filter_answer_sheets()

    def _filter_answer_sheets(self):
        for w in self.ans_list.winfo_children():
            w.destroy()
        query = self.ans_search.get().strip().lower()
        filtered = [s for s in self.answer_sheets_data if not query or query in s["label"].lower()]
        if not filtered:
            ctk.CTkLabel(self.ans_list, text=self._tr("no_answer_sheets"), font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=30)
            return
        for sheet in filtered:
            has_key = bool(sheet["answer_key"])
            status = "\u2705" if has_key else "\u26a0\ufe0f"
            key_lines = sheet["answer_key"].count("\n") + 1 if has_key else 0
            label_text = f"{status} {sheet['label'][:55]}"
            btn = ctk.CTkButton(self.ans_list, text=label_text, anchor="w", height=32,
                                font=ctk.CTkFont(size=11),
                                command=lambda s=sheet: self._show_answer(s))
            btn.pack(fill="x", pady=2)
            if has_key:
                ctk.CTkLabel(self.ans_list, text=self._tr("ans_count").format(count=key_lines),
                            font=ctk.CTkFont(size=9), text_color="#000000", anchor="w").pack(fill="x", padx=(15, 0))

    def _show_answer(self, sheet):
        self._current_answer_sheet = sheet
        self.ans_view.configure(state="normal")
        self.ans_view.delete("0.0", "end")
        for tag in self.ans_view.tag_names():
            if tag != "sel":
                self.ans_view.tag_delete(tag)
        self.ans_view.tag_config("title", foreground="#1a73e8", spacing3=8, spacing2=5)
        self.ans_view.tag_config("header", foreground="#333", spacing3=6, spacing2=3)
        self.ans_view.tag_config("key", foreground="#81C784", spacing3=2, spacing2=1)
        self.ans_view.tag_config("no_key", foreground="#EF9A9A")
        self.ans_view.tag_config("hr", foreground="#cccccc")
        _, subj_color, _ = self._parse_md_label(sheet["label"])
        self.ans_view.tag_config("subj", foreground=subj_color, spacing3=6)
        label_emoji = ""
        for kw, e in SUBJECT_EMOJI_MAP:
            if kw in sheet["label"].lower():
                label_emoji = e
                break
        lang = self.ans_lang_var.get().lower() if hasattr(self, "ans_lang_var") else self.language
        self.language = lang
        use_en = lang == "english" and sheet.get("answer_key_en")
        use_tl = lang == "tagalog" and sheet.get("answer_key_tl")
        if use_tl:
            answer_key = sheet["answer_key_tl"]
            lang_tag = " (TL)"
        elif use_en:
            answer_key = sheet["answer_key_en"]
            lang_tag = " (EN)"
        else:
            answer_key = sheet["answer_key"]
            lang_tag = ""
        self.ans_view.insert("end", f" {label_emoji}  {sheet['label']}{lang_tag}\n", "subj")
        self.ans_view.insert("end", "\u2500" * 70 + "\n\n", "hr")
        if answer_key:
            self.ans_view.insert("end", "ANSWER KEY\n", "title")
            self.ans_view.insert("end", "\u2500" * 40 + "\n", "hr")
            for line in answer_key.split("\n"):
                stripped = line.strip()
                if stripped.startswith("- ") or stripped.startswith("* "):
                    self.ans_view.insert("end", "  \u2022  " + stripped[2:] + "\n", "key")
                elif stripped.startswith("## "):
                    self.ans_view.insert("end", stripped[3:] + "\n", "title")
                elif stripped.startswith("# "):
                    self.ans_view.insert("end", stripped[2:] + "\n", "title")
                elif not stripped:
                    self.ans_view.insert("end", "\n")
                else:
                    self.ans_view.insert("end", line + "\n", "key")
        else:
            self.ans_view.insert("end", "No answer key found in this file.\n", "no_key")
            self.ans_view.insert("end", "\nFull content:\n\n", "header")
            self.ans_view.insert("end", sheet["full_content"])
        self.ans_view.configure(state="disabled")

    def _show_all_answers(self):
        self.ans_view.configure(state="normal")
        self.ans_view.delete("0.0", "end")
        for tag in self.ans_view.tag_names():
            if tag != "sel":
                self.ans_view.tag_delete(tag)
        self.ans_view.tag_config("title", foreground="#1a73e8", spacing3=10, spacing2=5)
        self.ans_view.tag_config("hr", foreground="#cccccc", spacing3=4)
        self.ans_view.tag_config("sep", foreground="#999", spacing3=8)
        self.ans_view.tag_config("key", foreground="#81C784", spacing3=2)
        self.ans_view.tag_config("no_key", foreground="#EF9A9A")
        self.ans_view.tag_config("empty", foreground="#888")
        total = len(self.answer_sheets_data)
        lang = self.ans_lang_var.get().lower() if hasattr(self, "ans_lang_var") else self.language
        def get_answer_key(sheet):
            if lang == "english" and sheet.get("answer_key_en"):
                return sheet["answer_key_en"], " (EN)"
            if lang == "tagalog" and sheet.get("answer_key_tl"):
                return sheet["answer_key_tl"], " (TL)"
            return sheet["answer_key"], ""
        with_key = sum(1 for s in self.answer_sheets_data if get_answer_key(s)[0])
        self.ans_view.insert("end", "ALL ANSWER KEYS\n", "title")
        self.ans_view.insert("end", self._tr("ans_summary").format(with_key=with_key, total=total), "empty")
        self.ans_view.insert("end", "\u2500" * 70 + "\n\n", "hr")
        for i, sheet in enumerate(self.answer_sheets_data):
            if i > 0:
                self.ans_view.insert("end", "\n" + "\u2500" * 40 + "\n", "sep")
            _, subj_color, _ = self._parse_md_label(sheet["label"])
            self.ans_view.tag_config(f"subj_{i}", foreground=subj_color, spacing3=6)
            label_emoji = ""
            for kw, e in SUBJECT_EMOJI_MAP:
                if kw in sheet["label"].lower():
                    label_emoji = e
                    break
            answer_key, lang_tag = get_answer_key(sheet)
            self.ans_view.insert("end", f" {label_emoji}  {sheet['label']}{lang_tag}\n", f"subj_{i}")
            if answer_key:
                self.ans_view.insert("end", "\u2500" * 30 + "\n", "hr")
                for line in answer_key.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("- ") or stripped.startswith("* "):
                        self.ans_view.insert("end", "  \u2022  " + stripped[2:] + "\n", "key")
                    elif stripped.startswith("## ") or stripped.startswith("# "):
                        self.ans_view.insert("end", "  " + stripped.lstrip("# ") + "\n", "key")
                    elif not stripped:
                        self.ans_view.insert("end", "\n")
                    else:
                        self.ans_view.insert("end", "  " + line.strip() + "\n", "key")
            else:
                self.ans_view.insert("end", "  No answer key available\n", "no_key")
        self.ans_view.configure(state="disabled")

    def setup_admin_tab(self):
        main = ctk.CTkFrame(self.tab_admin)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(main, text=self._tr("admin_panel"), font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, pady=(10, 20))
        nb = ctk.CTkTabview(main)
        nb.grid(row=1, column=0, sticky="nsew")
        nb.grid_columnconfigure(0, weight=1)
        nb.grid_rowconfigure(0, weight=1)
        self._setup_admin_users(nb.add(self._tr("manage_users")))
        self._setup_admin_backup(nb.add(self._tr("backup_restore")))
        self._setup_admin_password(nb.add(self._tr("change_password")))

    def _setup_admin_users(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", pady=(15, 10))
        ctk.CTkLabel(top, text=self._tr("username"), font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", padx=10)
        self.admin_new_user = ctk.CTkEntry(top, width=200, font=ctk.CTkFont(size=12))
        self.admin_new_user.grid(row=0, column=1, sticky="w", padx=10)
        ctk.CTkLabel(top, text=self._tr("password"), font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", padx=10)
        self.admin_new_pass = ctk.CTkEntry(top, width=200, font=ctk.CTkFont(size=12), show="*")
        self.admin_new_pass.grid(row=1, column=1, sticky="w", padx=10)
        ctk.CTkLabel(top, text="Role:", font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky="w", padx=10)
        self.admin_new_role = ctk.CTkOptionMenu(top, values=["student", "teacher"], width=190)
        self.admin_new_role.grid(row=2, column=1, sticky="w", padx=10)
        ctk.CTkButton(top, text=self._tr("add_user"), command=self._admin_add_user, width=120,
                      height=38, font=ctk.CTkFont(size=14, weight="bold")).grid(row=3, column=0, columnspan=2, pady=15)
        self.admin_user_status = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=12))
        self.admin_user_status.grid(row=4, column=0, columnspan=2, pady=10)
        list_frame = ctk.CTkFrame(parent)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        student_frame = ctk.CTkFrame(list_frame)
        student_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        ctk.CTkLabel(student_frame, text=self._tr("students_label"), font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        self.admin_student_list = ctk.CTkScrollableFrame(student_frame)
        self.admin_student_list.pack(fill="both", expand=True, padx=10, pady=5)
        teacher_frame = ctk.CTkFrame(list_frame)
        teacher_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        ctk.CTkLabel(teacher_frame, text=self._tr("teachers_label"), font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5), padx=10)
        self.admin_teacher_list = ctk.CTkScrollableFrame(teacher_frame)
        self.admin_teacher_list.pack(fill="both", expand=True, padx=10, pady=5)
        self._refresh_user_lists()

    def _refresh_user_lists(self):
        for w in self.admin_student_list.winfo_children():
            w.destroy()
        for w in self.admin_teacher_list.winfo_children():
            w.destroy()
        aname, users = auth_manager.list_users()
        for s in users.get("students", []):
            f = ctk.CTkFrame(self.admin_student_list, fg_color="transparent")
            f.pack(fill="x", pady=3)
            ctk.CTkLabel(f, text=s, font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
            ctk.CTkButton(f, text=self._tr("remove"), width=70, height=28,
                          command=lambda u=s: self._admin_remove_user(u)).pack(side="right", padx=10)
        for t in users.get("teachers", []):
            f = ctk.CTkFrame(self.admin_teacher_list, fg_color="transparent")
            f.pack(fill="x", pady=3)
            ctk.CTkLabel(f, text=t, font=ctk.CTkFont(size=13)).pack(side="left", padx=10)
            ctk.CTkButton(f, text=self._tr("remove"), width=70, height=28,
                          command=lambda u=t: self._admin_remove_user(u)).pack(side="right", padx=10)

    def _admin_add_user(self):
        u = self.admin_new_user.get().strip()
        p = self.admin_new_pass.get()
        r = self.admin_new_role.get()
        if not u or not p:
            self.admin_user_status.configure(text=self._tr("fill_all_fields"), text_color="#000000")
            return
        if len(p) < 4:
            self.admin_user_status.configure(text=self._tr("password_too_short"), text_color="#000000")
            return
        auth_manager.add_user(u, p, r)
        self.admin_new_user.delete(0, "end")
        self.admin_new_pass.delete(0, "end")
        self.admin_user_status.configure(text=self._tr("user_added").format(role=r, user=u), text_color="#000000")
        self._refresh_user_lists()

    def _admin_remove_user(self, username):
        if messagebox.askyesno(self._tr("confirm_title"), self._tr("confirm_remove_user").format(username=username)):
            auth_manager.remove_user(username)
            self.admin_user_status.configure(text=self._tr("user_removed").format(username=username), text_color="#000000")
            self._refresh_user_lists()

    def _setup_admin_password(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(pady=30)
        ctk.CTkLabel(form, text=self._tr("change_admin_password"), font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        ctk.CTkLabel(form, text=self._tr("current_password"), font=ctk.CTkFont(size=14)).grid(row=1, column=0, sticky="w", pady=8)
        self.admin_old_pw = ctk.CTkEntry(form, width=220, font=ctk.CTkFont(size=12), show="*")
        self.admin_old_pw.grid(row=1, column=1, pady=8, padx=10)
        ctk.CTkLabel(form, text=self._tr("new_password"), font=ctk.CTkFont(size=14)).grid(row=2, column=0, sticky="w", pady=8)
        self.admin_new_pw = ctk.CTkEntry(form, width=220, font=ctk.CTkFont(size=12), show="*")
        self.admin_new_pw.grid(row=2, column=1, pady=8, padx=10)
        ctk.CTkLabel(form, text=self._tr("confirm_new"), font=ctk.CTkFont(size=14)).grid(row=3, column=0, sticky="w", pady=8)
        self.admin_confirm_pw = ctk.CTkEntry(form, width=220, font=ctk.CTkFont(size=12), show="*")
        self.admin_confirm_pw.grid(row=3, column=1, pady=8, padx=10)
        self.admin_pw_status = ctk.CTkLabel(form, text="", font=ctk.CTkFont(size=12))
        self.admin_pw_status.grid(row=4, column=0, columnspan=2, pady=10)
        ctk.CTkButton(form, text=self._tr("change_password"), command=self._admin_change_password,
                      width=180, height=38, font=ctk.CTkFont(size=14, weight="bold")).grid(row=5, column=0, columnspan=2, pady=15)

    def _admin_change_password(self):
        old = self.admin_old_pw.get()
        new = self.admin_new_pw.get()
        confirm = self.admin_confirm_pw.get()
        if not old or not new:
            self.admin_pw_status.configure(text=self._tr("fill_all_fields"), text_color="#000000")
            return
        if new != confirm:
            self.admin_pw_status.configure(text=self._tr("new_passwords_no_match"), text_color="#000000")
            return
        if len(new) < 4:
            self.admin_pw_status.configure(text=self._tr("password_too_short"), text_color="#000000")
            return
        ok, msg = auth_manager.change_admin_password(self.current_user, old, new)
        if ok:
            self.admin_old_pw.delete(0, "end")
            self.admin_new_pw.delete(0, "end")
            self.admin_confirm_pw.delete(0, "end")
            self.admin_pw_status.configure(text=msg, text_color="#000000")
        else:
            self.admin_pw_status.configure(text=msg, text_color="#000000")

    def _setup_admin_backup(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(parent, text=self._tr("backup_restore"), font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, pady=(15, 10))
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=10)
        ctk.CTkButton(btn_frame, text=self._tr("create_backup"), command=self._admin_create_backup, width=140,
                      height=38, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=self._tr("restore_backup"), command=self._admin_restore_backup, width=140,
                      height=38, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        self.admin_backup_status = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=12))
        self.admin_backup_status.grid(row=2, column=0, pady=10)

    def _admin_create_backup(self):
        path = backup_manager.create_backup()
        size = os.path.getsize(path)
        size_str = f"{size/1024/1024:.1f} MB" if size > 1024*1024 else f"{size/1024:.1f} KB"
        self.admin_backup_status.configure(text=f"Backup created: {os.path.basename(path)} ({size_str})",
                                          text_color="#000000")

    def _admin_restore_backup(self):
        choice = filedialog.askopenfilename(
            title=self._tr("select_backup_restore"),
            initialdir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups"),
            filetypes=[("ZIP files", "*.zip")]
        )
        if not choice:
            return
        if messagebox.askyesno(self._tr("confirm_title"), self._tr("confirm_restore")):
            restored_dir = backup_manager.restore_backup(choice)
            self.admin_backup_status.configure(text=self._tr("restored_to").format(directory=restored_dir), text_color="#000000")

    def setup_mycontent_tab(self):
        main = ctk.CTkFrame(self.tab_mycontent)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(header, text=self._tr("my_created_lessons"),
                     font=ctk.CTkFont(size=22, weight="bold"), text_color="#000000").grid(
            row=0, column=0, sticky="w")
        ctk.CTkButton(header, text=self._tr("new_lesson"), width=110, height=32,
                       font=ctk.CTkFont(size=13, weight="bold"), fg_color="#42A5F5", hover_color="#1E88E5",
                       command=self._show_new_lesson_dialog).grid(row=0, column=1, sticky="e", padx=(10, 5))
        ctk.CTkButton(header, text=self._tr("refresh"), width=100, height=32,
                       font=ctk.CTkFont(size=13), command=self._refresh_mycontent).grid(
            row=0, column=2, sticky="e")
        self.mc_list = ctk.CTkScrollableFrame(main)
        self.mc_list.grid(row=1, column=0, sticky="nsew")
        self._refresh_mycontent()

    def _refresh_mycontent(self):
        for w in self.mc_list.winfo_children():
            w.destroy()
        found = []
        custom_dir = os.path.join(learning_data.APP_ROOT, "Custom_Lessons")
        if not os.path.isdir(custom_dir):
            ctk.CTkLabel(self.mc_list, text="No custom lessons yet.\nGo to Generate Curriculum → Prompt Lesson to create one!",
                         font=ctk.CTkFont(size=14), text_color="#000000", justify="center").pack(pady=50)
            return
        for dirpath, dirnames, fnames in os.walk(custom_dir):
            for f in sorted(fnames):
                if f.endswith(".md"):
                    rel = os.path.relpath(os.path.join(dirpath, f), custom_dir)
                    found.append((rel, os.path.join(dirpath, f)))
        if not found:
            ctk.CTkLabel(self.mc_list, text="No custom lessons yet.\nGo to Generate Curriculum → Prompt Lesson to create one!",
                         font=ctk.CTkFont(size=14), text_color="#000000", justify="center").pack(pady=50)
            return
        for rel, fpath in found:
            card = ctk.CTkFrame(self.mc_list, fg_color="#FFF8F0", corner_radius=8)
            card.pack(fill="x", pady=3, padx=5)
            ctk.CTkLabel(card, text=rel, font=ctk.CTkFont(size=13)).pack(side="left", padx=10, pady=8)
            ctk.CTkButton(card, text=self._tr("open"), width=60, height=28,
                           font=ctk.CTkFont(size=11),
                           command=lambda p=fpath: self._open_mycontent_file(p)).pack(side="right", padx=10)

    def _open_mycontent_file(self, path):
        if hasattr(self, "_open_imported_viewer"):
            self.tab_view.set(self._tr("imported_files"))
            self._open_imported_viewer(path)
        else:
            webbrowser.open(path)

    def _show_new_lesson_dialog(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title(self._tr("new_lesson"))
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        dialog.transient(self.window)
        dialog.grab_set()

        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(frame, text=self._tr("lesson_title"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").grid(row=0, column=0, sticky="w", pady=(0, 3))
        title_entry = ctk.CTkEntry(frame, placeholder_text="My Lesson", font=ctk.CTkFont(size=13))
        title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(frame, text=self._tr("level"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").grid(row=2, column=0, sticky="w", pady=(0, 3))
        grade_var = ctk.StringVar(value="Grade 1")
        grades = [f"Grade {i}" for i in range(1, 13)] + ["Grade 11 SHS", "Grade 12 SHS", "College"]
        ctk.CTkOptionMenu(frame, variable=grade_var, values=grades, width=200,
                          font=ctk.CTkFont(size=13)).grid(row=3, column=0, sticky="w", pady=(0, 10))

        ctk.CTkLabel(frame, text=self._tr("subject_course"), font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000").grid(row=4, column=0, sticky="w", pady=(0, 3))
        content_label = ctk.CTkLabel(frame, text=self._tr("lesson_content"),
                                      font=ctk.CTkFont(size=14, weight="bold"), text_color="#000000")
        content_label.grid(row=5, column=0, sticky="nw", pady=(0, 3))
        content_text = ctk.CTkTextbox(frame, wrap="word", font=ctk.CTkFont(size=12), text_color="#000000")
        content_text.grid(row=5, column=0, sticky="nsew", pady=(0, 10))
        content_text.insert("0.0", self._tr("lesson_content_placeholder").replace("\\n", "\n"))

        def do_save():
            title = title_entry.get().strip()
            content = content_text.get("0.0", "end-1c").strip()
            if not title:
                messagebox.showwarning(self._tr("missing_title"), self._tr("missing_title_msg"))
                return
            safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip()
            if not safe_title:
                safe_title = "untitled"
            grade_key = grade_var.get().replace(" ", "_").replace("__", "_")
            custom_dir = os.path.join(learning_data.APP_ROOT, "Custom_Lessons", grade_key)
            os.makedirs(custom_dir, exist_ok=True)
            fpath = os.path.join(custom_dir, f"{safe_title}.md")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{content}")
            dialog.destroy()
            messagebox.showinfo(self._tr("success"),
                                self._tr("saved_to_custom") + f"\n{safe_title}.md")
            self._refresh_mycontent()

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.grid(row=6, column=0, sticky="e", pady=(5, 0))
        ctk.CTkButton(btn_frame, text=self._tr("cancel"), width=80, height=32,
                       font=ctk.CTkFont(size=13), command=dialog.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self._tr("save"), width=80, height=32,
                       font=ctk.CTkFont(size=13), fg_color="#43A047", command=do_save).pack(side="left", padx=5)

    def _start_lockout_timer(self, remaining=30):
        if not hasattr(self, "_lockout_timer_active"):
            self._lockout_timer_active = False
        if self._lockout_timer_active:
            return
        self._lockout_timer_active = True
        self._tick_lockout(remaining)

    def _tick_lockout(self, remaining):
        if remaining <= 0:
            self.login_status.configure(text=self._tr("enter_usr_pw"))
            self._lockout_timer_active = False
            return
        self.login_status.configure(text=f"Too many attempts. Try again in {remaining} seconds.")
        self.window.after(1000, lambda: self._tick_lockout(remaining - 1))

    def run(self):
        self.window.mainloop()

    def _open_quiz_dialog(self):
        if not self._current_filepath:
            messagebox.showinfo(self._tr("quiz"), self._tr("select_lesson_first"))
            return
        if self.visual_viewer.winfo_ismapped():
            orig = self._current_filepath
            md_path = orig
            if md_path and os.path.exists(md_path):
                with open(md_path, encoding="utf-8") as f:
                    quiz_content = f.read()
            else:
                messagebox.showinfo(self._tr("quiz"), "Could not find lesson content for quiz.")
                return
        else:
            if not self._current_raw_content:
                messagebox.showinfo(self._tr("quiz"), self._tr("select_lesson_first"))
                return
            quiz_content = self._current_raw_content
        questions = quiz_engine.generate_combined_quiz(quiz_content)
        if not questions:
            messagebox.showinfo(self._tr("quiz"), "Could not generate quiz from this lesson.")
            return
        QuizDialog(self.window, self._tr, questions, self._current_filepath, self.current_user)

    def setup_progress_tab(self):
        main = ctk.CTkFrame(self.tab_progress)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(header, text=self._tr("my_progress"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")

        content = ctk.CTkScrollableFrame(main)
        content.grid(row=1, column=0, sticky="nsew")

        stats = lesson_db.get_student_stats(self.current_user)
        gam = lesson_db.get_gamification(self.current_user)

        stats_frame = ctk.CTkFrame(content, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        stats_items = [
            (self._tr("total_points"), str(stats["total_points"]), "#FFD54F"),
            (self._tr("lessons_completed"), str(stats["total_lessons"]), "#A5D6A7"),
            (self._tr("quizzes_taken"), str(stats["total_quizzes"]), "#81D4FA"),
            (self._tr("avg_score"), f"{stats['avg_score']}%", "#CE93D8"),
            (self._tr("streak"), f"{stats['current_streak']} day", "#FFAB91"),
            (self._tr("weekly_activity"), str(stats["weekly_activity"]), "#80DEEA"),
        ]
        for i, (label, value, color) in enumerate(stats_items):
            card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10)
            card.grid(row=i//3, column=i%3, padx=8, pady=8, sticky="nsew")
            stats_frame.grid_columnconfigure(i%3, weight=1)
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"),
                         text_color="#000000").pack(pady=(15, 5))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=13),
                         text_color="#000000").pack(pady=(0, 15))

        ctk.CTkLabel(content, text=self._tr("badges"), font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#000000").pack(anchor="w", pady=(20, 10))
        badges = gam.get("badges", [])
        if badges:
            b_frame = ctk.CTkFrame(content, fg_color="transparent")
            b_frame.pack(fill="x")
            for b in badges:
                b_card = ctk.CTkFrame(b_frame, fg_color="#FFF8E1", corner_radius=8)
                b_card.pack(side="left", padx=5, pady=5)
                ctk.CTkLabel(b_card, text=f"   {b}   ", font=ctk.CTkFont(size=12),
                             text_color="#000000").pack(padx=10, pady=8)
        else:
            ctk.CTkLabel(content, text=self._tr("no_data_yet"), font=ctk.CTkFont(size=13),
                         text_color="#000000").pack(anchor="w", padx=5)

        ctk.CTkLabel(content, text=self._tr("subject_progress"), font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#000000").pack(anchor="w", pady=(20, 10))
        subj_prog = lesson_db.get_subject_progress(self.current_user)
        if subj_prog:
            for sp in subj_prog:
                pct = (sp["done"] / sp["total"] * 100) if sp["total"] > 0 else 0
                subj_frame = ctk.CTkFrame(content, fg_color="transparent")
                subj_frame.pack(fill="x", pady=3)
                ctk.CTkLabel(subj_frame, text=f"{sp['grade']} - {sp['subject']}",
                             font=ctk.CTkFont(size=13), text_color="#000000").pack(side="left", padx=5)
                prog_bar = ctk.CTkProgressBar(subj_frame, width=200)
                prog_bar.pack(side="left", padx=10)
                prog_bar.set(pct / 100)
                ctk.CTkLabel(subj_frame, text=f"{sp['done']}/{sp['total']} ({pct:.0f}%)",
                             font=ctk.CTkFont(size=12), text_color="#000000").pack(side="left")
        else:
            ctk.CTkLabel(content, text=self._tr("no_data_yet"), font=ctk.CTkFont(size=13),
                         text_color="#000000").pack(anchor="w", padx=5)

        ctk.CTkButton(content, text=self._tr("refresh"), width=100, height=32,
                       font=ctk.CTkFont(size=13), command=lambda: (self.tab_progress.destroy(),
                       setattr(self, 'tab_progress', self.tab_view.add(self._tr("my_progress"))),
                       self.setup_progress_tab())).pack(pady=20)

    def setup_leaderboard_tab(self):
        main = ctk.CTkFrame(self.tab_leaderboard)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(header, text=self._tr("leaderboard"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")

        scroll = ctk.CTkScrollableFrame(main)
        scroll.grid(row=1, column=0, sticky="nsew")

        leaders = lesson_db.get_leaderboard(50)
        if self.current_role in ("teacher", "admin") or self._king_mode:
            try:
                peers = self._discover_peers()
                for cl, _ in peers:
                    remote_lb = cl.get_leaderboard(50)
                    for r in remote_lb:
                        r["_remote"] = True
                        r["_host"] = cl.host
                    leaders.extend(remote_lb)
                leaders.sort(key=lambda x: x.get("total_points", 0), reverse=True)
                leaders = leaders[:50]
            except Exception:
                pass
        if not leaders:
            ctk.CTkLabel(scroll, text=self._tr("no_data_yet"), font=ctk.CTkFont(size=14),
                         text_color="#000000").pack(pady=40)
            return

        header_row = ctk.CTkFrame(scroll, fg_color="#E0E0E0", corner_radius=8)
        header_row.pack(fill="x", pady=2)
        for i, h in enumerate(["#", self._tr("username_leaderboard"), self._tr("total_points"), self._tr("lessons_completed"), self._tr("streak")]):
            ctk.CTkLabel(header_row, text=h, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#000000", width=80 if i > 0 else 40).pack(side="left", padx=5, pady=5)

        medals = ["\U0001F947", "\U0001F948", "\U0001F949"]
        for rank, l in enumerate(leaders, 1):
            row_color = "#FFFDE7" if rank <= 3 else "transparent"
            row = ctk.CTkFrame(scroll, fg_color=row_color, corner_radius=4)
            row.pack(fill="x", pady=1)
            rank_text = f"{medals[rank-1]} " if rank <= 3 else f"#{rank}"
            ctk.CTkLabel(row, text=rank_text, font=ctk.CTkFont(size=13),
                         text_color="#000000", width=40).pack(side="left", padx=5, pady=5)
            name = l["display_name"] or l["username"]
            if l.get("_remote"):
                name += f" @{l['_host']}"
            ctk.CTkLabel(row, text=name,
                         font=ctk.CTkFont(size=13), text_color="#000000",
                         width=200, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(row, text=str(l["total_points"]), font=ctk.CTkFont(size=13),
                         text_color="#000000", width=80).pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(row, text=str(l["lessons_completed"]), font=ctk.CTkFont(size=13),
                         text_color="#000000", width=80).pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(row, text=f"{l['current_streak']}d", font=ctk.CTkFont(size=13),
                         text_color="#000000", width=60).pack(side="left", padx=5, pady=5)

    def setup_analytics_tab(self):
        main = ctk.CTkFrame(self.tab_analytics)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(header, text=self._tr("analytics"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")

        content = ctk.CTkScrollableFrame(main)
        content.grid(row=1, column=0, sticky="nsew")

        dash = lesson_db.get_teacher_dashboard(self.current_user)

        peers = self._discover_peers()
        remote_students = self._get_remote_students(peers)
        if remote_students:
            dash["students"] = dash["students"] + remote_students
            dash["enrolled"] += len(remote_students)

        summary_frame = ctk.CTkFrame(content, fg_color="transparent")
        summary_frame.pack(fill="x", pady=10)
        summary_items = [
            (self._tr("enrolled_students"), str(dash["enrolled"]), "#81D4FA"),
            (self._tr("active_today"), str(dash["active_today"]), "#A5D6A7"),
            (self._tr("lessons_completed"), str(dash["today_lessons"]), "#FFD54F"),
        ]
        for i, (label, value, color) in enumerate(summary_items):
            card = ctk.CTkFrame(summary_frame, fg_color=color, corner_radius=10)
            card.grid(row=0, column=i, padx=8, pady=8, sticky="nsew")
            summary_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=32, weight="bold"),
                         text_color="#000000").pack(pady=(15, 5))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=13),
                         text_color="#000000").pack(pady=(0, 15))

        ctk.CTkLabel(content, text=self._tr("student_performance"),
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#000000").pack(anchor="w", pady=(20, 10))

        if not dash["students"]:
            ctk.CTkLabel(content, text=self._tr("no_students_yet"), font=ctk.CTkFont(size=14),
                         text_color="#000000").pack(pady=20)
            return

        for s in dash["students"]:
            card = ctk.CTkFrame(content, fg_color="#F5F5F5", corner_radius=10)
            card.pack(fill="x", pady=4, padx=2)
            card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(card, text=s["display_name"], font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")

            details = f"Points: {s['total_points']} | Lessons: {s['total_lessons']} | Quizzes: {s['total_quizzes']} | Avg: {s['avg_score']}% | Streak: {s['current_streak']}d"
            ctk.CTkLabel(card, text=details, font=ctk.CTkFont(size=12),
                         text_color="#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")

            prog_frame = ctk.CTkFrame(card, fg_color="transparent")
            prog_frame.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            ctk.CTkProgressBar(prog_frame, width=80, height=8).pack(side="left", padx=3)
            val = min(s["total_lessons"] / 50, 1.0)
            ctk.CTkProgressBar(prog_frame, width=80, height=8).pack(side="left", padx=3)
            prog_frame.winfo_children()[0].set(val)

            if s["badges"]:
                ctk.CTkLabel(card, text="  ".join(s["badges"][:3]), font=ctk.CTkFont(size=10),
                             text_color="#FF8F00").grid(row=0, column=3, padx=5)

    def setup_king_tab(self):
        main = ctk.CTkFrame(self.tab_network)
        main.pack(fill="both", expand=True, padx=15, pady=15)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        ctk.CTkLabel(header, text=self._tr("king_view"),
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w")

        content = ctk.CTkScrollableFrame(main)
        content.grid(row=1, column=0, sticky="nsew")

        refresh_btn = ctk.CTkButton(content, text=self._tr("refresh"), width=100, height=32,
                                      font=ctk.CTkFont(size=13),
                                      command=lambda: self._refresh_king_tab(content))
        refresh_btn.pack(anchor="ne", pady=(0, 10))

        self._refresh_king_tab(content)

    def _refresh_king_tab(self, content):
        for w in content.winfo_children():
            if w.winfo_class() != "CTkButton":
                w.destroy()

        local_admin = auth_manager.get_admin_username() or self.current_user

        summary_frame = ctk.CTkFrame(content, fg_color="transparent")
        summary_frame.pack(fill="x", pady=10)

        peers = self._discover_peers()
        remote_count = len(peers)
        total_peers = 1 + remote_count

        ctk.CTkLabel(summary_frame, text=f"Network peers: {total_peers} (local + {remote_count} remote)",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color="#000000").pack(anchor="w", pady=(0, 10))

        stats_items = [
            ("Instances", str(total_peers), "#81D4FA"),
            ("Local Role", f"{self.current_role.title()}", "#A5D6A7"),
            ("King Status", "Active" if self._king_mode else "Follower", "#FFD54F"),
        ]
        for i, (label, value, color) in enumerate(stats_items):
            card = ctk.CTkFrame(summary_frame, fg_color=color, corner_radius=10)
            card.grid(row=1, column=i, padx=8, pady=8, sticky="nsew")
            summary_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold"),
                         text_color="#000000").pack(pady=(15, 5))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=13),
                         text_color="#000000").pack(pady=(0, 15))

        ctk.CTkLabel(content, text="Remote Instances",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#000000").pack(anchor="w", pady=(20, 10))

        if not peers:
            ctk.CTkLabel(content, text="No remote peers discovered on LAN.",
                         font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=20)
        else:
            for cl, info in peers:
                try:
                    role_info = cl.get_role()
                    remote_user = cl.username or "unknown"
                    remote_role = role_info or "unknown"
                except Exception:
                    remote_user = "?"
                    remote_role = "?"
                card = ctk.CTkFrame(content, fg_color="#F5F5F5", corner_radius=10)
                card.pack(fill="x", pady=4, padx=2)
                card.grid_columnconfigure(1, weight=1)
                ctk.CTkLabel(card, text=f"{info['host']}:{info['port']}",
                             font=ctk.CTkFont(size=14, weight="bold"),
                             text_color="#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")
                ctk.CTkLabel(card, text=f"{remote_user} ({remote_role})",
                             font=ctk.CTkFont(size=12),
                             text_color="#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(content, text="All Students (Local + Remote)",
                     font=ctk.CTkFont(size=18, weight="bold"), text_color="#000000").pack(anchor="w", pady=(20, 10))

        remote_students = self._get_remote_students(peers)
        local_students = lesson_db.get_teacher_dashboard(self.current_user).get("students", [])
        all_students = local_students + remote_students
        all_students.sort(key=lambda s: s.get("total_points", 0), reverse=True)

        if not all_students:
            ctk.CTkLabel(content, text=self._tr("no_students_yet"), font=ctk.CTkFont(size=14),
                         text_color="#000000").pack(pady=20)
            return

        for s in all_students:
            is_remote = s.get("_remote", False)
            display_name = s.get("display_name", s.get("username", "?"))
            host = s.get("_host", "local")
            card = ctk.CTkFrame(content, fg_color="#FFF8E1" if is_remote else "#F5F5F5", corner_radius=10)
            card.pack(fill="x", pady=4, padx=2)
            card.grid_columnconfigure(1, weight=1)

            label_text = f"{display_name} {'[remote]' if is_remote else '[local]'}"
            ctk.CTkLabel(card, text=label_text, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#000000").grid(row=0, column=0, padx=10, pady=5, sticky="w")

            details = f"Points: {s.get('total_points', 0)} | Lessons: {s.get('total_lessons', 0)} | Quizzes: {s.get('total_quizzes', 0)} | Avg: {s.get('avg_score', 0)}% | Streak: {s.get('current_streak', 0)}d"
            ctk.CTkLabel(card, text=details, font=ctk.CTkFont(size=12),
                         text_color="#000000").grid(row=0, column=1, padx=10, pady=5, sticky="w")

            if is_remote:
                ctk.CTkLabel(card, text=f"@{host}", font=ctk.CTkFont(size=10),
                             text_color="#FF6F00").grid(row=0, column=2, padx=5)

            badges = s.get("badges", [])
            if badges:
                ctk.CTkLabel(card, text="  ".join(badges[:3]), font=ctk.CTkFont(size=10),
                             text_color="#FF8F00").grid(row=0, column=3, padx=5)


class QuizDialog:
    def __init__(self, parent, tr, questions, lesson_path, username):
        self.tr = tr
        self.questions = questions
        self.lesson_path = lesson_path
        self.username = username
        self.current_q = 0
        self.score = 0
        self.total = len(questions)
        self.answers = []

        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(tr("quiz"))
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.main = ctk.CTkFrame(self.dialog, fg_color="transparent")
        self.main.pack(fill="both", expand=True, padx=20, pady=20)

        self.prog_label = ctk.CTkLabel(self.main, text="", font=ctk.CTkFont(size=13), text_color="#000000")
        self.prog_label.pack(anchor="w")

        self.prog_bar = ctk.CTkProgressBar(self.main, width=560)
        self.prog_bar.pack(fill="x", pady=(5, 15))
        self.prog_bar.set(0)

        self.q_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        self.q_frame.pack(fill="both", expand=True)

        self._show_question()

    def _show_question(self):
        for w in self.q_frame.winfo_children():
            w.destroy()

        if self.current_q >= self.total:
            self._show_result()
            return

        q = self.questions[self.current_q]
        self.prog_label.configure(text=self.tr("question_of").format(n=self.current_q+1, total=self.total))
        self.prog_bar.set((self.current_q + 1) / self.total)

        type_label = {"mcq": "Multiple Choice", "true_false": "True or False", "fill_blank": "Fill in the Blank"}
        ctk.CTkLabel(self.q_frame, text=type_label.get(q["type"], "Question"),
                     font=ctk.CTkFont(size=12, weight="bold"), text_color="#1565C0").pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(self.q_frame, text=q["question"], font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#000000", wraplength=540, justify="left").pack(anchor="w", pady=(0, 15))

        self.var = ctk.StringVar(value="")

        if q["type"] == "true_false":
            for opt in q["options"]:
                rb = ctk.CTkRadioButton(self.q_frame, text=opt, variable=self.var, value=opt,
                                        font=ctk.CTkFont(size=14), text_color="#000000")
                rb.pack(anchor="w", pady=5, padx=20)
        elif q["type"] == "fill_blank":
            self.entry = ctk.CTkEntry(self.q_frame, width=400, font=ctk.CTkFont(size=14))
            self.entry.pack(anchor="w", padx=20, pady=10)
            self.entry.bind("<Return>", lambda e: self._submit_answer())
            self.entry.focus()
        else:
            for opt in q["options"]:
                rb = ctk.CTkRadioButton(self.q_frame, text=opt, variable=self.var, value=opt,
                                        font=ctk.CTkFont(size=14), text_color="#000000")
                rb.pack(anchor="w", pady=5, padx=20)

        btn_frame = ctk.CTkFrame(self.q_frame, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=(15, 0))
        ctk.CTkButton(btn_frame, text=self.tr("submit_quiz") if self.current_q == self.total - 1 else self.tr("next_question"),
                      command=self._submit_answer, width=150, height=38,
                      font=ctk.CTkFont(size=14, weight="bold")).pack(side="right")

    def _submit_answer(self):
        q = self.questions[self.current_q]
        if q["type"] == "fill_blank":
            user_ans = self.entry.get().strip()
        else:
            user_ans = self.var.get()

        if not user_ans:
            messagebox.showwarning(self.tr("quiz"), "Please select/enter an answer.")
            return

        is_correct = user_ans.strip().lower() == q["correct"].strip().lower()
        if is_correct:
            self.score += 1

        lesson_db.record_quiz_answer(
            self.username, self.lesson_path,
            q["question"], q["correct"], user_ans, is_correct, q["type"]
        )
        self.answers.append((q["question"], q["correct"], user_ans, is_correct))

        feedback_color = "#2E7D32" if is_correct else "#C62828"
        feedback = ctk.CTkLabel(self.q_frame, text="",
                                font=ctk.CTkFont(size=13), text_color=feedback_color)
        feedback.pack(anchor="w", pady=(5, 0))

        if is_correct:
            feedback.configure(text="Correct!")
        else:
            feedback.configure(text=f"Incorrect. Answer: {q['correct']}")

        self.dialog.after(1500, self._next_question)

    def _next_question(self):
        self.current_q += 1
        self._show_question()

    def _show_result(self):
        for w in self.q_frame.winfo_children():
            w.destroy()
        for w in self.main.winfo_children():
            w.destroy()

        pct = (self.score / self.total * 100) if self.total > 0 else 0
        lesson_db.save_quiz_result(self.username, self.lesson_path,
                                    [q["question"] for q in self.questions],
                                    [a[2] for a in self.answers],
                                    self.score, self.total)

        ctk.CTkLabel(self.main, text=self.tr("quiz_result"), font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#000000").pack(pady=(20, 10))
        ctk.CTkLabel(self.main, text=f"{self.score} / {self.total}", font=ctk.CTkFont(size=48, weight="bold"),
                     text_color="#2E7D32" if pct >= 70 else "#C62828").pack(pady=10)
        ctk.CTkLabel(self.main, text=f"{pct:.0f}%", font=ctk.CTkFont(size=20),
                     text_color="#000000").pack()
        ctk.CTkLabel(self.main, text=f"{self.tr('total_points')}: +{self.score * 2}{' + ' + self.tr('perfect_score_bonus') if self.score == self.total else ''}",
                     font=ctk.CTkFont(size=14), text_color="#000000").pack(pady=10)

        result_frame = ctk.CTkScrollableFrame(self.main, height=200)
        result_frame.pack(fill="x", pady=10)
        for q_text, correct, user_ans, correct_flag in self.answers:
            r_color = "#E8F5E9" if correct_flag else "#FFEBEE"
            r = ctk.CTkFrame(result_frame, fg_color=r_color, corner_radius=5)
            r.pack(fill="x", pady=2, padx=5)
            icon = "\u2713" if correct_flag else "\u2717"
            ctk.CTkLabel(r, text=f"{icon} {q_text[:80]}...", font=ctk.CTkFont(size=12),
                         text_color="#000000", wraplength=500, justify="left").pack(anchor="w", padx=10, pady=5)
            ctk.CTkLabel(r, text=f"Your answer: {user_ans} | Correct: {correct}",
                         font=ctk.CTkFont(size=11), text_color="#000000").pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(self.main, text=self.tr("close"), command=self.dialog.destroy,
                      width=120, height=38, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=15)

    def run(self):
        self.dialog.wait_window()


if __name__ == "__main__":
    app = LearnAssistantGUI()
    app.run()
