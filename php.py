#-*- coding:utf-8 -*-
from config import config
from common import get_commit_files
from sh import phpcs, awk
from termcolor import colored

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
