FROM python:3.10.6-alpine

WORKDIR /minio_start

COPY requirements.txt requirements.txt 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

#   RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . . 

# RUN ./minio server /data --console-address :9001 &
# Запустите Minio
# CMD ["./minio", "server", "/data", "--console-address", ":9001", "|", "python3", "minio_file.py"]
# CMD ["nohup", "./minio", "server", "/data", "--console-address", ":9001"]
CMD ["python", "minio_file.py"]
# RUN pip install --no-cache-dir --upgrade -r requirements.txt


# CMD ["ls"]


