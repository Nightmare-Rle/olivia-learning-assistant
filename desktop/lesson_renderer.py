"""Visual HTML lesson viewer using tkinterweb HtmlFrame.

Renders study-friendly HTML lessons with:
- Subject-colored header banners
- Difficulty badges
- Inline images from the web (for Grades 1-4: extra visual aids)
- Step-by-step numbered boxes
- Progress dots
- Printable answer key toggle
"""

import os
import json
import logging
import threading
import tkinter as tk
import customtkinter as ctk
from tkinterweb import HtmlFrame

import lesson_db

logger = logging.getLogger(__name__)

SUBJECT_COLORS = {
    "Mathematics": "#1565C0", "Science": "#2E7D32", "English": "#6A1B9A",
    "Filipino": "#E65100", "Araling_Panlipunan": "#C62828",
    "EPP_TLE": "#4E342E", "TLE": "#4E342E",
    "Music_and_Arts": "#F9A825", "MAPEH": "#F9A825",
    "PE_and_Health": "#00838F", "GMRC": "#AD1457",
    "Values_Education": "#AD1457", "Makabansa": "#1B5E20",
    "Language": "#283593", "Reading_and_Literacy": "#4A148C",
    "Cognitive_Development": "#00695C", "Aesthetic_Creative_Development": "#F57C00",
    "Language_Literacy_Communication": "#283593",
    "Physical_Health_Motor_Development": "#00838F",
    "Socio_emotional_Development": "#AD1457", "Values_Development": "#AD1457",
}
SUBJECT_EMOJI = {
    "Mathematics": "📐", "Science": "🔬", "English": "📖", "Filipino": "🇵🇭",
    "Araling_Panlipunan": "🌏", "EPP_TLE": "🛠", "TLE": "🛠",
    "Music_and_Arts": "🎨", "MAPEH": "🎨", "PE_and_Health": "🏃",
    "GMRC": "💚", "Values_Education": "💚",
    "Makabansa": "🇵🇭", "Language": "💬", "Reading_and_Literacy": "📚",
    "Cognitive_Development": "🧠", "Aesthetic_Creative_Development": "🎭",
    "Language_Literacy_Communication": "🗣", "Physical_Health_Motor_Development": "💪",
    "Socio_emotional_Development": "❤️", "Values_Development": "🌟",
}
DIFF_COLORS = {
    "Full Lesson": "#81C784", "Easy": "#A5D6A7", "Medium": "#FFE082",
    "Hard": "#EF9A9A", "Practice": "#CE93D8", "Full Assessment": "#F48FB1",
}


class LessonRenderer(ctk.CTkFrame):
    """A tab that renders visual HTML lessons with images and interactive elements."""

    def __init__(self, parent, tr_func, current_user, **kwargs):
        super().__init__(parent, **kwargs)
        self._tr = tr_func
        self.current_user = current_user
        self._current_filepath = None
        self._current_label = ""
        self._html_root = None
        self._current_lang = "english"
        self._lang_content = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_toolbar()
        self._build_viewer()

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        bar.grid_columnconfigure(2, weight=1)

        emoji_label = ctk.CTkLabel(bar, text="📖", font=("Segoe UI Emoji", 20))
        emoji_label.grid(row=0, column=0, padx=(0, 10))

        self.title_label = ctk.CTkLabel(bar, text=self._tr("select_lesson_first"),
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        text_color="#000000")
        self.title_label.grid(row=0, column=1, sticky="w")

        lang_frame = ctk.CTkFrame(bar, fg_color="transparent")
        lang_frame.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(lang_frame, text=self._tr("language"), font=ctk.CTkFont(size=11),
                     text_color="#000000").pack(side="left", padx=(0, 5))
        self.lang_combo = ctk.CTkOptionMenu(lang_frame, values=["english", "tagalog"],
                                            command=self._on_lang_change, width=100,
                                            font=ctk.CTkFont(size=11))
        self.lang_combo.pack(side="left")

        self.quiz_btn = ctk.CTkButton(bar, text=self._tr("take_quiz"), width=100, height=30,
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       fg_color="#FF8F00", hover_color="#E65100",
                                       command=self._on_quiz)
        self.quiz_btn.grid(row=0, column=4, padx=5)

    def _build_viewer(self):
        container = ctk.CTkFrame(self)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.html_frame = HtmlFrame(container, messages_enabled=False)
        self.html_frame.grid(row=0, column=0, sticky="nsew")

        self._show_welcome()

    def _show_welcome(self):
        welcome = """<!DOCTYPE html><html><body style="
            font-family: 'Segoe UI', Arial, sans-serif;
            text-align: center; padding: 60px 20px;
            background: #FFF8E1;
        ">
            <div style="font-size:64px; margin-bottom:20px;">📖</div>
            <h2 style="color:#333;">Select a lesson from the sidebar</h2>
            <p style="color:#666; font-size:16px;">
                Visual lessons with images, step-by-step guides, and progress tracking.
            </p>
        </body></html>"""
        self.html_frame.load_html(welcome)

    def open_lesson(self, filepath, label, grade="", subject="", difficulty=""):
        self._current_filepath = filepath
        self._current_label = label
        self._html_root = os.path.dirname(filepath)

        subject_clean = subject.replace("_", " ")
        emoji = SUBJECT_EMOJI.get(subject, "📖")
        self.title_label.configure(text=f"{emoji}  {label}")

        self._lang_content = {}
        for lang in ("english", "tagalog"):
            lp = self._get_lang_path(filepath, lang)
            if lp and os.path.exists(lp):
                with open(lp, encoding="utf-8") as f:
                    self._lang_content[lang] = f.read()

        self._render_current_lang()

        lesson_db.record_lesson_access(
            self.current_user, filepath, label,
            curriculum="K12", grade=grade, subject=subject, difficulty=difficulty
        )

    def _get_lang_path(self, filepath, lang):
        if lang == "english":
            return filepath
        d = os.path.dirname(filepath)
        parent = os.path.dirname(d)
        grade_dir = os.path.basename(d)
        orig_parent_name = os.path.basename(parent)

        if "Visual_Lessons" in parent:
            lang_parent = parent.replace("Visual_Lessons", f"Visual_Lessons_{lang.upper()}")
        else:
            lang_parent = os.path.join(os.path.dirname(parent), f"Visual_Lessons_{lang.upper()}")

        fname = os.path.basename(filepath)
        return os.path.join(lang_parent, grade_dir, fname)

    def _on_lang_change(self, lang):
        self._current_lang = lang
        self._render_current_lang()

    def _render_current_lang(self):
        content = self._lang_content.get(self._current_lang)
        if content:
            self.html_frame.load_html(content)

    def _on_quiz(self):
        from quiz_engine import generate_combined_quiz
        if not self._current_filepath:
            from tkinter import messagebox
            messagebox.showinfo(self._tr("quiz"), self._tr("select_lesson_first"))
            return
        try:
            with open(self._current_filepath, encoding="utf-8") as f:
                content_text = f.read()
            base_content = self._lang_content.get("english", content_text)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(base_content, "html.parser")
            text = soup.get_text(separator="\n")
            questions = generate_combined_quiz(text)
            if questions:
                from learn_assistant_gui import QuizDialog
                QuizDialog(self.winfo_toplevel(), self._tr, questions,
                          self._current_filepath, self.current_user)
            else:
                from tkinter import messagebox
                messagebox.showinfo(self._tr("quiz"), "Could not generate quiz from this lesson.")
        except Exception as e:
            logger.error("Quiz generation error: %s", e)
            from tkinter import messagebox
            messagebox.showerror(self._tr("gen_error"), str(e))

    def load_lesson_content(self, html, filepath=None, label=""):
        """Load HTML content directly (used for in-memory generated content)."""
        if filepath:
            self._current_filepath = filepath
        if label:
            self._current_label = label
            self.title_label.configure(text=label)
        self.html_frame.load_html(html)
