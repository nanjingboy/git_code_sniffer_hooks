#-*- coding:utf-8 -*-
from sh import jshint, tail
from termcolor import colored
from config import base_path
from common import get_commit_errors as get_javascript_commit_errors
from common import get_receive_errors as get_javascript_receive_errors

def get_commit_errors():
  return get_javascript_commit_errors("js", _get_commit_file_error)

def _get_commit_file_error(path):
  error =  jshint(
    "--config",
    "%s/configs/jshint.json" % base_path,
    path,  _ok_code = [0, 2]
  )
  if error:
    return colored(error, "red")

  return None

def get_receive_errors(rev_old, rev_new):
  return get_javascript_receive_errors(
    rev_old, rev_new, "js", _get_receive_file_error
  )

def _get_receive_file_error(path):
  error = tail(
    jshint(
      "--config", "%s/configs/jshint.json" % base_path,
      path, _ok_code = [0, 2]
    ), "-n", 1
  )
  if error:
    return  "     " + colored(str(error).strip("\n"), "red")

  return None
