# -*- coding: utf-8 -*-

class Command:
  def __init__(self, xmlAttributes, deviceName):
    self.name = str(xmlAttributes[0].value('Name'))
    self.command = str(xmlAttributes[0].value('Data'))
    self.structure = str(xmlAttributes[0].value('Structure'))
    self.xmlAttributes = xmlAttributes
    self.deviceName = deviceName

  def data(self, column):
    if   column == 0: return self.name
    elif column == 1: return self.command
    elif column == 2: return self.structure
