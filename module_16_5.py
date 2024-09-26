from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")
app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

@app.get("/")
async  def get_users(request : Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}")
async def get_user_page(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.post("/user/{username}/{age}")
async def reg_user(user: User, username: str, age: int) -> str:
    len_user = len(users)
    if len_user == 0:
        user.id = 1
    else:
        user.id = users[len_user - 1].id + 1
    user.username = username
    user.age = age
    users.append(user)
    return f"User {username} created!"

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int, user: str = Body()) -> str:
    try:
        edit_user = users[user_id - 1]
        edit_user.username = username
        edit_user.age = age
        return f"User ID={user_id} values have been changed. Username: {username}, age: {age}"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> str:
   try:
       users.pop(user_id - 1)
       return f"User ID={user_id} was deleted!"
   except:
       raise HTTPException(status_code=404, detail="User was not found")
