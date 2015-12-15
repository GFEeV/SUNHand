# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from Queue import queueItem

class Item(queueItem.Item):

  def neededByParent(self):
    return True


  def flags(self):
    return QtCore.Qt.ItemIsEnabled | \
           QtCore.Qt.ItemIsSelectable

  def addChild(self, child):
    return False

