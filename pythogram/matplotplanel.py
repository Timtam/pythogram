import matplotlib.pyplot as plt
import numpy
import wx
from matplotlib.backends.backend_wxagg import (
  FigureCanvasWxAgg as FigureCanvas,
  NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap



class MatplotPanel(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER,
               x=numpy.arange(0.0, 10, 0.1),
               y=numpy.sin(numpy.arange(0.0, 10, 0.1)), grid=True,
               ylim=None, title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style,
                      )
    
    self.figure = Figure(tight_layout=True)
    self.axes = self.figure.add_subplot(111)
    plt.style.use('ggplot')
    #self.figure.subplots_adjust(left=0.2, bottom=0.2)
    self.axes.plot(x, y)
    if grid:
      self.axes.grid(True)
    else:
      self.axes.grid(False)
    if ylim:
      self.axes.set_ylim(ylim)
    if title:
      self.axes.set_title(title)
    if xlabel:
      self.axes.set_xlabel(xlabel)
    if ylabel:
      self.axes.set_ylabel(ylabel)
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    # vertical box with toolbar and figure canvas
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.v_box)
    #self.v_box.Add(item=self.toolbar, proportion=1, flag=wx.EXPAND)
    #self.v_box.AddSpacer(4)
    self.v_box.Add(item=self.canvas, proportion=1,
                   flag= #wx.LEFT | wx.TOP |
                   wx.GROW
    )



class MatplotSpectrogram(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER,
               x=numpy.arange(0.0, 10, 0.1),
               y=numpy.sin(numpy.arange(0.0, 10, 0.1)), grid=True,
               ylim=None, title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style)
    
    self.figure = Figure(tight_layout=True)
    self.axes = self.figure.add_subplot(111)
    plt.style.use('ggplot')
    #self.figure.subplots_adjust(left=0.2, bottom=0.2)
    cmap = LinearSegmentedColormap(name='Test',
        segmentdata={'red':   [(0.0,  0.0, 0.0),
                               (0.7,  1.0, 1.0),
                               (1.0,  1.0, 1.0)],

                     'green': [(0.0,  0.0, 0.0),
                               (0.7,  0.0, 0.0),
                               (1.0,  1.0, 1.0)],

                     'blue':  [(0.0,  0.0, 0.0),
                               (0.7,  0.0, 0.0),
                               (1.0,  1.0, 1.0)],
                     
                     'alpha': [(0.0, 0.0, 0.0),
                               (0.7, 0.0, 1.0),
                               (1.0, 1.0, 1.0)]
                     })
    pxx, freq, t, cax = self.axes.specgram(x=x, Fs=44100, cmap=cmap, NFFT=512)
    if grid:
      self.axes.grid(True)
    else:
      self.axes.grid(False)
    if ylim:
      self.axes.set_ylim(ylim)
    if title:
      self.axes.set_title(title)
    if xlabel:
      self.axes.set_xlabel(xlabel)
    if ylabel:
      self.axes.set_ylabel(ylabel)
    self.figure.colorbar(cax).set_label('Intensity [dB]')
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    # vertical box with toolbar and figure canvas
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.v_box)
    self.v_box.Add(item=self.toolbar, proportion=1, flag=wx.EXPAND)
    #self.v_box.AddSpacer(4)
    self.v_box.Add(item=self.canvas, proportion=1,
                   flag=#wx.LEFT | wx.TOP |
                   wx.GROW
    )



class MatplotImage(wx.Panel):
  def __init__(self, parent, size=(0, 0), style=wx.BORDER,
               x=numpy.arange(0.0, 10, 0.1),
               y=numpy.sin(numpy.arange(0.0, 10, 0.1)), grid=True,
               ylim=None, title='', xlabel='', ylabel=''):
    wx.Panel.__init__(self, parent, size=size, style=style)
    
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    plt.style.use('ggplot')
    self.figure.subplots_adjust(left=0.2, bottom=0.2)
    
    X = [[-1, 0], [0.5, 1]]
    
    self.axes.imshow(X)
    
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    # vertical box with toolbar and figure canvas
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.v_box)
    self.v_box.Add(item=self.toolbar, proportion=1, flag=wx.EXPAND)
    self.v_box.AddSpacer(4)
    self.v_box.Add(item=self.canvas, proportion=1,
                   flag=#wx.LEFT | wx.TOP |
                   wx.GROW
    )