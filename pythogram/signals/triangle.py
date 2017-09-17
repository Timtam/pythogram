import numpy as np
from scipy.signal import sawtooth

from ..signal import Signal



class TriangleSignal(Signal):
  def __init__(self, freq=440.0, l=10.0, amp=1.0, srate=44100):
    Signal.__init__(self)
    self.sample_rate = srate
    self.length = l
    self.amplitude = amp
    self.frequency = freq
  
  
  @property
  def _signal(self):
    return self.amplitude * (sawtooth(2 * np.pi * np.arange(
      self.sample_rate * self.length) * self.frequency / self.sample_rate,
                                      0.5)).astype(np.float32)
