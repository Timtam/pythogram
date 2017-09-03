from ..signal import Signal

import numpy as np

class SineSignal(Signal):

  @property
  def sample_rate(self):
    return 44100

  @property
  def channels(self):
    return 1


  @property
  def signal(self):
    return (np.sin(2*np.pi*np.arange(self.sample_rate*10.0)*440.0/self.sample_rate)).astype(np.float32)
