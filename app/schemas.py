from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    description: str
    author: str


class Note(NoteCreate):
    created_at: datetime

    class Config:
        orm_mode = True
