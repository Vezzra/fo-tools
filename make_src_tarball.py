#!/usr/bin/python


from os import getcwd, chdir
from subprocess import check_output


exclude_items = [
    r"Installer/*",
    r"msvc2010/*",
    r"msvc2013/*",
    r"Xcode/*",
    r".git/*",
    r".*",
    r"*.pyc",
]


check_output(["dot_clean -m ."], shell=True)

r = check_output([r"cmake/make_versioncpp.py . CMake"], shell=True)
print r,
build_no = r.splitlines()[-1].split(" ")[-1]
fname = "FreeOrion_" + build_no + "_Source.tar.gz"

cmd = ["tar", "-czf", fname]
for exclude_item in exclude_items:
    cmd.append("--exclude='" + exclude_item + "'")
cmd.append(getcwd().split(r"/")[-1])

chdir("..")
r = check_output([" ".join(cmd)], shell=True)
print r
