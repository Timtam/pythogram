from abc import *

# just an interface

class Signal(object):
  __metaclass__ = ABCMeta

  @abstractproperty
  def sample_rate(self):
    return NotImplemented

  @abstractproperty
  def channels(self):
    return NotImplemented

  @abstractproperty
  def signal(self):
    return NotImplemented
