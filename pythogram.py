import wx

from pythogram.mainframe import MainFrame



def main():
  app = wx.App(False)
  frame = MainFrame()
  frame.Show()
  app.MainLoop()



main()
