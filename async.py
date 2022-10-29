import asyncio
import time
from aiohttp import ClientSession


async def get_burtranslate(word):
    async with ClientSession() as session:
        url = f'http://burlang.ru/api/v1/russian-word/translate'
        params = {'q': word}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            return {word: weather_json}


async def main(words_list):
    tasks = []
    for word in words_list:
        tasks.append(asyncio.create_task(get_burtranslate(word)))
    print(tasks)
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

words_list = ['собака', 'бабушка', 'дедушка', 'брат', 'мама',
          'папа', 'русский', 'китаец', 'бурят', 'бурятия', 'красный']

print(time.strftime('%X'))

asyncio.run(main(words_list))

print(time.strftime('%X'))
