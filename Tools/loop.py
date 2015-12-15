# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from Queue import queueItem
from Items.spinBox import ItemSpinBox

class LoopItem(queueItem.Item):

  def __init__(self, name, data = 1, parent = None):
    super(LoopItem, self).__init__(name, data, parent)


  def countCustomChildren(self):
    return sum(child.countCustomChildren() for child in self.children) * self._data

  def execute(self, postman, pHelper):
    for i in range(self._data):
      for child in self.children:
        child.execute(postman, pHelper)
    return True


  def flags(self):
    return QtCore.Qt.ItemIsDragEnabled | \
           QtCore.Qt.ItemIsDropEnabled | \
           QtCore.Qt.ItemIsEnabled | \
           QtCore.Qt.ItemIsSelectable | \
           QtCore.Qt.ItemIsEditable


  def getEditor(self, parent):
    ret = QtWidgets.QSpinBox(parent)
    ret.setRange(0, 99999)
    ret.setValue(int(self._data))
    return ret


  def getEditorValue(self, editor):
    return editor.value()
