from typing import AsyncIterator
from fastapi import Depends, APIRouter, HTTPException
from database import get_db
from models import BookDB
from schemas import BookCreate, BookResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter()

@router.post('/', response_model=BookResponse)
async def create_book(book: BookCreate, session: AsyncIterator[AsyncSession] = Depends(get_db)):
    db_book = BookDB(**book.model_dump())  # dict() deprecated, use model_dump()
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book
    

@router.get('/')
async def get_books(session: AsyncIterator[AsyncSession] = Depends(get_db)) -> list[BookResponse]:
    query = select(BookDB) # select * from books
    result = await session.execute(query) # ChunkIterator
    return result.scalars().all()


@router.get('/{book_id}')
async def get_books(book_id: int, session: AsyncIterator[AsyncSession] = Depends(get_db)) -> BookResponse | None:
    query = select(BookDB).filter_by(id=book_id) # select * from books where id = {book_id}
    result = await session.execute(query) # ChunkIterator
    book = result.scalar_one_or_none()
    if book:
        return book
    raise HTTPException(404, f"Book with={book_id} not found.")

