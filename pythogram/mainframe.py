# coding: UTF-8

import importlib
import os

import wx

from const import *
from controlpanel import ControlPanel
from matplotplanel import MatplotPanel
from signals import Sine



class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, parent=None, title=TITLE,
                      size=(WIDTH, HEIGHT),
                      style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                            wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION |
                            wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_SHAPED)
    self.SetBackgroundColour("black")
    self.SetMinClientSize((1100, 800))
    self.Center()
    
    menu_bar = wx.MenuBar()
    menu_file = wx.Menu()
    # file_open = wx.MenuItem(id=wx.ID_OPEN, text="&Open file\tCtrl+O",
    #                         help="Open a file with explorer",
    #                         kind=wx.ITEM_NORMAL)
    file_close = wx.MenuItem(id=wx.ID_EXIT, text="&Close\tCtrl+C",
                             help="Close the application", kind=wx.ITEM_NORMAL)
    # menu_file.AppendItem(file_open)
    menu_file.AppendItem(file_close)
    menu_bar.Append(menu=menu_file, title="&File")
    self.SetMenuBar(menu_bar)
    
    self.Bind(wx.EVT_MENU, self.onQuit, file_close)
    # self.Bind(wx.EVT_MENU, self.onOpenFile, file_open)
    
    self.dlg = wx.FileDialog(self, message="Choose a file",
                             defaultDir=os.getcwd(), defaultFile="",
                             wildcard=FILE_TYPES,
                             style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)

    self.status_bar = self.CreateStatusBar(style=wx.BORDER_SUNKEN)
    self.main_panel = MainPanel(parent=self)
    self.main_box = wx.BoxSizer()
    self.main_box.Add(item=self.main_panel, proportion=1, flag=wx.EXPAND)
    self.SetSizer(self.main_box)
    
    self.status_bar.SetStatusText("Initialized")
  
  
  # def onOpenFile(self, event):
  #   if self.dlg.ShowModal() == wx.ID_OK:
  #     self.file_path = self.dlg.GetPath()
  #     self.SetStatusText("You chose following file: " + self.file_path)
  
  
  def onQuit(self, event):
    self.dlg.Destroy()
    self.Close()



class MainPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
    self.SetBackgroundColour("white")
    
    # control panel for user input/output
    self.control_panel = ControlPanel(self)
    
    # create sine signal
    self.signal = Sine()
    self.nfft = 256
    
    self.createMatplotPanels()
    
    # the main box sizer
    main_hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.SetSizer(main_hbox)
    
    # left box containing control panel and spectrogram
    left_vbox = wx.BoxSizer(wx.VERTICAL)
    left_vbox.Add(item=self.control_panel, proportion=0, flag=wx.EXPAND)
    left_vbox.Add(item=self.matplot_panel3, proportion=1, flag=wx.EXPAND)
    
    # right box for signal and spectrum
    right_vbox = wx.BoxSizer(wx.VERTICAL)
    right_vbox.Add(item=self.matplot_panel1, proportion=1, flag=wx.EXPAND)
    right_vbox.Add(item=self.matplot_panel2, proportion=1, flag=wx.EXPAND)
    
    # all together in main box
    main_hbox.Add(item=left_vbox, proportion=5, flag=wx.EXPAND)
    main_hbox.Add(item=right_vbox, proportion=4, flag=wx.EXPAND)
  
  
  def createMatplotPanels(self):
    # plot the signal
    self.matplot_panel1 = MatplotPanel(parent=self, xlim=(0.0, 1.0),
                                       # ylim=(-1.0, 1.0),
                                       title='Waveform',
                                       xlabel='Time in seconds (s)',
                                       ylabel='Amplitude')
    # spectrum
    self.matplot_panel2 = MatplotPanel(parent=self, xlim=(20, 24000),
                                       # ylim=(0, 1e6),
                                       title='Spectrum',
                                       xlabel='Frequency in hertz (Hz)',
                                       ylabel='Intensity in decibel '
                                              'relative\n to full scale (db '
                                              'FS)')
    # spectrogram
    self.matplot_panel3 = MatplotPanel(parent=self, ylim=(20, 24000),
                                       title='Spectrogram',
                                       xlabel='Time in seconds (s)',
                                       ylabel='Frequency in hertz (Hz)')
  
  
  def plotSignal(self, signal=None, nfft=256):
    # a progress dialog when processing takes much time (i.e. songs)
    dlg = wx.ProgressDialog(parent=self, message="Processing signal plot...",
                            title="Processing info", maximum=3)
    # plot the signal
    self.matplot_panel1 = self.matplot_panel1.plot(signal=signal)
    dlg.Update(1, "Processing spectrum...")
    # spectrum
    self.matplot_panel2 = self.matplot_panel2.plotSpectrum(signal=signal)
    dlg.Update(2, "Processing spectrogram...")
    # spectrogram
    self.matplot_panel3 = self.matplot_panel3.plotSpectrogram(signal=signal,
                                                              nfft=nfft)
    dlg.Update(3, "Complete")
    dlg.Destroy()
  
  
  def changeSignal(self, signal, f=440.0, l=1.0, amp=1.0, fs=44100, path=None):
    if signal is None or path is None:
      return
    signal_str = signal
    try:
      signals_module = importlib.import_module('.signals', 'pythogram')
      try:
        if signal in ["Sine", "Square", "Sawtooth", "Triangle"]:
          self.signal = getattr(signals_module, signal)(freq=f, l=l, amp=amp,
                                                        srate=fs)
          signal_str = signal + ", F: " + str(f) + " Hz, FS: " + str(
            fs) + " Hz, Len: " + str(l) + " s, Amp: " + str(amp)
        elif signal == "WNoise":
          self.signal = getattr(signals_module, signal)(l=l, amp=amp, srate=fs)
          signal_str = "White Noise, FS: " + str(
            fs) + " Hz, Len: " + str(l) + " s, Amp: " + str(amp)
        
        elif signal == "File" and path is not None:
          self.signal = getattr(signals_module, signal)(path)
          signal_str = path + ", FS: " + str(
            self.signal.sample_rate) + " Hz, Len: " + str(self.signal.length)
      except AttributeError:
        print("Class does not exist")
    except ImportError:
      print("Module does not exist")
    self.GetTopLevelParent().status_bar.SetStatusText(
      "You have chosen the following signal: " + signal_str)
    self.plotSignal(self.signal, self.nfft)
    self.setInformation(self.signal)
  
  
  def setInformation(self, signal):
    if self.control_panel is not None:
      self.control_panel.output_fs.SetLabel(str(signal.sample_rate))
      self.control_panel.output_len.SetLabel(str(signal.length))
