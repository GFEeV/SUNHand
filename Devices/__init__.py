# -*- coding: utf-8 -*-

from Devices.Serial.serialDevice import SerialDevice
from Devices.TCP.tcpDevice    import TcpDevice
from Devices.Bluetooth.bluetoothDevice import BluetoothDevice
from Devices.MetaWatch.metawatchDevice import MetawatchDevice
from Classes import deviceClass

CLASSDICT = {
              "TCP" : TcpDevice,
           "Serial" : SerialDevice,
        "Bluetooth" : BluetoothDevice,
        "MetaWatch" : MetawatchDevice,
         }

def getDevice(deviceType):
  return CLASSDICT.get(deviceType, deviceClass.Device)
