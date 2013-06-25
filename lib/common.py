#-*- coding:utf-8 -*-
import sqlite3
import datetime
from os import path, system
from sh import awk, grep, cat, mkdir, rm
from commands import getoutput
from termcolor import colored
from config import base_path, config, except_paths

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
  for file_path in files:
    if path.exists(file_path):
      file_error = function(file_path)
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

  if not checkable:
    return None

  files = _get_receive_files(rev_old, rev_new, file_type)
  if not files:
    return None

  tmp_dir = config.get("receive", "TMP_DIR")
  errors = []

  reports = []
  save_report = config.getboolean("receive", "SAVE_REPORT")
  if save_report:
    user_info = _get_user_info(rev_old, rev_new)

  for file_path in files:
    mkdir("-p", "/".join((tmp_dir + file_path).split("/")[:-1]))
    system("git show %s:%s > %s" % (rev_new, file_path, tmp_dir + file_path))
    if path.exists(tmp_dir + file_path):
      file_error, error_count, warning_count = function(tmp_dir + file_path)
      if file_error and (error_count > 0 or warning_count > 0):
        if save_report:
          reports.append(
            (
              user_info, file_path, error_count, warning_count,
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
          )
        errors.append(file_path + file_error)

  if save_report:
    _save_report(reports)

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
  if not except_paths:
    return files

  except_files = []
  for file_path in files:
    for except_path in except_paths:
      if file_path not in except_files and file_path.startswith(except_path):
        except_files.append(file_path)

  return [file_path for file_path in files if file_path not in except_files]

def _get_user_info(rev_old, rev_new):
  return getoutput(
    "git rev-list --pretty=format:%aN\<%ae\>" + " %s..%s" % (rev_old, rev_new)
  ).strip().split('\n')[1]

def _save_report(reports):
  if not reports:
    return False

  connection = sqlite3.connect("%s/data/report.db" % base_path)
  cursor = connection.cursor()
  cursor.executemany(
      '''INSERT INTO `report` (`user`, `file`, `errors`, `warnings`, `datetime`)
      VALUES (?, ?, ?, ?, ?)''',
      reports
  )
  connection.commit()
  connection.close()
