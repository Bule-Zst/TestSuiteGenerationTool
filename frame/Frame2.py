#Boa:Frame:Frame2

import wx

def create(parent):
    return Frame2(parent)

[wxID_FRAME2] = [wx.NewId() for _init_ctrls in range(1)]

class Frame2(wx.Frame):
    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, style=wx.DEFAULT_FRAME_STYLE, name='', parent=prnt, title='Frame2', pos=wx.Point(-1, -1), id=wxID_FRAME2, size=wx.Size(-1, -1))

    def __init__(self, parent):
        self._init_ctrls(parent)
