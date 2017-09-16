import os

import wx
from wx.lib.intctrl import IntCtrl
from wx.lib.masked.numctrl import NumCtrl

from const import *

ID_FILE_SIGNAL = wx.NewId()
ID_SAWTOOTH_SIGNAL = wx.NewId()
ID_SINE_SIGNAL = wx.NewId()
ID_SQUARE_SIGNAL = wx.NewId()
ID_TRIANGLE_SIGNAL = wx.NewId()
ID_WNOISE_SIGNAL = wx.NewId()



class ControlPanel(wx.Panel):
  def __init__(self, parent, size=(100, 100)):
    wx.Panel.__init__(self, parent=parent, size=size)
    
    self.dlg = wx.FileDialog(self, message="Choose a file",
                             defaultDir=os.getcwd(), defaultFile="",
                             wildcard=FILE_TYPES,
                             style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)
    
    bandpass = self.buildBandpassBox()
    test_signals = self.buildTestSignalsBox()
    output = self.buildOutput()
    
    left_vbox = wx.BoxSizer(wx.VERTICAL)
    left_vbox.Add(bandpass, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    left_vbox.Add(output, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
    
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(left_vbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    hbox.Add(test_signals, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    
    self.SetSizer(hbox)
  
  
  def buildBandpassBox(self):
    bandpass_box = wx.StaticBox(self, label="Bandpass filter")
    text_start_fq = wx.StaticText(bandpass_box, label="Low frequency:")
    self.input_start_fq = IntCtrl(bandpass_box)
    self.input_start_fq.SetMaxLength(5)
    text_end_fq = wx.StaticText(bandpass_box, label="High frequency:")
    self.input_end_fq = IntCtrl(bandpass_box)
    self.input_end_fq.SetMaxLength(5)
    button_apply_bandpass = wx.Button(bandpass_box,
                                      label="Apply bandpass filter")
    
    button_apply_bandpass.Bind(wx.EVT_BUTTON, self.onApplyBandpass)
    
    gridbag_sizer = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer.Add(text_start_fq, pos=(1, 1), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_start_fq, pos=(1, 3), flag=wx.EXPAND)
    gridbag_sizer.Add(text_end_fq, pos=(2, 1), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_end_fq, pos=(2, 3), flag=wx.EXPAND)
    gridbag_sizer.Add(button_apply_bandpass, pos=(4, 3), flag=wx.EXPAND)
    
    gridbag_sizer.AddGrowableCol(2)
    gridbag_sizer.AddGrowableRow(3)
    
    box_sizer = wx.StaticBoxSizer(bandpass_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer, proportion=1, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def buildTestSignalsBox(self):
    testsignals_box = wx.StaticBox(self, label="Generate test signals")
    
    text_freq = wx.StaticText(testsignals_box, label="Freq. (Hz):")
    self.input_freq = IntCtrl(testsignals_box)
    self.input_freq.SetMaxLength(5)
    self.input_freq.SetValue(440)
    text_len = wx.StaticText(testsignals_box, label="Len. (s):")
    self.input_len = NumCtrl(testsignals_box)
    self.input_len.SetLimitOnFieldChange(True)
    self.input_len.SetBounds(min=0.01, max=10.0)
    self.input_len.SetValue(1.0)
    text_amp = wx.StaticText(testsignals_box, label="Amp.:")
    self.input_amp = NumCtrl(testsignals_box)
    self.input_amp.SetLimitOnFieldChange(True)
    self.input_amp.SetBounds(min=0.01, max=10.0)
    self.input_amp.SetValue(1.0)
    text_fs = wx.StaticText(testsignals_box, label="Sample rate (Hz):")
    self.input_fs = IntCtrl(testsignals_box)
    self.input_fs.SetMaxLength(6)
    self.input_fs.SetValue(44100)
    
    button_file = wx.Button(testsignals_box, id=ID_FILE_SIGNAL,
                            label="Open file")
    button_sawtooth = wx.Button(testsignals_box, id=ID_SAWTOOTH_SIGNAL,
                                label="Sawtooth")
    button_sine = wx.Button(testsignals_box, id=ID_SINE_SIGNAL, label="Sine")
    button_square = wx.Button(testsignals_box, id=ID_SQUARE_SIGNAL,
                              label="Square")
    button_triangle = wx.Button(testsignals_box, id=ID_TRIANGLE_SIGNAL,
                                label="Triangle")
    button_wnoise = wx.Button(testsignals_box, id=ID_WNOISE_SIGNAL,
                              label="White noise")
    
    button_file.Bind(wx.EVT_BUTTON, self.onSignalButton, button_file)
    button_sawtooth.Bind(wx.EVT_BUTTON, self.onSignalButton, button_sawtooth)
    button_sine.Bind(wx.EVT_BUTTON, self.onSignalButton, button_sine)
    button_square.Bind(wx.EVT_BUTTON, self.onSignalButton, button_square)
    button_triangle.Bind(wx.EVT_BUTTON, self.onSignalButton, button_triangle)
    button_wnoise.Bind(wx.EVT_BUTTON, self.onSignalButton, button_wnoise)
    
    gridbag_sizer_top = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer_top.Add(text_freq, pos=(1, 1), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_freq, pos=(1, 3), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_fs, pos=(2, 1), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_fs, pos=(2, 3), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_len, pos=(3, 1), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_len, pos=(3, 3), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_amp, pos=(4, 1), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_amp, pos=(4, 3), flag=wx.EXPAND)
    gridbag_sizer_top.AddGrowableCol(2)
    
    gridbag_sizer_bottom = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer_bottom.Add(button_sine, pos=(1, 1), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_square, pos=(1, 2), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_sawtooth, pos=(1, 3), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_triangle, pos=(2, 1), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_wnoise, pos=(2, 2), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_file, pos=(2, 3), flag=wx.EXPAND)
    gridbag_sizer_bottom.AddGrowableCol(1)
    gridbag_sizer_bottom.AddGrowableCol(2)
    gridbag_sizer_bottom.AddGrowableCol(3)
    
    box_sizer = wx.StaticBoxSizer(testsignals_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer_top, proportion=1, flag=wx.EXPAND)
    box_sizer.AddStretchSpacer(1)
    box_sizer.Add(gridbag_sizer_bottom, proportion=0, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def buildOutput(self):
    output_box = wx.StaticBox(self, label="Information output")
    text_fs = wx.StaticText(output_box, label="Sample rate:")
    self.output_fs = IntCtrl(output_box)
    self.output_fs.SetMaxLength(5)
    text_len = wx.StaticText(output_box, label="Length:")
    self.output_len = NumCtrl(output_box)
    self.output_len.SetLimitOnFieldChange(True)
    self.output_len.SetBounds(min=0.01, max=10.0)
    
    gridbag_sizer = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer.Add(text_fs, pos=(1, 1), flag=wx.EXPAND)
    gridbag_sizer.Add(self.output_fs, pos=(1, 3), flag=wx.EXPAND)
    gridbag_sizer.Add(text_len, pos=(2, 1), flag=wx.EXPAND)
    gridbag_sizer.Add(self.output_len, pos=(2, 3), flag=wx.EXPAND)
    
    gridbag_sizer.AddGrowableCol(2)
    
    box_sizer = wx.StaticBoxSizer(output_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer, proportion=1, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def onApplyBandpass(self, event):
    top_parent = self.GetTopLevelParent()
    top_parent.main_panel.signal._low_cutoff = self.input_start_fq.GetValue()
    top_parent.main_panel.signal._high_cutoff = self.input_end_fq.GetValue()
  
  
  def onSignalButton(self, event):
    source = event.GetId()
    
    file_path = ""
    
    if source == ID_FILE_SIGNAL:
      if self.dlg.ShowModal() == wx.ID_OK:
        file_path = self.dlg.GetPath()
        self.GetTopLevelParent().SetStatusText(
          "You chose following file: " + file_path)
        signal = "File"
      else:
        file_path = None
        signal = None
    elif source == ID_SAWTOOTH_SIGNAL:
      signal = "Sawtooth"
    elif source == ID_SINE_SIGNAL:
      signal = "Sine"
    elif source == ID_SQUARE_SIGNAL:
      signal = "Square"
    elif source == ID_TRIANGLE_SIGNAL:
      signal = "Triangle"
    elif source == ID_WNOISE_SIGNAL:
      signal = "WNoise"
    else:
      signal = None
      print("Missing ID for event object")
    
    self.GetParent().changeSignal(signal,
                                  f=self.input_freq.GetValue(),
                                  l=self.input_len.GetValue(),
                                  amp=self.input_amp.GetValue(),
                                  fs=self.input_fs.GetValue(),
                                  path=file_path)
