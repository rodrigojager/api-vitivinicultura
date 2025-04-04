# main_api.py
import os
import datetime, sqlalchemy, databases
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import List
from auth import jwt_auth, create_access_token, verify_password
from playwright.async_api import async_playwright
from services import run_scraping
from models import Production_or_Commercialization

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Tabela de usuários (idem ao seu código original)
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, index=True, nullable=False),
    sqlalchemy.Column("password_hash", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

app = FastAPI(
    title="Dados de uva, vinho e derivados",
    description="API para buscar informações referentes à quantidade de uvas processadas, produção e comercialização de vinhos, suco e derivados provenientes do Estado do Rio Grande do Sul",
    version="1.0.0",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Seus endpoints de login e docs também podem ficar aqui, usando funções do módulo auth

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    file_path = Path(__file__).parent / "custom_swagger.html"
    return HTMLResponse(file_path.read_text(encoding="utf-8"))

@app.post("/login", summary="Autenticação", tags=["Autenticação"])
async def login(username: str, password: str):
    user = await get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/production", summary="Produção de vinhos, sucos e derivados do Rio Grande do Sul", tags=["Production"])
async def get_production(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        productions = await run_scraping(year,'opt_02')
        return {"productions": productions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/commercialization", summary="Comercialização de vinhos e derivados no Rio Grande do Sul", tags=["Commercialization"])
async def get_production(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        commercializations = await run_scraping(year,'opt_04')
        return {"commercializations": commercializations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
