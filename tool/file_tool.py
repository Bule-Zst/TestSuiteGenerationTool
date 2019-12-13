import wx

defaultDir = ""


def showChooseFileDialog(frame, message, wildCrad=None):
    global defaultDir
    fileDialog = wx.FileDialog(frame, message, style=wx.FD_OPEN)
    if wildCrad is not None:
        fileDialog.SetWildcard( wildCrad )
    if defaultDir is not "":
        fileDialog.SetDirectory(defaultDir)
    dialogResult = fileDialog.ShowModal()
    file_path = ""
    if dialogResult == wx.ID_OK:
        file_path = fileDialog.GetPath()
        defaultDir = fileDialog.GetDirectory()
    fileDialog.Destroy()
    return file_path
