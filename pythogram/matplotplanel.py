# import matplotlib.mlab as mlab
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import wx
from matplotlib.backends.backend_wxagg import (
  FigureCanvasWxAgg as FigureCanvas,
  NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from scipy.fftpack import fft



class MatplotPanel(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER, grid=True, xlim=None,
               ylim=None, title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style)
    
    # figure
    self.figure = Figure(tight_layout=True)
    self.axes = self.figure.add_subplot(111)
    # just a recommended style
    plt.style.use('ggplot')
    mpl.rcParams['agg.path.chunksize'] = 10000
    
    # our custom color map for spectrogram
    self.cmap = LinearSegmentedColormap(name='Custom',
                                        segmentdata={'red'  : [(0.0, 0.0, 0.0),
                                                               (0.7, 1.0, 1.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'green': [(0.0, 0.0, 0.0),
                                                               (0.7, 0.0, 0.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'blue' : [(0.0, 0.0, 0.0),
                                                               (0.7, 0.0, 0.0),
                                                               (1.0, 1.0, 1.0)],
    
                                                     'alpha': [(0.0, 0.0, 0.0),
                                                               (0.5, 0.0, 1.0),
                                                               (1.0, 1.0, 1.0)]
                                                     })
    
    # grid?
    self.axes.grid(grid)
    self.grid = grid
    # limits on x?
    if xlim:
      self.axes.set_xlim(xlim)
    # limits on y?
    if ylim:
      self.axes.set_ylim(ylim)
    # title?
    if title:
      self.axes.set_title(title)
    # label on x?
    if xlabel:
      self.axes.set_xlabel(xlabel)
    # label on y?
    if ylabel:
      self.axes.set_ylabel(ylabel)
    
    # canvas for integration in wxPython
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    # vertical box with toolbar and figure canvas
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.v_box)
    self.v_box.Add(item=self.toolbar, proportion=1, flag=wx.EXPAND)
    # self.v_box.AddSpacer(4)
    self.v_box.Add(item=self.canvas, proportion=1,
                   flag=wx.GROW)
  
  
  def plot(self, signal):
    t = np.arange(0.0, signal.length, (1.0 / signal.sample_rate))
    self.axes.plot(t, signal._signal)
    return self
  
  
  def spectrum(self, signal):
    
    # f: frequencies, pxx: peaks (amplitude)
    # f, pxx = sig.periodogram(x=signal, fs=self.signal.sample_rate,
    # scaling='spectrum')
    
    sig = signal._signal
    pxx = abs(fft(sig))
    pxx = pxx[:(len(pxx) / 2)]
    f = np.linspace(0.0, signal.sample_rate / 2, len(pxx))
    pxx = pxx / max(pxx)
    pxx = 20 * np.log10(1e-6 + pxx)
    
    # amp fix: sinus with amp x -> frequency with amp x
    # pxx = pxx / len(pxx)
    
    # f, pxx = sig.periodogram(signal, fs=self.signal.sample_rate)
    
    self.axes.plot(f, pxx, '-')
    self.axes.set_xscale('log')
    # self.axes.set_yscale('symlog')
    self.axes.set_xticks([20, 100, 200, 1000, 2000, 10000, 20000])
    self.axes.grid(self.grid, which='both', ls='-')
    self.axes.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    return self
  
  
  def spectrogram(self, signal):
    sig = signal._signal
    sig[sig == 0] = np.nan
    pxx, freq, t, im = self.axes.specgram(x=sig, NFFT=1024,
                                          Fs=signal.sample_rate, cmap='plasma')
    # pxx, freq, t = mlab.specgram(x=x, Fs=fs, NFFT=512)
    # self.axes.pcolormesh(t, freq, pxx, cmap=mpl.cm.hot)
    # self.axes.set_yscale('symlog')
    # self.axes.imshow(x)
    self.figure.colorbar(im).set_label('Intensity [dB]')
    return self
