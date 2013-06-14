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
  errors = _get_error(path).split("\n")
  return "     " + colored("%s error(s)" % len(errors) - 2, "red") if errors else None

def _get_error(path):
  return  getoutput(
    "%s/jshint.js --config %s/configs/jshint.json %s"  %
    (base_path, base_path, path)
  )
