from fastapi import Body, FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Annotated

import database



app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Шаблоны для отображения данных с бэка на фронт
templates = Jinja2Templates(directory="frontend")


book_list = {}


# JSON раскладываются сюда
class Info(BaseModel):
     prompt: str
     filters: list[str]



@app.get('/')
def root(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})


# Метод POST, получающий поисковой запрос от JS fetch (prompt = Body())
@app.post('/get_books')
async def get_books(request: Request, info: Info):
    prompt = info.prompt
    filters = info.filters

    data = database.full_text_search(prompt).data
    data_len = len(data)
    

    book_list['book_list'] = data
    book_list['count'] = data_len
 
    return RedirectResponse('/books', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/books', response_class=HTMLResponse)
async def books(request: Request):
    return templates.TemplateResponse("books.html", {"request": request, 'book_list': book_list})


@app.get("/books/{book_id}", response_class=HTMLResponse)
async def show_book(request: Request, book_id: int):
    
    book = None

    for b in book_list['book_list']:
        print(b)
        if b['book_id'] == book_id:
            book = b

    return templates.TemplateResponse("book.html", {"request": request, "book": book})

