# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
from Queue import queueItem
import time
from Items.doubleSpinBox import ItemDoubleSpinBox

class TimeDelayItem(queueItem.Item):

  def __init__(self, name, data = 2.0, parent = None):
    super(TimeDelayItem, self).__init__(name, data, parent)


  def execute(self, postman, pHelper):
    time.sleep(int(self._data))
    pHelper.process()
    return True


  def flags(self):
    return QtCore.Qt.ItemIsDragEnabled | \
           QtCore.Qt.ItemIsEnabled | \
           QtCore.Qt.ItemIsSelectable | \
           QtCore.Qt.ItemIsEditable


  def getEditor(self, parent):
    ret = QtWidgets.QDoubleSpinBox(parent)
    ret.setRange(0.0, 99999.9)
    ret.setValue(float(self._data))
    return ret


  def getEditorValue(self, editor):
    return editor.value()


  def data(self, column, role):
    if role == QtCore.Qt.DisplayRole:
      if column == 1:
        return '%.2f seconds' % self._data
    return super(TimeDelayItem, self).data(column, role)
