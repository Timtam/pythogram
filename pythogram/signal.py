from abc import *

from scipy.signal import butter, lfilter

# just an interface

class Signal(object):
  __metaclass__ = ABCMeta

  def __init__(self):
    self.low_cutoff = 0.0
    self.high_cutoff = 20000.00


  @abstractproperty
  def sample_rate(self):
    return NotImplemented

  @property
  def channels(self):
    return 1

  @abstractproperty
  def _signal(self):
    return NotImplemented

  @property
  def signal(self):
    # processing the filtering in here
    # nyquist frequency
    nyq = 0.5 * self.sample_rate
    low = self.low_cutoff / nyq
    high = self.high_cutoff / nyq

    b, a = butter(4, [low, high], btype='band')

    return lfilter(b, a, self._signal)

  @abstractproperty
  def length(self):
    return NotImplemented

  @abstractproperty
  def amplitude(self):
    return NotImplemented
