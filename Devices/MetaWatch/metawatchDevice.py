# -*- coding: utf-8 -*-

from Classes.commandClass import Command
from Classes.deviceClass import Device
from Devices.MetaWatch.metawatchWidget import MetawatchWidget

class MetawatchDevice(Device):
  def __init__(self, xmlAttributes):
    super(MetawatchDevice, self).__init__(xmlAttributes)

    self.address = str(xmlAttributes[0].value('Address'))
    self.commands = []
    for item in range(1, len(xmlAttributes)):
      self.commands.append(Command(xmlAttributes[item], self.name))


  def getName(self):
    return self.name


  def getWidget(self, postman):
    return MetawatchWidget(self, postman)

