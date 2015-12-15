  # -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtSerialPort
import time
import binascii


class SerialThread(QtCore.QObject):
  valuesAvailable = QtCore.pyqtSignal(str)

  def __init__(self, device, postman, parent=None):
    super(SerialThread, self).__init__(parent)
    self.postman = postman
    self.device = device
    self.data = b''
    self.serial = QtSerialPort.QSerialPort(self.device.info)
    self.serial.readyRead.connect(self.handleSerial)
    self.serial.error.connect(self.handleError)


  def handleSerial(self):
    if not self.device.terminate:
      self.data = b''
    while self.serial.bytesAvailable():
      char = self.serial.read(1)
      self.data += char
      if self.device.terminate:
        if char == bytes(self.device.terminate, 'utf-8'):
          self.postman.Post.emit('SerialThread', self.device.getName(), binascii.hexlify(self.data).decode('utf-8'))
          self.data = b''
    if not self.device.terminate:
      if self.data:
        self.postman.Post.emit('SerialThread', self.device.getName(), binascii.hexlify(self.data).decode('utf-8'))


  def handleError(self, error):
    if error > QtSerialPort.QSerialPort.NoError:
      self.postman.Post.emit('Serial_Thread_' + self.device.getName(), self.device.getName(), self.serial.errorString())


  def connect(self):
    self.serial.setPort(self.device.info)
    if self.device.advanced:
      self.serial.setParity(self.device.Parity.get(self.device.parity, QtSerialPort.QSerialPort.NoParity))
      self.serial.setBaudRate(int(self.device.baudrate))
      self.serial.setDataBits(self.device.DataBits.get(self.device.byteSize, QtSerialPort.QSerialPort.Data8))
      self.serial.setFlowControl(self.device.FlowControl.get(self.device.flowControl, QtSerialPort.QSerialPort.NoFlowControl))
      self.serial.setStopBits(self.device.StopBits.get(self.device.stopbits, QtSerialPort.QSerialPort.OneStop))

    self.postman.Post.emit('Serial_Thread_' + self.device.getName(), self.device.getName(),
        'Connect:<br>&nbsp;Port: %s<br>&nbsp;Baudrate: %s<br>&nbsp;Parity: %s<br>&nbsp;DataBits: %s<br>&nbsp;StopBits: %s<br>&nbsp;FlowControl: %s<br>&nbsp;' %
                           (self.serial.portName(),
                            self.serial.baudRate(),
                            self.serial.parity(),
                            self.serial.dataBits(),
                            self.serial.stopBits(),
                            self.serial.flowControl()))
    return self.serial.open(QtCore.QIODevice.ReadWrite)


  def write(self, text):
    if self.serial.isOpen():
      self.serial.write(text + self.device.terminate)


