#-*- coding:utf-8 -*-
from sh import phpcs
from termcolor import colored
from common import get_commit_errors as get_php_commit_errors
from common import get_receive_errors as get_php_receive_errors
from config import config

def get_commit_errors():
  return get_php_commit_errors("php", _get_commit_file_error)

def _get_commit_file_error(path):
  file_errors = phpcs("--report=emacs", path, _iter = True, _ok_code = [0, 1])
  if not file_errors:
    return None

  errors = []
  for error in file_errors:
    error_type = error.split(' ')[1]
    if error_type == 'error':
      errors.append(colored(error, "red"))
    elif config.getboolean('common', 'DISPLAY_WARING'):
      errors.append(colored(error, "yellow"))

  return "\n".join(errors)

def get_receive_errors(rev_old, rev_new):
  return get_php_receive_errors(
    rev_old, rev_new, "php", _get_receive_file_error
  )

def _get_receive_file_error(path):
  errors = phpcs("--report=summary", path, _iter = True, _ok_code = [0, 1])
  if errors:
    errors = [str(error) for error in errors]
    errors = errors[-3].split(" ")
    error = None
    if int(errors[3]) > 0:
      error = colored("%s error(s)" % errors[3], "red")

    if config.getboolean('common', 'DISPLAY_WARING') and int(errors[6]) > 0:
      warning = colored("%s warning(s)" % errors[6], "yellow")
      return "    %s  %s" % (error, warning)

    return "    %s" % error if error else None

  return None
