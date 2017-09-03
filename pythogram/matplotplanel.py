import numpy
import wx
from matplotlib.backends.backend_wxagg import (
  FigureCanvasWxAgg as FigureCanvas,
  NavigationToolbar2WxAgg as NavigationToolbar)
from matplotlib.figure import Figure



class MatplotPanel(wx.Panel):
  def __init__(self, parent, size=(100, 100), t=numpy.arange(0.0, 10, 0.1),
               signal=numpy.sin(numpy.arange(0.0, 10, 0.1))):
    wx.Panel.__init__(self, parent, size=size)
    
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.axes.plot(t, signal)
    self.canvas = FigureCanvas(parent=self, id=wx.NewId(), figure=self.figure)
    self.toolbar = NavigationToolbar(self.canvas)
    
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.vbox)
    self.vbox.Add(item=self.toolbar, proportion=0, flag=wx.EXPAND)
    self.vbox.Add(item=self.canvas, proportion=1,
                  flag=wx.LEFT | wx.TOP | wx.GROW)
