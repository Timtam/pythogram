import numpy as np
from scipy.signal import filtfilt, iirfilter, resample
import wave

class Signal(object):

  def __init__(self):
    self._define_attribute('_low_cutoff', None)
    self._define_attribute('_high_cutoff', None)
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
    low = min(self.low_cutoff / nyq, 1)
    high = min(self.high_cutoff / nyq, 1)

    b, a = iirfilter(5, Wn=[low, high], btype='bandpass', ftype='bessel')

    signal = filtfilt(b, a, self._signal).astype(np.float32)

    if signal.size != self._signal.size:
      signal = resample(signal, self._signal.size)

    if np.max(np.abs(signal), axis = 0) > 1.0:
      signal /= np.max(np.abs(signal), axis = 0)

    return signal


  def __add__(self, other):

    # is the other object a signal too?
    if not isinstance(other, Signal):
      raise TypeError('non-signal cannot be added to signal')

    # different sample rates?
    # we will always resample towards our own sample rate
    # that means, if you write a +b, the resulting signal will always
    # have the same sample rate as a
    # switch positions if you want it differently
    if self.sample_rate != other.sample_rate:
      other_signal = resample(other._signal, int(other.length*self.sample_rate))
    else:
      other_signal = other._signal

    if self._signal.size < other_signal.size:
      s1 = self._signal
      s2 = other_signal
    else:
      s1 = other_signal
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


  # exports the signal into a file
  def write(self, filename):
    w = wave.open(filename, 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(self.sample_rate)
    w.writeframes((32768.0*self.signal).astype(np.int16))
    w.close()


  @property
  def low_cutoff(self):
    if self._low_cutoff is None:
      return 3.0

    return self._low_cutoff

  @low_cutoff.setter
  def low_cutoff(self, value):

    if value is None:
      self._low_cutoff = None
      return

    # may not drop below 3.0
    if value < 3.0:
      raise ValueError('low cutoff must at least be 3 hz')

    if value >= self.high_cutoff:
      raise ValueError('low cutoff may not be higher or equal high cutoff')

    self._low_cutoff = float(value)


  @property
  def high_cutoff(self):

    if self._high_cutoff is None:
      return float(self.sample_rate*0.5)-5

    return self._high_cutoff


  @high_cutoff.setter
  def high_cutoff(self, value):

    if value is None:
      self._high_cutoff = None
      return

    if value <= self.low_cutoff:
      raise ValueError("high cutoff may not be equal or lower than the low cutoff")

    if value > float(self.sample_rate*0.5)-5:
      raise ValueError("high cutoff may not exceed %f"%(float(self.sample_rate*0.5)-5))

    self._high_cutoff = float(value)
