#-*- coding:utf-8 -*-
from commands import getoutput
from termcolor import colored
from config import base_path
from common import get_commit_errors as get_javascript_commit_errors
from common import get_receive_errors as get_javascript_receive_errors

def get_commit_errors():
  return get_javascript_commit_errors("js", _get_commit_file_error)

def _get_commit_file_error(path):
  error = _get_error(path)
  return colored(error, "red") if error else None

def get_receive_errors(rev_old, rev_new):
  return get_javascript_receive_errors(
    rev_old, rev_new, "js", _get_receive_file_error
  )

def _get_receive_file_error(path):
  error = _get_error(path)
  if error:
    error_count = len(error.split("\n")) - 2
    return "     " + colored("%s error(s)" % error_count, "red"), error_count, 0

  return None, 0, 0

def _get_error(path):
  return  getoutput(
    "%s/jshint/jshint --config %s/configs/jshint.json %s"  %
    (base_path, base_path, path)
  )
