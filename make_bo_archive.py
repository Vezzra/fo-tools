import sys
import os
from datetime import datetime
from subprocess import check_output
from zipfile import ZipFile, ZIP_DEFLATED


os.chdir(os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), "FreeOrion")))

build_no = "XXXX"
try:
    commit = str(check_output(["git", "show", "-s", "--format=%h", "--abbrev=7", "HEAD"]).decode()).strip()
    timestamp = float(check_output(["git", "show", "-s", "--format=%ct", "HEAD"]).strip())
    build_no = ".".join([datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d"), commit])
except:
    print("WARNING: git not installed, can't determine build number")

out_dir = os.path.dirname(sys.argv[0])
out_file = "FreeOrion_%s_Test_Win32_BinariesOnly.zip" % build_no
out_path = os.path.join(out_dir, out_file)
if os.path.exists(out_file):
    os.remove(out_file)

in_files = [
    "FreeOrion.exe",
    "FreeOrionCA.exe",
    "FreeOrionD.exe",
    "GiGi.dll"
]

print("Creating %s in %s" % (out_file, out_dir))

with ZipFile(out_path, "w", ZIP_DEFLATED) as ar:
    for f in in_files:
        ar.write(f)
