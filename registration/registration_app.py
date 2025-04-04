# registration/registration_app.py
import os
import random
import datetime
import bcrypt
import sqlalchemy
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import databases
from db import database, users, init_db  # Importa do módulo comum de banco de dados

load_dotenv()

# Inicializa o banco de dados (se necessário)
init_db()

templates = Jinja2Templates(directory="templates")
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

def generate_captcha():
    # Captcha simples: soma de dois números aleatórios entre 1 e 9.
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    return a, b, a + b

@app.get("/", response_class=HTMLResponse)
async def register_form(request: Request):
    a, b, result = generate_captcha()
    return templates.TemplateResponse("register.html", {"request": request, "a": a, "b": b, "captcha_sum": result})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    captcha: int = Form(...),
    captcha_sum: int = Form(...)
):
    # Valida o captcha
    if int(captcha) != int(captcha_sum):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Captcha incorreto"})
    
    # Verifica se o usuário já existe
    query = users.select().where(users.c.username == username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Usuário já existe"})
    
    # Cria hash da senha utilizando bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = users.insert().values(
        username=username,
        password_hash=hashed.decode('utf-8'),
        created_at=datetime.datetime.utcnow()
    )
    await database.execute(query)
    return RedirectResponse(url="/", status_code=302)

