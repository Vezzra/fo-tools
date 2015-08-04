#!/usr/bin/python


import sys
from subprocess import check_output


if len(sys.argv) != 3:
    print "Usage: filter_cherry_pick.py <branch-to-cherry-pick-from> <branch-to-cherry-pick-into>"
    quit()

for sha in check_output(["git", "rev-list", "--cherry-pick", "--left-only", "--no-merges",
                         "%s...%s" % (sys.argv[1], sys.argv[2])]).splitlines():
    author = check_output(["git", "show", "-s", r"--format=%an", sha]).strip(" \n")
    msg = check_output(["git", "show", "-s", r"--format=%s", sha]).strip(" \n")
    print "%s   %s [%s]" % (sha[:7], msg[:50], author)
