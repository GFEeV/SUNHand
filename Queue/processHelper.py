# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class ProcessHelper(QtCore.QObject):
  processed = QtCore.pyqtSignal(int)

  def __init__(self, parent = None):
    super(ProcessHelper, self).__init__(parent)
    self.count = 0

  def process(self):
    self.count += 1
    self.processed.emit(self.count)

  def reset(self):
    self.count = 0

