# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from Monitor.filter import Filter

class LogModel (QtCore.QAbstractListModel):

  def __init__(self, log, parent=None):
    super(LogModel, self).__init__(None)
    self.logList = log


  def data(self, index, role):
    if not index.isValid():
      return QtCore.QVariant()

    row = index.row()
    column = index.column()
    return self.logList[row].data(column, role)


  def setData(self, index, value, role):
    if not index.isValid():
      return QtCore.QVariant()

    row = index.row()
    column = index.column()
    return self.logList[row].setData(value, column, role)


  def flags(self, index):
    if index.isValid():
      return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable


  def rowCount(self, parent = QtCore.QModelIndex()):
    return len(self.logList)


  def columnCount(self, parent = QtCore.QModelIndex()):
    return 1


  def getLog(self, row):
    return self.logList[row]


  def addLog(self, log = None):
    if not log:
      return False
    if not isinstance(log, Filter):
      return False
    length = len(self.logList)
    self.beginInsertRows(QtCore.QModelIndex(), length, length)
    self.logList.append(log)
    self.endInsertRows()
    return True


  def remLog(self, row):
    self.beginRemoveRows(QtCore.QModelIndex(), row, row)
    del self.logList[row]
    self.endRemoveRows()


