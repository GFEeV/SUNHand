# -*- coding: utf-8 -*-

from PyQt5 import QtGui, uic
from Abstracts import abstractTab

class Tab(abstractTab.AbstractTab):
  def __init__(self, device, ui, postman, parent = None):
    super(Tab, self).__init__(device, parent)
    self.postman = postman
    self.device = device
    uic.loadUi(ui, self)

