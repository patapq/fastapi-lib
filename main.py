from fastapi import Body, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Annotated


app = FastAPI()

app.mount("/frontend/", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend/")



BOOKS = [ 
	{'id': 1, 'title': 'Jane Eyre', 'author': 'Jane Austen', 'category': 'period drama'},
	{'id': 2, 'title': 'Great Expectations', 'author': 'Charles Dickens', 'category': 'period drama'},
	{'id': 3, 'title': 'Bourne Idemtity', 'author': 'Robert Ludlum', 'category': 'mystery/thriller'},
	{'id': 4, 'title': 'DaVinci Code', 'author': 'Dan Brown', 'category': 'mystery/thriller'},
	{'id': 5, 'title': 'The Match Girl', 'author': 'Charles Dickens', 'category': 'tragedy'}
]



@app.get('/')
def root(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})


@app.post('/books', response_class=HTMLResponse)
async def books(request: Request, prompt: Annotated[str, Form(...)]):
	
	book_list = []
	for book in BOOKS:
		if book.get('title').casefold() == prompt.casefold() or book.get('author').casefold() == prompt.casefold() or book.get('category').casefold() == prompt.casefold():
			book_list.append(book)

	return templates.TemplateResponse("books.html", {"request": request, 'book_list': book_list})



@app.get("/books/{book_id}", response_class=HTMLResponse)
async def show_book(request: Request, book_id: int):
	book = BOOKS[book_id - 1]
	return templates.TemplateResponse("book.html", {"request": request, "book": book})



# @app.post("/books/{book_id}", response_class=HTMLResponse)
# async def show_book(request: Request, book_id: int, prompt = Form(...)):
# 	book = BOOKS[book_id - 1]
# 	return templates.TemplateResponse("book.html", {"request": request, "book": book})




# #READ
# @app.get('/books')
# async def read_all_books():
# 	return BOOKS


# #CREATE
# @app.post('/books/create_book')
# async def create_book(new_book=Body()):
# 	BOOKS.append(new_book)



# @app.get('/books/{book_title}') #lets fastapi know that at this endpoint, you return the data in the function below it
# async def read_all_books(book_title: str): #async is fairly optional on fastapi
# 	for book in BOOKS:
# 		if book.get('title').casefold() ==  book_title.casefold():
# 			return book



# @app.get('/books/{book_author}/') #query params can be used with dynamic params
# async def filter_books_query_title(book_author: str, category: str):
# 	book_category = []
# 	for book in BOOKS:
# 		if book.get('author').casefold() ==  book_author.casefold() and book.get('category').casefold() == category.casefold():
# 			book_category.append(book)
# 	return book_category
	

# #UPDATE
# @app.put('/books/update_book')
# async def update_book(update_book=Body()):
# 	for i in range(len(BOOKS)):
# 		if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
# 			BOOKS[i] = update_book

# #DELETE
# @app.delete('/books/delete_book')
# async def delete_book(book_title: str):
# 	for i in range(len(BOOKS)):
# 		if BOOKS[i].get('title').casefold() == book_title.casefold():
# 			BOOKS.pop(i)
# 			break
