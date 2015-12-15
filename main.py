#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import copy
import os
import fnmatch
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from Models.deviceModel import DeviceModel
from Models.queueModel import QueueModel
from Models.toolModel import ToolModel
import Devices
from Queue.queueDelegate import QueueDelegate
from Queue.queueThread import QueueThread
import Tools
from Monitor.monitor import Monitor
from Helper import parseXML

from postman import Postman

class MainWindow(QtWidgets.QMainWindow):

  def __init__(self):
    super(MainWindow, self).__init__()
    uic.loadUi('GUI/mainwindow.ui', self)

    self.openTabs = {} # Dict for Post-Office
    self.postman = Postman()
    self.postman.Post.connect(self.postOffice)

    ### Parse XML ###
    root = parseXML(directory="xml")

    ### Create Devices ###
    liste = []
    for item in root:
      _class = Devices.getDevice(item[0].value('Type'))
      liste.append(_class(item))
    ###

    self.wToolbox.setVisible(False)
    self.wQueue.setVisible(False)

    ### Prepare Device View ###
    self.deviceModel = DeviceModel(liste)
    self.listView.setModel(self.deviceModel)
    self.listView.doubleClicked.connect(self.tabAdd)
    self.uiTabs.tabCloseRequested.connect(self.tabClose)
    ###

    ### Prepare Queue ###
    self.qModel = QueueModel()
    self.treeView.setModel(self.qModel)
    self.treeView.setItemDelegate(QueueDelegate())
    self.queueThread = QueueThread(self.postman)
    self.thread = QtCore.QThread()
    self.queueThread.moveToThread(self.thread)
    self.thread.started.connect(self.queueThread.process)
    self.queueThread.finished.connect(self.thread.quit)
    self.queueThread.newMaximum.connect(self.queueProgress.setMaximum)
    self.queueThread.processed.connect(self.queueProgress.setValue)
    ###

    ### Prepare Logging Monitor ###
    self.monitor = Monitor(self.postman, self)
    self.actionLogging_Monitor.triggered.connect(self.monitor.show)
    ###

    self.bExecute.clicked.connect(self.startExecute)
    self.bQueueRemoveItem.clicked.connect(self.removeQueueItem)
    self.bClearAll.clicked.connect(self.qModel.clearAll)

    self.toolModel = ToolModel(Tools.TOOL_LIST)
    self.uiToolList.setModel(self.toolModel)

    self.show()


  def tabAdd(self, index):
    device = self.deviceModel.getDevice(index.row())
    if device._active():
      return
    tab = device.getWidget(self.postman)
    if not tab:
      return
    device._setActive(True)
    tab.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.uiTabs.addTab(tab,device.getName())
    self.openTabs[device.getName()] = tab


  def tabClose(self, tabNumber):
    widget = self.uiTabs.widget(tabNumber)
    device = widget.getDevice()
    device._setActive(False)
    self.uiTabs.removeTab(tabNumber)
    del self.openTabs[device.getName()]
    widget.close()
    del widget
    pass


  def removeQueueItem(self):
    index = self.treeView.currentIndex()
    if index:
      self.qModel.removeRow(index.row(), index.parent())


  def postOffice(self, sender, reciever, message):
    for to in str(reciever).split(";"):
      rec = self.openTabs.get(to)
      if rec is None:
        pass
      else:
        rec.post(sender, message)
        print( "Message from", sender, " to", to, ":",)
        print( message)


  def startExecute(self):
    if self.thread.isRunning():
      print( 'still running')
      return False
    self.queueThread.setQueue(copy.deepcopy(self.qModel.root))
    self.thread.start()





if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MainWindow()
  sys.exit(app.exec_())
