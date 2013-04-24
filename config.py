#-*- coding:utf-8 -*-
from os import path
from json import load
try:
  from ConfigParser import ConfigParser
except ImportError:
  from configparser import ConfigParser

base_path = path.abspath(__file__ + "/../")

except_paths = None
with file("%s/configs/except.json" % base_path) as fp:
  except_paths = load(fp)

config = ConfigParser()
config.read("%s/configs/default.cfg" % base_path)
