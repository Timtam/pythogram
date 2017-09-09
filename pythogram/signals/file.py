import numpy as np
import wave

from ..signal import Signal

class FileSignal(Signal):

  def __init__(self, filename):
    Signal.__init__(self)
    self.__wave = wave.open(filename, 'r')
    self.__amplitude = 1.0


  @property
  def sample_rate(self):
    return self.__wave.getframerate()


  @property
  def channels(self):
    return self.__wave.getnchannels()


  @property
  def _signal(self):
    self.__wave.rewind()
    signal = self.__wave.readframes(-1)
    return self.__amplitude * (np.fromstring(signal, 'Int16').astype(np.float32))


  @property
  def length(self):
    # we need to calculate this manually here
    return float(len(self._signal))/(self.sample_rate*self.channels)


  @property
  def amplitude(self):
    return self.__amplitude


  @amplitude.setter
  def amplitude(self, value):
    self.__amplitude = value
