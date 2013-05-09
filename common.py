#-*- coding:utf-8 -*-
from os import path, system
from sh import awk, grep, cat, mkdir, rm
from termcolor import colored
from config import config, except_paths

def get_commit_errors(file_type, function):
  checkable = True
  if file_type == "js":
    checkable = config.getboolean("commit", "CHECK_JAVASCRIPT")
  elif file_type == "php":
    checkable = config.getboolean("commit", "CHECK_PHP")

  if not checkable:
    return None

  files = _get_commit_files(file_type)
  if not files:
    return None

  errors = []
  for path in files:
    file_error = function(path)
    if file_error:
      errors.append(file_error)

  if errors:
    errors = colored(
      "There are some errors in below %s files:\n\n" % file_type, "magenta"
    ) + "\n".join(errors).strip("\n")

  return errors

def get_receive_errors(rev_old, rev_new, file_type, function):
  checkable = True
  if file_type == "js":
    checkable = config.getboolean("receive", "CHECK_JAVASCRIPT")
  elif file_type == "php":
    checkable = config.getboolean("receive", "CHECK_PHP")

  files = _get_receive_files(rev_old, rev_new, file_type)
  if not files:
    return None

  tmp_dir = config.get("receive", "TMP_DIR")
  errors = []
  for path in files:
    mkdir("-p", "/".join((tmp_dir + path).split("/")[:-1]))
    system("git show %s:%s > %s" % (rev_new, path, tmp_dir + path))
    file_error = function(tmp_dir + path)
    if file_error:
      errors.append(path + file_error)

  rm("-rf", tmp_dir)
  return "\n".join(errors)

def _get_commit_files(file_type):
  system("git diff --cached --name-status > /tmp/git_hook")
  return _get_files(file_type, 2)

def _get_receive_files(rev_old, rev_new, file_type):
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
  files = [file_path[:file_path.rindex(exten) + len(exten)] for file_path in files]
  files = [file_path for file_path in files if path.exists(file_path)]
  if except_paths:
    for except_path in except_paths:
      for file_path in files:
        if file_path.startswith(except_path):
          files.remove(file_path)

  return files
