
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
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)


        self.Show(True)

app = wx.App(False)
ver='1.1.1'
title='cyrtranscode v.{}'.format(ver)
frame = MainWindow(None, title)
app.MainLoop()