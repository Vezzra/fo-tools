#!/usr/bin/python


import sys
from os import getcwd, chdir, remove
from os.path import exists
from shutil import rmtree
from subprocess import check_call, check_output


EXCLUDE_ITEMS = [
    r"Installer/*",
    r"msvc2010/*",
    r"msvc2013/*",
    r"msvc2015/*",
    r"Xcode/*",
    r".git/*",
    r".*",
    r"*.pyc",
]
WC_DIR = "src-tarball"


if len(sys.argv) != 2:
    print "Usage: make_src_tarball.py branch"
    exit(1)
branch = sys.argv[1]

original_dir = getcwd()
try:
    print "Cloning FO repo into '%s'..." %  WC_DIR
    check_call("git clone https://github.com/freeorion/freeorion.git %s" % WC_DIR, shell=True)
    chdir(WC_DIR)
    print "Checkout %s..." % branch
    check_call("git checkout %s" % branch, shell=True)
    print "Remove OSX specific garbage..."
    check_call("dot_clean -m .", shell=True)

    print "Determine FO version & build..."
    r = check_output(r"cmake/make_versioncpp.py . CMake", shell=True)
    print r
    build_no = r.splitlines()[-1].split(" ")[-1]
    fname = "FreeOrion_" + build_no + "_Source.tar.gz"

    cmd = ["tar", "-czf", fname]
    for exclude_item in EXCLUDE_ITEMS:
        cmd.append("--exclude='" + exclude_item + "'")
    cmd.append(getcwd().split(r"/")[-1])

    chdir("..")
    if exists(fname):
        print "Delete existing '%s'..." %fname
        remove(fname)
    print "Create source tarball '%s'..." % fname
    r = check_output(" ".join(cmd), shell=True)
    print r

finally:
    chdir(original_dir)
    if exists(WC_DIR):
        print "Removing temporary folder '%s'..." % WC_DIR
        rmtree(WC_DIR)
