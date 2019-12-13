#!/usr/bin/env python
#Boa:App:BoaApp

import wx

from frame import  main_frame

modules ={'Frame1': [0, '', u'frame/Frame1.py'],
 u'main_frame': [1, 'Main frame of Application', u'frame/main_frame.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = main_frame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
