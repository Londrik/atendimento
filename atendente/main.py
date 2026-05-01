from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuração de CORS para permitir acesso de diferentes origens (Totem, Atendente, TV)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESTADO DO SERVIDOR (Em Memória) ---

counters = {
    "CONVENCIONAL": 0, 
    "PRIORITARIO": 0, 
    "MATRICULA": 0, 
    "INFORMACAO": 0
}

prefixes = {
    "CONVENCIONAL": "C", 
    "PRIORITARIO": "P", 
    "MATRICULA": "M", 
    "INFORMACAO": "I"
}

fila_espera = []

# NOVA VARIÁVEL: Armazena o estado do que deve aparecer na TV
ultima_senha_chamada = {
    "codigo": "---",
    "nome": "Aguardando",
    "tipo": "Nenhum"
}

# --- MODELOS DE DADOS ---

class SenhaRequest(BaseModel):
    nome: str
    tipo: str

# --- ROTAS ---

@app.post("/gerar-senha")
async def gerar_senha(request: SenhaRequest):
    tipo = request.tipo.upper()
    counters[tipo] += 1
    
    codigo = f"{prefixes.get(tipo, 'S')}-{str(counters[tipo]).zfill(3)}"
    
    nova_senha = {
        "codigo": codigo,
        "nome": request.nome,
        "tipo": tipo
    }
    
    fila_espera.append(nova_senha)
    return nova_senha

@app.get("/listar-fila")
async def listar_fila():
    return fila_espera

@app.post("/chamar-proxima")
async def chamar_proxima():
    global ultima_senha_chamada  # Referenciando a variável global
    
    if not fila_espera:
        raise HTTPException(status_code=404, detail="Nenhuma senha na fila")
    
    # Remove o primeiro da fila (FIFO)
    proxima = fila_espera.pop(0)
    
    # ATUALIZAÇÃO: Salvamos quem foi chamado agora para a rota da TV consultar
    ultima_senha_chamada = proxima
    
    print(f"Painel Atualizado: {ultima_senha_chamada['codigo']}")
    return proxima

@app.get("/ultima-chamada")
async def get_ultima_chamada():
    """Rota que a TV ficará consultando via polling"""
    return ultima_senha_chamada

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)