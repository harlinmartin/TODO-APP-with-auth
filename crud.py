from sqlalchemy.orm import Session
import models
from auth import hash_password

def create_user(db: Session, user):
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        return None

    db_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_todo(db: Session, title: str, user_id: int):
    todo = models.Todo(title=title, owner_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, user_id: int, completed: bool | None):
    query = db.query(models.Todo).filter(models.Todo.owner_id == user_id)
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    return query.all()

def update_todo_status(db, todo_id: int, user_id: int, completed: bool):
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.owner_id == user_id
    ).first()

    if not todo:
        return None

    todo.completed = completed
    db.commit()
    db.refresh(todo)
    return todo
