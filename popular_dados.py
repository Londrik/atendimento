from sqlalchemy.orm import Session
from atendente.database import SessionLocal, engine
from atendente import models
from datetime import datetime, timedelta
import random

db = SessionLocal()

def popular():
    print("🚀 Gerando dados de teste para o Dashboard...")
    tipos = ["Geral", "Matrícula", "Preferencial"]
    nomes = ["Ana Silva", "Bruno Souza", "Carla Dias", "Diego Lemos", "Elena Fox"]
    
    for i in range(50):
        # Gera uma hora aleatória entre 08h e 18h
        hora_aleatoria = random.randint(8, 18)
        minuto_aleatorio = random.randint(0, 59)
        data_fake = datetime.now().replace(hour=hora_aleatoria, minute=minuto_aleatorio)
        
        espera = random.randint(300, 1800) # Entre 5 e 30 min
        tipo = random.choice(tipos)
        
        historico = models.HistoricoAtendimento(
            codigo=f"T{i:03d}",
            nome=random.choice(nomes),
            guiche=f"Guichê {random.randint(1,4)}",
            tipo=tipo,
            data_chegada=data_fake - timedelta(seconds=espera),
            data_chamada=data_fake,
            tempo_espera_segundos=espera
        )
        db.add(historico)
    
    db.commit()
    print("✅ 50 atendimentos inseridos com sucesso!")

if __name__ == "__main__":
    popular()