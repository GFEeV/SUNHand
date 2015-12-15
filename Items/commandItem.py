# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets
from Queue import queueItem
import time
from Items.lineEdit import ItemLineEdit

class CommandItem(queueItem.Item):

  def __init__(self, name = "", parent = None, deviceName = None, command = None):
    super(CommandItem, self).__init__(name, parent)
    self._deviceName = deviceName
    self._command = command.command
    for param in range(1, len(command.xmlAttributes)):
      self.addChild(ItemLineEdit(command.xmlAttributes[param][0].value('Name'),
                          data = command.xmlAttributes[param][0].value('Data')))


  def execute(self, postman, pHelper):
    postman.Post.emit('CommandItem', self._deviceName, self._command)
    pHelper.process()
    time.sleep(0.5) #TODO
    return True


  def getEditor(self, parent):
    ret = QtWidgets.QLineEdit(parent)
    ret.setText(self._command)
    return ret


  def getEditorValue(self, editor):
    return editor.text()


  def flags(self):
    return QtCore.Qt.ItemIsDragEnabled | \
           QtCore.Qt.ItemIsEnabled | \
           QtCore.Qt.ItemIsSelectable | \
           QtCore.Qt.ItemIsEditable


