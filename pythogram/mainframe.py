# coding: UTF-8

import wx

from const import *



class MainFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, parent=None, title=TITLE,
                      size=(WIDTH, HEIGHT),
                      style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX |
                            wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION |
                            wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_SHAPED,
                      name="main frame")
    self.SetBackgroundColour("black")
    self.SetMinClientSize((192, 108))
    self.Center()
    
    menu_bar = wx.MenuBar()
    self.SetMenuBar(menu_bar)
    
    self.main_panel = wx.Panel(parent=self, style=wx.BORDER_SUNKEN)
    self.main_panel.SetBackgroundColour("grey")
    self.main_box = wx.BoxSizer()
    self.main_box.Add(item=self.main_panel, proportion=1, flag=wx.EXPAND)
    self.SetSizer(self.main_box)
    
    self.CreateStatusBar(style=wx.BORDER_SUNKEN)
