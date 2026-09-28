# Copy an aapt2-linked base.apk, inject classes.dex and assets/www, preserving
# STORED compression for resources.arsc / AndroidManifest.xml (zipalign-safe).
import os, shutil, sys, zipfile

BASE = sys.argv[1]
DEX = sys.argv[2]
WEB = sys.argv[3]
OUT = sys.argv[4]

with zipfile.ZipFile(OUT, "w") as zout:
    with zipfile.ZipFile(BASE, "r") as zin:
        for info in zin.infolist():
            data = zin.read(info.filename)
            # keep .arsc and manifest uncompressed for alignment
            if info.filename in ("resources.arsc", "AndroidManifest.xml"):
                info.compress_type = zipfile.ZIP_STORED
            else:
                info.compress_type = info.compress_type
            zout.writestr(info, data)
    zout.write(DEX, "classes.dex", zipfile.ZIP_DEFLATED)
    for root, _dirs, files in os.walk(WEB):
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, WEB).replace("\\", "/")
            zout.write(full, "assets/www/" + rel, zipfile.ZIP_DEFLATED)
print("pack", OUT, "entries added")