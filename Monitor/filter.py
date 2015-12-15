# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui
import os
from Monitor.trigger import Trigger
from Monitor.preprocess import Preprocess

class Filter(QtGui.QStandardItem):
  DEFAULT_FORMAT = '{sender} {receiver} {message}'

  def __init__(self,
               name = 'New',
               linebreak = True,
               active = False,
               overwrite = True,
               formatString = DEFAULT_FORMAT,
               trigger = [],
               preprocess = [],
               header = '',
               outputFile = 'new.log'):
    self.name = name
    self.linebreak = linebreak
    self.active = active
    self.overwrite = overwrite
    self.formatString = formatString
    self.header = header
    self.trigger = trigger
    self.preprocess = preprocess
    self.outputFile = outputFile

    if not self.formatString:
      self.formatString = Filter.DEFAULT_FORMAT
    self.line = None


  @classmethod
  def fromAttributes(self, xmlAttributes):
    trigger = []
    preprocess = []
    for x in xmlAttributes[1:]:
      if x[0].value('Reader_Name') == 'Trigger':
        trigger.append(Trigger.fromAttributes(x))
      if x[0].value('Reader_Name') == 'Preprocess':
        preprocess.append(Preprocess.fromAttributes(x))
    return Filter(
        name =   xmlAttributes[0].value('Name'),
        linebreak = xmlAttributes[0].value('Linebreak') == 'True',
        active = xmlAttributes[0].value('Active') == 'True',
        overwrite = xmlAttributes[0].value('Overwrite') == 'True',
        formatString = xmlAttributes[0].value('Format'),
        header = xmlAttributes[0].value('Header'),
        trigger = trigger,
        preprocess = preprocess,
        outputFile = xmlAttributes[0].value('Output'))


  def serialize(self):
    output = QtCore.QByteArray()
    stream = QtCore.QXmlStreamWriter(output)
    stream.setAutoFormatting(True)
    stream.writeStartDocument()
    stream.writeStartElement("Filter")
    stream.writeAttribute("Name",self.name)
    stream.writeAttribute("Linebreak",str(self.linebreak))
    stream.writeAttribute("Active",str(self.active))
    stream.writeAttribute("Overwrite",str(self.overwrite))
    stream.writeAttribute("Format",self.formatString)
    stream.writeAttribute("Output",self.outputFile)
    stream.writeAttribute("Header",self.header)
    for trigger in self.trigger:
      trigger.serialize(stream)
    for preprocess in self.preprocess:
      preprocess.serialize(stream)
    stream.writeEndElement()
    stream.writeEndDocument()
    return output


  def data(self, column, role):
    if role == QtCore.Qt.DisplayRole:
      return self.name
    if role == QtCore.Qt.CheckStateRole:
      if self.active:
        return QtCore.Qt.Checked
      else:
        return QtCore.Qt.Unchecked
    return QtCore.QVariant()


  def setData(self, value, column, role):
    if role == QtCore.Qt.CheckStateRole:
      self.active = bool(value)
      return True
    return False


  def match(self, sender, receiver, message):
    for t in self.trigger:
      if t.match(sender, receiver, message):
        return True
    return False


  def breakLine(self, f):
    f.write(os.linesep)
    self.line += 1


  def execute(self, sender, receiver, message):
    m = message[:]
    if not self.line:
      if self.overwrite or not os.path.isfile(self.outputFile):
        with open(self.outputFile, 'w', encoding='utf-8') as f:
          if self.header:
            f.write(self.header)
            f.write(os.linesep)
      self.line = 0
      with open(self.outputFile, 'r', encoding='utf-8') as f:
        self.line = sum(1 for line in f)
    for a in self.preprocess:
      m = a.process(m)
    with open(self.outputFile, 'a', encoding='utf-8') as f:
      f.write(self.formatString.format(sender=sender, receiver=receiver, message=m, line=self.line))
      if self.linebreak:
        self.breakLine(f)
