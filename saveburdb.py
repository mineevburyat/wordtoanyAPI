import json
import requests

def getburtranslate(word:str):
    # print(word, end=' ')
    payload = {'q': word.strip()}  
    req = requests.get('http://burlang.ru/api/v1/russian-word/translate', params=payload)
    # print(req.status_code, req.url)
    if req.status_code == 200:
        translate = []
        for item in req.json().get('translations'):
            translate.append(item.get('value'))
        return translate
    else:
        return None
'''гиперфункцию'''
if __name__ == "__main__":
    dic = {}
    with open('rusianwords/russian-words/russian.utf-8.txt', 'r') as f:
        line = f.readline().rstrip('\n').strip()
        while line:
            translate = getburtranslate(line)
            print(line, end='')
            if translate:
                oldlist = dic.get(line, [])
                oldlist.extend(translate)
                dic[line] = oldlist
                with open('ruburdic.json', 'w') as savefile:
                    json.dump(dic, savefile, indent=2, ensure_ascii=False)
                print('-', translate)
            else:
                print()
            line = f.readline().rstrip('\n').strip()
        f.close()
        
# root = ET.fromstring(country_data_as_string)