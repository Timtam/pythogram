from ..signal import Signal

import numpy as np

class SineSignal(Signal):

  def GenerateSignal(self, frequency = 440.0, length = 10.0, amplitude = 1.0):
    return amplitude * (np.sin(2*np.pi*np.arange(self.sample_rate*duration)*frequency/self.sample_rate)).astype(np.float32)


  @property
  def sample_rate(self):
    return 44100

  @property
  def channels(self):
    return 1

