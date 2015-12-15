# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets


class QueueDelegate(QtWidgets.QStyledItemDelegate):
  def __init__(self, parent = None):
    super(QueueDelegate, self).__init__(parent)


  def createEditor(self, parent, option, index):
    if index.column() == 1:
      return index.internalPointer().getEditor(parent)
    return None


  def setEditorData(self, editor, index):
    editor.blockSignals(True)
    #editor.setCurrentIndex(index.model().data(index, QtCore.Qt.DisplayRole))
    editor.blockSignals(False)


  def setModelData(self, editor, model, index):
    if not index.isValid():
      return None
    item = index.internalPointer()
    model.setData(index, item.getEditorValue(editor))


  def currentIndexChanged(self):
    self.commitData.emit(self.sender())


  def sizeHint(self, option, index):
    return QtCore.QSize(20,25)

