
from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

# Создаем экземпляр приложения FastAPI
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user_user_id(request: Request, user_id: int = Path(ge=1, le=100,
                                 description='Enter User ID', example='1')):
    for i in users:
        if i.id == user_id:
            return templates.TemplateResponse(
                request=request, name='users.html', context={'user': i})
    raise HTTPException(status_code=404, detail='User was not found')


@app.post("/user/{username}/{age}")
async def post_users(
        username: str = Path(min_length=5, max_length=20, description='Enter Username', example='UrbanUser'),
        age: int = Path(ge=18, le=120, description='Enter Age', example='24')):
    user_id = (users[-1].id + 1) if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user




@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str = Path(min_length=5, max_length=20,
                      description='Enter Username', example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description='Enter Age', example='24')):
    try:
        user = (user for user in users if user.id == user_id)
        user.username = username
        user.age = age
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
