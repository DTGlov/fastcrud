from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from typing import List
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Notes API"}


@app.get("/notes", response_model=List[schemas.Note])
def get_notes(db: Session = Depends(get_db)):
    my_notes = db.query(models.Note).all()
    return my_notes


@app.get("/notes/{id}", response_model=schemas.Note)
def get_note(id: int, response: Response, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"note with id: {id} not found")
    return note


@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=schemas.Note)
def create_notes(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, response: Response, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id)
    if note.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    note.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/notes/{id}", response_model=schemas.Note)
def update_note(id: int, updated_note: schemas.NoteCreate, db: Session = Depends(get_db)):
    note_query = db.query(models.Note).filter(models.Note.id == id)
    note = note_query.first()
    if note == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} not found")
    note_query.update(updated_note.dict(), synchronize_session=False)
    db.commit()
    return note_query.first()
