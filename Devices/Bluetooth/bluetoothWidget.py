# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, uic, QtBluetooth
from Models import commandModel
from Classes.tabClass import Tab
from Devices.Bluetooth.bluetoothThread import BluetoothThread
from Devices.Bluetooth.bluetoothSearch import BluetoothSearch
import time

class BluetoothWidget(Tab):

  def __init__(self, device, postman, parent = None):
    super(BluetoothWidget, self).__init__(device,
                                          'GUI/bluetoothWidget.ui',
                                          postman,
                                          parent)
    self.thread = BluetoothThread(self.device, self.postman, self)

    self.commandModel = commandModel.CommandModel(device.commands)
    self.uiCommandList.setModel(self.commandModel)

    self.bSend.clicked.connect(self.sendMessage)
    self.bSearch.clicked.connect(self.search)
    self.bConnect.clicked.connect(self.connect)
    self.uiCommandList.clicked.connect(self.messageSet)
    self.uiCommandList.doubleClicked.connect(self.sendMessage)
    self.command.returnPressed.connect(self.sendMessage)


  def post(self, sender, message):
    if sender == "BluetoothThread":
      self.write(message)
    else:
      self.writeOutput(message, "#00AA00")
      self.dev.write(message)


  def sendMessage(self):
    text = self.command.text()
    if text:
      self.postman.Post.emit("Bluetooth_" + self.device.getName(), self.device.getName(), text)


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


  def search(self):
    conf = BluetoothSearch(self.device, self.postman, self)
    conf.setModal(True)
    conf.show()


  def connect(self):
    print('connecting to', self.device.address)
    addr = QtBluetooth.QBluetoothAddress(self.device.address)
    self.dev = QtBluetooth.QBluetoothSocket(QtBluetooth.QBluetoothServiceInfo.RfcommProtocol, self)
    self.dev.connected.connect(self.onConnected)
    self.dev.disconnected.connect(self.onDisconnected)
    self.dev.error.connect(self.onError)
    self.dev.connectToService(addr, QtBluetooth.QBluetoothUuid.SerialPort)


  def onConnected(self):
    print('connected')
    self.bConnect.setEnabled(False)


  def onDisconnected(self):
    print('error connect')
    self.bConnect.setEnabled(True)


  def onError(self, E):
    print(self.dev.errorString())
