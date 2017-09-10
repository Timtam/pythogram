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
  def _signal(self):
    self.__wave.rewind()
    signal = self.__wave.readframes(-1)
    signal = self.__amplitude * np.fromstring(signal, 'Int16')
    if signal.size%self.__wave.getnchannels() > 0:
      signal = signal[:-(signal.size%self.__wave.getnchannels())]
    if self.__wave.getnchannels() > 1:
      # we need it to be reshaped first
      nsignal = np.reshape(signal, (signal.size/self.__wave.getnchannels(), self.__wave.getnchannels()))
      # and then we can merge it into one mono signal
      signal = nsignal.sum(axis = 1) / self.__wave.getnchannels()
    return signal


  @property
  def length(self):
    # we need to calculate this manually here
    return float(self._signal.size)/(self.sample_rate)


  @property
  def amplitude(self):
    return self.__amplitude


  @amplitude.setter
  def amplitude(self, value):
    self.__amplitude = value
