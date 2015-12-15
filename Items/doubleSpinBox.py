# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from Queue import queueSubItem

class ItemDoubleSpinBox(queueSubItem.Item):

  def getEditor(self, parent):
    ret = QtWidgets.QDoubleSpinBox(parent)
    ret.setRange(0.0, 99999.9)
    ret.setValue(float(self._data))
    return ret

  def getEditorValue(self, editor):
    return editor.value()


  def flags(self):
    return self.parent.flags() | QtCore.Qt.ItemIsEditable

