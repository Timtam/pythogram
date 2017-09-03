from ..signal import Signal

import numpy as np

class SineSignal(Signal):

  def __init__(self):
    self.__sample_rate = 44100
    self.__length = 10.0
    self.__amplitude = 1.0
    self.__frequency = 440.0


  @property
  def signal(self):
    return self.amplitude * (np.sin(2*np.pi*np.arange(self.__sample_rate*self.__length)*self.__frequency/self.__sample_rate)).astype(np.float32)


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
