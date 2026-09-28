import os
import sys
import shutil
import datetime
import json
import zipfile


def _get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _get_study_root():
    base = _get_base_dir()
    for _ in range(4):
        candidate = os.path.join(base, "Study_Materials")
        if os.path.isdir(candidate):
            return candidate
        base = os.path.dirname(base)
    fallback = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "OLIVIA", "Study_Materials")
    if os.path.isdir(fallback):
        return fallback
    return None


def _get_cred_path():
    return os.path.join(_get_base_dir(), "credentials.json")


def create_backup():
    backup_dir = os.path.join(_get_base_dir(), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(backup_dir, f"olivia_backup_{ts}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        study_root = _get_study_root()
        if study_root:
            for root, dirs, files in os.walk(study_root):
                for f in files:
                    if f.endswith(".md"):
                        fp = os.path.join(root, f)
                        arcname = os.path.relpath(fp, os.path.dirname(study_root))
                        zf.write(fp, arcname)
    return zip_path


def list_backups():
    backup_dir = os.path.join(_get_base_dir(), "backups")
    if not os.path.isdir(backup_dir):
        return []
    backups = []
    for f in sorted(os.listdir(backup_dir), reverse=True):
        if f.endswith(".zip"):
            fp = os.path.join(backup_dir, f)
            size = os.path.getsize(fp)
            ts = f.replace("olivia_backup_", "").replace(".zip", "")
            backups.append({"file": f, "path": fp, "size": size, "timestamp": ts})
    return backups


def restore_backup(zip_path):
    backup_dir = os.path.join(_get_base_dir(), "restored")
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    os.makedirs(backup_dir)
    with zipfile.ZipFile(zip_path, "r") as zf:
        for entry in zf.infolist():
            name = entry.filename.replace("\\", "/")
            if ".." in name.split("/") or name.startswith("/"):
                continue
            zf.extract(entry, backup_dir)
    return backup_dir
