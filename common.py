#-*- coding:utf-8 -*-
from os import system
from sh import awk, grep, cat, mkdir, rm
from config import config

def create_tmp_dir():
  tmp_dir = config.get("receive", "TMP_DIR")
  if tmp_dir:
    mkdir("-p", tmp_dir)

  return tmp_dir

def remove_tmp_dir():
  tmp_dir = config.get("receive", "TMP_DIR")
  if tmp_dir:
    rm("-rf", tmp_dir)

def get_commit_files(file_type):
  system("git diff --cached --name-status > /tmp/git_hook")
  return _get_files(file_type, 2)

def get_receive_files(rev_old, rev_new, file_type):
  system("git diff-tree -r %s..%s > /tmp/git_hook" % (rev_old, rev_new))
  return _get_files(file_type, 6)

def _get_files(file_type, file_index):
  files = awk(
    grep(
      cat("/tmp/git_hook"), "-P", "(A|M).*.%s$" % file_type,
      _ok_code = [0, 1]
    ),
    "{print $%s}" % file_index, _iter = True
  )

  if not files:
    return None

  exten = ".%s" % file_type
  return [path[:path.rindex(exten) + len(exten)] for path in files]
