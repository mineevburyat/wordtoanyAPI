# docker build -t fastapi --build-arg  FASTAPI_PORT=8092 --build-arg WORKERS=4 --build-arg LOG_DRIVER=True .
# docker run -p 8092:8092 fastapi

FROM python:latest

ARG FASTAPI_PORT=8092
ARG WORKERS=4
ARG LOG_DRIVER='false'

COPY ./requirements.txt .
COPY ./api_settings.py .
COPY ./app_logger.py .
COPY ./main.py .
COPY ./sheme.py .
RUN pip3 install --no-cache-dir -r ./requirements.txt
ENV FASTAPI_PORT="${FASTAPI_PORT}"
ENV WORKERS="${WORKERS}"
ENV LOG_DRIVER="${LOG_DRIVER}"

ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port "${FASTAPI_PORT}" --workers "${WORKERS}" 
# CMD ["python3", "./main.py"]

