# -*- coding: utf-8 -*-

from Abstracts import abstractDevice
from Classes.commandClass import Command
from Classes.deviceClass import Device
from Devices.Bluetooth.bluetoothWidget import BluetoothWidget

class BluetoothDevice(Device):
  def __init__(self, xmlAttributes):
    super(BluetoothDevice, self).__init__(xmlAttributes)

    self.address = str(xmlAttributes[0].value('Address'))
    self.commands = []
    for item in range(1, len(xmlAttributes)):
      self.commands.append(Command(xmlAttributes[item], self.name))


  def getName(self):
    return self.name


  def getWidget(self, postman):
    return BluetoothWidget(self, postman)

