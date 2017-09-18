import matplotlib as mpl

mpl.use('WXAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import wx
from matplotlib.backends.backend_wxagg import (
  FigureCanvasWxAgg as FigureCanvas,
  NavigationToolbar2WxAgg as NavigationToolbar)
# from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from spectral_tool import SpectralTool



class MatplotPanel(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER, grid=True, xlim=None,
               ylim=None, title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style)
    
    # figure and subplot
    self.figure = Figure(tight_layout=True)
    self.axes = self.figure.add_subplot(111)
    # just a recommended style
    plt.style.use('ggplot')
    # when processing big arrays, it crashed sometimes...
    # this should prevent crashes when trying to show big data on diagrams
    mpl.rcParams['agg.path.chunksize'] = 10000
    
    self.grid = grid
    self.xlim = xlim
    self.ylim = ylim
    self.title = title
    self.xlabel = xlabel
    self.ylabel = ylabel
    self.colorbar = None
    
    self.setProperties()
    
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
  
  
  def setProperties(self):
    # grid?
    self.axes.grid(self.grid)
    # limits on x?
    if self.xlim:
      self.axes.set_xlim(self.xlim)
    # limits on y?
    if self.ylim:
      self.axes.set_ylim(self.ylim)
    # title?
    if self.title:
      self.axes.set_title(self.title)
    # label on x?
    if self.xlabel:
      self.axes.set_xlabel(self.xlabel)
    # label on y?
    if self.ylabel:
      self.axes.set_ylabel(self.ylabel)
  
  
  def setXLimits(self, lim=(0, 1)):
    self.xlim = lim
  
  
  def resetXLimits(self):
    self.xlim = None
  
  
  def plot(self, signal):
    self.axes.clear()
    self.setProperties()
    t = np.linspace(0.0, signal.length, len(signal.signal))
    self.axes.plot(t, signal.signal, '-')
    self.axes.grid(self.grid, ls='-')
    self.figure.canvas.draw()
    return self
  
  
  def plotSpectrum(self, signal):
    self.axes.clear()
    self.setProperties()
    # f: frequencies, pxx: peaks (amplitude)
    f, pxx = SpectralTool().spectrum(signal)
    
    self.axes.plot(f, pxx, '-')
    self.axes.set_xscale('log')
    # self.axes.set_yscale('symlog')
    self.axes.set_xticks([20, 100, 200, 1000, 2000, 10000, 20000])
    self.axes.grid(self.grid, which='both', ls='-')
    self.axes.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    self.figure.canvas.draw()
    return self
  
  
  def plotSpectrogram(self, signal, nfft=256):
    self.axes.clear()
    self.setProperties()
    f, t, pxx = SpectralTool().spectrogram(signal, nfft)
    
    # display calculated values
    im = self.axes.pcolormesh(t, f, pxx, cmap=mpl.cm.hot)
    
    self.axes.set_yscale('log')
    self.axes.set_yticks([20, 100, 200, 1000, 2000, 10000, 20000])
    self.axes.grid(self.grid, which='both', ls='-')
    self.axes.get_yaxis().set_major_formatter(ticker.ScalarFormatter())
    # create a colorbar or change mappable
    if self.colorbar is None:
      self.colorbar = self.figure.colorbar(im)
      self.colorbar.set_label('Intensity [dB FS]')
    else:
      self.colorbar.on_mappable_changed(im)
    self.figure.canvas.draw()
    return self
