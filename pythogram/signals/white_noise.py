import numpy as np

from ..signal import Signal



class WhiteNoiseSignal(Signal):
  def __init__(self, l=10.0, amp=1.0, srate=44100):
    Signal.__init__(self)
    self.sample_rate = srate
    self.length = l
    self.amplitude = amp
  
  
  @property
  def _signal(self):

    signal = self.amplitude * np.random.normal(0, 1, size=int(self.sample_rate*self.length)).astype(np.float32)

    signal /= np.max(np.abs(signal), axis = 0)

    return signal

