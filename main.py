from fastapi import Body, FastAPI, Request, Form, status, HTTPException 
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Annotated

import database


from minio import Minio
from minio.error import S3Error
import os
import requests
from minio import Minio
import urllib3
from urllib.parse import urlparse
import certifi
from minio.commonconfig import REPLACE, CopySource

#Подключение к MiniO
minio_endpoint = os.getenv("MINIO_ENDPOINT", "https://192.168.1.110:9000")
secure = False

minio_endpoint = urlparse(minio_endpoint)

if minio_endpoint.scheme == 'https':
    secure = True

ok_http_client = urllib3.PoolManager(
            timeout=urllib3.util.Timeout(connect = 10, read = 10),
            maxsize = 10,
            cert_reqs = 'CERT_NONE',
            ca_certs = os.environ.get('SSL_CERT_FILE') or certifi.where(),
            retries = urllib3.Retry(
                total = 5,
                backoff_factor = 0.2,
                status_forcelist = [500, 502, 503, 504]
            )
        )

minioClient = Minio(minio_endpoint.netloc,
                    access_key = 'minioadmin',
                    secret_key = 'minioadmin',
                    http_client = ok_http_client,
                    secure = secure)

# Функция для получения метрик MiniO
def get_minio_metrics():
    try:
        # Получаем количество файлов в бакете на MiniO сервере
        bucket_name = "books-images"
        objects = minioClient.list_objects(bucket_name)
        total_files = len([obj.object_name for obj in objects])

        metrics = {
            'total_files': total_files
        }
        return metrics
    except S3Error as e:
        return {'error': str(e)}

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Шаблоны для отображения данных с бэка на фронт
templates = Jinja2Templates(directory="frontend")


book_list = {}


# JSON раскладываются сюда
class Info(BaseModel):
     prompt: str
     filters: list[str]


# Exception handler if page does not exist
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse('/books')


# Root page
@app.get('/')
def root(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})


# Метод POST, получающий поисковой запрос от JS fetch (prompt = Body())
# POST method that collects info and redirects to /books to show list of books
@app.post('/get_books')
async def get_books(request: Request, info: Info):
    prompt = info.prompt
    filters = info.filters
    data = database.full_text_search(prompt, filters).data
    data_len = len(data)

    book_list['book_list'] = data
    book_list['count'] = data_len

    return RedirectResponse('/books', status_code=status.HTTP_303_SEE_OTHER)


# List of books page
@app.get('/books', response_class=HTMLResponse)
async def books(request: Request):
    return templates.TemplateResponse("books.html", {"request": request, 'book_list': book_list})


# Specific book page
@app.get("/books/{book_id}", response_class=HTMLResponse)
async def show_book(request: Request, book_id: int):
    
    book = None

    if not book_list:
        raise HTTPException(status_code=404, detail='Empty book_list')
    for b in book_list['book_list']:
        if b['book_id'] == book_id:
            book = b

    if book is None:
        raise HTTPException(status_code=404, detail='Empty book_list')

    return templates.TemplateResponse("book.html", {"request": request, "book": book})

@app.get("/health")
async def health_check():
    metrics = get_minio_metrics()
    return metrics