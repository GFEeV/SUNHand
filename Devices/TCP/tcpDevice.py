# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from Abstracts import abstractDevice
from Classes.commandClass import Command
from Classes.deviceClass import Device
from Devices.TCP.tcpWidget import TcpWidget

class TcpDevice(Device):
  def __init__(self, xmlAttributes):
    super(TcpDevice, self).__init__(xmlAttributes)

    self.commands = []
    for item in range(1, len(xmlAttributes)):
      self.commands.append(Command(xmlAttributes[item], self.name))
    self.server = str(xmlAttributes[0].value('Server'))
    self.port = str(xmlAttributes[0].value('Port'))


  def getName(self):
    return self.name


  def getWidget(self, postman):
    return TcpWidget(self, postman)

