#-*- coding:utf-8 -*-
from os import system
from sh import awk, grep, cat

def get_commit_files(file_type):
  system("git diff --cached --name-status > /tmp/git_hook")

  files = awk(
    grep(
     cat("/tmp/git_hook"), "-P", "(A|M).*.%s$" % file_type,
     _ok_code = [0, 1]
    ), "{print $2}", _iter = True
  )

  if not files:
    return None

  exten = ".%s" % file_type
  return [path[:path.rindex(exten) + len(exten)] for path in files]
