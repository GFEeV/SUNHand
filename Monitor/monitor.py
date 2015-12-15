# -*- coding: utf-8 -*-

from PyQt5 import QtCore, uic, QtWidgets
import os
import fnmatch
from Models.loggingFilterModel import LogModel
from Monitor.filterConfig import FilterConfig
from Monitor.filter import Filter
from Helper import parseXML

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Monitor(QtWidgets.QDialog):
  def __init__(self, postman, parent = None):
    super(Monitor, self).__init__(parent)
    uic.loadUi('GUI/loggingMonitor.ui', self)

    self.postman = postman
    self.postman.Post.connect(self.postOffice)

    root = parseXML(directory = 'Monitor/filter', structure = 'Filter')

    self.filterList = []
    for f in root:
      self.filterList.append(Filter.fromAttributes(f))

    self.model = LogModel(self.filterList, self)
    self.loggingMonitorView.setModel(self.model)
    self.loggingMonitorView.doubleClicked.connect(self.config)

    self.bSave.clicked.connect(self.save)
    self.bAdd.clicked.connect(self.add)
    self.bDel.clicked.connect(self.rem)
    self.bEdit.clicked.connect(self.config)



  def postOffice(self, sender, receiver, message):
    self.uiMonitor.insertHtml('<br><font color="red">'+ sender +
        '</font> <font color="green">' + receiver +
        '</font> ' + message + "</font></br>")
    for f in self.filterList:
      if f.active:
        if f.match(sender, receiver, message):
          f.execute(sender, receiver, message)


  def config(self, index = None):
    if not index:
      index = self.loggingMonitorView.currentIndex()
    f = FilterConfig(self.model.getLog(index.row()), self)
    f.show()


  def save(self):
    for f in range(self.model.rowCount()):
      self.saveFilter(self.model.getLog(f))
    print('All filter saved.')


  def add(self):
    self.model.addLog(Filter())


  def rem(self):
    row = self.loggingMonitorView.currentIndex().row()
    self.model.remLog(row)


  def saveFilter(self, f):
    outputFile = QtCore.QFile("Monitor/filter/" + f.name + ".xml")
    if not outputFile.open(QtCore.QIODevice.WriteOnly):
      print( 'could not write', f.name + ".xml")
      return
    outputFile.write(f.serialize())
    outputFile.close()


