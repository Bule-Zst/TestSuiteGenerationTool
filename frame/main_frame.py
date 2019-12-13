# Boa:Frame:Frame1
import os

import wx
import wx.grid

import subprocess

from tool import file_tool, config_tool, dataTool


def create(parent):
    return Frame1(parent)


[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1BUTTON3,
 wxID_FRAME1BUTTON4, wxID_FRAME1INPUTBUTTON, wxID_FRAME1INPUTSTATICTEXT,
 wxID_FRAME1INPUTTEXTCTRL, wxID_FRAME1PANEL1, wxID_FRAME1STATICTEXT1,
 wxID_FRAME1TEXTCTRL1,
] = [wx.NewId() for _init_ctrls in range(11)]


def boolean(str):
    if type(str) is type(False):
        return str
    if str.lower() == "false":
        return False
    return True


class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(278, 58), size=wx.Size(708, 631),
              style=wx.DEFAULT_FRAME_STYLE, title='Combination Testing')
        self.SetClientSize(wx.Size(692, 592))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(692, 592),
              style=wx.TAB_TRAVERSAL)

        self.inputStaticText = wx.StaticText(id=wxID_FRAME1INPUTSTATICTEXT,
              label=u'input file path: ', name=u'inputStaticText',
              parent=self.panel1, pos=wx.Point(48, 27), size=wx.Size(84, 17),
              style=0)

        self.inputTextCtrl = wx.TextCtrl(id=wxID_FRAME1INPUTTEXTCTRL,
              name=u'inputTextCtrl', parent=self.panel1, pos=wx.Point(139, 25),
              size=wx.Size(442, 22), style=0, value=u'')

        self.inputButton = wx.Button(id=wxID_FRAME1INPUTBUTTON, label=u'select',
              name=u'inputButton', parent=self.panel1, pos=wx.Point(592, 23),
              size=wx.Size(48, 24), style=0)
        self.inputButton.Bind(wx.EVT_BUTTON, self.chooseInputFile,
              id=wxID_FRAME1INPUTBUTTON)

        self.staticText1 = wx.StaticText(id=wxID_FRAME1STATICTEXT1,
              label=u'generate: ', name='staticText1', parent=self.panel1,
              pos=wx.Point(144, 76), size=wx.Size(58, 17), style=0)

        self.button1 = wx.Button(id=wxID_FRAME1BUTTON1, label=u'json',
              name='button1', parent=self.panel1, pos=wx.Point(224, 73),
              size=wx.Size(75, 24), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.jsonGenerate,
              id=wxID_FRAME1BUTTON1)

        self.button2 = wx.Button(id=wxID_FRAME1BUTTON2, label=u'xml',
              name='button2', parent=self.panel1, pos=wx.Point(323, 73),
              size=wx.Size(75, 24), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.xmlGenerate,
              id=wxID_FRAME1BUTTON2)

        self.button3 = wx.Button(id=wxID_FRAME1BUTTON3, label=u'txt',
              name='button3', parent=self.panel1, pos=wx.Point(422, 72),
              size=wx.Size(75, 24), style=0)
        self.button3.Bind(wx.EVT_BUTTON, self.txtGenerate,
              id=wxID_FRAME1BUTTON3)

        # self.textCtrl1 = wx.TextCtrl(id=wxID_FRAME1TEXTCTRL1, name='textCtrl1',
        #       parent=self.panel1, pos=wx.Point(74, 112), size=wx.Size(542, 416),
        #       style=wx.TE_MULTILINE, value='textCtrl1')
        self.textCtrl1 = wx.TextCtrl(self.panel1, -1, "",
                                pos=wx.Point(74, 112), size=wx.Size(542, 416),
                                style=wx.TE_MULTILINE)

        self.button4 = wx.Button(id=wxID_FRAME1BUTTON4, label=u'save',
              name='button4', parent=self.panel1, pos=wx.Point(200, 548),
              size=wx.Size(275, 24), style=0)
        self.button4.Bind(wx.EVT_BUTTON, self.saveContent,
              id=wxID_FRAME1BUTTON4)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.showCoverageRemaind = boolean(config_tool.get("showCoverageRemaind", True))

    def chooseInputFile(self, event):
        filesFilter = "json file(*.json)|*.json|" \
                      "xml file(*.xml)|*.xml|" \
                      "txt file(*.txt)|*.txt"
        self.inputfile_path = file_tool.showChooseFileDialog(self, 'choose input file', filesFilter)
        self.inputTextCtrl.SetLabel(self.inputfile_path)

    def chooseOutputFile(self, event):
        pass
        # filesFilter = "json file(*.json)|*.json|" \
        #               "xml file(*.xml)|*.xml|" \
        #               "txt file(*.txt)|*.txt"
        # self.outputfile_path = file_tool.showChooseFileDialog(self, 'choose output file', filesFilter)
        # self.outputTextCtrl.SetLabel(self.outputfile_path)
        # if self.showCoverageRemaind:
        #     remaindDialog = wx.MessageDialog(None,
        #                                      'the raw file will be overwritten, please backup\nDo not show again?',
        #                                      "Remaind", wx.YES_NO or wx.ICON_QUESTION)
        #     result = remaindDialog.ShowModal()
        #     if result == wx.ID_YES:
        #         self.showCoverageRemaind = False
        #         config_tool.set("showCoverageRemaind", False)

    def generateCombinationTestData( self, choose ):
        try:
            self.inputfile_path = self.inputTextCtrl.GetValue()

            jsonDict = None
            if self.inputfile_path.__contains__(".json"):
                jsonDict = dataTool.jsonFile2JsonDict(self.inputfile_path)
            if self.inputfile_path.__contains__(".xml"):
                jsonDict = dataTool.xmlFile2JsonDict(self.inputfile_path)
            if self.inputfile_path.__contains__(".txt"):
                jsonDict = dataTool.txtFile2JsonDict(self.inputfile_path)
            req = dataTool.jsonDict2Requirement(jsonDict)
            req.print("tmp.txt")
            command = "generate.exe tmp.txt"
            result = os.popen(command)
            # p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            # for r in p.stdout.readlines():
            for r in result:
                # r = str(r, encoding="utf-8")
                # print( r )
                r = r.replace("\n", "")
                if not r.__contains__(":"):
                    continue
                index = r.index(':')
                r = r[index + 2:]
                testcase = r.split('\t')
                req.addTestcase(testcase)
            if choose == 0:
                res = req.getJsonOutput()
            if choose == 1:
                res = req.getXmlOutput()
            if choose == 2:
                res = req.getTxtOutput()
            self.textCtrl1.SetValue( res )
        except Exception as e:
            pass
            # wx.MessageBox( e )

    def jsonGenerate(self, event):
        self.generateCombinationTestData(0)

    def xmlGenerate(self, event):
        self.generateCombinationTestData(1)

    def txtGenerate(self, event):
        self.generateCombinationTestData(2)

    def saveContent(self, event):
        fileDialog = wx.FileDialog(self, "save file", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        dialogResult = fileDialog.ShowModal()
        if dialogResult != wx.ID_OK:
            return
        with open( fileDialog.GetPath(), "w", encoding="utf-8" ) as fout:
            fout.write( self.textCtrl1.GetValue() )
