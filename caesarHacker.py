
SYMBOLS = "abcdefgijklmnopquvw123456 ABCDEFGIJKLMNOPQАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧабвгдеёжзийклмню,.:-!?"
def decipher_message_symbols(message:str, key:int):
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
    ciphrtext = "Йэрофотосъ,b?йKaйcншйфтйKу.юKлыял-aйK:юba-Kкомйчю!K-Kпроцлютйdщ-хK?рюстьяcf"
    for key in range(len(SYMBOLS)):
        print(key, decipher_message_symbols(ciphrtext, key))