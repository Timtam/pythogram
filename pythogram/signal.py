import numpy as np
from scipy.signal import butter, lfilter

class Signal(object):

  def __init__(self):
    self._define_attribute('low_cutoff', 0.0)
    self._define_attribute('high_cutoff', 20000.0)
    self._define_attribute('sample_rate', 44100)
    self._define_attribute('_signal', np.zeros(0, dtype=np.float32))
    self._define_attribute('length', 1.0)
    self._define_attribute('amplitude', 1.0)

  def _define_attribute(self, attrib, value):

    if not attrib in self.__dict__:
      self.__dict__[attrib] = value


  @property
  def signal(self):
    # processing the filtering in here
    # nyquist frequency
    nyq = 0.5 * self.sample_rate
    low = self.low_cutoff / nyq
    high = self.high_cutoff / nyq

    b, a = butter(4, [low, high], btype='band')

    return lfilter(b, a, self._signal)


  def __add__(self, other):

    # is the other object a signal too?
    if not isinstance(other, Signal):
      raise TypeError('non-signal cannot be added to signal')

    # different sample rates?
    if self.sample_rate != other.sample_rate:
      raise TypeError('cannot add signals with different sample rates yet')

    if self._signal.size < other._signal.size:
      s1 = self._signal
      s2 = other._signal
    else:
      s1 = other._signal
      s2 = self._signal

    if s1.size != s2.size:
      # s1 is the shorter one and needs to be padded
      s1 = np.pad(s1, (0, s2.size - s1.size), 'constant')

    # generate a new signal as addition
    s = s1+s2

    # normalization
    if np.max(np.abs(s), axis = 0)>1.0:
      s /= np.max(np.abs(s), axis = 0)

    # new class and attribute definition

    os = Signal()
    os.sample_rate = self.sample_rate
    os.length = float(s.size)/self.sample_rate

    os._signal = s

    return os
