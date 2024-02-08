from fastapi import Body, FastAPI, Request, Form, status, HTTPException 
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

