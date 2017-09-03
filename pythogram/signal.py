from abc import ABCMeta

# just an interface

class Signal(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def GetNextFrames(frames = 1):
    return NotImplemented

  @abstractproperty
  def sample_rate(self):
    return NotImplemented
