#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fnmatch
from PyQt5 import QtCore


def parseXML(directory = '.', filetype = '*.xml', structure = 'Device'):
  #TODO use a structure
  root = []
  for structure in fnmatch.filter(os.listdir(directory), filetype):
    f = QtCore.QFile(directory + '/' + structure)
    if not f.open(QtCore.QIODevice.ReadOnly):
      print( 'could not open', structure)
      continue
    reader = QtCore.QXmlStreamReader(f)
    xmlDevice = []
    count = -1

    while not reader.atEnd():
      if reader.readNext():
        if reader.isStartElement():
          count += 1
          attr = reader.attributes()
          attr.append('Reader_Name', reader.name())
          attr.append('Name', os.path.splitext(os.path.basename(structure))[0])
          xmlDevice.append((count, attr))
        elif reader.isEndElement():
          count -= 1
      if reader.hasError():
        break
    if reader.hasError():
      print( '')
      print( 'ERROR at %s:%i' % (structure, reader.lineNumber()))
      print( reader.errorString())
      print( '')
    else:
      root.append(xmlDevice)
  shrunken = []
  for x in root:
    shrink(shrunken, x)

  return shrunken


def shrink(ret = None, liste = None, index = 0):
  while liste:
    (level, item) = liste[0]
    if level == 0:
      newItem = [item]
      liste = shrink(newItem, liste[1:], level)
      ret.append(newItem)
    elif level == index:
      return liste
      newItem = [item]
      liste = shrink(newItem, liste[1:], level)
      ret.append(newItem)
    elif level > index:
      newItem = [item]
      liste = shrink(newItem, liste[1:], level)
      ret.append(newItem)
    else:
      return liste

