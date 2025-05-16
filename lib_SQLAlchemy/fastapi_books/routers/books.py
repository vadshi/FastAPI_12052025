from typing import AsyncIterator
from fastapi import Body, Depends, APIRouter, HTTPException
from database import get_db
from models import BookDB
from schemas import BookCreate, BookResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update


router = APIRouter()

@router.post('/', response_model=BookResponse, status_code=201)
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
async def get_book_by_id(book_id: int, session: AsyncIterator[AsyncSession] = Depends(get_db)) -> BookResponse | None:
    query = select(BookDB).filter_by(id=book_id) # select * from books where id = {book_id}
    result = await session.execute(query) # ChunkIterator
    book = result.scalar_one_or_none()
    if book:
        return book
    raise HTTPException(404, f"Book with={book_id} not found.")


@router.put('/{book_id}')
async def update_book_by_id(
        book_id: int, 
        book: BookCreate = Body(), 
        session: AsyncIterator[AsyncSession] = Depends(get_db)
    ) -> BookResponse:
    query = update(BookDB).where(BookDB.id == book_id) # 
    query = query.values(**book.model_dump(exclude_none=True))
    result = await session.execute(query) # ChunkIterator
    await session.commit()

    if not result.rowcount:
       raise HTTPException(404, f"Book with={book_id} not found.")
    
    return await get_book_by_id(book_id, session=session)


@router.delete('/{book_id}')
async def delete_book_by_id(book_id: int, session: AsyncIterator[AsyncSession] = Depends(get_db)) -> BookResponse | dict:
    query = select(BookDB).where(BookDB.id == book_id) # 
    result = await session.execute(query) # ChunkIterator
    book = result.scalar_one_or_none()

    if not book:
       raise HTTPException(404, f"Book with={book_id} not found.")
    
    await session.delete(book)
    await session.commit()
    return {'message': f"Book with={book_id} has deleted."}