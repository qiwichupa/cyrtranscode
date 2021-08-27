#!/usr/bin/env python3
# Cyrtranscode GUI Edition
# v1.0
# by Sergey Pavlov aka Qiwichupa

import tkinter as tk
import tkinter.ttk as ttk
import encodings
from cyrtranscode import Transcode


class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.text_input = tk.Text(self,height=10,width=80,font='Arial 10')
        self.text_input.grid(row=0, column=0, columnspan=2)
        self.sbi = ttk.Scrollbar(self,orient='vert',command=self.text_input.yview)
        self.text_input['yscrollcommand'] = self.sbi.set
        self.sbi.grid(row=0, column=2,sticky='ns')

        self.text_output = tk.Text(self,height=10,width=80,font='Arial 10')
        self.text_output.grid(row=1, column=0, columnspan=2)
        self.sbo = ttk.Scrollbar(self,orient='vert',command=self.text_output.yview)
        self.text_output['yscrollcommand'] = self.sbo.set
        self.sbo.grid(row=1, column=2,sticky='ns')

        encs = encodings.aliases.aliases.items()
        encs_list = []
        for i, e in encs:
            encs_list.append(e)
        encs_list = list(set(encs_list))
        encs_list.sort()
        encs_list = ['auto'] + encs_list

        self.enc_in_list = ttk.Combobox(self,values=encs_list,height=10)
        self.enc_in_list.set('auto')
        self.enc_in_list.bind("<<ComboboxSelected>>", self.lock_encodings)
        self.enc_in_list.grid(row=2, column=0)
        self.enc_out_list = ttk.Combobox(self,values=encs_list[1:],height=10,state=tk.DISABLED)
        self.enc_out_list.set('auto')
        self.enc_out_list.grid(row=3, column=0)

        self.show_codepage = tk.IntVar()
        self.show_codepage_checkbox = ttk.Checkbutton(self,text='Показывать кодировку',variable=self.show_codepage,onvalue=1,offvalue=0)
        self.show_codepage_checkbox.grid(row=2, column=1)

        self.trans_button = ttk.Button(self, text='Разобрать кракозябры', command=self.translate)
        self.trans_button.grid(row=3, column=1, columnspan=3)


    def lock_encodings(self,v):
        if self.enc_in_list.get() == 'auto':
            self.enc_out_list.config(state=tk.DISABLED)
            self.enc_in_list_last_state = 'auto'
            self.enc_out_list_last_state = self.enc_out_list.get()
            self.enc_out_list.set('auto')
        else:
            self.enc_out_list.config(state=tk.NORMAL)
            if self.enc_in_list_last_state == 'auto':
                self.enc_out_list.set(self.enc_out_list_last_state)
            self.enc_in_list_last_state = self.enc_in_list.get()

    def translate(self):
        trans = Transcode()
        self.text_output.delete('1.0', tk.END)
        text = self.text_input.get('1.0', tk.END)
        lines = text.splitlines()
        for line in lines:
            (string, codepage) = trans.transcode(line,self.enc_in_list.get(),self.enc_out_list.get())
            if self.show_codepage.get() == 1:
                codepage = ' ↔ '.join(codepage.split('|'))
                result_string = '[' + codepage + '] ' + string
            else:
                result_string = string
            self.text_output.insert(tk.END, result_string + '\n')



def main_window():
    root = tk.Tk()
    root.title('Cyrtranscoder GUI Ed. 1.0')
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()


if __name__ == "__main__":
    main_window()
