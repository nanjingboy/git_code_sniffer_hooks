#-*- coding:utf-8 -*-
from os import path
try:
  from ConfigParser import ConfigParser
except ImportError:
  from configparser import ConfigParser

base_path = path.abspath(__file__ + "/../")

config = ConfigParser()
config.read("%s/configs/default.cfg" % base_path)
