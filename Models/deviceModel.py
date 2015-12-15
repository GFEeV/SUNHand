# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from Abstracts import abstractDevice
import pickle

class DeviceModel (QtCore.QAbstractListModel):

  def __init__(self, deviceList = [], parent=None):
    super(DeviceModel, self).__init__(None)
    all(self.__is_instance_check__(item) for item in deviceList)
    self.deviceList = deviceList

  def __is_instance_check__(self, item):
    if not isinstance(item, abstractDevice.AbstractDevice):
      raise Exception("Device %s must be subclass of AbstractDevice" % item)

  def data(self, index, role):
    if not index.isValid():
      return QtCore.QVariant()
    if index.row() >= len(self.deviceList):
      return QtCore.QVariant()
    if role == QtCore.Qt.DisplayRole:
      return self.deviceList[index.row()].getName()
    return QtCore.QVariant()


  def flags(self, index):
    if index.isValid():
      return QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


  def rowCount(self, parent = QtCore.QModelIndex()):
    return len(self.deviceList)


  def getDevice(self, row):
    return self.deviceList[row]
