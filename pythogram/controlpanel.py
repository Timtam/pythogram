import os

import wx
from wx.lib.masked import NumCtrl

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
    
    self.signal_status_text = None
    self.dlg = wx.FileDialog(self, message="Choose a file",
                             defaultDir=os.getcwd(), defaultFile="",
                             wildcard=FILE_TYPES,
                             style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)
    
    bandpass = self.buildBandpassBox()
    time_options = self.buildTimeOptions()
    test_signals = self.buildTestSignalsBox()
    output = self.buildOutput()
    
    left_vbox = wx.BoxSizer(wx.VERTICAL)
    left_vbox.Add(test_signals, proportion=0, flag=wx.EXPAND)
    left_vbox.Add(output, proportion=0, flag=wx.EXPAND)
    
    right_vbox = wx.BoxSizer(wx.VERTICAL)
    right_vbox.Add(bandpass, proportion=0, flag=wx.EXPAND)
    right_vbox.AddStretchSpacer(1)
    right_vbox.Add(time_options, proportion=0, flag=wx.EXPAND)
    
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(left_vbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    hbox.Add(right_vbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    
    self.SetSizer(hbox)
    
    self.Fit()
    self.SetMinSize(self.GetSize())
  
  
  def buildBandpassBox(self):
    bandpass_box = wx.StaticBox(self, label="Bandpass filter")
    text_start_fq = wx.StaticText(bandpass_box, label="Low cutoff:")
    self.input_start_fq = NumCtrl(bandpass_box, value=20, integerWidth=5,
                                  fractionWidth=0, allowNegative=False, min=20,
                                  max=20000)
    text_end_fq = wx.StaticText(bandpass_box, label="High cutoff:")
    self.input_end_fq = NumCtrl(bandpass_box, value=20000.0, integerWidth=5,
                                fractionWidth=0, allowNegative=False, min=100,
                                max=25000)
    button_apply_bandpass = wx.Button(bandpass_box,
                                      label="Apply bandpass filter")
    button_reset_bandpass = wx.Button(bandpass_box, label="Delete bandpass")
    
    button_apply_bandpass.Bind(wx.EVT_BUTTON, self.onApplyBandpass)
    button_reset_bandpass.Bind(wx.EVT_BUTTON, self.onResetBandpass)
    
    gridbag_sizer = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer.Add(text_start_fq, pos=(0, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_start_fq, pos=(0, 2), flag=wx.EXPAND)
    gridbag_sizer.Add(text_end_fq, pos=(1, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_end_fq, pos=(1, 2), flag=wx.EXPAND)
    gridbag_sizer.Add(button_reset_bandpass, pos=(3, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(button_apply_bandpass, pos=(3, 2), flag=wx.EXPAND)
    
    gridbag_sizer.AddGrowableCol(1)
    # gridbag_sizer.AddGrowableRow(3)
    
    box_sizer = wx.StaticBoxSizer(bandpass_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer, proportion=1, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def buildTimeOptions(self):
    time_box = wx.StaticBox(self, label="Displayed time limits")
    text_start_time = wx.StaticText(time_box, label="Start:")
    self.input_start_time = NumCtrl(time_box, value=0.0, integerWidth=3,
                                    fractionWidth=2, allowNegative=False,
                                    min=0.00)
    text_end_time = wx.StaticText(time_box, label="End:")
    self.input_end_time = NumCtrl(time_box, value=1.0, integerWidth=3,
                                  fractionWidth=2, allowNegative=False,
                                  min=0.01)
    button_apply_time = wx.Button(time_box, label="Apply time limits")
    button_reset_time = wx.Button(time_box, label="Reset time limits")
    
    button_apply_time.Bind(wx.EVT_BUTTON, self.onApplyTime)
    button_reset_time.Bind(wx.EVT_BUTTON, self.onResetTime)
    
    gridbag_sizer = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer.Add(text_start_time, pos=(0, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_start_time, pos=(0, 2), flag=wx.EXPAND)
    gridbag_sizer.Add(text_end_time, pos=(1, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.input_end_time, pos=(1, 2), flag=wx.EXPAND)
    gridbag_sizer.Add(button_reset_time, pos=(3, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(button_apply_time, pos=(3, 2), flag=wx.EXPAND)
    
    gridbag_sizer.AddGrowableCol(1)
    # gridbag_sizer.AddGrowableRow(3)
    
    box_sizer = wx.StaticBoxSizer(time_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer, proportion=1, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def buildTestSignalsBox(self):
    testsignals_box = wx.StaticBox(self, label="Generate test signals")
    
    text_freq = wx.StaticText(testsignals_box, label="Freq. (Hz):")
    self.input_freq = NumCtrl(testsignals_box, value=440.0, integerWidth=5,
                              fractionWidth=1, allowNegative=False, min=1.0,
                              max=50000.0)
    text_len = wx.StaticText(testsignals_box, label="Len. (s):")
    self.input_len = NumCtrl(testsignals_box, value=2.0, integerWidth=3,
                             fractionWidth=2, allowNegative=False, min=0.10,
                             max=100.00)
    text_amp = wx.StaticText(testsignals_box, label="Amp.:")
    self.input_amp = NumCtrl(testsignals_box, value=1.0, integerWidth=2,
                             fractionWidth=2, allowNegative=False, min=0.01,
                             max=10.00)
    text_fs = wx.StaticText(testsignals_box, label="Sample rate (Hz):")
    self.input_fs = NumCtrl(testsignals_box, value=44100, integerWidth=6,
                            fractionWidth=0, allowNegative=False, min=1.0,
                            max=200000.0)
    text_fft = wx.StaticText(testsignals_box, label="FFT size:")
    self.input_fft = wx.ComboBox(testsignals_box, value='1024',
                                 choices=['16', '32', '64', '128', '256', '512',
                                          '1024', '2048', '4096', '8192',
                                          '16384', '32768', '65536'])
    
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
    gridbag_sizer_top.Add(text_freq, pos=(0, 0), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_freq, pos=(0, 2), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_fs, pos=(1, 0), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_fs, pos=(1, 2), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_len, pos=(2, 0), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_len, pos=(2, 2), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_amp, pos=(3, 0), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_amp, pos=(3, 2), flag=wx.EXPAND)
    gridbag_sizer_top.Add(text_fft, pos=(5, 0), flag=wx.EXPAND)
    gridbag_sizer_top.Add(self.input_fft, pos=(5, 2), flag=wx.EXPAND)
    gridbag_sizer_top.AddGrowableCol(1)
    
    gridbag_sizer_bottom = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer_bottom.Add(button_sine, pos=(0, 0), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_square, pos=(0, 1), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_sawtooth, pos=(0, 2), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_triangle, pos=(1, 0), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_wnoise, pos=(1, 1), flag=wx.EXPAND)
    gridbag_sizer_bottom.Add(button_file, pos=(1, 2), flag=wx.EXPAND)
    gridbag_sizer_bottom.AddGrowableCol(0)
    gridbag_sizer_bottom.AddGrowableCol(1)
    gridbag_sizer_bottom.AddGrowableCol(2)
    
    box_sizer = wx.StaticBoxSizer(testsignals_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer_top, proportion=1, flag=wx.EXPAND)
    box_sizer.AddSpacer(5)
    box_sizer.Add(gridbag_sizer_bottom, proportion=0, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def buildOutput(self):
    output_box = wx.StaticBox(self, label="Information output")
    text_fs = wx.StaticText(output_box, label="Sample rate:")
    self.output_fs = wx.StaticText(output_box, label="000000")
    text_len = wx.StaticText(output_box, label="Length:")
    self.output_len = wx.StaticText(output_box, label="0000")
    
    gridbag_sizer = wx.GridBagSizer(vgap=5, hgap=5)
    gridbag_sizer.Add(text_fs, pos=(0, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.output_fs, pos=(0, 2), flag=wx.EXPAND)
    gridbag_sizer.Add(text_len, pos=(1, 0), flag=wx.EXPAND)
    gridbag_sizer.Add(self.output_len, pos=(1, 2), flag=wx.EXPAND)
    
    # gridbag_sizer.AddGrowableCol(2)
    
    box_sizer = wx.StaticBoxSizer(output_box, wx.VERTICAL)
    box_sizer.Add(gridbag_sizer, proportion=1, flag=wx.EXPAND)
    
    return box_sizer
  
  
  def onApplyBandpass(self, event):
    if self.input_end_time.GetValue() <= self.input_start_time.GetValue():
      print("End time needs to be greater than start time")
      return
    parent = self.GetParent()
    parent.signal.low_cutoff = self.input_start_fq.GetValue()
    parent.signal.high_cutoff = self.input_end_fq.GetValue()
    if self.signal_status_text is None:
      self.signal_status_text = self.GetTopLevelParent().status_bar.GetStatusText()
    self.GetTopLevelParent().status_bar.SetStatusText(
      self.signal_status_text +
      " - Bandpass: Low: " + str(parent.signal.low_cutoff) + " Hz, "
                                                             "High: " + str(
        parent.signal.high_cutoff) + " Hz")
    parent.plotSignal(parent.signal, parent.nfft)
  
  
  def onResetBandpass(self, event):
    parent = self.GetParent()
    parent.signal._low_cutoff = None
    parent.signal._high_cutoff = None
    if self.signal_status_text is None:
      self.signal_status_text = self.GetTopLevelParent().status_bar.GetStatusText()
    self.GetTopLevelParent().status_bar.SetStatusText(
      self.signal_status_text +
      " - Bandpass: None")
    parent.plotSignal(parent.signal, parent.nfft)
  
  
  def onApplyTime(self, event):
    dlg = wx.ProgressDialog(parent=self, message="Processing...",
                            title="Processing info", maximum=1)
    parent = self.GetParent()
    parent.matplot_panel1.setXLimits(
      (self.input_start_time.GetValue(), self.input_end_time.GetValue()))
    parent.matplot_panel1.plot(parent.signal)
    parent.matplot_panel3.setXLimits(
      (self.input_start_time.GetValue(), self.input_end_time.GetValue()))
    parent.matplot_panel3.plotSpectrogram(parent.signal, parent.nfft)
    dlg.Update(1, "Complete")
    dlg.Destroy()
  
  
  def onResetTime(self, event):
    dlg = wx.ProgressDialog(parent=self, message="Processing...",
                            title="Processing info", maximum=1)
    parent = self.GetParent()
    parent.matplot_panel1.setXLimits((0.0, 1.0))
    parent.matplot_panel1.plot(parent.signal)
    parent.matplot_panel3.resetXLimits()
    parent.matplot_panel3.plotSpectrogram(parent.signal, parent.nfft)
    dlg.Update(1, "Complete")
    dlg.Destroy()
  
  
  def onSignalButton(self, event):
    source = event.GetId()
    
    file_path = ""
    
    if source == ID_FILE_SIGNAL:
      if self.GetTopLevelParent().dlg.ShowModal() == wx.ID_OK:
        file_path = self.GetTopLevelParent().dlg.GetPath()
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
    
    self.signal_status_text = None
    self.GetParent().nfft = int(self.input_fft.GetValue())
    self.GetParent().changeSignal(signal,
                                  f=self.input_freq.GetValue(),
                                  l=self.input_len.GetValue(),
                                  amp=self.input_amp.GetValue(),
                                  fs=self.input_fs.GetValue(),
                                  path=file_path)
