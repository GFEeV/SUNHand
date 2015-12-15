# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class Item(object):

  def __init__(self, name = "", data = None, parent = None):
    super(Item, self).__init__()
    self.children = []
    self.parent = parent
    self.name = name
    self._data = data
    if parent is not None:
      parent.addChild(self)


  def countChildren(self):
    return len(self.children)


  def getChild(self, position):
    if position < 0 or position >= self.countChildren():
      return None
    return self.children[position]


  def getParent(self):
    return self.parent


  def addChild(self, child):
    if not isinstance(child, Item):
      raise Exception("Child must be instance of Item")
    self.children.append(child)
    child.parent = self
    return child


  def move(self, _from, _to):
    self.children.insert(_to, self.children.pop(_from))


  def removeChild(self, position):
    del self.children[position]
    return True


  def data(self, column, role):
    if column == 0:
      if role == QtCore.Qt.DisplayRole:
        return self.name
      if role == QtCore.Qt.EditRole:
        return self.name
    if column == 1:
      if role == QtCore.Qt.DisplayRole:
        return self._data
      if role == QtCore.Qt.EditRole:
        return self._data
      if role == QtCore.Qt.UserRole:
        return self._data


  def setData(self, data):
    self._data = data


  def row(self):
    if self.parent is not None:
      return self.parent.children.index(self)


  ### CUSTOM BEHAVIOR ###
  #                     #

  def flags(self):
    return QtCore.Qt.ItemIsEnabled | \
           QtCore.Qt.ItemIsSelectable | \
           QtCore.Qt.ItemIsEditable


  def execute(self, postman, phelper):
    for child in self.children:
      child.execute(postman, pHelper)
      pHelper.process()

  def countCustomChildren(self):
    return 1

  def getEditor(self, parent):
    return None


  def getEditorValue(self, editor):
    raise Exception("getEditorValue must exist in %s" % self)


  def neededByParent(self):
    return False

  #                     #
  ### CUSTOM BEHAVIOR ###
