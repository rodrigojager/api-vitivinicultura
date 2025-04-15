import os
import datetime, sqlalchemy, databases, bcrypt, httpx
import boto3
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status, Query, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List
from auth import jwt_auth, create_access_token, verify_password
from services import run_scraping
from models import Production_or_Commercialization, Processing, Importing_or_Exporting

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, index=True, nullable=False),
    sqlalchemy.Column("password_hash", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.now(timezone.utc)),
)
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connection established.")
    try:
        yield
    finally:
        await database.disconnect()
        print("Database connection closed.")

app = FastAPI(
    title="Dados de uva, vinho e derivados",
    description="API para buscar informações referentes à quantidade de uvas processadas, produção e comercialização de vinhos, suco e derivados provenientes do Estado do Rio Grande do Sul",
    version="1.0.0",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

def update_last_access():
    ec2 = boto3.client('ec2', region_name='us-east-2')
    instance_id = 'i-080ad863d18ba54b4'
    
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[{
            'Key': 'LastAccessTime',
            'Value': datetime.now(timezone.utc).isoformat()
        }]
    )

@app.middleware("http")
async def update_access_middleware(request: Request, call_next):
    if request.url.path.startswith("/assets") or request.url.path.endswith((".css", ".js", ".png", ".svg")):
        return await call_next(request)
    update_last_access()
    return await call_next(request)

@app.get("/", include_in_schema=False)
async def root():
	return RedirectResponse(url="/docs/")

@app.get("/api", include_in_schema=False)
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

@app.get("/production", summary="Produção de vinhos, sucos e derivados do Rio Grande do Sul", tags=["Production"],response_model=List[Production_or_Commercialization])
async def get_production(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        productions = await run_scraping(year,'opt_02')
        return productions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/processing", summary="Quantidade de uvas processadas no Rio Grande do Sul", tags=["Processing"], response_model=List[Processing])
async def get_processing(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        processing = await run_scraping(year,'opt_03')
        return processing
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/commercialization", summary="Comercialização de vinhos e derivados no Rio Grande do Sul", tags=["Commercialization"], response_model=List[Production_or_Commercialization])
async def get_commercialization(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        commercializations = await run_scraping(year,'opt_04')
        return commercializations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/importing", summary="Importação de derivados de uva", tags=["Importing"], response_model=List[Importing_or_Exporting])
async def get_importing(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        importings = await run_scraping(year,'opt_05')
        return importings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/exporting", summary="Exportação de derivados de uva", tags=["Exporting"], response_model=List[Importing_or_Exporting])
async def get_exporting(
    year: int = Query(..., description="Ano obrigatório"),
    user: dict = Depends(jwt_auth)
):
    try:
        exportings = await run_scraping(year,'opt_06')
        return exportings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/registration", response_class=HTMLResponse, include_in_schema=False)
async def register_form(request: Request):
    site_key = os.getenv("RECAPTCHA_SITE_KEY")
    return templates.TemplateResponse("register.html", {"request": request, "site_key": site_key})

@app.post("/register", include_in_schema=False)
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    recaptcha_response: str = Form(...),
):

    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    if not secret_key:
         raise HTTPException(status_code=500, detail="Chave secreta do reCAPTCHA não configurada no servidor.")
         
    recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post(recaptcha_verify_url, data={
                "secret": secret_key,
                "response": recaptcha_response
            })
            r.raise_for_status()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=500, detail=f"Erro ao contatar o serviço reCAPTCHA: {exc}")

    result = r.json()
    if not result.get("success"):
        error_codes = result.get("error-codes", [])
        print(f"Falha na verificação do reCAPTCHA: {error_codes}")
        raise HTTPException(status_code=400, detail=f"Falha na verificação do reCAPTCHA: {', '.join(error_codes)}")

    existing_user = await get_user(username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Usuário já existe.")

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = users.insert().values(
        username=username,
        password_hash=hashed.decode('utf-8'),
        created_at=datetime.datetime.utcnow()
    )
    try:
        await database.execute(query)
        return JSONResponse({"success": True, "message": "Usuário registrado com sucesso."})
    except Exception as e:
        print(f"Erro ao inserir usuário no banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao registrar usuário.")

app.mount("/docs", StaticFiles(directory="site", html=True), name="docs")
