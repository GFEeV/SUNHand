# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, uic, QtWidgets, QtBluetooth

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class BluetoothSearch(QtWidgets.QDialog):
  def __init__(self, device, postman, parent = None):
    super(BluetoothSearch, self).__init__(parent)
    uic.loadUi('GUI/bluetoothSearch.ui', self)

    self.device = device
    self.postman = postman
    self.agent = QtBluetooth.QBluetoothDeviceDiscoveryAgent(self)
    self.agent.error.connect(self.error)
    self.agent.deviceDiscovered.connect(self.discovered)
    self.agent.finished.connect(self.stop)

    self.bScan.clicked.connect(self.scan)
    self.buttonBox.accepted.connect(self.save)
    self.localDevice = QtBluetooth.QBluetoothLocalDevice()
    if self.localDevice.isValid():
      self.localDevice.powerOn()
    self.postman.Post.emit("Bluetooth_" + self.device.getName(),
        self.device.getName(),
        'Connect to: ' + self.localDevice.name())


  def save(self):
    sel = self.deviceList.currentItem().text()
    if sel:
      self.device.address = sel.split()[0]


  def stop(self):
    self.agent.stop()
    self.bScan.setText('Scan')
    print('stopped discovery')


  def start(self):
    self.deviceList.clear()
    self.agent.start()
    self.bScan.setText('Stop')
    print('started discovery')


  def scan(self):
    if self.agent.isActive():
      self.stop()
    else:
      self.start()
      if self.agent.error():
        self.stop()


  def discovered(self, info):
    self.deviceList.addItem(info.address().toString() + ' ' + info.name())


  def error(self, E):
    if E:
      print(self.agent.errorString())
