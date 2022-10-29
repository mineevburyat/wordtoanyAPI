from difflib import SequenceMatcher
from typing import List
import re

def clean_message(subj):
    tmp = re.sub(r'[^а-яА-ЯёЁ ]', '', subj)
    return tmp

def get_most_similar(source: str, data_list: list, field_name: str):
    """Сравнение строки source  со списком объектов, а точнее со строкой хранящейся в ключе field_name 
    и выдает результатом структуру объект, где это поле имеет максимальную вероятность схожести"""
    # data = [{'key': '', 'value': ''} ...]
    best_case = {}
    source = clean_message(source)
    sm = SequenceMatcher()
    sm.set_seq2(source.lower().strip())
    max_ratio = 0
    for item in data_list:
        field = item.get(field_name)
        if type(field) == list:
            for tmp in item.get(field_name,[]):
                if type(tmp) != str:
                    continue
                sm.set_seq1(tmp.lower().strip())
                ratio = sm.ratio()
                if max_ratio < ratio:
                    max_ratio = ratio
                    best_case = item
        elif type(field == str):
            sm.set_seq1(field.lower().strip())
            ratio = sm.ratio()
            if max_ratio < ratio:
                max_ratio = ratio
                best_case = item
    if best_case:
        best_case.update({'max_ratio': round(max_ratio,2)})
        return best_case
    else:
        return None

def get_most_similar_old(source:str, data: List[object]):
    """ Сравнение строки source  со списком объектов  {'key': '', 'value': ''}
    и выдает результатом структуру {'key': '', 'value': '', 'ratio': max_value}
    с максимальной вероятностью похожести"""
    # data = [{'key': '', 'value': ''}, {'key': '', 'value': ''}, ...]
    best_case = {'key': None, 'value': None, 'ratio': 0}
    sm = SequenceMatcher()
    sm.set_seq2(source.lower())
    for data_item in data:
        print(data_item)
        tmp = data_item['key'].lower()
        sm.set_seq1(tmp)
        print(sm.ratio())
        if sm.ratio() > best_case['ratio']:
            best_case['ratio'] = sm.ratio()
            best_case['key'] = data_item['key']
            best_case['value'] = data_item['value']
    if best_case['key']:
        return best_case
    else:
        return None

if __name__ == "__main__":
    test_utt = [
        "ну в нижнеангарск",
        "северобайкальск",
        "мфц по улице ленина",
        "загорск",
        "иволга",
        "do you English",
        "апапаврап",
        "на ключевской",
        "в баргузине"
    ]
    list_offices = [
        {"key": "35", "value": ["МФЦ Баргузинского района", 12345]}, 
        {"key": "24", "value": ["МФЦ Заиграевского района"]}, 
        {"key": "23", "value": ["МФЦ Мухоршибирского района"]}, 
        {"key": "19", "value": ["МФЦ Тарбагатайского района"]}, 
        {"key": "26", "value": ["МФЦ Прибайкальского района"]}, 
        {"key": "5", "value": ["ГБУ 'МФЦ РБ' г. Улан-Удэ ул. Ключевская, 76а "]}, 
        {"key": "22", "value": ["МФЦ Джидинского района"]}, 
        {"key": "38", "value": ["МФЦ Селенгинского района"]}, 
        {"key": "36", "value": ["МФЦ Еравнинского района"]}, 
        {"key": "43", "value": ["МФЦ Баунтовского района"]}, 
        {"key": "45", "value": ["Филиал ГБУ 'МФЦ РБ' по Окинскому району"]}, 
        {"key": "34", "value": ["МФЦ Северо-Байкальского района (п. Нижнеангарск)"]}, 
        {"key": "21", "value": ["МФЦ г. Северобайкальск"]}, 
        {"key": "18", "value": ["МФЦ Тункинского района"]}, 
        {"key": "39", "value": ["МФЦ Железнодорожного района г. Улан-Удэ (Загорск)"]}, 
        {"key": "33", "value": ["МФЦ Курумканского района"]}, 
        {"key": "30", "value": ["МФЦ Бичурского района"]}, 
        {"key": "25", "value": ["МФЦ Иволгинского района"]}, 
        {"key": "31", "value": ["МФЦ Кижингинского района"]}, 
        {"key": "27", "value": ["МФЦ Кяхтинского района"]}, 
        {"key": "37", "value": ["МФЦ Хоринского района"]}, 
        {"key": "20", "value": ["МФЦ Муйского района"]}, 
        {"key": "28", "value": ["МФЦ Закаменского района"]}, 
        {"key": "44", "value": ["МФЦ Советского района г. Улан-Удэ ул. Кабанская, 55"]}, 
        {"key": "32", "value": ["МФЦ Кабанского района"]}]
    for utt in test_utt:
        print(utt, ': ', get_most_similar(utt, list_offices, 'value'))
    