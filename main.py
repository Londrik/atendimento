from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# Garante a criação das tabelas no banco de dados recém-criado
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Filas SENAI")

# CORS para permitir acesso do Totem, Atendente e TV
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

@app.post("/gerar-senha")
def gerar_senha(request: SenhaSchema, db: Session = Depends(get_db)):
    tipo_formatado = request.tipo.upper()
    prefixo = PREFIXOS.get(tipo_formatado, "S")

    # Conta quantas senhas deste tipo já existem para gerar o sequencial
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
    # Retorna apenas quem está aguardando (Status 'espera')
    return db.query(models.Atendimento)\
             .filter(models.Atendimento.status == "espera")\
             .order_by(models.Atendimento.id.asc()).all()

@app.post("/chamar-proxima")
def chamar_proxima(db: Session = Depends(get_db)):
    # Busca o primeiro da fila (FIFO) que ainda está em espera
    proximo = db.query(models.Atendimento)\
                .filter(models.Atendimento.status == "espera")\
                .order_by(models.Atendimento.id.asc()).first()
    
    if not proximo:
        raise HTTPException(status_code=404, detail="Não há ninguém na fila de espera.")

    # Atualiza o status
    proximo.status = "chamado"
    db.commit()
    db.refresh(proximo)
    return proximo

@app.get("/ultima-chamada")
def ultima_chamada(db: Session = Depends(get_db)):
    # Busca a última pessoa que teve o status alterado para 'chamado'
    ultima = db.query(models.Atendimento)\
               .filter(models.Atendimento.status == "chamado")\
               .order_by(models.Atendimento.id.desc()).first()
    
    if not ultima:
        return {"codigo": "---", "nome": "AGUARDANDO", "tipo": "NENHUM"}
    
    return ultima

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)