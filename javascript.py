#-*- coding:utf-8 -*-
from config import config, base_path
from common import get_commit_files, get_receive_files
from common import create_tmp_dir, remove_tmp_dir
from sh import jshint, tail
from termcolor import colored
from os import system

def get_commit_errors():
  checkable = config.getboolean("commit", "CHECK_JAVASCRIPT")
  if not checkable:
    return None

  files = get_commit_files('js')
  if not files:
    return None

  errors = []
  for path in files:
    file_errors = jshint(
      "--config",
      "%s/configs/jshint.json" % base_path,
      path,  _ok_code = [0, 2]
    )
    if file_errors:
      errors.append(colored(file_errors, "red"))

  if errors:
    errors = colored(
      "There are some errors in below javascript files:\n\n", "magenta"
    ) + "\n".join(errors).strip("\n")

  return errors

def get_receive_errors(rev_old, rev_new):
  checkable = config.getboolean("receive", "CHECK_JAVASCRIPT")
  if not checkable:
    return None

  files = get_receive_files(rev_old, rev_new, "js")
  if not files:
    return None

  errors = []
  tmp_dir = create_tmp_dir()
  for path in files:
    system("git show %s:%s > %s" % (rev_new, path, tmp_dir + path))

    file_error = tail(
      jshint(
        "--config",
        "%s/configs/jshint.json" % base_path,
        tmp_dir + path, _ok_code = [0, 2]
      ), "-n", 1
    )

    if file_error:
      errors.append(colored(path + " " + str(file_error).strip("\n"), "red"))

  remove_tmp_dir()
  return "\n".join(errors)
