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
        "name": "mw",
        "description": "Состояние и параметры MiddleWare. Установка параметров связи со службой InfoWatch.",
        "externalDocs": {
            "description": "Thrift IDL MiddleEWare схема",
            "url": "https://fastapi.tiangolo.com/",
        }
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.fastapi_host, 
        port=settings.fastapi_port, 
        access_log=False)
