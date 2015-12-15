# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtBluetooth

class BluetoothThread(QtCore.QObject):

  def __init__(self, device, postman, parent=None):
    super(BluetoothThread, self).__init__(parent)
    self.postman = postman
    self.device = device

