#!/usr/bin/python


import sys
import os
import os.path
from subprocess import call, check_output
from datetime import datetime


SRC_DIR = "src"
BUILD_DIR = "build"

XCODE_PROJECT = os.path.join(BUILD_DIR, "FreeOrion.xcodeproj")
TARGET_APP = "ALL_BUILD"
TARGET_PACKAGE = "package"
BUILD_CONFIG = "Release"

DMG_NAME = "FreeOrion-0.4.10+-MacOSX_10.12.dmg"


def get_buildno(src_dir=SRC_DIR):
    try:
        os.chdir(src_dir)
        commit = check_output(["git", "show", "-s", "--format=%h", "--abbrev=7", "HEAD"]).strip()
        timestamp = float(check_output(["git", "show", "-s", "--format=%ct", "HEAD"]).strip())
        os.chdir("..")
        return ".".join([datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d"), commit])
    except:
        print "WARNING: Can't determine build number"
        return "---"


def run_cmake(src_dir=SRC_DIR, build_dir=BUILD_DIR, log_dir="log"):
    with open(os.path.join(log_dir, "cmake.log"), "w") as logfile:
        retval = call(["cmake", "-G", "Xcode", "-B%s" % build_dir, "-H%s" % src_dir, "-DGLEW_USE_STATIC_LIBS=ON", "-Wno-dev"],
                      stdout=logfile, stderr=logfile)
    return retval == 0


def run_xcodebuild(project=XCODE_PROJECT, target=TARGET_PACKAGE, config=BUILD_CONFIG, log_dir="log"):
    with open(os.path.join(log_dir, "build.log"), "w") as logfile:
        build_cmd = ["xcodebuild",
            "-project", project,
            "-target", target,
            "-configuration", config,
            'CODE_SIGN_IDENTITY=""',
            'CODE_SIGN_ENTITLEMENTS=""',
            'CODE_SIGNING_REQUIRED="NO"',
            'CODE_SIGNING_ALLOWED="NO"'
        ]
        retval = call(build_cmd, stdout=logfile, stderr=logfile)
    return retval == 0


def rename_dmg(build_dir=BUILD_DIR, build_no="---"):
    fname = "./FreeOrion_%s_Test_MacOSX_10.12.dmg" % build_no
    os.rename(os.path.join(build_dir, fname), fname)


if __name__ == "__main__":
    app_dir, app_name = os.path.split(sys.argv[0])
    app_name = os.path.splitext(app_name)[0]

    if app_name == "build_app":
        build_target = TARGET_APP
    elif app_name in ["build_package", "build"]:
        build_target = TARGET_PACKAGE
    else:
        print "Invalid script name: %s" %app_name
        exit(1)

    os.chdir(app_dir)
    build_no = get_buildno(SRC_DIR)
    print "Building commit '%s' in '%s'" % (build_no, app_dir)
    print "Build target: %s" % build_target
    print "Build configuration: %s" % BUILD_CONFIG

    log_dir = "logs_%s" % datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    os.mkdir(log_dir)

    print "Running cmake..."
    if not run_cmake(SRC_DIR, BUILD_DIR, log_dir):
        print "CMake failed"
        exit(1)

    print "Running xcodebuild..."
    if not run_xcodebuild(XCODE_PROJECT, build_target, BUILD_CONFIG, log_dir):
        print "Build failed"
        exit(1)

    if build_target == TARGET_PACKAGE:
        print "Moving and renaming DMG package..."
        rename_dmg(BUILD_DIR, build_no)

    print "DONE."
