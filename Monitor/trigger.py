#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

class Trigger:
  def __init__(self, target, pattern):
    self.pattern = pattern
    self.target = target

  @classmethod
  def fromAttributes(self, xmlAttributes):
    return Trigger(xmlAttributes[0].value('Target').split(','),
        xmlAttributes[0].value('Pattern'))

  def match(self, sender, receiver, message):
    if 'sender' in self.target:
      return re.search(self.pattern, sender)
    if 'receiver' in self.target:
      return re.search(self.pattern, receiver)
    if 'message' in self.target:
      return re.search(self.pattern, message)
    return re.search(self.pattern, sender) or re.search(self.pattern, receiver) or re.search(self.pattern, message)


  def serialize(self, stream):
    stream.writeStartElement("Trigger")
    stream.writeAttribute("Target",','.join(self.target))
    stream.writeAttribute("Pattern",self.pattern)
    stream.writeEndElement()


