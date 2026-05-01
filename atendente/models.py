from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(10), nullable=False)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    status = Column(String(20), default="espera")  # 'espera' ou 'chamado'
    criado_em = Column(DateTime(timezone=True), server_default=func.now())