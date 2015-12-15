# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, uic, QtWidgets, QtSerialPort

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class SerialConfig(QtWidgets.QDialog):
  def __init__(self, device, parent = None):
    super(SerialConfig, self).__init__(parent)
    uic.loadUi('GUI/serialConfig.ui', self)

    self.device = device
    for item in QtSerialPort.QSerialPortInfo.availablePorts():
      self.cbPorts.addItem(item.portName())
    self.cbPorts.setCurrentIndex(max(0, self.cbPorts.findText(self.device.port)))

    self.advanced.setChecked(self.device.advanced)

    if self.device.advanced:
      self.fillForms()

    self.buttonBox.accepted.connect(self.save)
    self.advanced.clicked.connect(self.setAdvanced)


  def save(self):
    self.device.port = str(self.cbPorts.currentText())
    self.device.info = QtSerialPort.QSerialPortInfo(self.device.port)
    if self.device.advanced:
      self.device.baudrate = str(self.cbBaudrate.currentText())
      self.device.byteSize = str(self.cbByteSize.currentText())
      self.device.parity = str(self.cbParity.currentText())
      self.device.stopbits = str(self.cbStopbits.currentText())
      self.device.flowControl = str(self.cbFlowControl.currentText())


  def setAdvanced(self, clicked):
    self.device.advanced = clicked
    if clicked:
      self.fillForms()


  def fillForms(self):
    self.cbBaudrate.setCurrentIndex(max(0,self.cbBaudrate.findText(self.device.baudrate)))
    self.cbByteSize.setCurrentIndex(max(0,self.cbByteSize.findText(self.device.byteSize)))
    self.cbParity.setCurrentIndex(max(0,self.cbParity.findText(self.device.parity)))
    self.cbStopbits.setCurrentIndex(max(0,self.cbStopbits.findText(self.device.stopbits)))
    self.cbFlowControl.setCurrentIndex(max(0,self.cbFlowControl.findText(self.device.flowControl)))

