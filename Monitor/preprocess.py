# -*- coding: utf-8 -*-

import re
import binascii
from collections import defaultdict
from PyQt5 import QtCore

class Preprocess:
  def __init__(self, action, parameter):
    self.action = action
    self.parameter = parameter

  @classmethod
  def fromAttributes(self, xmlAttributes):
    return Preprocess(xmlAttributes[0].value('Action'),
                      xmlAttributes[0].value('Parameter'))

  def process(self, message):
    if self.action == 'Unhexlify':
      return binascii.unhexlify(message)
    if self.action == 'Decode':
      return message.decode('utf-8')
    if self.action == 'Encode':
      return bytes(message, 'utf-8')
    if self.action == 'JSON':
      doc = QtCore.QJsonDocument.fromJson(message)
      return self.parameter.format_map(
          defaultdict(
            str,
            defaultdict(str, { x: v.toString() for (x,v) in doc.object().items()})))
    return message


  def serialize(self, stream):
    stream.writeStartElement("Preprocess")
    stream.writeAttribute("Action",self.action)
    stream.writeAttribute("Parameter",self.parameter)
    stream.writeEndElement()
