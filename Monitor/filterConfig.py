# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, uic, QtWidgets
from Monitor.trigger import Trigger
from Monitor.preprocess import Preprocess

try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s

class FilterConfig(QtWidgets.QDialog):
  def __init__(self, _filter, parent = None):
    super(FilterConfig, self).__init__(parent)
    uic.loadUi('GUI/filterConfig.ui', self)

    self.filter = _filter

    self.buttonBox.accepted.connect(self.save)
    self.bAddTrigger.clicked.connect(self.addTrigger)
    self.bAddPreprocess.clicked.connect(self.addPreprocess)
    self.bDelTrigger.clicked.connect(self.delTrigger)
    self.bDelPreprocess.clicked.connect(self.delPreprocess)
    self.bOpenFile.clicked.connect(self.openFile)

    self.uiName.setText(self.filter.name)
    self.uiFormat.setText(self.filter.formatString)
    self.uiHeader.setText(self.filter.header)
    self.uiOutputFile.setText(self.filter.outputFile)
    self.uiLinebreak.setChecked(self.filter.linebreak)
    self.uiOverwrite.setChecked(self.filter.overwrite)
    self.uiActive.setChecked(self.filter.active)
    for (row, trigger) in enumerate(self.filter.trigger):
      self.uiTrigger.insertRow(row)
      self.uiTrigger.setItem(row, 0, QtWidgets.QTableWidgetItem(','.join(trigger.target)))
      self.uiTrigger.setItem(row, 1, QtWidgets.QTableWidgetItem(trigger.pattern))
    for (row, preprocess) in enumerate(self.filter.preprocess):
      self.uiPreprocess.insertRow(row)
      self.uiPreprocess.setItem(row, 0, QtWidgets.QTableWidgetItem(preprocess.action))
      self.uiPreprocess.setItem(row, 1, QtWidgets.QTableWidgetItem(preprocess.parameter))


  def save(self):
    self.filter.name = self.uiName.text()
    self.filter.formatString = self.uiFormat.text()
    if not self.filter.formatString:
      self.filter.formatString = self.filter.DEFAULT_FORMAT
    self.filter.header = self.uiHeader.text()
    self.filter.outputFile = self.uiOutputFile.text()
    self.filter.linebreak = self.uiLinebreak.isChecked()
    self.filter.active = self.uiActive.isChecked()
    self.filter.overwrite = self.uiOverwrite.isChecked()
    self.filter.trigger = []
    for row in range(self.uiTrigger.rowCount()):
      target = self.uiTrigger.item(row, 0)
      if not target:
        target = ''
      else:
        target = target.text()
      pattern = self.uiTrigger.item(row, 1)
      if not pattern:
        pattern = ''
      else:
        pattern = pattern.text()
      self.filter.trigger.append(Trigger(target.split(','), pattern))
    self.filter.preprocess = []
    for row in range(self.uiPreprocess.rowCount()):
      action = self.uiPreprocess.item(row, 0)
      if not action:
        action = ''
      else:
        action = action.text()
      parameter = self.uiPreprocess.item(row, 1)
      if not parameter:
        parameter = ''
      else:
        parameter = parameter.text()
      self.filter.preprocess.append(Preprocess(action, parameter))


  def addTrigger(self):
    self.uiTrigger.insertRow(self.uiTrigger.rowCount())

  def addPreprocess(self):
    self.uiPreprocess.insertRow(self.uiPreprocess.rowCount())

  def delTrigger(self):
    self.uiTrigger.removeRow(self.uiTrigger.currentRow())

  def delPreprocess(self):
    self.uiPreprocess.removeRow(self.uiPreprocess.currentRow())

  def openFile(self):
    (name, _filter) = QtWidgets.QFileDialog.getSaveFileName(self)
    if name:
      self.uiOutputFile.setText(name)



