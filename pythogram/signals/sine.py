import numpy as np

from ..signal import Signal



class SineSignal(Signal):
  def __init__(self, freq=440.0, l=10.0, amp=1.0, srate=44100):
    super(SineSignal, self).__init__()
    self.__sample_rate = srate
    self.__length = l
    self.__amplitude = amp
    self.__frequency = freq
  
  
  @property
  def _signal(self):
    return self.amplitude * (np.sin(2 * np.pi * np.arange(
      self.__sample_rate * self.__length) * self.__frequency /
                                    self.__sample_rate)).astype(
      np.int16)*32768
  
  
  @property
  def frequency(self):
    return self.__frequency
  
  
  @frequency.setter
  def frequency(self, value):
    self.__frequency = value
  
  
  @property
  def amplitude(self):
    return self.__amplitude
  
  
  @amplitude.setter
  def amplitude(self, value):
    self.__amplitude = value
  
  
  @property
  def sample_rate(self):
    return self.__sample_rate
  
  
  @sample_rate.setter
  def sample_rate(self, value):
    self.__sample_rate = value
  
  
  @property
  def length(self):
    return self.__length
  
  
  @length.setter
  def length(self, value):
    self.__length = value
