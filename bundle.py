#! /usr/bin/env python3

## THIS IS JUST SOME LAZY CODE TO GET THE JOB DONE
## PLEASE DON'T HURT ME

from os import path, listdir, chdir, getcwd, rename, makedirs
from subprocess import call
from re import match

GIT_URL_RE = r"https?:\/\/([\w.-]+)\/([\w-]+)\/([\w-]+)"
CWD = getcwd()

# (url, author, repo)
repo_list = []

with open("repo_list.txt") as fp:
    for line in fp.readlines():
        line = line.strip()

        if not line:
            continue

        m = match(GIT_URL_RE, line)

        if not m:
            continue

        # Add a new tuple and make a new url that's guaranteed
        repo_list.append(("https://{}/{}/{}".format(*m.groups()), m.groups()[1], m.groups()[2]))


for repo in repo_list:
    call("git clone {} {}.{}".format(*repo))

makedirs("bundles", exist_ok=True)

for item in listdir():
    if path.isfile(item) or item == "bundles":
        continue

    # Enter repo dir
    chdir(item)

    # bundle and move the resulting file
    call("git bundle create self.bundle --all")
    rename("self.bundle", path.join(CWD, "bundles", item + ".bundle"))

    # exit repo
    chdir(CWD)
