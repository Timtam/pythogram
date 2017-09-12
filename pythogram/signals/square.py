import numpy as np
from scipy.signal import square

from ..signal import Signal



class SquareSignal(Signal):
  def __init__(self, freq=440.0, l=10.0, amp=1.0, srate=44100):
    Signal.__init__(self)
    self.sample_rate = srate
    self.length = l
    self.amplitude = amp
    self.frequency = freq
  
  
  @property
  def _signal(self):
    return self.amplitude * (square(2 * np.pi * self.frequency * np.linspace(
      0, 1, self.sample_rate*self.length, endpoint=False))).astype(
      np.float32)
