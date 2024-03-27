FROM python:3.9

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "database.py","file_uploader_minio.py","main.py"]
