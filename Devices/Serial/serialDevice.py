# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtSerialPort
from Classes.commandClass import Command
from Classes.deviceClass import Device
from Devices.Serial.serialWidget import SerialWidget

class SerialDevice(Device):
  def __init__(self, xmlAttributes):
    super(SerialDevice, self).__init__(xmlAttributes)

    self.commands = []
    for item in range(1, len(xmlAttributes)):
      self.commands.append(Command(xmlAttributes[item], self.name))

    self.port = xmlAttributes[0].value('Port')
    self.info = QtSerialPort.QSerialPortInfo(self.port)

    self.FlowControl = { 'None' : QtSerialPort.QSerialPort.NoFlowControl,
                     'Hardware' : QtSerialPort.QSerialPort.HardwareControl,
                     'Software' : QtSerialPort.QSerialPort.SoftwareControl,
                      'Unknown' : QtSerialPort.QSerialPort.UnknownFlowControl }
    self.Parity =      { 'None' : QtSerialPort.QSerialPort.NoParity,
                         'Even' : QtSerialPort.QSerialPort.EvenParity,
                         'Odd'  : QtSerialPort.QSerialPort.OddParity,
                         'Mark' : QtSerialPort.QSerialPort.MarkParity,
                         'Space': QtSerialPort.QSerialPort.SpaceParity }
    self.StopBits =     { '1'   : QtSerialPort.QSerialPort.OneStop,
                          '1.5' : QtSerialPort.QSerialPort.OneAndHalfStop,
                          '2'   : QtSerialPort.QSerialPort.TwoStop }
    self.DataBits =  { '5' : QtSerialPort.QSerialPort.Data5,
                       '6' : QtSerialPort.QSerialPort.Data6,
                       '7' : QtSerialPort.QSerialPort.Data7,
                       '8' : QtSerialPort.QSerialPort.Data8 }

    self.baudrate = str(xmlAttributes[0].value('Baudrate'))
    self.byteSize = str(xmlAttributes[0].value('ByteSize'))
    self.parity = str(xmlAttributes[0].value('Parity'))
    self.stopbits = str(xmlAttributes[0].value('Stopbits'))
    self.flowControl = str(xmlAttributes[0].value('FlowControl'))
    self.terminate = bytes(xmlAttributes[0].value('Terminate'), 'utf-8').decode('unicode_escape')
    if str(xmlAttributes[0].value('Advanced')) == 'True':
      self.advanced = True
    else:
      self.advanced = False

  def getWidget(self, postman):
    return SerialWidget(self, postman)

