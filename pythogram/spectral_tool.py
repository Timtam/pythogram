import numpy as np
from scipy.fftpack import fft
from scipy.signal import spectrogram
import scipy.signal as scipysignal


class SpectralTool:
  def __init__(self):
    pass
  
  def spectrum(self, signal):
    # f, pxx = sig.periodogram(x=signal, fs=self.signal.sample_rate,
    # scaling='spectrum')

    pxx = abs(fft(signal._signal))
    pxx = pxx[:(len(pxx) / 2)]
    f = np.linspace(0.0, signal.sample_rate / 2, len(pxx))

    # amp fix: sine with amp x -> frequency with same amp x
    # pxx = pxx / max(pxx)
    pxx = pxx / len(pxx)
    pxx = 20 * np.log10(1e-6 + pxx)
    
    return f, pxx
  
  
  def spectrogram(self, signal):

    sig = signal._signal
    # sig[sig == 0] = np.nan # bugfix
    # pxx, freq, t = mlab.specgram(x=x, Fs=fs, NFFT=512)
    return