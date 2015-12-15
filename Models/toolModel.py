# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from Queue import queueItem
import pickle

class ToolModel (QtCore.QAbstractListModel):

  def __init__(self, tools, parent=None):
    super(ToolModel, self).__init__(parent)
    self.root = queueItem.Item("ROOT")
    for tool in tools:
      self.root.addChild(tool)

  def data(self, index, role):
    if not index.isValid():
      return None

    node = index.internalPointer()

    if role == QtCore.Qt.DisplayRole:
      return node.data(index.column(), role)
    return QtCore.QVariant()


  def flags(self, index):
    if index.isValid():
      return index.internalPointer().flags()
    return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


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


  def headerData(self, section, orientation, role):
    return None


  def rowCount(self, index = QtCore.QModelIndex()):
    if not index.isValid():
      parent = self.root
    else:
      parent = index.internalPointer()
    return parent.countChildren()

  def columnCount(self, parent = QtCore.QModelIndex()):
    return 1


  def mimeTypes(self):
    liste = QtCore.QStringList()
    liste << "application/queue.item.mime"
    return liste


  def mimeData(self, indexes):
    data = QtCore.QMimeData()
    liste = []
    for index in indexes:
      if index.isValid():
        packet = self.root.getChild(index.row())
        liste.append(packet)
    data.setData("application/queue.item.mime", pickle.dumps(liste))
    return data
