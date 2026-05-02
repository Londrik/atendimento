from pydantic import BaseModel
from typing import Optional

class AtendimentoBase(BaseModel):
    nome: str
    tipo: str

class AtendimentoCreate(AtendimentoBase):
    pass

class Atendimento(AtendimentoBase):
    id: int
    codigo: str
    status: str
    guiche: Optional[str] = None

    class Config:
        from_attributes = True

class ChamadaRequest(BaseModel):
    guiche: str
