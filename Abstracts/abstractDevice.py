# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class AbstractDevice():
  __metaclass__ = ABCMeta

  def __init__(self, xmlAttributes):
    self._isActive = False

  @abstractmethod
  def getName(self):
    """
    Passes the device name.
    Need to be overwritten.
    """
    pass

  def _setActive(self, state):
    self._isActive = state

  def _active(self):
    return self._isActive
