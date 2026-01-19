from fastapi import FastAPI, Depends, HTTPException, Form, BackgroundTasks
from sqlalchemy.orm import Session

import models, schemas, crud
from database import engine, SessionLocal
from auth import verify_password, create_access_token
from dependancies import get_current_user   


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User registered successfully"}

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}

def send_email_notification(username: str, title: str):
    print(f"📧 Email sent to {username} for task: {title}")


@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(
    todo: schemas.TodoCreate,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_todo = crud.create_todo(db, todo.title, current_user.id)

    background_tasks.add_task(
        send_email_notification,
        current_user.username,
        todo.title
    )

    return new_todo

@app.get("/todos", response_model=list[schemas.TodoResponse])
def list_todos(
    completed: bool | None = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_todos(db, current_user.id, completed)


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(
    todo_id: int,
    todo: schemas.TodoUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_todo = crud.update_todo_status(
        db,
        todo_id,
        current_user.id,
        todo.completed
    )

    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return updated_todo
