# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui
from Abstracts import abstractDevice
from Queue import queueItem
import pickle

class QueueModel (QtCore.QAbstractItemModel):

  def __init__(self, parent=None):
    super(QueueModel, self).__init__(parent)
    self.root = queueItem.Item("ROOT")


  def data(self, index, role):
    if not index.isValid():
      return None
    node = index.internalPointer()
    return node.data(index.column(), role)


  def setData(self, index, data, role = QtCore.Qt.EditRole):
    if not index.isValid():
      return QtCore.QVariant()
    node = index.internalPointer()
    if index.column() == 1:
      node.setData(data)
      self.dataChanged.emit(index, index)
    return True


  def flags(self, index):
    if index.isValid():
      return index.internalPointer().flags()
    return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled


  def headerData(self, section, orientation, role):
    return None


  def rowCount(self, index = QtCore.QModelIndex()):
    if not index.isValid():
      parent = self.root
    else:
      parent = index.internalPointer()
    return parent.countChildren()


  def columnCount(self, parent = QtCore.QModelIndex()):
    return 2


  def mimeTypes(self):
    liste = QtCore.QStringListModel(["application/queue.item.mime",
                                     "application/queue.item.internal.mime"])
    return liste.stringList()


  def removeRow(self, position, parent):
    if position == -1:
      return False
    if parent.isValid():
      if parent.internalPointer().getChild(position).neededByParent():
        return self.removeRow(parent.row(), parent.parent())
    self.beginRemoveRows(parent, position, position)
    if parent.isValid():
      parent.internalPointer().removeChild(position)
    else:
      self.root.removeChild(position)
    self.endRemoveRows()
    return True


  def mimeData(self, indexes):
    data = QtCore.QMimeData()
    liste = []
    for index in indexes:
      if index.isValid():
        liste.append(bytes([index.row()]))
    data.setData("application/queue.item.internal.mime", liste[0])
    return data


  def dropMimeData(self, data, action, row, column, parent):
    if action == QtCore.Qt.IgnoreAction:
      return True
    if parent.isValid():
      root = parent.internalPointer()
      if not root:
        return False
    else:
      root = self.root
    if data.hasFormat('application/queue.item.internal.mime'):
      item = int.from_bytes(data.data("application/queue.item.internal.mime"), 'little')
      if row < 0:
        row = root.countChildren()
      if item == row or item + 1 == row:
        return True
      if item >= root.countChildren():
        return True
      self.beginMoveRows(parent, item, item, parent, row)
      root.move(item, row)
      self.endMoveRows()
      return True

    if not data.hasFormat("application/queue.item.mime"):
      return False

    liste = pickle.loads(data.data("application/queue.item.mime"))
    listStart = root.countChildren()
    self.beginInsertRows(parent, listStart, listStart+len(liste)-1)
    for i in liste:
      root.addChild(i)
    self.endInsertRows()
    return True


  def addChildren(self, parent):
    self.beginInsertRows(parent, listStart, listStart)
    self.endInsertRows()


  def index(self, row, column, index):
    if not index.isValid():
      parent = self.root
    else:
      parent = index.internalPointer()

    child = parent.getChild(row)

    if child:
      return self.createIndex(row, column, child)
    else:
      return QtCore.QModelIndex()


  def parent(self, index):
    node = index.internalPointer()
    parent = node.getParent()

    if not parent:
      return QtCore.QModelIndex()
    if parent == self.root:
      return QtCore.QModelIndex()

    return self.createIndex(parent.row(), 0, parent)


  def clearAll(self):
    self.beginRemoveRows(QtCore.QModelIndex(), 0, self.root.countChildren())
    for i in range(self.root.countChildren()-1, -1, -1):
      self.root.removeChild(i)
    self.endRemoveRows()
