# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class AbstractTab(QtWidgets.QWidget):

  def __init__(self, device, parent = None):
    super(AbstractTab, self).__init__(parent)
    self._device = device

  def post(self, sender, message):
    pass

  def getDevice(self):
    return self._device
