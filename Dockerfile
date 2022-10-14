FROM python:latest
COPY ./requests.txt .
COPY ./api_settings.py .
COPY ./app_logger.py .
COPY ./main.py .
COPY ./sheme.py .
RUN pip3 install --no-cache-dir -r ./requests.txt
CMD ["python3", "./main.py"]
EXPOSE 8090
