# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from Queue.queueItem import Item
from Queue.processHelper import ProcessHelper

class QueueThread(QtCore.QObject):
  finished = QtCore.pyqtSignal()
  newMaximum = QtCore.pyqtSignal(int)
  processed = QtCore.pyqtSignal(int)

  def __init__(self, postman, parent=None):
    super(QueueThread, self).__init__(parent)
    self.root = Item("ROOT")
    self.postman = postman
    self.pHelper = ProcessHelper()
    self.pHelper.processed.connect(self.processed)


  def process(self):
    self.processed.emit(0)
    for i in range(self.root.countChildren()):
      self.root.getChild(i).execute(self.postman, self.pHelper)
    self.pHelper.reset()
    self.finished.emit()


  def setQueue(self, queue):
    self.clearAll()
    for i in range(queue.countChildren()):
      self.root.addChild(queue.getChild(i))
    self.newMaximum.emit(sum(child.countCustomChildren() for child in self.root.children))


  def clearAll(self):
    for i in range(self.root.countChildren()):
      self.root.removeChild(0)

