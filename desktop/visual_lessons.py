"""Generate visual HTML lessons for all K-12 grades.

For Grades 1-4: extra visual aids, emoji boxes, step indicators, inline images.
For Grades 5+: clean structured HTML with less decoration.

Content is aligned with the Philippine DepEd MATATAG curriculum (K-10)
and CHED SHS curriculum (Grades 11-12) with quarter-by-quarter lessons.
"""

import os
import shutil
import json
import base64
import hashlib
import urllib.request
import urllib.error
from datetime import date

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K12_SRC = os.path.join(APP_ROOT, "K-12_Philippine_Curriculum")
VISUAL_DIR = os.path.join(APP_ROOT, "Visual_Lessons")
STUDENT_VISUAL_DIR = os.path.join(APP_ROOT, "Visual_Lessons_Student")

CURRENT_YEAR = date.today().year

QUARTER_NAMES = ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"]

SUBJECT_INFO = {
    "Araling_Panlipunan": {"emoji": "🌏", "color": "#C62828", "name_en": "Araling Panlipunan", "name_tl": "Araling Panlipunan"},
    "English": {"emoji": "📖", "color": "#6A1B9A", "name_en": "English", "name_tl": "Ingles"},
    "EPP_TLE": {"emoji": "🛠", "color": "#4E342E", "name_en": "EPP / TLE", "name_tl": "EPP / TLE"},
    "Filipino": {"emoji": "🇵🇭", "color": "#E65100", "name_en": "Filipino", "name_tl": "Filipino"},
    "GMRC": {"emoji": "💚", "color": "#AD1457", "name_en": "GMRC", "name_tl": "GMRC"},
    "Mathematics": {"emoji": "📐", "color": "#1565C0", "name_en": "Mathematics", "name_tl": "Matematika"},
    "Music_and_Arts": {"emoji": "🎨", "color": "#F9A825", "name_en": "Music and Arts", "name_tl": "Musika at Sining"},
    "PE_and_Health": {"emoji": "🏃", "color": "#00838F", "name_en": "PE and Health", "name_tl": "PE at Kalusugan"},
    "Science": {"emoji": "🔬", "color": "#2E7D32", "name_en": "Science", "name_tl": "Agham"},
    "Makabansa": {"emoji": "🇵🇭", "color": "#1B5E20", "name_en": "Makabansa", "name_tl": "Makabansa"},
    "Language": {"emoji": "💬", "color": "#283593", "name_en": "Language", "name_tl": "Wika"},
    "Reading_and_Literacy": {"emoji": "📚", "color": "#4A148C", "name_en": "Reading and Literacy", "name_tl": "Pagbasa at Literasi"},
    "TLE": {"emoji": "🛠", "color": "#4E342E", "name_en": "TLE", "name_tl": "TLE"},
    "MAPEH": {"emoji": "🎨", "color": "#F9A825", "name_en": "MAPEH", "name_tl": "MAPEH"},
    "Values_Education": {"emoji": "💚", "color": "#AD1457", "name_en": "Values Education", "name_tl": "Edukasyon sa Pagpapahalaga"},
    "Cognitive_Development": {"emoji": "🧠", "color": "#00695C", "name_en": "Cognitive Development", "name_tl": "Pag-unlad ng Kognitibo"},
    "Aesthetic_Creative_Development": {"emoji": "🎭", "color": "#F57C00", "name_en": "Aesthetic & Creative Development", "name_tl": "Pag-unlad ng Estetiko at Malikhain"},
    "Language_Literacy_Communication": {"emoji": "🗣", "color": "#283593", "name_en": "Language, Literacy & Communication", "name_tl": "Wika, Literasi at Komunikasyon"},
    "Physical_Health_Motor_Development": {"emoji": "💪", "color": "#00838F", "name_en": "Physical, Health & Motor Development", "name_tl": "Pisikal, Kalusugan at Motor"},
    "Socio_emotional_Development": {"emoji": "❤️", "color": "#AD1457", "name_en": "Socio-emotional Development", "name_tl": "Sosyo-emosyonal na Pag-unlad"},
    "Values_Development": {"emoji": "🌟", "color": "#AD1457", "name_en": "Values Development", "name_tl": "Pagpapaunlad ng Pagpapahalaga"},
}

SHS_SUBJECT_INFO = {
    "21st_Century_Literature": {"emoji": "📚", "color": "#4A148C", "name_en": "21st Century Literature", "name_tl": "Panitikan ng Ika-21 Siglo"},
    "Contemporary_Philippine_Arts": {"emoji": "🎨", "color": "#F57C00", "name_en": "Contemporary Philippine Arts", "name_tl": "Kontemporaryong Sining ng Pilipinas"},
    "Disaster_Readiness_Risk_Reduction": {"emoji": "⚠️", "color": "#B71C1C", "name_en": "Disaster Readiness & Risk Reduction", "name_tl": "Kahandaan sa Sakuna"},
    "Earth_and_Life_Science": {"emoji": "🌍", "color": "#2E7D32", "name_en": "Earth and Life Science", "name_tl": "Agham ng Daigdig at Buhay"},
    "Earth_Science": {"emoji": "🌍", "color": "#2E7D32", "name_en": "Earth Science", "name_tl": "Agham ng Daigdig"},
    "General_Mathematics": {"emoji": "📐", "color": "#1565C0", "name_en": "General Mathematics", "name_tl": "Pangkalahatang Matematika"},
    "Introduction_to_Philosophy": {"emoji": "🤔", "color": "#4A148C", "name_en": "Introduction to Philosophy", "name_tl": "Introduksyon sa Pilosopiya"},
    "Komunikasyon_at_Pananaliksik": {"emoji": "💬", "color": "#E65100", "name_en": "Komunikasyon at Pananaliksik", "name_tl": "Komunikasyon at Pananaliksik"},
    "Media_and_Information_Literacy": {"emoji": "📱", "color": "#00838F", "name_en": "Media and Information Literacy", "name_tl": "Media at Information Literacy"},
    "Oral_Communication": {"emoji": "🗣", "color": "#283593", "name_en": "Oral Communication", "name_tl": "Oral na Komunikasyon"},
    "Personal_Development": {"emoji": "🧘", "color": "#AD1457", "name_en": "Personal Development", "name_tl": "Personal na Pag-unlad"},
    "Physical_Education_and_Health": {"emoji": "🏃", "color": "#00838F", "name_en": "Physical Education and Health", "name_tl": "Edukasyong Pangkatawan at Kalusugan"},
    "Physical_Science": {"emoji": "⚛️", "color": "#2E7D32", "name_en": "Physical Science", "name_tl": "Agham Pisikal"},
    "Reading_and_Writing": {"emoji": "📖", "color": "#4A148C", "name_en": "Reading and Writing", "name_tl": "Pagbasa at Pagsulat"},
    "Statistics_and_Probability": {"emoji": "📊", "color": "#1565C0", "name_en": "Statistics and Probability", "name_tl": "Estadistika at Probabilidad"},
    "Applied_Economics": {"emoji": "💰", "color": "#4E342E", "name_en": "Applied Economics", "name_tl": "Applied Economics"},
    "Business_Ethics_Social_Responsibility": {"emoji": "⚖️", "color": "#4E342E", "name_en": "Business Ethics & Social Responsibility", "name_tl": "Etika sa Negosyo"},
    "Business_Mathematics": {"emoji": "📊", "color": "#1565C0", "name_en": "Business Mathematics", "name_tl": "Business Mathematics"},
    "Fundamentals_of_Accountancy_Business_Management_1": {"emoji": "📒", "color": "#4E342E", "name_en": "FABM 1", "name_tl": "FABM 1"},
    "Organization_and_Management": {"emoji": "🏢", "color": "#4E342E", "name_en": "Organization and Management", "name_tl": "Organisasyon at Pamamahala"},
    "Business_Enterprise_Simulation": {"emoji": "💼", "color": "#4E342E", "name_en": "Business Enterprise Simulation", "name_tl": "Business Enterprise Simulation"},
    "Business_Finance": {"emoji": "💰", "color": "#4E342E", "name_en": "Business Finance", "name_tl": "Business Finance"},
    "Fundamentals_of_Accountancy_Business_Management_2": {"emoji": "📒", "color": "#4E342E", "name_en": "FABM 2", "name_tl": "FABM 2"},
    "Principles_of_Marketing": {"emoji": "📢", "color": "#4E342E", "name_en": "Principles of Marketing", "name_tl": "Principles of Marketing"},
    "Work_Immersion_ABM": {"emoji": "💼", "color": "#4E342E", "name_en": "Work Immersion (ABM)", "name_tl": "Work Immersion (ABM)"},
    "Disciplines_and_Ideas_in_Social_Sciences": {"emoji": "🌏", "color": "#C62828", "name_en": "Disciplines & Ideas in Soc. Sci.", "name_tl": "Disiplina sa Agham Panlipunan"},
    "Philippine_Politics_and_Governance": {"emoji": "🏛️", "color": "#C62828", "name_en": "Philippine Politics & Governance", "name_tl": "Politika at Pamamahala sa Pilipinas"},
    "World_Religions_Belief_Systems": {"emoji": "🕊️", "color": "#4A148C", "name_en": "World Religions & Belief Systems", "name_tl": "Mga Relihiyon sa Mundo"},
    "Community_Engagement_Solidarity_Citizenship": {"emoji": "🤝", "color": "#C62828", "name_en": "Community Engagement", "name_tl": "Pakikipag-ugnayan sa Komunidad"},
    "Creative_Nonfiction": {"emoji": "✍️", "color": "#4A148C", "name_en": "Creative Nonfiction", "name_tl": "Creative Nonfiction"},
    "Creative_Writing": {"emoji": "✍️", "color": "#4A148C", "name_en": "Creative Writing", "name_tl": "Creative Writing"},
    "Disciplines_and_Ideas_in_Applied_Social_Sciences": {"emoji": "🔍", "color": "#C62828", "name_en": "Disciplines & Ideas in Applied Soc. Sci.", "name_tl": "Disiplina sa Applied Soc. Sci."},
    "Trends_Networks_Critical_Thinking": {"emoji": "📡", "color": "#00838F", "name_en": "Trends, Networks & Critical Thinking", "name_tl": "Trends, Networks at Critical Thinking"},
    "Basic_Calculus": {"emoji": "∫", "color": "#1565C0", "name_en": "Basic Calculus", "name_tl": "Basic Calculus"},
    "General_Biology_1": {"emoji": "🧬", "color": "#2E7D32", "name_en": "General Biology 1", "name_tl": "General Biology 1"},
    "General_Chemistry_1": {"emoji": "⚗️", "color": "#2E7D32", "name_en": "General Chemistry 1", "name_tl": "General Chemistry 1"},
    "Pre_Calculus": {"emoji": "📐", "color": "#1565C0", "name_en": "Pre-Calculus", "name_tl": "Pre-Calculus"},
    "General_Biology_2": {"emoji": "🧬", "color": "#2E7D32", "name_en": "General Biology 2", "name_tl": "General Biology 2"},
    "General_Chemistry_2": {"emoji": "⚗️", "color": "#2E7D32", "name_en": "General Chemistry 2", "name_tl": "General Chemistry 2"},
    "General_Physics_1": {"emoji": "⚡", "color": "#1565C0", "name_en": "General Physics 1", "name_tl": "General Physics 1"},
    "General_Physics_2": {"emoji": "⚡", "color": "#1565C0", "name_en": "General Physics 2", "name_tl": "General Physics 2"},
    "Research_Project_STEM": {"emoji": "🔬", "color": "#2E7D32", "name_en": "Research Project (STEM)", "name_tl": "Research Project (STEM)"},
    "Work_Immersion_STEM": {"emoji": "🔬", "color": "#2E7D32", "name_en": "Work Immersion (STEM)", "name_tl": "Work Immersion (STEM)"},
    "Agri_Fishery_Arts": {"emoji": "🌾", "color": "#4E342E", "name_en": "Agri-Fishery Arts", "name_tl": "Agri-Fishery Arts"},
    "Home_Economics": {"emoji": "🍳", "color": "#4E342E", "name_en": "Home Economics", "name_tl": "Home Economics"},
    "ICT_Track": {"emoji": "💻", "color": "#4E342E", "name_en": "ICT Track", "name_tl": "ICT Track"},
    "Industrial_Arts": {"emoji": "🔧", "color": "#4E342E", "name_en": "Industrial Arts", "name_tl": "Industrial Arts"},
    "Media_Arts": {"emoji": "📷", "color": "#F57C00", "name_en": "Media Arts", "name_tl": "Media Arts"},
    "Performing_Arts": {"emoji": "🎭", "color": "#F57C00", "name_en": "Performing Arts", "name_tl": "Performing Arts"},
    "Visual_Arts": {"emoji": "🎨", "color": "#F57C00", "name_en": "Visual Arts", "name_tl": "Visual Arts"},
    "Fitness_and_Exercise_Programming": {"emoji": "🏋️", "color": "#00838F", "name_en": "Fitness & Exercise Programming", "name_tl": "Fitness at Exercise Programming"},
    "Sports_Officiating_and_Coaching": {"emoji": "⚽", "color": "#00838F", "name_en": "Sports Officiating & Coaching", "name_tl": "Sports Officiating at Coaching"},
    "Sports_Psychology_and_Nutrition": {"emoji": "🧠", "color": "#00838F", "name_en": "Sports Psychology & Nutrition", "name_tl": "Sports Psychology at Nutrition"},
    "Empowerment_Technologies": {"emoji": "💻", "color": "#00838F", "name_en": "Empowerment Technologies", "name_tl": "Empowerment Technologies"},
    "English_for_Academic_Professional_Purposes": {"emoji": "📝", "color": "#6A1B9A", "name_en": "EAPP", "name_tl": "EAPP"},
    "Entrepreneurship": {"emoji": "🚀", "color": "#4E342E", "name_en": "Entrepreneurship", "name_tl": "Entrepreneurship"},
    "Filipino_sa_Piling_Larangan": {"emoji": "✍️", "color": "#E65100", "name_en": "Filipino sa Piling Larangan", "name_tl": "Filipino sa Piling Larangan"},
    "Inquiries_Investigations_Immersion": {"emoji": "🔍", "color": "#4A148C", "name_en": "Inquiries, Investigations & Immersion", "name_tl": "Inquiries, Investigations & Immersion"},
    "Practical_Research_1": {"emoji": "📊", "color": "#4A148C", "name_en": "Practical Research 1", "name_tl": "Practical Research 1"},
    "Practical_Research_2": {"emoji": "📊", "color": "#4A148C", "name_en": "Practical Research 2", "name_tl": "Practical Research 2"},
    "Applied_Economics_GAS": {"emoji": "💰", "color": "#4E342E", "name_en": "Applied Economics (GAS)", "name_tl": "Applied Economics (GAS)"},
    "Disaster_Readiness_GAS": {"emoji": "⚠️", "color": "#B71C1C", "name_en": "Disaster Readiness (GAS)", "name_tl": "Disaster Readiness (GAS)"},
    "Humanities_1": {"emoji": "📚", "color": "#4A148C", "name_en": "Humanities 1", "name_tl": "Humanities 1"},
    "Humanities_2": {"emoji": "📚", "color": "#4A148C", "name_en": "Humanities 2", "name_tl": "Humanities 2"},
    "Organization_and_Management_GAS": {"emoji": "🏢", "color": "#4E342E", "name_en": "Organization and Management (GAS)", "name_tl": "Organization and Management (GAS)"},
    "Social_Science_1": {"emoji": "🌏", "color": "#C62828", "name_en": "Social Science 1", "name_tl": "Social Science 1"},
}

DIFFICULTIES = ["Full Lesson", "Easy", "Medium", "Hard", "Practice", "Full Assessment"]

# --------------- HTML templates ---------------

def _css():
    return """
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.7;
            color: #333;
            background: #FFF8E1;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .lesson-card {
            background: #fff;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .lesson-header {
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            color: #fff;
            text-align: center;
        }
        .lesson-header h1 { font-size: 26px; margin-bottom: 5px; }
        .lesson-header .emoji-icon { font-size: 48px; display: block; margin-bottom: 10px; }
        .difficulty-badge {
            display: inline-block;
            padding: 4px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
            color: #fff;
            margin-top: 8px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            border-left: 5px solid VAR_COLOR;
            padding-left: 12px;
            margin: 25px 0 15px;
        }
        .subsection-title {
            font-size: 17px;
            font-weight: 600;
            color: #444;
            margin: 20px 0 10px;
        }
        .step-card {
            background: #F5F5F5;
            border-radius: 10px;
            padding: 15px 20px;
            margin: 10px 0;
            border-left: 4px solid VAR_COLOR;
        }
        .step-card .step-num {
            display: inline-block;
            background: VAR_COLOR;
            color: #fff;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            text-align: center;
            line-height: 24px;
            font-size: 13px;
            font-weight: bold;
            margin-right: 8px;
        }
        .definition-box {
            background: #E3F2FD;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #BBDEFB;
        }
        .example-box {
            background: #FFF3E0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #FFE0B2;
        }
        .tip-box {
            background: #E8F5E9;
            border-radius: 10px;
            padding: 12px 15px;
            margin: 10px 0;
            border: 1px solid #C8E6C9;
        }
        .tip-box::before { content: "💡 "; }
        .warning-box {
            background: #FFEBEE;
            border-radius: 10px;
            padding: 12px 15px;
            margin: 10px 0;
            border: 1px solid #FFCDD2;
        }
        .warning-box::before { content: "⚠️ "; }
        .exercise-box {
            background: #F3E5F5;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #E1BEE7;
        }
        .image-box {
            text-align: center;
            margin: 15px 0;
            padding: 10px;
            background: #FAFAFA;
            border-radius: 8px;
        }
        .image-box img {
            max-width: 100%;
            border-radius: 8px;
        }
        .image-box .caption {
            font-size: 12px; color: #666; margin-top: 5px;
        }
        .answer-key {
            display: none;
            background: #E8F5E9;
            border: 1px solid #A5D6A7;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        .answer-key h4 { color: #2E7D32; margin-bottom: 8px; }
        .progress-dots {
            text-align: center;
            margin: 15px 0;
        }
        .progress-dots .dot {
            display: inline-block;
            width: 12px; height: 12px;
            border-radius: 50%;
            margin: 0 4px;
            background: #E0E0E0;
        }
        .progress-dots .dot.active { background: VAR_COLOR; }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin: 10px 0;
        }
        .fact-card {
            background: #fff;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            border: 1px solid #E0E0E0;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }
        .fact-card .fc-icon { font-size: 32px; display: block; margin-bottom: 5px; }
        .fact-card .fc-label { font-size: 13px; color: #555; }
        .key-points li { margin-bottom: 6px; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #E0E0E0;
            padding: 8px 12px;
            text-align: left;
        }
        th { background: VAR_COLOR; color: #fff; font-weight: 600; }
        tr:nth-child(even) { background: #F9F9F9; }
        .vis-g1 { font-size: 18px; }
        .vis-g1 .step-card { font-size: 16px; line-height: 1.8; }
        .vis-g1 p { margin-bottom: 8px; }
        @media (max-width: 600px) {
            .grid-2, .grid-3 { grid-template-columns: 1fr; }
            body { padding: 10px; }
            .lesson-card { padding: 15px; }
        }
    </style>
    """

def _student_css():
    return """
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.8;
            color: #2C3E50;
            background: #E8F5E9;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .lesson-card {
            background: #fff;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .lesson-header {
            background: linear-gradient(135deg, #43A047, #66BB6A);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 25px;
            color: #fff;
            text-align: center;
        }
        .lesson-header h1 { font-size: 28px; margin-bottom: 5px; }
        .lesson-header .emoji-icon { font-size: 56px; display: block; margin-bottom: 10px; }
        .section-title {
            font-size: 22px;
            font-weight: bold;
            color: #2E7D32;
            border-left: 5px solid #43A047;
            padding-left: 12px;
            margin: 25px 0 15px;
        }
        .subsection-title {
            font-size: 18px;
            font-weight: 600;
            color: #555;
            margin: 20px 0 10px;
        }
        .step-card {
            background: #F1F8E9;
            border-radius: 12px;
            padding: 15px 20px;
            margin: 10px 0;
            border-left: 4px solid #66BB6A;
        }
        .step-card .step-num {
            display: inline-block;
            background: #43A047;
            color: #fff;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            text-align: center;
            line-height: 28px;
            font-size: 14px;
            font-weight: bold;
            margin-right: 8px;
        }
        .definition-box {
            background: #E8F5E9;
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border: 1px solid #C8E6C9;
            font-size: 16px;
        }
        .example-box {
            background: #FFF8E1;
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border: 1px solid #FFE082;
        }
        .tip-box {
            background: #E3F2FD;
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border: 1px solid #BBDEFB;
        }
        .exercise-box {
            background: #F3E5F5;
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border: 1px solid #CE93D8;
        }
        .exercise-box p { margin-bottom: 8px; }
        .answer-key {
            background: #E0F2F1;
            border-radius: 12px;
            padding: 18px;
            margin: 10px 0;
            border: 1px solid #80CBC4;
        }
        .motivation-box {
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            border-radius: 14px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #E65100;
            border: 2px solid #FFB74D;
        }
        .key-points { padding-left: 24px; margin: 10px 0; }
        .key-points li { margin-bottom: 8px; font-size: 16px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 15px 0; }
        .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin: 15px 0; }
        .fact-card { background: #F5F5F5; border-radius: 10px; padding: 15px; text-align: center; }
        .fact-card .fc-icon { font-size: 32px; display: block; }
        .fact-card .fc-label { font-size: 13px; margin-top: 5px; color: #555; }
        .image-box { text-align: center; margin: 15px 0; padding: 8px; background: #F1F8E9; border-radius: 14px; }
        .image-box img { max-width: 100%; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .image-box svg { max-width: 100%; border-radius: 8px; }
        .image-box .caption { font-size: 13px; color: #555; margin-top: 6px; font-style: italic; }
        .grid-2 .image-box { background: transparent; padding: 4px; }
        .progress-dots { text-align: center; margin: 20px 0; }
        .progress-dots .dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin: 0 6px; }
        .progress-dots .dot.active { background: #43A047; }
        .progress-dots .dot.inactive { background: #E0E0E0; }
        .vis-g1 { font-size: 18px; }
        @media (max-width: 600px) {
            .grid-2, .grid-3 { grid-template-columns: 1fr; }
            body { padding: 10px; }
            .lesson-card { padding: 18px; }
        }
    </style>
    """

def _image_html(url, caption="", subject=""):
    b64_uri = _download_image_b64(url)
    if b64_uri:
        src = b64_uri
    else:
        src = url
    return f"""
    <div class="image-box">
        <img src="{src}" alt="{caption}" onerror="this.style.display='none'">
        {f'<div class="caption">{caption}</div>' if caption else ''}
    </div>"""


# ----- Image database for student lessons -----

_SUBJECT_IMAGES = {
    "Mathematics": [
        ("https://cdn.pixabay.com/photo/2016/03/27/07/12/education-1282263_1280.jpg", "Numbers and problem solving"),
        ("https://cdn.pixabay.com/photo/2018/03/03/20/03/abacus-3195486_1280.jpg", "Counting with abacus"),
        ("https://cdn.pixabay.com/photo/2017/11/30/17/30/geometry-2989356_1280.jpg", "Geometric shapes"),
        ("https://cdn.pixabay.com/photo/2016/04/20/19/49/ruler-1341825_1280.jpg", "Measuring and tools"),
        ("https://cdn.pixabay.com/photo/2017/06/20/22/14/man-2425124_1280.jpg", "Math in daily life"),
        ("https://cdn.pixabay.com/photo/2014/07/01/12/35/calculator-381209_1280.jpg", "Learning calculations"),
        ("https://cdn.pixabay.com/photo/2015/09/06/16/51/math-927418_1280.jpg", "Math equations"),
    ],
    "Science": [
        ("https://cdn.pixabay.com/photo/2016/11/30/11/23/laboratory-1869053_1280.jpg", "Science laboratory"),
        ("https://cdn.pixabay.com/photo/2019/06/26/18/57/microscope-4300509_1280.jpg", "Using a microscope"),
        ("https://cdn.pixabay.com/photo/2018/04/11/21/25/anatomy-3311539_1280.jpg", "Human body"),
        ("https://cdn.pixabay.com/photo/2015/12/07/10/35/plant-1082283_1280.jpg", "Plants and nature"),
        ("https://cdn.pixabay.com/photo/2020/06/14/17/21/solar-system-5298401_1280.jpg", "Solar system"),
        ("https://cdn.pixabay.com/photo/2017/07/25/18/30/butterfly-2538948_1280.jpg", "Animals and insects"),
        ("https://cdn.pixabay.com/photo/2015/07/14/18/14/water-845196_1280.jpg", "Water and environment"),
    ],
    "English": [
        ("https://cdn.pixabay.com/photo/2015/11/19/20/54/book-1052014_1280.jpg", "Reading books"),
        ("https://cdn.pixabay.com/photo/2016/03/31/14/56/alphabet-1293012_1280.jpg", "Learning the alphabet"),
        ("https://cdn.pixabay.com/photo/2017/09/01/21/16/letters-2705645_1280.jpg", "Letters and words"),
        ("https://cdn.pixabay.com/photo/2016/09/10/17/18/books-1659691_1280.jpg", "Story time"),
        ("https://cdn.pixabay.com/photo/2018/01/17/18/36/startup-3088811_1280.jpg", "Writing and expression"),
    ],
    "Reading_and_Literacy": [
        ("https://cdn.pixabay.com/photo/2015/11/19/20/54/book-1052014_1280.jpg", "Discover the joy of reading"),
        ("https://cdn.pixabay.com/photo/2017/09/01/21/16/letters-2705645_1280.jpg", "Letters make words"),
        ("https://cdn.pixabay.com/photo/2016/03/31/14/56/alphabet-1293012_1280.jpg", "Alphabet adventure"),
        ("https://cdn.pixabay.com/photo/2018/03/05/16/09/read-3201212_1280.jpg", "Reading together"),
    ],
    "Language": [
        ("https://cdn.pixabay.com/photo/2016/03/31/14/56/alphabet-1293012_1280.jpg", "Learning new words"),
        ("https://cdn.pixabay.com/photo/2017/09/01/21/16/letters-2705645_1280.jpg", "Building language skills"),
        ("https://cdn.pixabay.com/photo/2016/06/15/15/35/language-1459267_1280.jpg", "Communication"),
    ],
    "Filipino": [
        ("https://cdn.pixabay.com/photo/2016/03/30/00/05/flag-1290122_1280.jpg", "Watawat ng Pilipinas"),
        ("https://cdn.pixabay.com/photo/2017/03/14/14/22/asia-2143090_1280.jpg", "Mapa ng Pilipinas"),
        ("https://cdn.pixabay.com/photo/2019/02/24/16/35/people-4017447_1280.jpg", "Kultura at tradisyon"),
        ("https://cdn.pixabay.com/photo/2015/12/08/00/43/children-1081972_1280.jpg", "Wikang Filipino"),
    ],
    "Araling_Panlipunan": [
        ("https://cdn.pixabay.com/photo/2017/03/14/14/22/asia-2143090_1280.jpg", "Map of Asia"),
        ("https://cdn.pixabay.com/photo/2017/07/13/15/49/philippines-2500926_1280.jpg", "Philippine landscape"),
        ("https://cdn.pixabay.com/photo/2017/04/04/12/29/globe-2201671_1280.jpg", "Our world"),
        ("https://cdn.pixabay.com/photo/2016/03/05/19/02/historical-1238152_1280.jpg", "History and heritage"),
        ("https://cdn.pixabay.com/photo/2015/12/15/06/42/children-1093759_1280.jpg", "Community helpers"),
    ],
    "Makabansa": [
        ("https://cdn.pixabay.com/photo/2017/03/14/14/22/asia-2143090_1280.jpg", "Mapa ng Pilipinas"),
        ("https://cdn.pixabay.com/photo/2016/03/30/00/05/flag-1290122_1280.jpg", "Watawat ng Pilipinas"),
        ("https://cdn.pixabay.com/photo/2017/07/13/15/49/philippines-2500926_1280.jpg", "Magagandang tanawin"),
    ],
    "Music_and_Arts": [
        ("https://cdn.pixabay.com/photo/2016/11/23/06/57/art-1852305_1280.jpg", "Art and creativity"),
        ("https://cdn.pixabay.com/photo/2016/11/29/05/08/music-1107752_1280.jpg", "Music and instruments"),
        ("https://cdn.pixabay.com/photo/2017/08/06/22/57/art-2597046_1280.jpg", "Painting and drawing"),
        ("https://cdn.pixabay.com/photo/2015/05/07/12/04/children-756393_1280.jpg", "Dance and movement"),
    ],
    "MAPEH": [
        ("https://cdn.pixabay.com/photo/2016/11/23/06/57/art-1852305_1280.jpg", "Art and creativity"),
        ("https://cdn.pixabay.com/photo/2016/11/29/05/08/music-1107752_1280.jpg", "Music and instruments"),
        ("https://cdn.pixabay.com/photo/2017/08/06/22/57/art-2597046_1280.jpg", "Painting and drawing"),
        ("https://cdn.pixabay.com/photo/2016/11/29/12/16/exercise-1869358_1280.jpg", "Physical education"),
    ],
    "PE_and_Health": [
        ("https://cdn.pixabay.com/photo/2016/11/29/12/16/exercise-1869358_1280.jpg", "Exercise and fitness"),
        ("https://cdn.pixabay.com/photo/2017/07/02/19/24/running-2465304_1280.jpg", "Running and sports"),
        ("https://cdn.pixabay.com/photo/2017/07/13/08/59/vegetables-2499864_1280.jpg", "Healthy eating"),
        ("https://cdn.pixabay.com/photo/2015/05/31/10/55/children-791029_1280.jpg", "Playing outdoors"),
    ],
    "GMRC": [
        ("https://cdn.pixabay.com/photo/2017/07/25/09/17/hands-2537466_1280.jpg", "Helping others"),
        ("https://cdn.pixabay.com/photo/2016/06/07/18/36/people-1442258_1280.jpg", "Friendship and kindness"),
        ("https://cdn.pixabay.com/photo/2017/05/20/12/00/family-2328701_1280.jpg", "Family and respect"),
        ("https://cdn.pixabay.com/photo/2015/01/08/18/11/children-593313_1280.jpg", "Working together"),
    ],
    "Values_Education": [
        ("https://cdn.pixabay.com/photo/2017/07/25/09/17/hands-2537466_1280.jpg", "Helping and sharing"),
        ("https://cdn.pixabay.com/photo/2016/06/07/18/36/people-1442258_1280.jpg", "Friendship"),
        ("https://cdn.pixabay.com/photo/2017/05/20/12/00/family-2328701_1280.jpg", "Family values"),
    ],
    "EPP_TLE": [
        ("https://cdn.pixabay.com/photo/2017/06/16/07/26/tools-2408408_1280.jpg", "Tools and equipment"),
        ("https://cdn.pixabay.com/photo/2016/11/06/23/16/cooking-1804278_1280.jpg", "Cooking and preparation"),
        ("https://cdn.pixabay.com/photo/2017/09/21/18/17/sewing-2773012_1280.jpg", "Sewing and crafts"),
        ("https://cdn.pixabay.com/photo/2016/11/23/14/45/coding-1833356_1280.jpg", "Technology and computing"),
    ],
    "TLE": [
        ("https://cdn.pixabay.com/photo/2017/06/16/07/26/tools-2408408_1280.jpg", "Tools and equipment"),
        ("https://cdn.pixabay.com/photo/2016/11/06/23/16/cooking-1804278_1280.jpg", "Cooking and preparation"),
        ("https://cdn.pixabay.com/photo/2016/11/23/14/45/coding-1833356_1280.jpg", "Technology"),
    ],
    "Cognitive_Development": [
        ("https://cdn.pixabay.com/photo/2017/06/09/18/44/puzzle-2387796_1280.jpg", "Puzzles and thinking"),
        ("https://cdn.pixabay.com/photo/2016/03/27/22/22/cubes-1284461_1280.jpg", "Building and exploring"),
        ("https://cdn.pixabay.com/photo/2019/08/29/15/26/children-4438543_1280.jpg", "Learning through play"),
        ("https://cdn.pixabay.com/photo/2016/03/27/07/12/education-1282263_1280.jpg", "Discovering new things"),
    ],
    "Aesthetic_Creative_Development": [
        ("https://cdn.pixabay.com/photo/2016/11/23/06/57/art-1852305_1280.jpg", "Creative expression"),
        ("https://cdn.pixabay.com/photo/2017/08/06/22/57/art-2597046_1280.jpg", "Drawing and painting"),
        ("https://cdn.pixabay.com/photo/2016/11/29/05/08/music-1107752_1280.jpg", "Making music"),
        ("https://cdn.pixabay.com/photo/2017/06/27/08/49/children-2446537_1280.jpg", "Imaginative play"),
    ],
    "Language_Literacy_Communication": [
        ("https://cdn.pixabay.com/photo/2016/03/31/14/56/alphabet-1293012_1280.jpg", "Learning letters"),
        ("https://cdn.pixabay.com/photo/2015/11/19/20/54/book-1052014_1280.jpg", "Story time"),
        ("https://cdn.pixabay.com/photo/2017/09/01/21/16/letters-2705645_1280.jpg", "Words and language"),
    ],
    "Physical_Health_Motor_Development": [
        ("https://cdn.pixabay.com/photo/2015/05/31/10/55/children-791029_1280.jpg", "Active play"),
        ("https://cdn.pixabay.com/photo/2016/11/29/12/16/exercise-1869358_1280.jpg", "Exercise and movement"),
        ("https://cdn.pixabay.com/photo/2017/07/13/08/59/vegetables-2499864_1280.jpg", "Healthy habits"),
    ],
    "Socio_emotional_Development": [
        ("https://cdn.pixabay.com/photo/2016/06/07/18/36/people-1442258_1280.jpg", "Making friends"),
        ("https://cdn.pixabay.com/photo/2017/05/20/12/00/family-2328701_1280.jpg", "Feelings and emotions"),
        ("https://cdn.pixabay.com/photo/2015/01/08/18/11/children-593313_1280.jpg", "Playing together"),
    ],
    "Values_Development": [
        ("https://cdn.pixabay.com/photo/2017/07/25/09/17/hands-2537466_1280.jpg", "Helping each other"),
        ("https://cdn.pixabay.com/photo/2015/01/08/18/11/children-593313_1280.jpg", "Sharing and caring"),
        ("https://cdn.pixabay.com/photo/2017/05/20/12/00/family-2328701_1280.jpg", "Respecting others"),
    ],
}

def _get_cache_dir():
    import sys
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), ".img_cache")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".img_cache")


_IMAGE_CACHE_DIR = _get_cache_dir()


def _download_image_b64(url):
    """Download an image and return a base64 data URI. Caches locally."""
    os.makedirs(_IMAGE_CACHE_DIR, exist_ok=True)
    cache_key = hashlib.md5(url.encode()).hexdigest() + ".b64"
    cache_path = os.path.join(_IMAGE_CACHE_DIR, cache_key)
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return f.read()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        ct = resp.headers.get("Content-Type", "image/jpeg")
        b64 = base64.b64encode(data).decode()
        uri = f"data:{ct};base64,{b64}"
        with open(cache_path, "w") as f:
            f.write(uri)
        return uri
    except Exception:
        return ""


_SUBJECT_VISUAL_CARDS = {
    "Mathematics": [
        {"emojis": "📐 📏 🔢", "bg": "#E3F2FD", "border": "#1565C0", "items": ["Numbers", "Shapes", "Measuring"], "caption": "Math is everywhere!"},
        {"emojis": "➕ ➖ ✖️ ➗", "bg": "#E8F5E9", "border": "#43A047", "items": ["Add", "Subtract", "Multiply", "Divide"], "caption": "Basic Operations"},
    ],
    "Science": [
        {"emojis": "🔬 🧪 🌱", "bg": "#E8F5E9", "border": "#2E7D32", "items": ["Observe", "Experiment", "Discover"], "caption": "Explore the world!"},
        {"emojis": "🌍 ☀️ 💧", "bg": "#FFF3E0", "border": "#E65100", "items": ["Earth", "Sun", "Water"], "caption": "Nature all around us"},
    ],
    "English": [
        {"emojis": "📖 ✏️ 💬", "bg": "#F3E5F5", "border": "#6A1B9A", "items": ["Read", "Write", "Speak"], "caption": "Communication skills"},
        {"emojis": "🔤 📝 🗣", "bg": "#E8EAF6", "border": "#283593", "items": ["Letters", "Words", "Sentences"], "caption": "Build your vocabulary"},
    ],
    "Reading_and_Literacy": [
        {"emojis": "📚 📖 🌟", "bg": "#F3E5F5", "border": "#4A148C", "items": ["Read", "Learn", "Grow"], "caption": "Discover new worlds through reading!"},
        {"emojis": "🔤 🔤 ✨", "bg": "#E8EAF6", "border": "#283593", "items": ["Letters", "Words", "Stories"], "caption": "Reading is an adventure"},
    ],
    "Language": [
        {"emojis": "💬 🗣 📝", "bg": "#E8EAF6", "border": "#283593", "items": ["Listen", "Speak", "Write"], "caption": "Language connects us"},
    ],
    "Filipino": [
        {"emojis": "🇵🇭 📖 ✏️", "bg": "#FFF3E0", "border": "#E65100", "items": ["Wikang Filipino", "Pagbasa", "Pagsulat"], "caption": "Mahalin ang wikang Filipino!"},
    ],
    "Araling_Panlipunan": [
        {"emojis": "🌏 🗺 🏠", "bg": "#FFEBEE", "border": "#C62828", "items": ["Our World", "Maps", "Community"], "caption": "Know your surroundings"},
    ],
    "Makabansa": [
        {"emojis": "🇵🇭 🌏 💚", "bg": "#E8F5E9", "border": "#1B5E20", "items": ["Pilipinas", "Kultura", "Wika"], "caption": "Proud to be Filipino!"},
    ],
    "Music_and_Arts": [
        {"emojis": "🎨 🎵 🎭", "bg": "#FFF8E1", "border": "#F9A825", "items": ["Art", "Music", "Dance"], "caption": "Express yourself!"},
        {"emojis": "🎶 ✏️ 🖌", "bg": "#FFF3E0", "border": "#F57C00", "items": ["Songs", "Drawing", "Painting"], "caption": "Creativity has no limits"},
    ],
    "MAPEH": [
        {"emojis": "🎨 🏃 💚", "bg": "#FFF8E1", "border": "#F9A825", "items": ["Arts", "PE", "Health"], "caption": "Mind and body wellness"},
    ],
    "PE_and_Health": [
        {"emojis": "🏃 ⚽ 🥗", "bg": "#E0F7FA", "border": "#00838F", "items": ["Move", "Play", "Eat Healthy"], "caption": "Stay active and healthy!"},
        {"emojis": "💪 🏀 🍎", "bg": "#E8F5E9", "border": "#43A047", "items": ["Exercise", "Sports", "Nutrition"], "caption": "Strong body, strong mind"},
    ],
    "GMRC": [
        {"emojis": "💚 🤝 ⭐", "bg": "#FCE4EC", "border": "#AD1457", "items": ["Kindness", "Respect", "Honesty"], "caption": "Being a good person"},
    ],
    "Values_Education": [
        {"emojis": "❤️ 🤝 🌟", "bg": "#FCE4EC", "border": "#AD1457", "items": ["Love", "Share", "Care"], "caption": "Good values for life"},
    ],
    "EPP_TLE": [
        {"emojis": "🛠 🍳 🧵", "bg": "#EFEBE9", "border": "#4E342E", "items": ["Tools", "Cooking", "Crafts"], "caption": "Learn useful skills!"},
    ],
    "TLE": [
        {"emojis": "🛠 💻 🍳", "bg": "#EFEBE9", "border": "#4E342E", "items": ["Tools", "Technology", "Home"], "caption": "Skills for life"},
    ],
    "Cognitive_Development": [
        {"emojis": "🧠 🧩 🎯", "bg": "#E0F2F1", "border": "#00695C", "items": ["Think", "Solve", "Create"], "caption": "Train your brain!"},
    ],
    "Aesthetic_Creative_Development": [
        {"emojis": "🎨 🎵 🌈", "bg": "#FFF3E0", "border": "#F57C00", "items": ["Colors", "Sounds", "Beauty"], "caption": "See beauty everywhere!"},
    ],
    "Language_Literacy_Communication": [
        {"emojis": "🗣 📖 ✏️", "bg": "#E8EAF6", "border": "#283593", "items": ["Talk", "Read", "Write"], "caption": "Words are powerful!"},
    ],
    "Physical_Health_Motor_Development": [
        {"emojis": "💪 🏃 🥗", "bg": "#E0F7FA", "border": "#00838F", "items": ["Move", "Play", "Grow"], "caption": "Be active every day!"},
    ],
    "Socio_emotional_Development": [
        {"emojis": "😊 🤗 ❤️", "bg": "#FCE4EC", "border": "#AD1457", "items": ["Feelings", "Friends", "Family"], "caption": "Understand your feelings"},
    ],
    "Values_Development": [
        {"emojis": "⭐ 💚 🤝", "bg": "#FCE4EC", "border": "#AD1457", "items": ["Honesty", "Kindness", "Respect"], "caption": "Grow with good values"},
    ],
}


def _build_visual_card(card):
    """Build an HTML/CSS visual card from a card dict."""
    items_html = "".join(f'<span style="background:{card["border"]};color:#fff;padding:4px 10px;border-radius:12px;font-size:12px;font-weight:600;">{it}</span>' for it in card["items"])
    return f"""<div class="image-box" style="background:{card['bg']};border:2px solid {card['border']};padding:15px;border-radius:12px;text-align:center;margin:10px 0;">
<div style="font-size:32px;margin-bottom:8px;">{card['emojis']}</div>
<div style="display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-bottom:8px;">{items_html}</div>
<div style="font-size:13px;color:#555;font-style:italic;">{card['caption']}</div>
</div>"""


def _img_html_b64(url, caption="", subject=""):
    """Return image HTML with a base64 data URI downloaded from url."""
    uri = _download_image_b64(url)
    if not uri:
        return ""
    cap_html = f'<div class="caption">{caption}</div>' if caption else ""
    return f"""<div class="image-box">
<img src="{uri}" alt="{caption}" style="max-width:100%;border-radius:10px;">
{cap_html}
</div>"""

QUARTER_CONTENT = {}

def _load_quarter_content():
    """Load quarter-based curriculum content from the JSON asset file."""
    global QUARTER_CONTENT
    import json
    qpath = os.path.join(os.path.dirname(__file__), "quarter_curriculum.json")
    if os.path.exists(qpath):
        with open(qpath, "r", encoding="utf-8") as f:
            QUARTER_CONTENT = json.load(f)


def _quarter(grade_num, subject, quarter_idx, field="title"):
    """Get a quarter-specific curriculum field. Returns the quarter label + content."""
    key = str(grade_num)
    subj_key = subject
    if key in QUARTER_CONTENT and subj_key in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subj_key]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get(field, "")
    return ""


def _quarter_weeks(grade_num, subject, quarter_idx):
    """Get a list of week topics for the given quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("weeks", [])
    return []


def _quarter_standards(grade_num, subject, quarter_idx, field="content_standard"):
    """Get content/performance standards for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get(field, "")
    return ""


def _quarter_melcs(grade_num, subject, quarter_idx):
    """Get MELCs list for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("melcs", [])
    return []


def _quarter_exercises(grade_num, subject, quarter_idx):
    """Get exercises for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("exercises", [])
    return []


def _quarter_assessment(grade_num, subject, quarter_idx):
    """Get assessment items for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("assessment", [])
    return []


def _quarter_answers(grade_num, subject, quarter_idx):
    """Get answer key for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("answer_key", [])
    return []


def _quarter_description(grade_num, subject, quarter_idx):
    """Get lesson description for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("description", "")
    return ""


def _quarter_study_guide(grade_num, subject, quarter_idx):
    """Get study guide questions for a quarter."""
    key = str(grade_num)
    if key in QUARTER_CONTENT and subject in QUARTER_CONTENT[key]:
        qdata = QUARTER_CONTENT[key][subject]
        if quarter_idx < len(qdata):
            return qdata[quarter_idx].get("study_guide", {})
    return {}


def _build_visual_images(grade_num, subject, difficulty, count=2):
    """Generate subject-appropriate visual images for student lessons.

    Returns HTML with visual cards (HTML/CSS) and real photos (base64-encoded)
    appropriate for the subject, grade level, and position in the lesson.
    Early grades (K-5) get more images; older grades (6+) get fewer.
    """
    if isinstance(grade_num, str):
        try:
            grade_num = int(grade_num.split("_")[0])
        except ValueError:
            return ""
    heavy_visuals = grade_num <= 5

    # Determine how many image slots to fill
    num_images = count if heavy_visuals else max(1, count - 1)

    html_parts = []

    # Get visual cards for this subject (HTML/CSS cards that tkinterweb renders)
    cards = _SUBJECT_VISUAL_CARDS.get(subject, [])
    if not cards:
        for kw, card_list in _SUBJECT_VISUAL_CARDS.items():
            if kw.lower().replace("_", " ") in subject.lower().replace("_", " "):
                cards = card_list
                break

    # Get real images from database
    db_images = _SUBJECT_IMAGES.get(subject, [])
    if not db_images:
        for kw, imgs in _SUBJECT_IMAGES.items():
            if kw.lower().replace("_", " ") in subject.lower().replace("_", " "):
                db_images = imgs
                break
    if not db_images:
        db_images = _SUBJECT_IMAGES.get("Cognitive_Development", [])

    # Build the image grid
    used_cards = set()
    used_photos = []

    for i in range(num_images):
        # Alternate between cards and photos for heavy visuals
        if heavy_visuals and i % 2 == 0 and cards:
            card_idx = i // 2
            if card_idx < len(cards) and card_idx not in used_cards:
                html_parts.append(_build_visual_card(cards[card_idx]))
                used_cards.add(card_idx)
                continue

        # Use a photo from the database
        if db_images:
            idx = i % len(db_images)
            if idx not in used_photos:
                url, cap = db_images[idx]
                img_html = _img_html_b64(url, cap, subject)
                if img_html:
                    html_parts.append(img_html)
                used_photos.append(idx)

    # Ensure at least one image is shown
    if not html_parts:
        if cards:
            html_parts.append(_build_visual_card(cards[0]))
        elif db_images:
            img_html = _img_html_b64(db_images[0][0], db_images[0][1], subject)
            if img_html:
                html_parts.append(img_html)
        else:
            html_parts.append(_img_html_b64(
                "https://cdn.pixabay.com/photo/2016/03/27/07/12/education-1282263_1280.jpg",
                "Learning is fun!", subject))

    # Layout: use grid for early grades (2 columns)
    if len(html_parts) >= 2:
        result = '<div class="grid-2">'
        for h in html_parts[:2]:
            result += f'<div style="text-align:center;">{h}</div>'
        result += '</div>'
        for h in html_parts[2:]:
            result += h
        return result
    else:
        return "\n".join(html_parts)


def _kindergarten_content(grade_num, subject, difficulty, is_early):
    """Generate development-domain content for Kindergarten subjects."""
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    sections = []

    domain_blurbs = {
        "Cognitive_Development": ("Thinking and Problem-Solving", "Children develop early thinking skills through exploration, sorting, matching, and simple problem-solving activities that build a foundation for logical reasoning."),
        "Aesthetic_Creative_Development": ("Creativity and Expression", "Children explore art, music, movement, and imaginative play to express themselves and appreciate beauty in their environment."),
        "Language_Literacy_Communication": ("Language and Communication", "Children build vocabulary, listening, speaking, and pre-reading skills through stories, songs, and conversations."),
        "Mathematics": ("Early Math Concepts", "Children learn about numbers, shapes, patterns, and measurements through hands-on activities and play."),
        "Physical_Health_Motor_Development": ("Physical Growth and Motor Skills", "Children develop fine and gross motor skills, practice healthy habits, and learn about body awareness."),
        "Socio_emotional_Development": ("Social and Emotional Growth", "Children learn to identify emotions, build relationships, share, take turns, and develop self-awareness."),
        "Values_Development": ("Values and Character Formation", "Children learn basic values such as honesty, kindness, respect, and responsibility through stories and role modeling."),
    }

    blurb = domain_blurbs.get(subject, (en, "Children explore and learn through developmentally appropriate activities."))

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">{blurb[0]}</div>')
    sections.append(f"<p>{blurb[1]}</p>")

    if is_early:
        sections.append(_build_visual_images(grade_num, subject, difficulty))

    sections.append("""
    <div class="grid-2">
        <div class="fact-card"><span class="fc-icon">🎯</span><div class="fc-label">Learning Goal</div></div>
        <div class="fact-card"><span class="fc-icon">🎮</span><div class="fc-label">Play-Based</div></div>
    </div>
    """)

    sections.append(f'<div class="subsection-title">Fun Activities</div>')
    sections.append("<ul>")
    sections.append("<li>Sing a song about what we are learning today!</li>")
    sections.append("<li>Look at pictures and talk about what you see.</li>")
    sections.append("<li>Draw or color something that reminds you of this lesson.</li>")
    sections.append("</ul>")

    sections.append(f'<div class="tip-box">')
    sections.append("Let your child explore at their own pace. Celebrate every small achievement!")
    sections.append(f'</div>')

    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Try This:</strong> Talk with your child about what they learned today.</p>")
    sections.append("</div>")

    sections.append(f'<div class="progress-dots">')
    for i in range(3):
        sections.append(f'<span class="dot active" style="background:{info["color"]};"></span>')
    sections.append(f'</div>')

    content = "\n".join(sections)
    title = f"Kindergarten — {en}"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _melcs(grade_num, subject):
    """Alias for backward compatibility - returns Q1 MELCs"""
    return _quarter_melcs(grade_num, subject, 0)


def _wrap_html(content, title, subject, difficulty, grade_num):
    si = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    color = si["color"]
    emoji = si["emoji"]
    dc = {"Full Lesson": "#81C784", "Easy": "#A5D6A7", "Medium": "#FFE082",
           "Hard": "#EF9A9A", "Practice": "#CE93D8", "Full Assessment": "#F48FB1"}
    diff_color = dc.get(difficulty, "#888")
    css = _css().replace("VAR_COLOR", color)

    if isinstance(grade_num, int) and grade_num <= 4:
        extra_class = ' class="vis-g1"'
    else:
        extra_class = ""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{css}
</head><body{extra_class}>

<div class="lesson-card">
    <div class="lesson-header" style="background:{color};">
        <span class="emoji-icon">{emoji}</span>
        <h1>{title}</h1>
        <div style="font-size:14px;opacity:0.9;">{si['name_en']}</div>
        <span class="difficulty-badge" style="background:{diff_color};">{difficulty}</span>
    </div>

{content}

    <div style="text-align:center;margin-top:30px;padding-top:20px;border-top:1px solid #E0E0E0;font-size:12px;color:#999;">
        O.L.I.V.I.A. Visual Learning &mdash; Aligned with DepEd MATATAG / CHED Curriculum &mdash; {CURRENT_YEAR}
    </div>
</div>
</body></html>"""


def _student_wrap_html(content, title, subject, difficulty, grade_num):
    """Wrap student-friendly content in HTML with the student CSS theme."""
    si = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    emoji = si["emoji"]
    css = _student_css()

    if isinstance(grade_num, int) and grade_num <= 4:
        extra_class = ' class="vis-g1"'
    else:
        extra_class = ""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{css}
</head><body{extra_class}>

<div class="lesson-card">
    <div class="lesson-header">
        <span class="emoji-icon">{emoji}</span>
        <h1>{title}</h1>
        <div style="font-size:15px;opacity:0.95;">{si['name_en']}</div>
    </div>

{content}

    <div class="motivation-box">
        🌟 You're doing great! Keep learning and growing every day! 🌟
    </div>

    <div style="text-align:center;margin-top:30px;padding-top:20px;border-top:1px solid #C8E6C9;font-size:12px;color:#888;">
        O.L.I.V.I.A. Student Learning &mdash; Aligned with DepEd MATATAG / CHED Curriculum &mdash; {CURRENT_YEAR}
    </div>
</div>
</body></html>"""


def _student_lesson(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    """Generate a complete student-friendly lesson for one quarter.
    Includes ALL the content from the full lesson (content standards, MELCs,
    week-by-week topics, definitions, examples, study guide, exercises, answer key)
    presented in a warm, encouraging style with the green theme."""
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    emoji = info["emoji"]
    is_early = isinstance(grade_num, int) and grade_num <= 4
    heavy_visuals = isinstance(grade_num, int) and grade_num <= 5

    sections = []
    qtitle = _get_quarter_title(subject, quarter_idx)
    std = _quarter_standards(grade_num, subject, quarter_idx)
    desc = _quarter_description(grade_num, subject, quarter_idx)
    melc_list = _quarter_melcs(grade_num, subject, quarter_idx)
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)
    exercises = _quarter_exercises(grade_num, subject, quarter_idx)
    answers = _quarter_answers(grade_num, subject, quarter_idx)
    sg = _quarter_study_guide(grade_num, subject, quarter_idx)

    # -- Header / Introduction --
    sections.append(f'<div class="section-title">📖 Welcome to {qtitle}</div>')
    if heavy_visuals:
        sections.append(_build_visual_images(grade_num, subject, difficulty, count=3))
    sections.append(f"<p style='font-size:17px;'>{desc or f'Welcome to your {en} lesson! This quarter covers important topics that will help you learn and grow.'}</p>")

    # -- Content Standards --
    sections.append(f'<div class="section-title">🎯 Learning Goals</div>')
    sections.append(f"<p>{std or f'By the end of this quarter, you will understand the key concepts of {en} and be able to apply them in real life.'}</p>")
    if heavy_visuals:
        sections.append(_build_visual_images(grade_num, subject, difficulty, count=2))

    # -- MELCs --
    if melc_list:
        sections.append(f'<div class="subsection-title">📋 What You Will Learn</div>')
        sections.append("<ul class='key-points'>")
        for m in melc_list:
            sections.append(f"<li>{m}</li>")
        sections.append("</ul>")

    # -- Lesson Content (week-by-week) --
    sections.append(f'<div class="section-title">📚 Lesson Content</div>')
    if weeks:
        for i, week in enumerate(weeks[:5]):
            sections.append(f"""
        <div class="step-card">
            <span class="step-num">{i+1}</span>
            <strong>{week}</strong>
            <p>Explore this topic step by step. Take notes and review them later to help you remember!</p>
        </div>""")
    else:
        sections.append(f"""
        <div class="step-card">
            <span class="step-num">1</span>
            <strong>Introduction to {en}</strong>
            <p>This lesson introduces the core ideas you need to know.</p>
        </div>
        <div class="step-card">
            <span class="step-num">2</span>
            <strong>Key Ideas</strong>
            <p>Learn the most important concepts step by step.</p>
        </div>
        <div class="step-card">
            <span class="step-num">3</span>
            <strong>Practice and Apply</strong>
            <p>Try what you have learned with fun activities.</p>
        </div>""")

    # -- Key Concepts --
    sections.append(f'<div class="section-title">💡 Key Concepts</div>')
    concept_text = f"This section covers the most important ideas in {en} for {grade_label}. Read each idea carefully and think about how it connects to what you already know."
    if weeks:
        concept_text = f"This section covers the following topics: {', '.join(weeks[:3])}. Master each topic before moving to the next one."
    sections.append(f"<p>{concept_text}</p>")

    sections.append(f'<div class="definition-box">')
    sections.append(f"<strong>{en}</strong> — {desc or f'{en} is the study of important ideas that help us understand the world around us.'}")
    sections.append(f'</div>')

    sections.append(f'<div class="example-box">')
    if melc_list:
        sections.append(f"<strong>Example Skill:</strong> {melc_list[0]}")
    else:
        sections.append(f"<strong>Example:</strong> Practicing {en} helps you think critically and solve problems in everyday life.")
    sections.append(f'</div>')

    sections.append(f'<div class="tip-box">')
    sections.append("<strong>Study Tip:</strong> Read each section slowly. If something is confusing, read it again or ask for help. You've got this!")
    sections.append(f'</div>')

    # Key Concepts from study_guide
    if sg and sg.get("key_concepts"):
        sections.append(f'<div class="subsection-title">📌 Key Points to Remember</div>')
        sections.append("<ul class='key-points'>")
        for kc in sg["key_concepts"]:
            sections.append(f"<li>{kc}</li>")
        sections.append("</ul>")

    # Visual aid for the concepts section (for older grades, a lighter touch)
    if not is_early:
        sections.append(_build_visual_images(grade_num, subject, difficulty, count=1))

    # Summary
    if sg and sg.get("summary"):
        sections.append(f'<div class="section-title">📝 Summary</div>')
        sections.append(f'<div class="definition-box">{sg["summary"]}</div>')

    # Review Questions
    if sg and sg.get("review_questions"):
        sections.append(f'<div class="section-title">❓ Review Questions</div>')
        sections.append("<p>Test yourself! Try to answer these without looking back at the lesson:</p>")
        for i, qq in enumerate(sg["review_questions"]):
            sections.append(f'<div class="step-card"><span class="step-num">{i+1}</span> <strong>Question:</strong> {qq}</div>')
        sections.append(f'<div class="tip-box">💡 Say your answers out loud — research shows it helps you remember better!</div>')
        if heavy_visuals:
            sections.append(_build_visual_images(grade_num, subject, difficulty, count=1))

    # Practice Exercises
    sections.append(f'<div class="section-title">✏️ Practice Exercises</div>')
    if heavy_visuals:
        sections.append(_build_visual_images(grade_num, subject, difficulty, count=1))
    sections.append(f'<div class="exercise-box">')
    if exercises:
        for i, ex in enumerate(exercises[:5]):
            sections.append(f"<p><strong>{i+1}.</strong> {ex}</p>")
    else:
        sections.append("<p><strong>1.</strong> Write down three new things you learned in this lesson.</p>")
        sections.append("<p><strong>2.</strong> Give one example of how this applies to your daily life.</p>")
        sections.append("<p><strong>3.</strong> Explain what you learned to a friend or family member.</p>")
        sections.append("<p><strong>4.</strong> Draw or describe something that represents this topic.</p>")
        sections.append("<p><strong>5.</strong> Write one question you still have — then try to find the answer!</p>")
    sections.append("</div>")

    # Motivation footer
    sections.append(f'<div class="progress-dots">')
    for i in range(5):
        sections.append(f'<span class="dot active"></span>')
    sections.append('</div>')
    sections.append("<p style='text-align:center;font-size:16px;color:#666;'>\u2b50 You worked hard on this lesson! Keep it up! \u2b50</p>")

    qtitle_full = _get_quarter_title(subject, quarter_idx)
    content = "\n".join(sections)
    title = f"{grade_label} — {en} — {qtitle_full}"
    return _student_wrap_html(content, title, subject, difficulty, grade_num)


# --------------- Lesson content generators ---------------

def _get_quarter_title(subject, quarter_idx):
    """Get a descriptive title for a quarter's content."""
    qnames = ["First Quarter", "Second Quarter", "Third Quarter", "Fourth Quarter"]
    return qnames[quarter_idx] if quarter_idx < 4 else f"Quarter {quarter_idx + 1}"


def _full_lesson(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    emoji = info["emoji"]
    is_early = isinstance(grade_num, int) and grade_num <= 4

    sections = []
    qtitle = _get_quarter_title(subject, quarter_idx)
    std = _quarter_standards(grade_num, subject, quarter_idx)
    desc = _quarter_description(grade_num, subject, quarter_idx)
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)
    melc_list = _quarter_melcs(grade_num, subject, quarter_idx)
    exercises = _quarter_exercises(grade_num, subject, quarter_idx)
    answers = _quarter_answers(grade_num, subject, quarter_idx)

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">{qtitle}</div>')
    sections.append(f"<p>{desc or f'This quarter covers essential concepts in {en} for {grade_label}.'}</p>")

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Content Standards</div>')
    sections.append(f"<p>{std or f'The learner demonstrates understanding of key concepts in {en}.'}</p>")

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Most Essential Learning Competencies (MELCs)</div>')
    sections.append("<ul class='key-points'>")
    if melc_list:
        for m in melc_list:
            sections.append(f"<li>{m}</li>")
    else:
        sections.append(f"<li>Understand and apply core concepts of {en}</li>")
        sections.append(f"<li>Develop skills relevant to {grade_label} level</li>")
        sections.append(f"<li>Demonstrate understanding through various activities</li>")
    sections.append("</ul>")

    if is_early:
        sections.append(_build_visual_images(grade_num, subject, difficulty))

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Lesson Content</div>')

    if weeks:
        for i, week in enumerate(weeks[:5]):
            sections.append(f"""
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">{i+1}</span>
            <strong>{week}</strong>
            <p>Explore this topic through guided activities and examples.</p>
        </div>
        """.replace("VAR_COLOR", info["color"]))
    elif is_early:
        sections.append("""
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">1</span>
            <strong>Let's Learn Together!</strong>
            <p>In this lesson, we will explore important ideas step by step.</p>
        </div>
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">2</span>
            <strong>Key Concepts</strong>
            <p>Understanding these ideas will help you in everyday life.</p>
        </div>
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">3</span>
            <strong>Let's Practice!</strong>
            <p>Now it's time to try it yourself.</p>
        </div>
        """.replace("VAR_COLOR", info["color"]))
    else:
        sections.append(f"""
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">1</span>
            <strong>Overview of {en}</strong>
            <p>This lesson covers the core topics for {grade_label}.</p>
        </div>
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">2</span>
            <strong>Deep Dive</strong>
            <p>Study each concept carefully with the provided examples.</p>
        </div>
        <div class="step-card" style="border-color:VAR_COLOR;">
            <span class="step-num" style="background:VAR_COLOR;">3</span>
            <strong>Application</strong>
            <p>Apply what you've learned to solve problems.</p>
        </div>
        """.replace("VAR_COLOR", info["color"]))

    sections.append(f'<div class="subsection-title">Key Concepts</div>')
    concept_text = f"This section covers the fundamental concepts of {en} for {grade_label}. Focus on understanding each idea before moving to the next."
    if weeks:
        concept_text = f"This section covers the following topics for {grade_label} {en}: {', '.join(weeks[:3])}. Master each topic before proceeding."
    sections.append(f"<p>{concept_text}</p>")

    sections.append(f'<div class="definition-box">')
    sections.append(f"<strong>{en}</strong> — {desc or f'{en} is the study and application of key principles that help us understand the world around us.'}")
    sections.append(f'</div>')

    sections.append(f'<div class="example-box">')
    if melc_list:
        sections.append(f"<strong>Example:</strong> One key skill to practice is: {melc_list[0]}")
    else:
        sections.append(f"<strong>Example:</strong> Practicing {en} helps develop critical thinking and problem-solving skills that are useful in daily life.")
    sections.append(f'</div>')

    sections.append(f'<div class="tip-box">')
    sections.append("Take your time reading each section. If you don't understand something, read it again or ask your teacher for help.")
    sections.append(f'</div>')

    sg = _quarter_study_guide(grade_num, subject, quarter_idx)
    if sg:
        sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Study Guide</div>')
        if sg.get("key_concepts"):
            sections.append(f'<div class="definition-box"><strong>Key Concepts:</strong> {", ".join(sg["key_concepts"])}</div>')
        if sg.get("summary"):
            sections.append(f'<div class="tip-box"><strong>Summary:</strong> {sg["summary"]}</div>')
        if sg.get("review_questions"):
            sections.append(f'<div class="subsection-title">Review Questions</div>')
            for i, qq in enumerate(sg["review_questions"]):
                sections.append(f'<div class="step-card" style="border-color:{info["color"]};"><span class="step-num" style="background:{info["color"]};">{i+1}</span> <strong>Study Question:</strong> {qq}</div>')
            sections.append(f'<div class="tip-box">Review these questions to strengthen your understanding. Try answering them without looking back at the lesson.</div>')

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Practice Exercises</div>')
    sections.append(f'<div class="exercise-box">')
    if exercises:
        for i, ex in enumerate(exercises[:5]):
            sections.append(f"<p><strong>Exercise {i+1}:</strong> {ex}</p>")
    else:
        sections.append("<p><strong>Exercise 1:</strong> Write down three things you learned from this lesson.</p>")
        sections.append("<p><strong>Exercise 2:</strong> Give one example of how this concept applies in real life.</p>")
        sections.append("<p><strong>Exercise 3:</strong> Discuss with a classmate what you found most interesting.</p>")
    sections.append(f'</div>')

    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    if answers:
        for a in answers[:5]:
            sections.append(f"<p>{a}</p>")
    else:
        sections.append("<p><em>Answers will vary. Discuss your responses with your teacher.</em></p>")
    sections.append(f'</div>')

    sections.append(f'<div class="progress-dots">')
    for i in range(5):
        sections.append(f'<span class="dot active" style="background:{info["color"]};"></span>')
    sections.append(f'</div>')
    sections.append('<p style="text-align:center;font-size:13px;color:#888;">Complete all steps to master this lesson!</p>')

    qtitle_full = _get_quarter_title(subject, quarter_idx)
    content = "\n".join(sections).replace("VAR_COLOR", info["color"])
    title = f"{grade_label} — {en} — {qtitle_full}"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _easy(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    is_early = isinstance(grade_num, int) and grade_num <= 4

    sections = []
    desc = _quarter_description(grade_num, subject, quarter_idx)
    melc_list = _quarter_melcs(grade_num, subject, quarter_idx)

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Quick Review — {_get_quarter_title(subject, quarter_idx)}</div>')
    sections.append(f"<p>{desc or f'A simple review of the basic ideas in {en}.'}</p>")

    if is_early:
        sections.append(_build_visual_images(grade_num, subject, difficulty))
        sections.append("""
        <div class="grid-2">
            <div class="fact-card"><span class="fc-icon">✅</span><div class="fc-label">Learn Easy</div></div>
            <div class="fact-card"><span class="fc-icon">⭐</span><div class="fc-label">Practice</div></div>
        </div>
        """)

    sections.append(f'<div class="subsection-title">Basic Concepts</div>')
    sections.append(f"<p>Here are the easiest ideas to remember about {en}:</p>")
    sections.append("<ul>")
    sections.append("<li>Understanding starts with the basics</li>")
    sections.append("<li>Practice makes learning easier</li>")
    sections.append("<li>Ask questions when something is unclear</li>")
    if melc_list:
        sections.append(f"<li>Key skill: {melc_list[0]}</li>")
    sections.append("</ul>")

    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Quick Practice:</strong> Write one sentence about what you learned.</p>")
    sections.append(f'</div>')

    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Compare your answer with a classmate or ask your teacher.</em></p>")
    sections.append(f'</div>')

    content = "\n".join(sections)
    title = f"{grade_label} — {en} (Easy)"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _medium(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)
    desc = _quarter_description(grade_num, subject, quarter_idx)

    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Intermediate Concepts — {_get_quarter_title(subject, quarter_idx)}</div>')
    sections.append(f"<p>{desc or f'Building on the basics of {en} with more detailed explanations.'}</p>")
    sections.append(f'<div class="step-card" style="border-color:{info["color"]};">')
    sections.append("<strong>Key Idea:</strong> Apply what you already know to understand new topics.")
    sections.append("</div>")

    if weeks:
        sections.append("<ul>")
        for w in weeks[:4]:
            sections.append(f"<li>{w}</li>")
        sections.append("</ul>")

    sections.append(f'<div class="example-box">')
    sections.append(f"<strong>Example:</strong> In {en}, connecting new ideas to familiar ones helps you learn faster.")
    sections.append("</div>")
    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Exercise:</strong> Write two examples of this concept in action.</p>")
    sections.append("</div>")
    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Sample answers are available from your teacher.</em></p>")
    sections.append("</div>")
    content = "\n".join(sections)
    title = f"{grade_label} — {en} (Medium)"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _hard(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)
    melc_list = _quarter_melcs(grade_num, subject, quarter_idx)

    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Advanced Study — {_get_quarter_title(subject, quarter_idx)}</div>')
    sections.append(f"<p>Challenging concepts in {en} for deeper understanding.</p>")
    sections.append(f'<div class="warning-box">This section contains advanced topics. Make sure you understand the basics first.</div>')
    sections.append(f'<div class="step-card" style="border-color:{info["color"]};">')
    sections.append("<strong>Challenge:</strong> Try to solve problems using multiple steps.")
    sections.append("</div>")

    if melc_list:
        sections.append("<p><strong>Advanced MELCs to master:</strong></p><ul>")
        for m in melc_list:
            sections.append(f"<li>{m}</li>")
        sections.append("</ul>")

    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Challenge Exercise:</strong> Solve the following and explain your reasoning.</p>")
    if weeks:
        sections.append(f"<p>Topic focus: {weeks[0] if weeks else 'Core concepts'}</p>")
    sections.append("</div>")
    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Ask your teacher to check your work.</em></p>")
    sections.append("</div>")
    content = "\n".join(sections)
    title = f"{grade_label} — {en} (Hard)"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _practice(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    is_early = isinstance(grade_num, int) and grade_num <= 4
    exercises = _quarter_exercises(grade_num, subject, quarter_idx)
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)

    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Practice Worksheet — {_get_quarter_title(subject, quarter_idx)}</div>')
    sections.append(f"<p>Practice what you've learned in {en}.</p>")
    sections.append(f'<div class="exercise-box">')

    if exercises:
        for i, ex in enumerate(exercises[:5]):
            sections.append(f"<p><strong>{i+1}.</strong> {ex}</p>")
    else:
        sections.append("<p><strong>1.</strong> What is the most important thing you learned?</p>")
        sections.append("<p><strong>2.</strong> How does this connect to what you already know?</p>")
        sections.append(f'{"<p><strong>3.</strong> Draw or describe a real-life example.</p>" if is_early else "<p><strong>3.</strong> Provide a detailed real-world application.</p>"}')
        sections.append("<p><strong>4.</strong> Write one question you still have about this topic.</p>")
        sections.append("<p><strong>5.</strong> Explain this concept to a friend in your own words.</p>")
    sections.append("</div>")

    if weeks:
        sections.append(f'<div class="tip-box">Focus on these topics: {", ".join(weeks[:3])}</div>')

    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Answers will vary. Discuss with your teacher.</em></p>")
    sections.append("</div>")
    content = "\n".join(sections)
    title = f"{grade_label} — {en} (Practice)"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _full_assessment(grade_num, grade_label, subject, difficulty, quarter_idx=0):
    info = SUBJECT_INFO.get(subject, {"emoji": "📖", "color": "#333", "name_en": subject, "name_tl": subject})
    en = info["name_en"]
    assessment = _quarter_assessment(grade_num, subject, quarter_idx)
    answers = _quarter_answers(grade_num, subject, quarter_idx)
    weeks = _quarter_weeks(grade_num, subject, quarter_idx)

    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Full Assessment — {_get_quarter_title(subject, quarter_idx)}</div>')
    sections.append(f"<p>Test your understanding of {en}.</p>")
    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Part I — Multiple Choice</strong></p>")

    if assessment:
        for i, item in enumerate(assessment[:5]):
            sections.append(f"<p>{i+1}. {item}</p>")
    else:
        sections.append("<p>1. Which of the following best describes the main concept of this lesson?</p>")
        sections.append("<p>2. How does this topic relate to everyday life?</p>")
        sections.append("<p>3. What is one skill you developed from studying this topic?</p>")
    sections.append("</div>")

    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>Part II — Written Response</strong></p>")
    sections.append("<p>Answer in 2-3 sentences.</p>")
    sections.append("<p>4. Explain the most important idea from this lesson in your own words.</p>")
    sections.append("<p>5. Describe a situation where you could use what you learned.</p>")
    if weeks:
        sections.append(f"<p><em>Topic reference: {weeks[0]}</em></p>")
    sections.append("</div>")

    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    if answers:
        for a in answers[:5]:
            sections.append(f"<p>{a}</p>")
    else:
        sections.append("<p><em>Discuss your answers with your teacher for feedback.</em></p>")
    sections.append("</div>")
    content = "\n".join(sections)
    title = f"{grade_label} — {en} (Full Assessment)"
    return _wrap_html(content, title, subject, difficulty, grade_num)


GENERATORS = {
    "Full Lesson": _full_lesson,
    "Easy": _easy,
    "Medium": _medium,
    "Hard": _hard,
    "Practice": _practice,
    "Full Assessment": _full_assessment,
}


# --------------- SHS generators ---------------

def _shs_full_lesson(grade_num, grade_label, subject, difficulty, shs_info):
    info = shs_info
    en = info["name_en"]
    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Content Standards</div>')
    sections.append(f"<p>The learner demonstrates understanding of key concepts in {en} at the senior high school level.</p>")

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Learning Competencies</div>')
    sections.append("<ul class='key-points'>")
    sections.append(f"<li>Analyze core theories and principles of {en}</li>")
    sections.append(f"<li>Apply concepts to real-world scenarios</li>")
    sections.append(f"<li>Demonstrate critical thinking through problem-solving</li>")
    sections.append("</ul>")

    sections.append(f'<div class="subsection-title">Key Concepts</div>')
    sections.append(f"<p>{en} covers foundational and advanced topics that prepare learners for higher education and career pathways.</p>")

    sections.append(f'<div class="definition-box">')
    sections.append(f"<strong>{en}</strong> — A subject under the Senior High School curriculum designed to develop competencies aligned with CHED standards.")
    sections.append('</div>')

    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">Exercises</div>')
    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>1.</strong> Summarize the main objective of this subject.</p>")
    sections.append("<p><strong>2.</strong> Identify three real-world applications.</p>")
    sections.append("<p><strong>3.</strong> Prepare a short explanation you could present to the class.</p>")
    sections.append("</div>")

    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Evaluate your responses using the rubric provided by your teacher.</em></p>")
    sections.append("</div>")

    content = "\n".join(sections)
    title = f"{grade_label} — {en}"
    return _wrap_html(content, title, subject, difficulty, grade_num)


def _shs_generic(grade_num, grade_label, subject, difficulty, shs_info, level_name):
    info = shs_info
    en = info["name_en"]
    sections = []
    sections.append(f'<div class="section-title" style="border-color:{info["color"]};">{level_name}</div>')
    sections.append(f"<p>Reinforce your understanding of {en}.</p>")
    sections.append(f'<div class="exercise-box">')
    sections.append("<p><strong>1.</strong> Define the key concept in your own words.</p>")
    sections.append("<p><strong>2.</strong> Give an example of how this is applied.</p>")
    sections.append("<p><strong>3.</strong> What questions do you still have?</p>")
    sections.append("</div>")
    sections.append(f'<div class="answer-key">')
    sections.append("<h4>Answer Key</h4>")
    sections.append("<p><em>Discuss your answers with your teacher.</em></p>")
    sections.append("</div>")
    content = "\n".join(sections)
    title = f"{grade_label} — {en} ({level_name})"
    return _wrap_html(content, title, subject, difficulty, grade_num)


# --------------- File generation ---------------

def generate_for_grade(grade_num, grade_folder, subjects):
    """Generate all visual lesson HTML files for one grade level, one file per quarter."""
    is_early = grade_num <= 4
    grade_label = grade_folder.replace("_", " ").title()
    if grade_label.startswith("00 "):
        grade_label = "Kindergarten"
    elif grade_label.startswith("0"):
        grade_label = f"Grade {grade_num}"

    grade_dir = os.path.join(VISUAL_DIR, grade_folder)
    os.makedirs(grade_dir, exist_ok=True)

    total_files = 0
    for subject_base in subjects:
        for qi in range(4):
            qname = QUARTER_NAMES[qi].replace(" ", "_")
            for diff in DIFFICULTIES:
                gen = GENERATORS.get(diff)
                if not gen:
                    continue

                html = gen(grade_num, grade_label, subject_base, diff, qi)
                suffix = "" if diff == "Full Lesson" else f"_{diff.replace(' ', '_')}"
                fname = f"{subject_base}_{qname}{suffix}.html"
                fpath = os.path.join(grade_dir, fname)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)
                total_files += 1

    print(f"  Generated {total_files} files for {grade_label} (4 quarters x {len(subjects)} subjects x {len(DIFFICULTIES)} difficulties)")


def generate_shs_level(grade_num, grade_folder, strands):
    """Generate SHS visual lesson HTML files."""
    for strand_name, subjects in strands:
        for subject_base in subjects:
            shs_info = SHS_SUBJECT_INFO.get(subject_base, {"emoji": "📖", "color": "#555", "name_en": subject_base.replace("_", " "), "name_tl": subject_base.replace("_", " ")})
            strand_label = strand_name.replace("_", " ").title()
            strand_label = strand_label.replace("S T E M", "STEM").replace("A B M", "ABM")
            strand_label = strand_label.replace("G A S", "GAS").replace("H U M S S", "HUMSS").replace("T V L", "TVL")
            grade_label = f"Grade {grade_num} SHS — {strand_label}"
            subject_en = shs_info["name_en"].replace("_", " ")
            grade_dir = os.path.join(VISUAL_DIR, grade_folder, strand_name)
            os.makedirs(grade_dir, exist_ok=True)

            for diff in DIFFICULTIES:
                if diff == "Full Lesson":
                    html = _shs_full_lesson(grade_num, grade_label, subject_base, diff, shs_info)
                else:
                    html = _shs_generic(grade_num, grade_label, subject_base, diff, shs_info, diff)

                suffix = "" if diff == "Full Lesson" else f"_{diff.replace(' ', '_')}"
                fname = f"{subject_base}{suffix}.html"
                fpath = os.path.join(grade_dir, fname)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)

    total = sum(len(s) for _, s in strands) * len(DIFFICULTIES)
    print(f"  Generated {total} files for Grade {grade_num} SHS")


def generate_all():
    os.makedirs(VISUAL_DIR, exist_ok=True)
    _load_quarter_content()

    grade_map = {
        "00_Kindergarten": (0, [
            "Cognitive_Development", "Aesthetic_Creative_Development",
            "Language_Literacy_Communication", "Mathematics",
            "Physical_Health_Motor_Development", "Socio_emotional_Development",
            "Values_Development"
        ]),
        "01_Grade_1": (1, ["GMRC", "Language", "Makabansa", "Mathematics", "Reading_and_Literacy"]),
        "02_Grade_2": (2, ["English", "Filipino", "GMRC", "Makabansa", "Mathematics"]),
        "03_Grade_3": (3, ["English", "Filipino", "GMRC", "Makabansa", "Mathematics", "Science"]),
        "04_Grade_4": (4, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "05_Grade_5": (5, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "06_Grade_6": (6, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "07_Grade_7": (7, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "08_Grade_8": (8, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "09_Grade_9": (9, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "10_Grade_10": (10, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
    }

    for folder, (gnum, subjects) in grade_map.items():
        label = "Kindergarten" if gnum == 0 else f"Grade {gnum}"
        print(f"\nGenerating {label}...")
        if gnum == 0:
            # Kindergarten uses special generator
            generate_kindergarten(folder, subjects)
        else:
            generate_for_grade(gnum, folder, subjects)

    # SHS Grades
    strand_map = {
        "Core_Subjects": [
            "21st_Century_Literature", "Contemporary_Philippine_Arts",
            "Disaster_Readiness_Risk_Reduction", "Earth_and_Life_Science",
            "Earth_Science", "General_Mathematics", "Introduction_to_Philosophy",
            "Komunikasyon_at_Pananaliksik", "Media_and_Information_Literacy",
            "Oral_Communication", "Personal_Development",
            "Physical_Education_and_Health", "Physical_Science",
            "Reading_and_Writing", "Statistics_and_Probability"
        ],
        "ABM_Strand": [
            "Applied_Economics", "Business_Ethics_Social_Responsibility",
            "Business_Mathematics", "Fundamentals_of_Accountancy_Business_Management_1",
            "Organization_and_Management"
        ],
        "GAS_Strand": [
            "Applied_Economics_GAS", "Disaster_Readiness_GAS",
            "Humanities_1", "Humanities_2",
            "Organization_and_Management_GAS", "Social_Science_1"
        ],
        "HUMSS_Strand": [
            "Disciplines_and_Ideas_in_Social_Sciences",
            "Philippine_Politics_and_Governance", "World_Religions_Belief_Systems"
        ],
        "STEM_Strand": [
            "Basic_Calculus", "General_Biology_1", "General_Chemistry_1", "Pre_Calculus"
        ],
        "TVL_Track": [
            "Agri_Fishery_Arts", "Home_Economics", "ICT_Track", "Industrial_Arts"
        ],
        "Arts_and_Design_Track": [
            "Media_Arts", "Performing_Arts", "Visual_Arts"
        ],
        "Sports_Track": [
            "Fitness_and_Exercise_Programming", "Sports_Officiating_and_Coaching",
            "Sports_Psychology_and_Nutrition"
        ],
        "Applied_Track": [
            "Empowerment_Technologies", "English_for_Academic_Professional_Purposes",
            "Entrepreneurship", "Filipino_sa_Piling_Larangan",
            "Inquiries_Investigations_Immersion", "Practical_Research_1",
            "Practical_Research_2"
        ],
    }

    g12_extra = {
        "ABM_Strand": [
            "Business_Enterprise_Simulation", "Business_Finance",
            "Fundamentals_of_Accountancy_Business_Management_2",
            "Principles_of_Marketing", "Work_Immersion_ABM"
        ],
        "HUMSS_Strand": [
            "Community_Engagement_Solidarity_Citizenship", "Creative_Nonfiction",
            "Creative_Writing", "Disciplines_and_Ideas_in_Applied_Social_Sciences",
            "Trends_Networks_Critical_Thinking"
        ],
        "STEM_Strand": [
            "General_Biology_2", "General_Chemistry_2",
            "General_Physics_1", "General_Physics_2",
            "Research_Project_STEM", "Work_Immersion_STEM"
        ],
    }

    print("\nGenerating Grade 11 SHS...")
    g11_strands = [(sn, subs) for sn, subs in strand_map.items()]
    generate_shs_level(11, "11_Grade_11_SHS", g11_strands)

    print("\nGenerating Grade 12 SHS...")
    g12_strands = []
    for sn, subs in strand_map.items():
        extra = g12_extra.get(sn, [])
        if extra:
            g12_strands.append((sn, extra))
        else:
            g12_strands.append((sn, subs))
    generate_shs_level(12, "12_Grade_12_SHS", g12_strands)

    print(f"\n{'='*50}")
    print(f"All visual lessons generated in: {VISUAL_DIR}")


def generate_student_grade(grade_num, grade_folder, subjects):
    """Generate student-friendly HTML files for one grade level."""
    grade_label = grade_folder.replace("_", " ").title()
    if grade_label.startswith("00 "):
        grade_label = "Kindergarten"
    elif grade_label.startswith("0"):
        grade_label = f"Grade {grade_num}"

    grade_dir = os.path.join(STUDENT_VISUAL_DIR, grade_folder)
    os.makedirs(grade_dir, exist_ok=True)

    total_files = 0
    for subject_base in subjects:
        for qi in range(4):
            qname = QUARTER_NAMES[qi].replace(" ", "_")
            html = _student_lesson(grade_num, grade_label, subject_base, "Full Lesson", qi)
            fname = f"{subject_base}_{qname}.html"
            fpath = os.path.join(grade_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)
            total_files += 1

    print(f"  Generated {total_files} student files for {grade_label}")


def generate_all_student():
    """Generate all student-friendly lesson HTML files into Visual_Lessons_Student/."""
    os.makedirs(STUDENT_VISUAL_DIR, exist_ok=True)
    _load_quarter_content()

    grade_map = {
        "00_Kindergarten": (0, [
            "Cognitive_Development", "Aesthetic_Creative_Development",
            "Language_Literacy_Communication", "Mathematics",
            "Physical_Health_Motor_Development", "Socio_emotional_Development",
            "Values_Development"
        ]),
        "01_Grade_1": (1, ["GMRC", "Language", "Makabansa", "Mathematics", "Reading_and_Literacy"]),
        "02_Grade_2": (2, ["English", "Filipino", "GMRC", "Makabansa", "Mathematics"]),
        "03_Grade_3": (3, ["English", "Filipino", "GMRC", "Makabansa", "Mathematics", "Science"]),
        "04_Grade_4": (4, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "05_Grade_5": (5, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "06_Grade_6": (6, ["Araling_Panlipunan", "English", "EPP_TLE", "Filipino", "GMRC", "Mathematics", "Music_and_Arts", "PE_and_Health", "Science"]),
        "07_Grade_7": (7, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "08_Grade_8": (8, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "09_Grade_9": (9, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
        "10_Grade_10": (10, ["Araling_Panlipunan", "English", "Filipino", "MAPEH", "Mathematics", "Science", "TLE", "Values_Education"]),
    }

    for folder, (gnum, subjects) in grade_map.items():
        label = "Kindergarten" if gnum == 0 else f"Grade {gnum}"
        print(f"\nGenerating student {label}...")
        generate_student_grade(gnum, folder, subjects)

    print(f"\n{'='*50}")
    print(f"All student lessons generated in: {STUDENT_VISUAL_DIR}")


def generate_kindergarten(folder, subjects):
    """Generate kindergarten visual lesson files using development domain content."""
    grade_dir = os.path.join(VISUAL_DIR, folder)
    os.makedirs(grade_dir, exist_ok=True)
    for subject_base in subjects:
        for diff in DIFFICULTIES:
            html = _kindergarten_content(0, subject_base, diff, True)
            suffix = "" if diff == "Full Lesson" else f"_{diff.replace(' ', '_')}"
            fname = f"{subject_base}{suffix}.html"
            fpath = os.path.join(grade_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)
    print(f"  Generated {len(subjects)} x {len(DIFFICULTIES)} = {len(subjects)*len(DIFFICULTIES)} files for Kindergarten")


if __name__ == "__main__":
    generate_all()
    generate_all_student()
