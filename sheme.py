
from pydantic import BaseModel, Field
# from typing import List, Union
# from enum import Enum


class InfoDynamic(BaseModel):
    '''Динамическая информация о fastAPI сервисе (ip-адрес, dns-имя)'''
    docker_ip: str = Field(..., title="ip адрес контейнера")
    docker_name: str = Field(..., title="имя контейнера")
    py_version: str = Field(..., title="текущая версия python")

