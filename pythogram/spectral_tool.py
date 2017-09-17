import numpy as np
from scipy.fftpack import fft



class SpectralTool:
  def __init__(self):
    pass
  
  
  @staticmethod
  def spectrum(signal):
    # f, pxx = sig.periodogram(x=signal, fs=self.signal.sample_rate,
    # scaling='spectrum')
    
    pxx = abs(fft(signal.signal))
    pxx = pxx[:(len(pxx) / 2)]
    f = np.linspace(0.0, signal.sample_rate / 2, len(pxx))
    
    # amp fix: sine with amp x -> frequency with same amp x
    # pxx = pxx / max(pxx)
    pxx = pxx / len(pxx)
    pxx = 20 * np.log10(1e-6 + pxx)
    
    return f, pxx
  
  
  @staticmethod
  def spectrogram(signal):
    sig = signal.signal
    # sig[sig == 0] = np.nan # bugfix
    # pxx, freq, t = mlab.specgram(x=x, Fs=fs, NFFT=512)
    return
