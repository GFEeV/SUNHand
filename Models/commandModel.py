# -*- coding: utf-8 -*-

from PyQt5 import QtCore
import pickle
from Items.commandItem import CommandItem

class CommandModel (QtCore.QAbstractListModel):

  def __init__(self, command, parent=None):
    super(CommandModel, self).__init__(None)
    self.commandList = command


  def data(self, index, role):
    if not index.isValid():
      return QtCore.QVariant()

    row = index.row()
    column = index.column()

    if role == QtCore.Qt.DisplayRole:
      return self.commandList[row].data(column)
    return QtCore.QVariant()


  def flags(self, index):
    if index.isValid():
      return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


  def rowCount(self, parent = QtCore.QModelIndex()):
    return len(self.commandList)


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
        packet = self.packMime(index.row())
        liste.append(packet)
    data.setData("application/queue.item.mime", pickle.dumps(liste))
    return data


  def getCommand(self, row):
    return self.commandList[row]


  def packMime(self, row):
    command = self.commandList[row]
    a = CommandItem(command.name, None, command.deviceName, command )
    return a

