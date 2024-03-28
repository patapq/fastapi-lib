FROM python:3.10.6-alpine

WORKDIR /minio_work

COPY requirements.txt requirements.txt 

RUN pip install --no-cache-dir --upgrade -r requirements.txt




# # Загрузите и установите Minio
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio \
    && chmod +x minio

# Для установки пакета nohup # отвечающий за фоновую работу
RUN apk add coreutils

#   RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . . 

# RUN ./minio server /data --console-address :9001 &
# Запустите Minio
# CMD ["./minio", "server", "/data", "--console-address", ":9001", "|", "python3", "minio_file.py"]
CMD ["./minio", "server", "/data", "--console-address", ":9001"]

# RUN pip install --no-cache-dir --upgrade -r requirements.txt


# CMD ["ls"]


