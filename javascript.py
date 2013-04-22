#-*- coding:utf-8 -*-
from config import config, base_path
from common import get_commit_files
from sh import jshint
from termcolor import colored

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
      errors.append(str(file_errors))

  if errors:
    errors = colored(
      "There are some errors in below javascript files:\n", "red",
      attrs = ["dark"]
    ) + "\n".join(errors)

  return errors
