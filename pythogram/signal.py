from abc import *

# just an interface

class Signal(object):
  __metaclass__ = ABCMeta

  @abstractproperty
  def sample_rate(self):
    return NotImplemented

  @property
  def channels(self):
    return 1

  @abstractproperty
  def signal(self):
    return NotImplemented

  @abstractproperty
  def length(self):
    return NotImplemented

  @abstractproperty
  def amplitude(self):
    return NotImplemented
