from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255)) 
    codigo = Column(String(50), unique=True, index=True)
    tipo = Column(String(50)) # Normal ou Prioritário
    status = Column(String(50), default="Aguardando") 
    guiche = Column(String(50), nullable=True)
    
    # IMPORTANTE: Precisamos desta coluna para calcular o tempo de espera na Fase 2
    data_criacao = Column(DateTime, default=datetime.now)

class HistoricoAtendimento(Base):
    __tablename__ = "historico_atendimento"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10))
    nome = Column(String(100))
    guiche = Column(String(50))
    data_chegada = Column(DateTime)
    data_chamada = Column(DateTime, default=datetime.now)
    tempo_espera_segundos = Column(Integer)