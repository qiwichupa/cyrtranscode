#!/usr/bin/env python3
# Cyrtranscoder GUI Edition
# v1.0
# by Sergey Pavlov aka Qiwichupa

import tkinter as tk
import tkinter.ttk as ttk
import regex
import encodings

class Transcode:

    def transcode(self, text, enc1='auto', enc2='auto'):
        if text.strip() == '':
            return('','Null')
        else:
            encs = encodings.aliases.aliases.items()
            strings = []
            encs_combos = []
            if enc1 == 'auto' and enc2 == 'auto': 
                for i, enc1 in encs:
                    for i, enc2 in encs:
                        try:
                            strings.append(text.encode(enc1).decode(enc2))
                            encs_combos.append(enc1 + '|' + enc2)
                        except:
                            pass
            elif enc1 != 'auto' and enc2 != 'auto':
                try:
                    strings.append(text.encode(enc1).decode(enc2))
                    encs_combos.append(enc1 + '|' + enc2)
                except:
                    pass
            else:
                if enc1 == 'auto':
                    for i, enc1 in encs:
                        try:
                            strings.append(text.encode(enc1).decode(enc2))
                            encs_combos.append(enc1 + '|' + enc2)
                        except:
                            pass
                if enc2 == 'auto':
                    for i, enc2 in encs:
                        try:
                            strings.append(text.encode(enc1).decode(enc2))
                            encs_combos.append(enc1 + '|' + enc2)
                        except:
                            pass

            strings_original = strings
            alph_str =        'абвгдеёжзийклмнопрстуфхцчшщыэюя'
            alph_str_full =   'абвгдеёжзийклмнопрстуфхцчшщыэюяьъ'
            alph_str_up = alph_str.upper()
            alph_str_up_full = alph_str_full.upper()
            alph = list(alph_str_full)
            dictionary_str =  'я мы вы он она они оно в к с по под на и но над до можно'
            dictionary = dictionary_str.split() + dictionary_str.title().split()
            words_begin_with_str = ('без бес вне внутри воз возо вос все изо испод кое кой меж '
                               'междо между над надо наи небез небес недо низ низо нис обо '
                               'обез обес около ото пере под под поза после пра пре при про '
                               'раз рас сверх среди сыз тре чрез через черес анти архи вице  '
                               'гипер дез дис интер квази контр макро микро обер пост прото '
                               'псевдо суб супер транс ультра экзо экс  '
                               # части сложных слов
                               'агит глав гор гос деп дет диа здрав ино кол ком лик маг маш '
                               'мин мол обл окруж орг март молит потреб прод пром проп рай '
                               'рег род рос сек сель сов сот соц студ тер фед хоз хос гов'
                               )
            words_begin_with = words_begin_with_str.split() + words_begin_with_str.title().split()
            strings = list(set(strings))
            strings.sort()

            rating_max = 0
            string_max = []
            for string in strings:
                rating = 0
                adds = []

                # RATING+
                for letter in alph:
                    if letter in string:
                        rating += 2  # list(string).count(letter)

                for word in dictionary:
                    if " {} ".format(word) in string:
                        rating += 50

                if len(string.split()) > 1:
                    rating += 50

                for prefix in words_begin_with:
                    prefix_pattern = '\s' + prefix + '.+\s'
                    add_rating = len(regex.findall(prefix_pattern, string, overlapped=True)) * 10
                    if add_rating > 0:
                        rating += add_rating
                        adds += (prefix_pattern, add_rating)

                rus_letters = '[' + alph_str_up + ']{0,1}[' + alph_str_full + ']+'
                rus_word_pattern = (
                    '^'  + rus_letters + '[,\.:;]{0,1}' '\s'
                    '|'
                    '\s' + rus_letters + '[,\.:;]{0,1}' '\s'
                    '|'
                    '\s' + rus_letters + '[,\.:;]{0,1}'  '$'
                                   )
                rus_words = regex.findall(rus_word_pattern, string, overlapped=True)
                add_rating = len(rus_words) * 10
                if add_rating > 0:
                    rating += add_rating
                    adds += (rus_words, add_rating)

                # RATING-
                if string[:2] == "яю" or string.lstrip()[:2] == "юя":
                    rating -= 50

                rus_letters_again = '[' + alph_str_up + ']{0,1}[' + alph_str_full + ']+'
                weird_rus_word_pattern = (
                    '^' +  rus_letters_again + '[^a-zA-Zа-яА-Я0-9\(\),\.:;\s]+'  '[^\s]*' '\s'
                    '|'
                    '\s' + rus_letters_again + '[^a-zA-Zа-яА-Я0-9\(\),\.:;\s]+'  '[^\s]*' '\s'
                    '|'
                    '\s' + rus_letters_again + '[^a-zA-Zа-яА-Я0-9\(\),\.:;\s]+'  '[^\s]*' '$'
                    '|'
                    '$[ьъЬЪ]+[^\s]+\s' '|' '\s[ьъЬЪ]+[^\s]+\s' '|' '\s[ьъЬЪ]+[^\s]+$'
                                       )
                weird_rus_words = regex.findall(weird_rus_word_pattern, string, overlapped=True)
                add_rating = len(weird_rus_words) * -2
                if add_rating < 0:
                    rating += add_rating
                    adds += (weird_rus_words, add_rating)

                # RESULT
                if rating_max < rating:
                    rating_max = rating
                    string_max.append(string)
            result_string = string_max[len(string_max)-1]
            result_string_index = strings_original.index(result_string)
            result_string_encs = encs_combos[result_string_index]
            return(result_string.strip(),result_string_encs)




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
