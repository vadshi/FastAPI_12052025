from fastapi import FastAPI
import uvicorn
from routers.books import router as books_router

app = FastAPI(title="Books REST API")
app.include_router(books_router, prefix='/books',tags=['books'])

@app.get('/')
def get_root():
    return {"message": "Welcome to Books REST API"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)