# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, QtWidgets, uic
import time
import binascii
from Models import commandModel
from Devices.Serial import serialThread
from Devices.Serial.serialConfig import SerialConfig
from Devices.Serial.fileExport import ExportFile
from Classes.tabClass import Tab

class SerialWidget(Tab):

  def __init__(self, device, postman, parent = None):
    super(SerialWidget, self).__init__(device,
                                       'GUI/serialWidget.ui',
                                       postman,
                                       parent)
    self.serial = serialThread.SerialThread(device, postman)
    self.thread = QtCore.QThread()
    self.serial.moveToThread(self.thread)

    self.bSend.clicked.connect(self.onMessageSend)
    self.bConnect.clicked.connect(self.connect)
    self.bConfig.clicked.connect(self.config)
    self.uiCommandList.clicked.connect(self.messageSet)
    self.uiCommandList.doubleClicked.connect(self.onMessageSend)
    self.command.returnPressed.connect(self.onMessageSend)

    self.commandModel = commandModel.CommandModel(self._device.commands)
    self.uiCommandList.setModel(self.commandModel)


  def updateOutput(self):
    self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())


  def clearOutput(self):
    self.output.setText("");


  def writeOutput(self, text, color="#FF0000"):
    self.write('<br /><font color="'+color+'">' + time.strftime("%H:%M:%S: ") + str(text) + "</font><br />")


  def write(self, text):
    self.output.moveCursor(QtGui.QTextCursor.End)
    if not isinstance(text, bytes):
      self.output.insertHtml(bytes(text, 'utf-8').decode('unicode_escape'))
    else:
      self.output.insertHtml(text.decode('unicode_escape'))
    self.updateOutput()


  def messageSet(self, index):
    command = self.commandModel.getCommand(index.row())
    temp = command.structure
    if not temp:
      temp = "C"
    temp = temp.replace("C",command.command)
    """
    for i in command.parameter:
      if i.default:
        temp = temp.replace(("P%d" % (command.parameter.index(i) + 1)),i.default)
      else:
        temp = temp.replace(("P%d" % (listWidgetItem.command.parameter.index(i) + 1)),i.typ)
    """
    self.command.setText(temp)


  def onMessageSend(self):
    text = self.command.text()
    if text:
      self.serial.write(text)
      self.postman.Post.emit("Serial_" + self.device.getName(), self.device.getName(), text)


  def post(self, sender, message):
    if sender == "SerialThread":
      self.write(binascii.unhexlify(message))
    elif sender == 'CommandItem':
      self.writeOutput(message, "#0000AA")
      self.serial.write(message)
    else:
      self.writeOutput(message, "#AA0055")


  def connect(self):
    if self.serial.connect():
      self.bConnect.setEnabled(False)
      self.bConfig.setEnabled(False)


  def config(self):
    conf = SerialConfig(self.device, self)
    conf.show()
