# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from Queue import queueSubItem

class ItemLineEdit(queueSubItem.Item):

  def getEditor(self, parent):
    ret = QtWidgets.QLineEdit(parent)
    ret.setText(str(self._data))
    return ret

  def getEditorValue(self, editor):
    return editor.text()
