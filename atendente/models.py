from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255)) 
    codigo = Column(String(50), unique=True, index=True)
    tipo = Column(String(50)) # Ex: Geral, Matrícula, Preferencial
    status = Column(String(50), default="Aguardando") 
    guiche = Column(String(50), nullable=True)
    
    # Registra o momento exato em que a senha foi emitida no Totem
    data_criacao = Column(DateTime, default=datetime.now)

class HistoricoAtendimento(Base):
    """
    Esta tabela armazena os dados permanentes para o Dashboard.
    Mesmo que a fila de hoje seja limpa, os dados aqui ficam salvos.
    """
    __tablename__ = "historico_atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10))
    nome = Column(String(100))
    guiche = Column(String(50))
    tipo = Column(String(50)) # Essencial para o gráfico de pizza do Dashboard
    data_chegada = Column(DateTime)
    data_chamada = Column(DateTime, default=datetime.now)
    tempo_espera_segundos = Column(Integer)