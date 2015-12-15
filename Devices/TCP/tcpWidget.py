# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, uic
import time
from Models import commandModel
from Classes.tabClass import Tab
from Devices.TCP.tcpThread import TcpThread

class TcpWidget(Tab):

  def __init__(self, device, postman, parent = None):
    super(TcpWidget, self).__init__(device,
                                    'GUI/tcpWidget.ui',
                                    postman,
                                    parent)
    self.thread = TcpThread(self.device, self.postman, self)
    self.thread.connected.connect(self.onConnected)
    self.thread.disconnected.connect(self.onDisconnected)

    self.commandModel = commandModel.CommandModel(device.commands)
    self.uiCommandList.setModel(self.commandModel)

    self.bSend.clicked.connect(self.sendMessage)
    self.bConnect.clicked.connect(self.connect)
    self.uiCommandList.clicked.connect(self.messageSet)
    self.uiCommandList.doubleClicked.connect(self.sendMessage)
    self.command.returnPressed.connect(self.sendMessage)


  def post(self, sender, message):
    if sender == "TcpThread":
      self.write(message)
    else:
      self.writeOutput(message, "#00AA00")
      self.thread.write(message)


  def sendMessage(self):
    text = self.command.text()
    if text:
      self.postman.Post.emit("Tcp_" + self.device.getName(), self.device.getName(), text)


  def messageSet(self, index):
    command = self.commandModel.getCommand(index.row())
    temp = command.structure
    if not temp:
      temp = "C"
    temp = temp.replace("C",command.command)
    self.command.setText(temp)


  def writeOutput(self, text, color="#FF0000"):
    self.write('<br /><font color="'+color+'">' + time.strftime("%H:%M:%S: ") + str(text) + "</font><br />")


  def write(self, text):
    self.output.moveCursor(QtGui.QTextCursor.End)
    self.output.insertHtml(text)
    self.updateOutput()


  def updateOutput(self):
    self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())


  def connect(self):
    self.device.server = str(self.uiIP.text())
    self.device.port = int(self.uiPort.text())
    self.thread.connect()


  def onConnected(self):
    self.bConnect.setEnabled(False)


  def onDisconnected(self):
    print('error connect')
    self.bConnect.setEnabled(True)

