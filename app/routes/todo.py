from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema
from sqlalchemy import select

router = APIRouter(prefix="/todo")

@router.get("/")
def index(db: Annotated[Session, Depends(get_db)]):
    data = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)
    # todos = db.query(TodoSchema).all()
    todos = db.execute(data).mappings().all()
    return {"message": "List of all TODO items", "data": todos}

@router.get("/{id}")
def find_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    data = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    return {"message": "Successfully", "data": data}

@router.post("/")
def store(item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "Create a new TODO item", "item": todo}

@router.delete("/{id}")
def delete_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    data = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not data:
        return {"message":"Item not found"}
    
    db.delete(data)
    db.commit()
    return{"message":"Item deleted successfully"}

@router.put("/{id}")
def update_by_id(id: int, item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    data = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not data:
        return {"message": "Item not found"}
    data.content = item.content
    data.is_completed = item.is_completed
    db.commit()
    db.refresh(data)
    return {"message": "Item update successfully", "data": data}