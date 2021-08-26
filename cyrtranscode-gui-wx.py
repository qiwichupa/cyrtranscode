
import regex
import encodings
import wx

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