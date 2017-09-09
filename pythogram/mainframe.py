# coding: UTF-8

import os

import numpy
import wx
from scipy import signal

from const import *
from matplotplanel import MatplotPanel, MatplotSpectrogram, MatplotImage
from signals.sine import SineSignal
from controlpanel import ControlPanel



class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, parent=None, title=TITLE,
                      size=(WIDTH, HEIGHT),
                      style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                            wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION |
                            wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_SHAPED)
    self.SetBackgroundColour("black")
    self.SetMinClientSize((192, 108))
    self.Center()
    
    menu_bar = wx.MenuBar()
    menu_file = wx.Menu()
    file_open = wx.MenuItem(id=wx.ID_OPEN, text="&Open file\tCtrl+O",
                            help="Open a file with explorer",
                            kind=wx.ITEM_NORMAL)
    file_close = wx.MenuItem(id=wx.ID_EXIT, text="&Close\tCtrl+C",
                             help="Close the application", kind=wx.ITEM_NORMAL)
    menu_file.AppendItem(file_open)
    menu_file.AppendItem(file_close)
    menu_bar.Append(menu=menu_file, title="&File")
    self.SetMenuBar(menu_bar)
    
    self.Bind(wx.EVT_MENU, self.onQuit, file_close)
    self.Bind(wx.EVT_MENU, self.onOpenFile, file_open)
    
    self.dlg = wx.FileDialog(self, message="Choose a file",
                             defaultDir=os.getcwd(), defaultFile="",
                             wildcard=FILE_TYPES,
                             style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)
    
    self.main_panel = MainPanel(parent=self)
    self.main_box = wx.BoxSizer()
    self.main_box.Add(item=self.main_panel, proportion=1, flag=wx.EXPAND)
    self.SetSizer(self.main_box)
    
    self.status_bar = self.CreateStatusBar(style=wx.BORDER_SUNKEN)
    self.SetStatusText("Initialized")
  
  
  def onOpenFile(self, event):
    if self.dlg.ShowModal() == wx.ID_OK:
      self.file_path = self.dlg.GetPath()
      self.SetStatusText("You chose following file: " + self.file_path)
  
  
  def onQuit(self, event):
    self.dlg.Destroy()
    self.Close()



class MainPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
    self.SetBackgroundColour("white")
    
    self.control_panel = ControlPanel(self)
    
    # create sine signal and spectrum
    self.sinus = SineSignal(freq=7648.0, l=1.0, amp=0.8, srate=44100)
    t = numpy.arange(0.0, self.sinus.length, (1.0 / self.sinus.sample_rate))
    freqz, amp = signal.periodogram(self.sinus.signal, self.sinus.sample_rate)
    
    # plot the signal and its spectrum
    self.matplot_panel1 = MatplotPanel(parent=self, x=t, y=self.sinus.signal,
                                       ylim=(-1.0, 1.0),
                                       title='Signal', xlabel='Time',
                                       ylabel='Amplitude')
    
    self.matplot_panel2 = MatplotPanel(parent=self, x=freqz, y=amp,
                                       ylim=(-0.1, 1.0),
                                       title='Spectrum', xlabel='Frequency',
                                       ylabel='Amplitude')
    
    self.matplot_panel3 = MatplotSpectrogram(parent=self, x=self.sinus.signal,
                                             # y=amp,
                                             #ymin=-0.1, ymax=self.sinus.sample_rate/2,
                                             title='Spectrogram',
                                             xlabel='Time',
                                             ylabel='Frequency')
    
    self.main_vbox = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(self.main_vbox)

    self.left_top_box = wx.BoxSizer()
    self.left_top_box.Add(item=self.control_panel, proportion=1, flag=wx.EXPAND)
    
    self.right_top_vbox = wx.BoxSizer(wx.VERTICAL)
    self.right_top_vbox.Add(item=self.matplot_panel1, proportion=1, flag=wx.EXPAND)
    self.right_top_vbox.Add(item=self.matplot_panel2, proportion=1, flag=wx.EXPAND)
    
    self.top_hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.top_hbox.Add(item=self.left_top_box, proportion=3, flag=wx.EXPAND)
    self.top_hbox.Add(item=self.right_top_vbox, proportion=2, flag=wx.EXPAND)
    
    self.bottom_box = wx.BoxSizer()
    self.bottom_box.Add(item=self.matplot_panel3, proportion=1, flag=wx.EXPAND)

    self.main_vbox.Add(item=self.top_hbox, proportion=6, flag=wx.EXPAND)
    self.main_vbox.Add(item=self.bottom_box, proportion=5, flag=wx.EXPAND)