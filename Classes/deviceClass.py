# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from Abstracts import abstractDevice

class Device(abstractDevice.AbstractDevice) :
  def __init__(self, xmlAttributes):
    super(Device, self).__init__(xmlAttributes)
    self.name = str(xmlAttributes[0].value('Name'))
    self.xmlAttributes = xmlAttributes

  def getName(self):
    return self.name

  def getWidget(self, postman):
    return None
