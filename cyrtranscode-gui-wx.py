#!/usr/bin/env python3
# Cyrtranscoder GUI Edition
# v1.0
# by Sergey Pavlov aka Qiwichupa

import encodings
import wx
from cyrtranscode import Transcode


class MainWindow(wx.Frame):

    enc_in_list_last_state = 'auto'
    enc_out_list_last_state = 'auto'

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.text_input  = wx.TextCtrl(self, size=(600, 200), style=wx.TE_MULTILINE | wx.HSCROLL)
        self.text_output = wx.TextCtrl(self, size=(600, 200), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        self.enc_in_list  = wx.ComboBox(self, choices=self.get_encs_list(), value='auto')
        self.enc_out_list = wx.ComboBox(self, choices=self.get_encs_list(), value='auto')
        self.enc_out_list.Disable()

        self.show_codepage_checkbox = wx.CheckBox(self, label='Показывать кодировку')
        self.trans_button = wx.Button(self, label='Разобрать кракозябры')
        self.trans_button.Bind(wx.EVT_BUTTON, self.translate)

        self.enc_in_list.Bind(wx.EVT_COMBOBOX, self.lock_encodings)

        sizer = wx.GridBagSizer()
        sizer.Add(self.text_input,      pos=(0, 0), span=(1, 2), flag=wx.EXPAND|wx.LEFT)
        sizer.Add(self.text_output,     pos=(1, 0), span=(1, 2), flag=wx.EXPAND|wx.LEFT)
        sizer.Add(self.enc_in_list, pos=(2, 0), flag=wx.LEFT)
        sizer.Add(self.show_codepage_checkbox, pos=(2, 1), flag=wx.RIGHT)
        sizer.Add(self.enc_out_list, pos=(3, 0), flag=wx.LEFT)
        sizer.Add(self.trans_button, pos=(3, 1), flag=wx.RIGHT)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Fit()
        self.Show(True)

    def change_frame_size(self, width, height):
        self.SetSize(wx.Size(width, height))

    def get_encs_list(self):
        encs = encodings.aliases.aliases.items()
        encs_list = []
        for i, e in encs:
            encs_list.append(e)
        encs_list = list(set(encs_list))
        encs_list.sort()
        encs_list = ['auto'] + encs_list
        return encs_list

    def lock_encodings(self, event):
        if self.enc_in_list.GetStringSelection() == 'auto':
            self.enc_out_list.Disable()
            self.enc_in_list_last_state = 'auto'
            self.enc_out_list_last_state = self.enc_out_list.GetStringSelection()
            self.enc_out_list.SetValue('auto')
        else:
            self.enc_out_list.Enable()
            if self.enc_in_list_last_state == 'auto':
                self.enc_out_list.SetValue(self.enc_out_list_last_state)
            self.enc_in_list_last_state = self.enc_in_list.GetStringSelection()

    def translate(self, event):
        trans = Transcode()
        self.text_output.Clear()
        text = self.text_input.GetValue()
        lines = text.splitlines()
        enc_in = self.enc_in_list_last_state
        enc_out = self.enc_out_list_last_state
        print(enc_in, enc_out)
        for line in lines:
            (string, codepage) = trans.transcode(line, enc_in, enc_out)
            if self.show_codepage_checkbox.GetValue():
                codepage = ' ↔ '.join(codepage.split('|'))
                result_string = '[' + codepage + '] ' + string
            else:
                result_string = string
            self.text_output.AppendText(result_string + '\n')

app = wx.App(False)
ver='1.1.1'
title='cyrtranscode v.{}'.format(ver)
frame = MainWindow(None, title)
app.MainLoop()