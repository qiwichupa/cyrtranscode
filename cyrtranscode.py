#!/usr/bin/env python3
# ver 0.02

import sys
import argparse

class Transcode:

    def transcode(self, text):
        encodings = __import__('encodings')
        regex = __import__('regex')
        if text.strip() == '':
            return('')
        else:
            encs = encodings.aliases.aliases.items()
            strings = []
            for i, enc1 in encs:
                for i, enc2 in encs:
                    try:
                        strings.append(text.encode(enc1).decode(enc2))
                    except:
                        pass
    
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
                    #string = string[2:]
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
                    string_max.append(string.strip())
                    #print(string)
                    #print(rating)
                    #print(adds)
                    #print()
            return(string_max[len(string_max)-1])
    


def out(line):
    global flush_outfile
    if args.output and flush_outfile:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(line + '\n')
            f.close()
        flush_outfile = False
    elif args.output and flush_outfile == False:
        with open(args.output, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
            f.close()
    else:
        print(line)




# MAIN


try:
    sys.argv[1]
except:
    sys.exit(sys.argv[0] + ":\n    -h Читать описание")

parser = argparse.ArgumentParser(prog='cyrtranscoder', description='Утилита пытается распознать битую кодировку')
parser.add_argument('-o', '--output', type=str, metavar='FILE', help="вывод в файл  (UTF-8)")
input_group = parser.add_mutually_exclusive_group()
input_group.add_argument('-i', '--input', type=str, metavar='FILE', help="чтение из файла (UTF-8)")
input_group.add_argument('-s', '--string', type=str, metavar='STRING', help='строка для распознавания')
input_group.add_argument('-p', '--pipe',  help='получать через pipe', action="store_true")
input_group.add_argument('-t',  help='тест распознавания', action="store_true")
args = parser.parse_args()

flush_outfile = True

t = Transcode()

if args.input:
    with open(args.input, 'r', encoding='utf-8') as input_file:
        text = input_file.readlines()
        for line in text:
            out(t.transcode(line))
elif args.pipe:
#    if select.select([sys.stdin, ], [], [], 0.0)[0]:  # if stdin has data
    for line in sys.stdin:
        out(t.transcode(line))
    else:
        pass
elif args.t:
    test_strings = '''цНПНД:йПЮЯМНЪПЯЙ рЕКЕТНМ: 
                      дПСЦНИ БХД ЯБЪГХ: 
                      нОХЬХРЕ ОПНАКЕЛС (ЛНФМН ЙПЮРЙН):
                      ÐšÐ°Ñ‚ÐµÐ³Ð¾Ñ€Ð¸ÑЏ Ð¿ÑƒÐ±Ð»Ð¸ÐºÐ °Ñ†Ð¸Ð¸
                      Ñîîáùåíèå ãîòîâî ê îòïðàâêå ñî ñëåäóþùèì ôàéëîì èëè âëîæåííîé ñâÿçêîé: 041
                      Ïðèìå÷àíèå: Äëÿ ïðåäîòâðàùåíèÿ çàðàæåíèÿ êîìïüþòåðíûìè âèðóñàìè ïî÷òîâûå ïðîãðàììû ìîãóò çàïðåùàòü îòïðàâëåíèå èëè ïîëó÷åíèå âëîæåííûõ ôàéëîâ. Ïðîâåðüòå ïàðàìåòðû áåçîïàñíîñòè ïî÷òîâîé ïðîãðàììû äëÿ îáðàáîòêè âëîæåíèé.
                      ЇҐаҐ г¬Ґа жЁп ЇҐаҐ¬Ґ ле 
                      ñîâåì íå ïîìîãàåò âàø äåêîðäåð! íó êàê òàê?! îòïðàâëÿëà ïèñüìî íà ïðàâèëüíîì ðóññêîì, à ìíå ïðèøåë îòâåò ,÷òî åãî íåâîçìîæíî ïðî÷èòàòü. çàõîæó â ïàïêó "îòïðàâëåííûå", ñìîòðþ - äåéñòâèòåëüíî îòïðàâèñëîñü ïèñüìî íåïîíÿòíåéøèì íàáîðîì ñèìâîëâ. îáðàòèëàñü â ñëóæáó ßíäåêñà, ïåðåïðàâèëè íà âàø ñàéò. è ÷òî æå? - ÍÈ×ÅÃÎ ÍÅ ÄÅÉÑÒÂÓÅÒ!!! íå ïîëó÷àåòñÿ ðàñøèôðîâàòü! âñå êîäèðîêè áûëè ïåðåïðîáîâàíû....ïðîñòî ïî- ÷åëîâå÷åñêè îáèäíî ïîòåðÿòü òðóäû ïîëó÷àñîâîãî ñèäåíèÿ çà êîìïüþòåðîì......
                      лБФС мЕМШ - нХУЙ рХУЙ
                      §©§Х§а§в§а§У§а! §Ї§С §Я§а§У§н§Ы §Ф§а§Х §б§в§Ъ§У§Ц§Щ§е 2 §Ь§в§е§д§н§з §Ю§а§Т§Ъ§Э§о§Я§н§з §г §Ь§С§Ю§Ц§в§а§Ы, §У §¬§С§Щ§С§Я§Ъ §д§С§Ь§Ъ§з §д§а§й§Я§а §Я§Ц§д, 7700 §в§е§Т§Э§Ц§Ы/§к§д§е§Ь§С, §Ц§г§Э§Ъ §Я§С§Х§а.
                      дЮ АКХМ, ЕЫЕ ПЮГ ЦНБНПЧ - АЮАНЙ МЕРС. йНЦДЮ АСДСР - ХГЛЕМЧ
                      Íåâîçìîæíî èñïîëüçîâàòü ''; ôàéë óæå èñïîëüçóåòñÿ.
                   '''
    for line in test_strings.splitlines():
        print(line.strip())
        out(t.transcode(line))
        print()
else:
    text = args.string
    out(t.transcode(text))
