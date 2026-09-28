import os
import sys
import shutil
import subprocess

APP_NAME = "O.L.I.V.I.A"
BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
OLIVIA_ROOT = os.path.dirname(BUILD_DIR)

DATA_DIRS = [
    "K-12_Philippine_Curriculum",
    "College_Programs",
    "K-12_Philippine_Curriculum_EN",
    "College_Programs_EN",
    "K-12_Philippine_Curriculum_TL",
    "College_Programs_TL",
    "Visual_Lessons",
    "Visual_Lessons_Student",
]

def find_icon():
    for c in ["icon.ico", "app.ico", "assets/icon.ico"]:
        p = os.path.join(BUILD_DIR, c)
        if os.path.exists(p):
            return p
    return None

def build():
    print("=" * 60)
    print(f"  Building {APP_NAME}")
    print("=" * 60)

    icon = find_icon()
    icon_args = ["--icon", icon] if icon else []

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--onedir",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--add-data", f"{BUILD_DIR}{os.pathsep}.",
        "--collect-all", "tkinterweb",
        "--collect-all", "customtkinter",
        "--collect-all", "speech_recognition",
        "--collect-all", "googlesearch",
        "--hidden-import", "deep_translator",
        "--hidden-import", "pyttsx3",
        "--hidden-import", "requests",
        "--hidden-import", "bs4",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL._tkinter_finder",
    ] + icon_args + [os.path.join(BUILD_DIR, "desktop_app.py")]

    print("\nRunning PyInstaller...\n")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print("\nBuild failed.")
        sys.exit(1)

    dist_dir = os.path.join(BUILD_DIR, "dist", APP_NAME)
    print(f"\nCopying curriculum data into dist folder...")
    for d in DATA_DIRS:
        src = os.path.join(OLIVIA_ROOT, d)
        dst = os.path.join(dist_dir, d)
        if os.path.isdir(src):
            print(f"  {d}")
            shutil.copytree(src, dst, dirs_exist_ok=True)

    print(f"\n  SUCCESS!")
    print(f"  App folder: {dist_dir}")
    print(f"  Share the entire '{APP_NAME}' folder.")
    print(f"  Run O.L.I.V.I.A.exe inside it.")

if __name__ == "__main__":
    build()
