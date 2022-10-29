# python 3.6 and more
# FastAPI service for docker 
# 
# example: 
# (build --build_arg WORKERS=5 --build-arg FASTAPI_PORT=8000 -t ASR2Format .)
# docker run -p 8000:8000 --rm ASR2Format
# or local start with uvicorn: uvicorn main:app

fastapi_description = '''
Сервис преобразования распознанных ответов на заданные вопросы в необходимый формат.

Состоит из следующих частей:
 * общая часть - отображает параметры и текущее состояние микросервиса, 
   имеет подключаемый логгер со своими настройками
 * операции с числами и числительными - необходимые операции, которые необходимо выполнить после 
   распознования речи человека содержащие числительные
 * операции с временем - необходимые операции, которые необходимо выполнить после 
   распознования речи человека содержащие время, часть суток и пр.
 * операции с датами - необходимые операции, которые необходимо выполнить после 
   распознования речи человека содержащие даты
 * операции с адресами - необходимые операции, которые необходимо выполнить после 
   распознования речи человека содержащие описательные признаки адреса в зависимости от особенностей региона
 * операции с услугами - необходимые операции, которые необходимо выполнить после 
   распознования речи человека содержащие описательные признаки услуги.

'''

from typing import Any
from fastapi import Depends, FastAPI, Body, Path, Query, Request, HTTPException, status
from functools import lru_cache
from api_settings import Settings
from sheme import *
import uvicorn
import os
import sys
import socket as sock

try:
    from app_logger import get_logger, LogLevel
    from app_logger import Settings as LogSettings
except Exception as e:
    print('Критическая ошибка!\nПроверте значения в конфигурационный файл log_config или переменные среды')
    print(e)
    sys.exit()

# Кэшируемые функции выполняющиеся один раз для заданных параметров
@lru_cache()
def get_settings():
    return Settings()


def get_log_conf():
    return LogSettings()

@lru_cache()
def get_status():
    try:
        host_name = os.uname().nodename
    except:
        host_name = sock.gethostname()
    host_ip = sock.gethostbyname(host_name)
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    return InfoDynamic(docker_ip=host_ip, docker_name=host_name, py_version=py_ver)


# Вычисление строки сообщения для логгера

def get_log_str(request: Request, func_name: str, answer: Any):
    client_ip = request.client.host
    method = request.method
    path = request.url.path
    if method.upper() == 'POST':
        body = request.body()
        result = "POST POST POST {body}"
    else:
        result = f"From {client_ip} {method} {path} SUCCESS worked {func_name} and return json({answer})"
    return result

############################ FastAPI инициализация
tags_metadata = [
    {
        "name": "common",
        "description": "Состояние и параметры сервиса fastAPI",
    },
    {
        "name": "number_manipulation",
        "description": "Утилиты для работы с числителями",
        # "externalDocs": {
        #     "description": "Thrift IDL MiddleEWare схема",
        #     "url": "https://fastapi.tiangolo.com/",
        # }
    },
    {
        "name": "time_manipulation",
        "description": "Утилиты для работы с временем",
    },
    {
        "name": "date_manipulation",
        "description": "Утилиты для работы с датами",
    },
    {
        "name": "address_search",
        "description": """Утилиты для поиска необходимого офиса или места
        по произвольному сообщению человека, исходя из особенностей региона""",
    },
    {
        "name": "service_search",
        "description": """Утилиты для поиска необходимого сервиса или услуги
        по произвольному сообщению человека, исходя из особенностей региона""",
    },
]
try:
    settings = get_settings()
    if settings.log_driver:
        logger_drv = get_logger(__name__, LogLevel.debug.value)
    else:
        logger_drv = None
except Exception as e:
    print('Критическая ошибка!\nПроверте значения в конфигурационных файлах или переменные среды')
    print(e)
    sys.exit()

app = FastAPI(
    title = settings.name_app,
    description = fastapi_description,
    version = settings.version,
    contact = {
        "name": "Mineev Alexander",
        "email": "mineev.buryat@gmail.com"
    }
)
    
@app.get('/', tags=['common'], response_model=Settings)
def api_settings(
    request: Request, 
    settings: Settings = Depends(get_settings)):
    '''Показать текущие параметры fastapi сервиса
    Параметры меняются через переменные среды. Имя параметра соответсвует переменной среды.'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'api_settings', settings))
    return settings

@app.get('/info', tags=['common'], response_model=InfoDynamic)
def api_info(
    request: Request, 
    info: InfoDynamic = Depends(get_status)):
    '''Показать динамические параметры fastapi сервиса
    Отображается текущий ip адрес, dns имя хоста и пр.'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'api_info', info))
    return info

@app.get('/conf_log', tags=['common'], response_model=LogSettings)
def log_config(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Показать конфигурацию логгера'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

############################# УТИЛИТЫ ################################################

# числительные
# {
#   "utterance": "сто тридцат шеcть двадцать пять и восемьдесят девить",
#   "only_numbers": 0
# }
@app.get('/util/number', tags=['number_manipulation'], response_model=LogSettings)
def word_to_number(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Преобразовать строку содержащие  числительные в список обнаруженых чисел'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

# время
@app.get('/util/time/partday', tags=['time_manipulation'], response_model=LogSettings)
def word_to_partday(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Преобразовать строку содержащее названое человеком часть суток в временной промежуток'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

@app.get('/util/time/time', tags=['time_manipulation'], response_model=LogSettings)
def word_to_time(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Преобразовать строку содержащее названое человеком время в часы и минуты'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

# дата
@app.get('/util/date/date', tags=['date_manipulation'], response_model=LogSettings)
def word_to_date(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Преобразовать строку содержащее названое человеком дату в день, месяц, год с учетом перехода между месяцами и годами'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf
# адрес
@app.get('/util/address/namespace', tags=['address_search'], response_model=LogSettings)
def has_address_namespace(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Показать имеющиеся в базе пространства имен для различных регионов.'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

@app.post('/util/address/namespace', tags=['address_search'], response_model=LogSettings)
def add_address_namespace(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Добавить новый регион с особенностями описания адресов'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

@app.post('/util/address/namespace/{space}', tags=['address_search'], response_model=LogSettings)
def add_address_sign(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Добавить в регион новый описательный признак адреса'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

@app.get('/util/address/search', tags=['address_search'], response_model=LogSettings)
def search_address(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Поиск конкретного адреса по названному человеком описательным признакам'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

# услуга
@app.get('/util/service/namespace', tags=['service_search'], response_model=LogSettings)
def has_service_namespace(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Показать имеющиеся в базе пространства имен услуг для различных регионов.'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

@app.get('/util/service/search', tags=['service_search'], response_model=LogSettings)
def search_service(
    request: Request, 
    log_conf: LogSettings = Depends(get_log_conf)):
    '''Поиск конкретной услуги по названному человеком описательным признакам'''
    if settings.log_driver and logger_drv:
        logger_drv.debug(get_log_str(request, 'log_config', log_conf))
    return log_conf

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.fastapi_host, 
        port=settings.fastapi_port, 
        access_log=False)
