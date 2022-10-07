""" Настройки микросервиса FastAPI"""

from typing import Final
from pydantic import BaseSettings

# стартовый шаблон для всех API сервисов:
# - настройки сервиса через конффайл и переменные среды
# - подключаемый драйвер логирования с отдельным файлом настроек или переменных среды
# - колорированный вывод в поток

VERSION_APP: Final = "0.0.2"
# Параметры приложения
FASTAPI_HOST_DEFAULT: Final = '0.0.0.0'
PORT_DEFAULT: Final = 8090
NAME_APP_DEFAULT: Final = 'API-ASR2Format'

#################### настройки (можно сменить переменными среды или файлом .env)
class Settings(BaseSettings):
    fastapi_host: str = FASTAPI_HOST_DEFAULT
    fastapi_port: int = 8090
    version: str = VERSION_APP
    name_app: str = NAME_APP_DEFAULT
    log_driver: bool = True
    
    class Config:
        env_file = "api_config.env"

