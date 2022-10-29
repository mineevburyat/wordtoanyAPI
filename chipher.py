from lib2to3.pygram import Symbols


key = 13
SYMBOLS='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩ '
power = len(SYMBOLS)
def codebychiphr(message, key):
    result = ''
    loops = key // power
    # key = key - loops * 
    for ch in message:
        result += chr(ord(ch) + key)
    return result

def decodebychiphr(message, key):
    result = ''
    loops = key // power
    # key = key - loops * 
    for ch in message:
        result += chr(ord(ch) - key)
        
    return result

if __name__ == '__main__':
    key = 16567500
    ciphrotext = codebychiphr('Каждый Охотник Желает Знать Где Сидит Фазан',key)
    print(ciphrotext)
    print(decodebychiphr(ciphrotext, key))
