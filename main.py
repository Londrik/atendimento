from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

# Importações do seu módulo interno
from atendente import models, schemas, crud
from atendente.database import SessionLocal, engine, get_db

# Inicializa as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Atendimento SENAI - Unidade Gama")

# --- CONFIGURAÇÕES DE ARQUIVOS ESTÁTICOS E TEMPLATES ---
# O mount permite que o navegador acesse as pastas /css e /js
app.mount("/static", StaticFiles(directory="atendente/static"), name="static")

# Define onde o Jinja2 deve procurar os arquivos HTML
templates = Jinja2Templates(directory="atendente/templates")

# Middleware para evitar erros de permissão (CORS)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# --- ROTAS DE PÁGINAS (HTML) ---

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Redireciona para o totem como página principal ou mantém o index
    return templates.TemplateResponse(request=request, name="totem.html")

@app.get("/totem", response_class=HTMLResponse)
async def exibir_totem(request: Request):
    return templates.TemplateResponse(request=request, name="totem.html")

@app.get("/painel", response_class=HTMLResponse)
async def exibir_painel(request: Request):
    return templates.TemplateResponse(request=request, name="painel.html")

@app.get("/atendente", response_class=HTMLResponse)
async def exibir_atendente(request: Request):
    return templates.TemplateResponse(request=request, name="atendente.html")

# --- ROTAS DA API (LÓGICA) ---

@app.post("/gerar-senha", response_model=schemas.Atendimento)
def gerar_senha(senha: schemas.AtendimentoCreate, db: Session = Depends(get_db)):
    """Recebe o nome e tipo do totem.js e cria a senha no banco."""
    return crud.criar_atendimento(db=db, nome=senha.nome, tipo=senha.tipo)

@app.get("/listar-fila")
def listar_fila(db: Session = Depends(get_db)):
    """Retorna a lista de pessoas aguardando para o painel e atendente."""
    return crud.get_fila_espera(db)

@app.post("/chamar-proxima", response_model=schemas.Atendimento)
def chamar_proxima(dados: schemas.ChamadaRequest, db: Session = Depends(get_db)):
    """O atendente chama a próxima senha disponível informando o seu guichê."""
    proximo = crud.chamar_proximo(db, guiche=dados.guiche)
    if not proximo:
        raise HTTPException(status_code=404, detail="Não há ninguém aguardando na fila.")
    return proximo

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)