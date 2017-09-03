# coding: UTF-8

import os

import wx

from const import *
from matplotplanel import MatplotPanel



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
    menu_file = wx.Menu()
    file_open = wx.MenuItem(id=wx.ID_OPEN, text="&Open\tCtrl+O",
                            help="Open a file with explorer",
                            kind=wx.ITEM_NORMAL)
    file_close = wx.MenuItem(id=wx.ID_EXIT, text="&Close\tCtrl+C",
                             help="Close the application", kind=wx.ITEM_NORMAL)
    menu_file.AppendItem(file_open)
    menu_file.AppendItem(file_close)
    menu_bar.Append(menu=menu_file, title="&File")
    self.SetMenuBar(menu_bar)
    
    self.Bind(wx.EVT_MENU, self.onQuit, file_close)
    self.Bind(wx.EVT_MENU, self.onOpen, file_open)
    
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
  
  
  def onOpen(self, event):
    if self.dlg.ShowModal() == wx.ID_OK:
      self.file_path = self.dlg.GetPath()
      self.SetStatusText("You chose following file: " + self.file_path)
  
  
  def onQuit(self, event):
    self.dlg.Destroy()
    self.Close()



class MainPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
    self.SetBackgroundColour("grey")
    
    self.matplot_panel1 = MatplotPanel(parent=self, size=(300, 100))
    self.matplot_panel2 = MatplotPanel(parent=self, size=(300, 100))
    
    # main centered box
    self.center_box = wx.BoxSizer()
    self.SetSizer(self.center_box)
    
    # vertical box for 2 matplot panels
    self.v_box = wx.BoxSizer(wx.VERTICAL)
    self.v_box.Add(item=self.matplot_panel1, proportion=0,
                   flag=wx.EXPAND | wx.SHAPED)
    self.v_box.Add(item=self.matplot_panel2, proportion=0,
                   flag=wx.EXPAND | wx.SHAPED)
    self.center_box.Add(item=self.v_box, proportion=1,
                        flag=wx.EXPAND | wx.SHAPED | wx.ALIGN_CENTER)
