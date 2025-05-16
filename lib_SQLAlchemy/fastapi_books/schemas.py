from pydantic import BaseModel, ConfigDict

class BookCreate(BaseModel):
    title: str
    author: str | None = None

class BookResponse(BookCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int