import wx
import  wx.lib.intctrl



class ControlPanel(wx.Panel):
  def __init__(self, parent, size=(100, 100)):
    wx.Panel.__init__(self, parent=parent, size=size)
    
    bandpass_box = wx.StaticBox(self, label="Bandpass filter")
    text_start_fq = wx.StaticText(bandpass_box, label="Low frequency:")
    self.input_start_fq = wx.wx.lib.intctrl.IntCtrl(bandpass_box)
    self.input_start_fq.SetMaxLength(5)
    text_end_fq = wx.StaticText(bandpass_box, label="High frequency:")
    self.input_end_fq = wx.wx.lib.intctrl.IntCtrl(bandpass_box)
    self.input_end_fq.SetMaxLength(5)
    
    low_fq_sizer = wx.BoxSizer(wx.HORIZONTAL)
    low_fq_sizer.Add(text_start_fq, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
    low_fq_sizer.AddStretchSpacer(1)
    low_fq_sizer.Add(self.input_start_fq, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
    
    high_fq_sizer = wx.BoxSizer(wx.HORIZONTAL)
    high_fq_sizer.Add(text_end_fq, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
    high_fq_sizer.AddStretchSpacer(1)
    high_fq_sizer.Add(self.input_end_fq, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)

    bandpass_sizer = wx.StaticBoxSizer(bandpass_box, wx.VERTICAL)
    bandpass_sizer.Add(low_fq_sizer, 0, wx.EXPAND)
    bandpass_sizer.Add(high_fq_sizer, 0, wx.EXPAND)
    
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(bandpass_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    
    self.SetSizer(hbox)