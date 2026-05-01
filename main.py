from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# AJUSTE DE IMPORTS: Referenciando a pasta 'atendente'
from atendente import models
from atendente.database import engine, get_db

# Garante a criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Filas SENAI")

# Monta a pasta 'static' para arquivos CSS, JS e Imagens
app.mount("/static", StaticFiles(directory="atendente/static"), name="static")

# Configura a pasta de templates HTML
templates = Jinja2Templates(directory="atendente/templates")

# CORS para permitir acesso de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeamento de prefixos
PREFIXOS = {
    "CONVENCIONAL": "C",
    "PRIORITARIO": "P",
    "MATRICULA": "M",
    "INFORMACAO": "I"
}

class SenhaSchema(BaseModel):
    nome: str
    tipo: str

# --- ROTAS DE INTERFACE (HTML) ---

@app.get("/totem", response_class=HTMLResponse)
async def exibir_totem(request: Request):
    return templates.TemplateResponse("totem.html", {"request": request})

@app.get("/painel", response_class=HTMLResponse)
async def exibir_painel(request: Request):
    return templates.TemplateResponse("painel.html", {"request": request})

# --- ROTAS DA API (LÓGICA) ---

@app.post("/gerar-senha")
def gerar_senha(request: SenhaSchema, db: Session = Depends(get_db)):
    tipo_formatado = request.tipo.upper()
    prefixo = PREFIXOS.get(tipo_formatado, "S")

    contagem = db.query(models.Atendimento).filter(models.Atendimento.tipo == tipo_formatado).count()
    sequencial = str(contagem + 1).zfill(3)
    novo_codigo = f"{prefixo}-{sequencial}"

    novo_registro = models.Atendimento(
        codigo=novo_codigo,
        nome=request.nome.upper(),
        tipo=tipo_formatado,
        status="espera"
    )

    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)
    return novo_registro

@app.get("/listar-fila")
def listar_fila(db: Session = Depends(get_db)):
    return db.query(models.Atendimento)\
             .filter(models.Atendimento.status == "espera")\
             .order_by(models.Atendimento.id.asc()).all()

@app.post("/chamar-proxima")
def chamar_proxima(db: Session = Depends(get_db)):
    proximo = db.query(models.Atendimento)\
                .filter(models.Atendimento.status == "espera")\
                .order_by(models.Atendimento.id.asc()).first()
    
    if not proximo:
        raise HTTPException(status_code=404, detail="Não há ninguém na fila de espera.")

    proximo.status = "chamado"
    db.commit()
    db.refresh(proximo)
    return proximo

@app.get("/ultima-chamada")
def ultima_chamada(db: Session = Depends(get_db)):
    ultima = db.query(models.Atendimento)\
               .filter(models.Atendimento.status == "chamado")\
               .order_by(models.Atendimento.id.desc()).first()
    
    if not ultima:
        return {"codigo": "---", "nome": "AGUARDANDO", "tipo": "NENHUM"}
    
    return ultima

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)