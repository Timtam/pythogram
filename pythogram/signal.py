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
