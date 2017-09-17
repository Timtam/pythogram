import numpy as np
from scipy.fftpack import fft



class SpectralTool:
  def __init__(self):
    pass
  
  
  @staticmethod
  def spectrum(signal):
    
    # calculate fft of whole signal and get real values
    pxx = abs(fft(signal.signal))
    # only use first half, because the second is just a mirrored first half (
    # nyquist)
    pxx = pxx[:(len(pxx) / 2)]
    # create frequency axis
    f = np.linspace(0.0, signal.sample_rate / 2, len(pxx))
    
    # normalize pxx and log scale
    pxx /= max(pxx)
    pxx = 20 * np.log10(1e-6 + pxx)
    
    return f, pxx
  
  
  @staticmethod
  def spectrogram(signal, nfft=256):
    sig = signal.signal
    # number of fft segments
    num_fft = len(sig) / nfft
    
    # split signal array in a 2d-array of num_fft element, which again have
    # nfft elements
    split_sig = np.reshape(sig[:(num_fft * nfft)], (num_fft, nfft))
    # multiply with a window to reduce fft artifacts
    split_sig *= np.blackman(nfft)
    # calculate fft on 2d-signal-array
    tmp = abs(fft(split_sig, nfft))
    # create a new 2d-array with also num_fft element, but which only have
    # half nfft elements
    pxx = np.empty((num_fft, nfft / 2))
    # "delete" the second half of the fft, which is just a mirrored first
    # half (nyquist)
    for i in xrange(0, len(tmp)):
      pxx[i] = tmp[i][:nfft / 2]
    
    # swap axes for diagram
    pxx = np.swapaxes(pxx, 0, 1)
    
    # normalize pxx and log scale
    pxx /= (nfft / 2)
    pxx = 20 * np.log10(1e-6 + pxx)
    
    # create time and frequency axis
    t = np.linspace(0.0, signal.length, num_fft)
    f = np.linspace(0.0, signal.sample_rate / 2, nfft / 2)
    
    return f, t, pxx
