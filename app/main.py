import uvicorn
import os
import asyncio
import time



from fastapi import Body, FastAPI, Request, Form, status, HTTPException 
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi import File, UploadFile, Path
from starlette.responses import StreamingResponse

from minio_handler import MinioHandler

from pydantic import BaseModel
from typing import Annotated

import database




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Шаблоны для отображения данных с бэка на фронт
templates = Jinja2Templates(directory="frontend")


book_list = {}


# JSON раскладываются сюда
class Info(BaseModel):
     prompt: str
     filters: list[str]


# Class for Minio
class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message

class UploadFileResponse(BaseModel):
    bucket_name: str
    file_name: str
    url: str


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

    for elem in data:
        try:
            string = f'{elem["book_id"]}.webp'
            elem["book_image"] = download_file_from_minio(filePath=string)
        except:
            print('error')

    print(data)
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


# Метод GET для Minio
@app.get("/download/minio/{filePath}")
def download_file_from_minio(
        *, filePath: str = Path(..., title="The relative path to the file", min_length=1, max_length=500)):
    try:
        minio_client = MinioHandler().get_instance()   
        # проверка клиента на наличие файла
        # if not minio_client.check_file_name_exists(minio_client.bucket_name, filePath):
        #     raise CustomException(http_code=400, code='400',
        #                           message='File not exists')
        if minio_client.check_file_name_exists(minio_client.bucket_name, filePath):
            # Чтение url адреса через 
            url = minio_client.presigned_get_object(minio_client.bucket_name, filePath)
        else:            
            # Чтение url адреса через 
            url = minio_client.presigned_get_object(minio_client.bucket_name, '0.webp')
        print(url)
        # return StreamingResponse(BytesIO(file)) # для вывода потока данных может потребоваться 
        return url
        # Чтение файла из Minio
        # file = minio_client.client.get_object(minio_client.bucket_name, filePath).read()
        # return StreamingResponse(BytesIO(file)) # для вывода потока данных может потребоваться 

    except CustomException as e:
        raise e
    except Exception as e:
        if e.__class__.__name__ == 'MaxRetryError':
            raise CustomException(http_code=400, code='400', message='Can not connect to Minio')
        raise CustomException(code='999', message='Server Error')


# метод POST для Minio
@app.post("/upload/minio", response_model=UploadFileResponse)
async def upload_file_to_minio(filename, file: UploadFile = File(...)):
    try:
        minio_client = MinioHandler().get_instance()  
        filePath = filename.split('/')[-1]
        if minio_client.check_file_name_exists(minio_client.bucket_name, filePath):
            # Чтение url адреса через 
            print(f'{filePath} file exists in Minio')
        else:            
            # data = file.file.read()
            data = file.read()
            # file_name = " ".join(file.filename.strip().split())
            file_name = " ".join(filename.strip().split())

            content_type = 'image/webp'

            data_file = MinioHandler().get_instance().put_object(
                file_name=file_name,
                file_data=BytesIO(data),
                content_type=content_type # file.content_type
            )
            return data_file
    except CustomException as e:
        raise e
    except Exception as e:
        if e.__class__.__name__ == 'MaxRetryError':
            raise CustomException(http_code=400, code='400', message='Can not connect to Minio')
        raise CustomException(code='999', message='Server Error')
    

async def main():   
    local_folder_path = "images/"
    image_files = [f for f in os.listdir(local_folder_path) if os.path.isfile(os.path.join(local_folder_path, f))]

    for image_file in image_files:
        with open(os.path.join(local_folder_path, image_file), "rb") as file:
            # Вызов функции upload_file_to_minio с передачей файла
            await upload_file_to_minio(filename=image_file, file=file)

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)

if __name__ == "__main__":
    # Подождать 3 секунды
    time.sleep(3)
    asyncio.run(main())
    
