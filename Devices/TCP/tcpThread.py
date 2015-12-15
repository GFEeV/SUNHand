# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtNetwork
import socket
import struct

class TcpThread(QtCore.QObject):
  connected = QtCore.pyqtSignal()
  disconnected = QtCore.pyqtSignal()

  def __init__(self, device, postman, parent=None):
    super(TcpThread, self).__init__(parent)
    self.postman = postman
    self.device = device
    self.tcp = QtNetwork.QTcpSocket(parent)
    #self.thread = QtCore.QThread()
    #self.tcp.moveToThread(self.thread)
    self.tcp.connected.connect(self.connected.emit)
    self.tcp.disconnected.connect(self.disconnected.emit)
    self.tcp.readyRead.connect(self.handleTcp)
    self.tcp.error.connect(self.handleError)
    #self.thread.start()


  def handleTcp(self):
    print('handle TCP')
    data = self.tcp.readAll()
    if data:
      self.postman.Post.emit('TcpThread', self.device.getName(), unicode(data, errors='ignore'))


  def handleError(self, error):
    if error:
      self.postman.Post.emit('Tcp_Thread_' + self.device.getName(), self.device.getName(), self.tcp.errorString())


  def connect(self):
    print('try to connect')
    if self.tcp.state() == QtNetwork.QAbstractSocket.UnconnectedState:
      print('is not connected')
      print('try', self.device.server, ':', str(self.device.port))
      self.tcp.connectToHost(self.device.server, int(self.device.port))
      print(self.tcp.waitForConnected(3000))


  def write(self, text):
    self.tcp.write(str(text))

