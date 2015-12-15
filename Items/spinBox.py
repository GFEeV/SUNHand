# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from Queue import queueSubItem

class ItemSpinBox(queueSubItem.Item):

  def getEditor(self, parent):
    ret = QtWidgets.QSpinBox(parent)
    ret.setRange(0, 99999)
    ret.setValue(int(self._data))
    return ret


  def getEditorValue(self, editor):
    return editor.value()

