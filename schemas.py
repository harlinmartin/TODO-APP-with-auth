from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TodoCreate(BaseModel):
    title: str

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True
        
class TodoUpdate(BaseModel):
    completed: bool
