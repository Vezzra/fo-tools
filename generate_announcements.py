#!/usr/bin/python


import sys
import os
from string import Template
from datetime import datetime
from subprocess import check_output


announcement_template = Template('''==========
New test build (build ${buildno}) available for Windows on sourceforge.

[url=http://sourceforge.net/projects/freeorion/files/FreeOrion/Test/FreeOrion_${buildno}_Test_Win32_Setup.exe/download]Download link for full installer.[/url]

[url=http://sourceforge.net/projects/freeorion/files/FreeOrion/Test/FreeOrion_${buildno}_Test_Win32_BinariesOnly.zip/download]Download link for zip archive with binaries only.[/url]
==========
New test build (build ${buildno}) available for macOS 10.12 and later on sourceforge.

[url=http://sourceforge.net/projects/freeorion/files/FreeOrion/Test/FreeOrion_${buildno}_MacOSX_10.12.dmg/download]Download link.[/url]
==========
New test builds available for Windows and macOS (build ${buildno}):
https://sourceforge.net/projects/freeorion/files/FreeOrion/Test/
==========
''')


build_no = "XXXX"
try:
    commit = check_output(["git", "show", "-s", "--format=%h", "--abbrev=7", "HEAD"]).strip()
    timestamp = float(check_output(["git", "show", "-s", "--format=%ct", "HEAD"]).strip())
    build_no = ".".join([datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d"), commit])
except:
    print "WARNING: Can't determine build number"

print announcement_template.substitute(buildno=build_no)
