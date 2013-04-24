#-*- coding:utf-8 -*-
from config import config
from common import get_commit_files, get_receive_files
from common import create_tmp_dir, remove_tmp_dir
from sh import phpcs
from termcolor import colored
from os import system

def get_commit_errors():
  checkable = config.getboolean("commit", "CHECK_PHP")
  if not checkable:
    return None

  files = get_commit_files('php')
  if not files:
    return None

  errors = []
  for path in files:
    file_errors = phpcs("--report=emacs", path, _iter = True, _ok_code = [0, 1])
    if file_errors:
      for file_error in file_errors:
        error_type = file_error.split(' ')[1]
        if error_type == 'error':
          errors.append(colored(file_error, "red"))
        else:
          errors.append(colored(file_error, "yellow"))

  if errors:
    errors = colored(
      "There are some errors in below php files:\n\n", "magenta"
    ) + "\n".join(errors)

  return errors

def get_receive_errors(rev_old, rev_new):
  checkable = config.get("receive", "CHECK_PHP")
  if not checkable:
    return None

  files = get_receive_files(rev_old, rev_new, "php")
  if not files:
    return None

  errors = []
  tmp_dir = create_tmp_dir()
  for path in files:
    system("git show %s:%s > %s" % (rev_new, path, tmp_dir + path))
    file_errors = phpcs(
      "--report=summary", tmp_dir + path, _iter = True, _ok_code = [0, 1]
    )
    if file_errors:
      file_errors = [str(file_error) for file_error in file_errors]
      error_info = file_errors[-3].split(" ")
      error = colored("%s error(s)" % error_info[3], "red")
      warning = colored("%s warning(s)" % error_info[6], "yellow")
      errors.append(path + "    " + error + "  " + warning)

  return "\n".join(errors)

