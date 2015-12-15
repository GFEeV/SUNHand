# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class ExportFile:
  def __init__(self, fileName):
    self.fileName = fileName
    self.mode = "a+"
    self.logFormat = '{} {} {}\n'

  def post(self, sender, reciever, message):
    data = open(self.fileName, self.mode)
    data.write(self.logFormat.format(sender, reciever, message))
    data.close()

