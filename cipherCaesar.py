'''
Свейгарт Э.
h t t p s://inventwithpython.com/cipherwheel/
перестановочный шифр

простой (открытый) текст
шифр - набор правил над текстом 
ключ (секретный) 
шифротекст
шифр Цезаря - шифровальный диск
арифметика и символы
можно ли усилить шифрование перестановочным методом используя два и более секретных ключей

Зашифруйте следующи е фразы и з кн иги Амброза Бирса "Словарь Сата н ы"
( "The Devil' s Dictioпary" ), используя ука занные ключи.

"AM B I D EXTROUS: ABLE ТО PICK WITH EQUAL S К I LL А R I GHT-HAN D
РОС КЕТ O R А LEFT. " (кл ю ч 4 ) .
" G U I LLOT I N E: А MACH I N E WH I C H MAKES А F R E N C H MAN S H R U G H I S
S H O U LDERS WITH GOOD REASON." ( кл ю ч 1 7) .
" I M PI ETY: YOU R I R R EVERENCE TOWARD М У D EITY." ( ключ 2 1 )
Дешифруйте следующие зашифрованные фрагменты текста, используя у ка­
за нные ключ и.
А. "ZXAI: р R D H IJ BT H D BTIXBTH LDGCQN H RD I RWBTC хе PBTGXRP PCS
PBTGXR PCHXC H R D IAPCS. " ( ключ 1 5 ) .
Б. " MQTSWXSV: Е VMZEP EWТMVERX XSTYFPMG LS RSVW." ( ключ 4).

Исполь зу йте про гра мму caesarCipher.py для шифрования следующих сооб­
щени й с помощью указанн ых ключей.
А.
' " You can s how Ы а сk is wh i t e Ь у a r g ument , " s a i d
" b u t you w i l l neve r convi nce me . " ' ( кл юч 8 ) .
Filby,
' 1 2 3 4 5 6 7 8 9 0 ' ( ключ 2 1 ) .
Исполь зуйте п ро г рамму caesarCipher. py для дешифро ва н ия следующих за­
ши фрованны х сообщений с помощью указанных ключей.
А.' Kv ? uqwp f u ? rncwu kdn g ? gp qw i j B ' (ключ 2 ) .
Б.' XC B S w 8 8 S 1 8 A l S 2 S B 4 1 S E . 8 z S EwAS 5 0 D 5 A 5 x 8 1 V ' ( ключ 2 2 ) .

message - входное сообщение
key - ключ
SYMBOLS - множество символов которые можно шифровать
translated - шифротекст
'''
key = 13
message = 'Каждый охотник желает знать где сидит фазан'
SYMBOLS = 'AВCDEFGHIJKLМNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?,-@#$%^&*()-+_=[]}{|;:<>\'/'
symbolPower = len(SYMBOLS)

def cipher_char(ch:str, key:int):
    key = key % 0x10ffff
    return chr(ord(ch) + key)

def decipher_char(ch:str, key:int):
    key = key % 0x10ffff
    return chr(ord(ch) - key)

def cipher_message(message:str, key:int):
    result = ''
    for ch in message:
        result += cipher_char(ch, key)
    return result

def decipher_message(message:str, key:int):
    result = ''
    for ch in message:
        result += decipher_char(ch, key)
    return result

def cipher_message_symbols(message:str, key:int):
    SYMBOLS = "abcdefgijklmnopquvw123456 ABCDEFGIJKLMNOPQАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧабвгдеёжзийклмню,.:-!?"
    max_power = len(SYMBOLS)
    result = ''
    for ch in message:
        if ch in SYMBOLS:
            index = SYMBOLS.find(ch)
            result += SYMBOLS[(index + key) % max_power]
        else:
            result += ch
    return result

def decipher_message_symbols(message:str, key:int):
    SYMBOLS = "abcdefgijklmnopquvw123456 ABCDEFGIJKLMNOPQАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧабвгдеёжзийклмню,.:-!?"
    max_power = len(SYMBOLS)
    result = ''
    for ch in message:
        if ch in SYMBOLS:
            index = SYMBOLS.find(ch)
            result += SYMBOLS[(index - key) % max_power]
        else:
            result += ch
    return result

if __name__ == "__main__":
    import random
    pangrammlist = [
        "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!",
        "Друг мой эльф! Яшке б свёз птиц южных чащ!",
        "Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.",
        "Шеф взъярён тчк щипцы с эхом гудбай Жюль.",
        "Эй, жлоб! Где туз? Прячь юных съёмщиц в шкаф.",
        "Экс-граф? Плюш изъят. Бьём чуждый цен хвощ!",
        "Съешь же ещё этих мягких французских булок да выпей чаю.",
        "Широкая электрификация южных губерний даст мощный толчок подъёму сельского хозяйства.",
        "Эй, цирюльникъ, ёжик выстриги, да щетину ряхи сбрей, феном вошь за печь гони!",
        "Аэрофотосъёмка ландшафта уже выявила земли богачей и процветающих крестьян.",
        "Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).",
        """ 
            Щипцами брюки разлохмачу,
            Гребёнкой волосы взъерошу.
            Эффектно ожидать удачу
            До самой смерти я не брошу!""",
        "БУКВОПЕЧАТАЮЩЕЙ СВЯЗИ НУЖНЫ ХОРОШИЕ Э/МАГНИТНЫЕ РЕЛЕ. ДАТЬ ЦИФРЫ (1234567890+= .?-)",
        "Brick quiz whangs jumpy veldt fox!",
        "Quick wafting zephyrs vex bold Jim.",
        "The quick brown fox jumps over the lazy dog.",
        "Breezily jangling ^$3,416,857,209 wise advertiser ambles to the bank, his exchequer amplified."
        ]
    for pangramm in pangrammlist:
        # key = random.randint(1, 1000)
        key = 10
        # ciphertext = cipher_message(pangramm, key)
        # print(ciphertext)
        # print(decipher_message(ciphertext, key))
        ciphertext = cipher_message_symbols(pangramm, key)
        print(ciphertext)
        print(decipher_message_symbols(ciphertext, key))