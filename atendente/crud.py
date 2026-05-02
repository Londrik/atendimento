from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def criar_atendimento(db: Session, nome: str, tipo: str):
    prefixo = "P" if tipo == "Prioritário" else "N"
    
    total = db.query(models.Atendimento).count() + 1
    codigo = f"{prefixo}{total:03d}"
    
    db_atendimento = models.Atendimento(
        nome=nome, 
        tipo=tipo, 
        codigo=codigo, 
        status="Aguardando",
        data_criacao=datetime.now() # Registra o momento da chegada
    )
    db.add(db_atendimento)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

def get_fila_espera(db: Session):
    return db.query(models.Atendimento).filter(
        models.Atendimento.status == "Chamado"
    ).order_by(models.Atendimento.id.desc()).limit(5).all()

def chamar_proximo(db: Session, guiche: str):
    # 1. Busca o próximo da fila
    proximo = db.query(models.Atendimento).filter(
        models.Atendimento.status == "Aguardando"
    ).order_by(
        models.Atendimento.tipo.desc(), 
        models.Atendimento.id.asc()
    ).first()

    if proximo:
        agora = datetime.now()
        
        # 2. Calcula o tempo de espera em segundos
        # Se data_criacao for None (senhas antigas), usamos 0 para não quebrar
        delta = agora - (proximo.data_criacao or agora)
        espera_segundos = int(delta.total_seconds())

        # 3. Salva no Histórico antes de atualizar/deletar
        historico = models.HistoricoAtendimento(
            codigo=proximo.codigo,
            nome=proximo.nome,
            guiche=guiche,
            data_chegada=proximo.data_criacao,
            data_chamada=agora,
            tempo_espera_segundos=espera_segundos
        )
        db.add(historico)

        # 4. Atualiza o status para aparecer no painel
        proximo.status = "Chamado"
        proximo.guiche = guiche 
        
        db.commit()
        db.refresh(proximo)
        return proximo
        
    return None