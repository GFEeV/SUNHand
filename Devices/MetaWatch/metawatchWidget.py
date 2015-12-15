# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore, uic, QtBluetooth
from Classes.tabClass import Tab
from Devices.MetaWatch.metawatchThread import MetawatchThread
from Devices.Bluetooth.bluetoothSearch import BluetoothSearch
import time

class MetawatchWidget(Tab):

  def __init__(self, device, postman, parent = None):
    super(MetawatchWidget, self).__init__(device,
                                          'GUI/metawatchWidget.ui',
                                          postman,
                                          parent)
    self.bluetooth = MetawatchThread(self.device, self.postman, self)
    self.thread = QtCore.QThread()
    self.bluetooth.moveToThread(self.thread)
    self.bluetooth.connected.connect(self.onConnected)
    self.bluetooth.disconnected.connect(self.onDisconnected)
    self.bluetooth.error.connect(self.onError)
    self.bluetooth.readyRead.connect(self.readAll)

    self.bSearch.clicked.connect(self.search)
    self.bConnect.clicked.connect(self.bluetooth.connect)
    self.bDisconnect.clicked.connect(self.bluetooth.disconnect)
    self.bText.clicked.connect(self.writeText)
    self.bBuzz.clicked.connect(self.buzz)
    self.bPicture.clicked.connect(self.writeImage)

    self.postman.Post.connect(self.postOffice)

  def post(self, sender, message):
    self.writeOutput(message, "#00AA00")


  def sendMessage(self):
    text = self.text.text()
    if text:
      self.postman.Post.emit("Metawatch_" + self.device.getName(), self.device.getName(), text)


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


  def onConnected(self):
    self.uiStatus.setText('Connected')
    self.uiStatus.setStyleSheet("QLabel { background-color : green; color : white;}")
    self.bConnect.setEnabled(False)
    self.bDisconnect.setEnabled(True)
    self.bluetooth.setButtonsEnabled(True)


  def onDisconnected(self):
    self.uiStatus.setText('Disconnected')
    self.uiStatus.setStyleSheet("QLabel { background-color : red; color : white;}")
    self.bConnect.setEnabled(True)
    self.bDisconnect.setEnabled(False)


  def onError(self, errorString):
    print(errorString)
    self.bConnect.setEnabled(True)
    self.bDisconnect.setEnabled(False)


  def buzz(self):
    self.bluetooth.buzz()


  def writeText(self):
    text = self.text.text()
    if text:
      self.bluetooth.writeText(text=text, pos_x=0, pos_y=0)


  def writeImage(self):
    self.bluetooth.writeImage(image="dalek.bmp")

  def readAll(self):
    msg = self.bluetooth.readAll()
    ret = self.messageIsButtonPressed(msg)
    if ret:
      self.postman.Post.emit("Metawatch_Button_" + self.device.getName(), self.device.getName(), ret)

  def messageIsButtonPressed(self, msg):
    if not msg:
      return False
    if msg.length() < 3:
      return False
    return str(int.from_bytes(bytes(msg[3], encoding='utf-8'), 'little'))


  def postOffice(self, sender, reciever, message):
    if "Digiface_Display" in sender:
      self.bluetooth.writeText(text=message, pos_x=0, pos_y=0)


