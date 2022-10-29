import asyncio
import time
from aiohttp import ClientSession
import json


async def get_burtranslate(word:str):
    async with ClientSession() as session:
        url = f'http://burlang.ru/api/v1/russian-word/translate'
        word = word.strip()
        params = {'q': word}

        async with session.get(url=url, params=params) as response:
            translate = []
            if response.status == 200:
                translate_json = await response.json()
                for item in translate_json.get('translations'):
                    translate.append(item.get('value'))
            return {word: translate}


async def main_corutine(words_list):
    tasks = []
    for word in words_list:
        tasks.append(asyncio.create_task(get_burtranslate(word)))
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)
        try:
            data = json.load(open('ruburdic_asinc.json', encoding='utf-8'))
        except:
            data = {}
        print('save')
        json.dump({**data, **result}, 
            open('ruburdic_asinc.json', mode='w', encoding='utf-8'), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    dic = {}
    with open('russian.utf-8.txt', 'r') as f:
        while True:
            words_list = f.readlines(10240)
            print(words_list)
            if words_list:
                asyncio.run(main_corutine(words_list))
        f.close()

# words_list = ['rfnfhcb', 'зеленый']

# print(time.strftime('%X'))



# print(time.strftime('%X'))
