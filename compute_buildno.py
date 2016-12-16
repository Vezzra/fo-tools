#!/usr/bin/python


from subprocess import check_output


build_no = "XXXX"
try:
    sha1 = check_output(["git", "show", "-s", "--format=%H", "HEAD"]).strip()[:4]
    count = check_output(["git", "rev-list", "--count", "HEAD"]).strip()
    build_no = ".".join([count, sha1])
except:
    print "WARNING: git not installed, can't determine build number"

print build_no
