#!/usr/bin/env python3
# Local build version: uses stdlib plistlib (no pyobjc dependency).
# Original relied on /Library/Frameworks/Python 3.9 + pyobjc.

import os
import sys
import time
import subprocess

import plistlib

if os.environ["CONFIGURATION"] == "Development":
    cmd = "git log -1 --format=\"%H\""
    output = subprocess.check_output(cmd, shell=True).decode("utf-8")

    revision = "git.unknown"
    for line in output.split("\n"):
        if len(line.strip()) > 0:
            revision = "git." + line.strip()[:10]
            break

elif os.environ["CONFIGURATION"] == "Nightly":
    revision = time.strftime("%Y%m%d-nightly")
else:
    revision = time.strftime("%Y%m%d")
version = open("version.txt").read().strip() % {"extra": revision}


def update(path):
    print("Updating versions:", path, version)
    try:
        with open(path, "rb") as f:
            plist = plistlib.load(f)
    except Exception as e:
        print(f"WARNING - FAILED TO LOAD PLIST from {path}: {e}")
        return
    plist["CFBundleShortVersionString"] = version
    plist["CFBundleGetInfoString"] = version
    plist["CFBundleVersion"] = version
    with open(path, "wb") as f:
        plistlib.dump(plist, f)


srcDir = os.environ["SRCROOT"]
print(f"SRCROOT={srcDir}")

path = os.path.join(srcDir, "plists", "iTerm2.plist")

update(path)
