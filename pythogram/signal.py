from abc import *

# just an interface

class Signal(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def GenerateSignal(self, frequency, length = 10.0, amplitude = 1.0):
    return NotImplemented

  @abstractproperty
  def sample_rate(self):
    return NotImplemented

  @abstractproperty
  def channels(self):
    return NotImplemented
