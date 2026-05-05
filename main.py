from fastapi import FastAPI, Request, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

# Importações do seu módulo interno
from atendente import models, schemas, crud
from atendente.database import SessionLocal, engine, get_db

# Inicializa as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Atendimento SENAI - Unidade Gama")

# --- LÓGICA DO WEBSOCKET (Connection Manager) ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

# --- CONFIGURAÇÕES DE ARQUIVOS ESTÁTICOS E TEMPLATES ---
app.mount("/static", StaticFiles(directory="atendente/static"), name="static")
templates = Jinja2Templates(directory="atendente/templates")

# Middleware CORS
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# --- ROTA DO WEBSOCKET ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- ROTAS DE PÁGINAS (HTML) ---
# CORREÇÃO: Usando argumentos nomeados (request=request, name="...") para evitar erros de versão

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
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

@app.get("/dashboard", response_class=HTMLResponse)
async def exibir_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")

# --- ROTAS DA API ---

@app.post("/gerar-senha", response_model=schemas.Atendimento)
async def gerar_senha(senha: schemas.AtendimentoCreate, db: Session = Depends(get_db)):
    nova_senha = crud.criar_atendimento(db=db, nome=senha.nome, tipo=senha.tipo)
    await manager.broadcast("atualizar_lista")
    return nova_senha

@app.get("/listar-fila")
def listar_fila(db: Session = Depends(get_db)):
    return crud.get_fila_espera(db)

@app.post("/chamar-proxima", response_model=schemas.Atendimento)
async def chamar_proxima(dados: schemas.ChamadaRequest, db: Session = Depends(get_db)):
    proximo = crud.chamar_proximo(db, guiche=dados.guiche)
    if not proximo:
        raise HTTPException(status_code=404, detail="Não há ninguém aguardando na fila.")
    
    await manager.broadcast("atualizar_painel")
    return proximo

# --- NOVAS ROTAS PARA O DASHBOARD ---

@app.get("/api/v1/metrics")
def get_metrics(db: Session = Depends(get_db)):
    resumo = crud.get_metricas_resumo(db)
    grafico_hora = crud.get_atendimentos_por_hora(db)
    return {
        "resumo": resumo,
        "grafico_hora": grafico_hora
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)