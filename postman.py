# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class Postman(QtCore.QObject):
  """
  Postman Class - used to send and receive messages
  """

  Post = QtCore.pyqtSignal(str, str, str)

  def __init__(self, parent = None):
    super(Postman, self).__init__(parent)

