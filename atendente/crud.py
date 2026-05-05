from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from . import models, schemas

def criar_atendimento(db: Session, nome: str, tipo: str):
    """Cria uma nova senha no banco de dados."""
    # Define o prefixo com base no tipo selecionado no Totem
    prefixo = "P" if tipo == "Preferencial" else "N"
    
    # Conta o total para gerar o número sequencial
    total = db.query(models.Atendimento).count() + 1
    codigo = f"{prefixo}{total:03d}"
    
    db_atendimento = models.Atendimento(
        nome=nome, 
        tipo=tipo, 
        codigo=codigo, 
        status="Aguardando",
        data_criacao=datetime.now()
    )
    db.add(db_atendimento)
    db.commit()
    db.refresh(db_atendimento)
    return db_atendimento

def get_fila_espera(db: Session):
    """Retorna as últimas 5 senhas chamadas para exibição no Painel."""
    return db.query(models.Atendimento).filter(
        models.Atendimento.status == "Chamado"
    ).order_by(models.Atendimento.id.desc()).limit(5).all()

def chamar_proximo(db: Session, guiche: str):
    """Lógica do Atendente para chamar a próxima pessoa da fila."""
    # Busca o próximo priorizando 'Preferencial' e depois ordem de chegada (ID)
    proximo = db.query(models.Atendimento).filter(
        models.Atendimento.status == "Aguardando"
    ).order_by(
        models.Atendimento.tipo.desc(), 
        models.Atendimento.id.asc()
    ).first()

    if proximo:
        agora = datetime.now()
        
        # Calcula o tempo de espera real
        delta = agora - (proximo.data_criacao or agora)
        espera_segundos = int(delta.total_seconds())

        # IMPORTANTE: Salvamos o 'tipo' no histórico para as métricas do Dashboard
        historico = models.HistoricoAtendimento(
            codigo=proximo.codigo,
            nome=proximo.nome,
            guiche=guiche,
            tipo=proximo.tipo, # Adicione esta coluna no seu model se ainda não tiver
            data_chegada=proximo.data_criacao,
            data_chamada=agora,
            tempo_espera_segundos=espera_segundos
        )
        db.add(historico)

        # Atualiza o status para o WebSocket avisar o Painel
        proximo.status = "Chamado"
        proximo.guiche = guiche 
        
        db.commit()
        db.refresh(proximo)
        return proximo
        
    return None

# --- FUNÇÕES PARA O DASHBOARD (MÉTRICAS) ---

def get_metricas_resumo(db: Session):
    """Calcula os dados para os cards informativos do Dashboard."""
    # Total de pessoas atendidas (quem já passou pelo guichê)
    total_atendidos = db.query(models.HistoricoAtendimento).count()
    
    # Média de espera em minutos
    media_espera = db.query(func.avg(models.HistoricoAtendimento.tempo_espera_segundos)).scalar() or 0
    media_minutos = round(media_espera / 60, 1)

    # Distribuição por tipo baseada no HISTÓRICO (dados permanentes)
    # Tenta buscar do Histórico, se der erro por falta da coluna, busca da Atendimento
    try:
        distribuicao_tipo = db.query(
            models.HistoricoAtendimento.tipo, 
            func.count(models.HistoricoAtendimento.id)
        ).group_by(models.HistoricoAtendimento.tipo).all()
    except:
        distribuicao_tipo = db.query(
            models.Atendimento.tipo, 
            func.count(models.Atendimento.id)
        ).group_by(models.Atendimento.tipo).all()

    return {
        "total": total_atendidos,
        "media_espera": media_minutos,
        "distribuicao": dict(distribuicao_tipo)
    }

def get_atendimentos_por_hora(db: Session):
    """Gera os dados para o gráfico de barras de volume por horário."""
    dados = db.query(
        func.hour(models.HistoricoAtendimento.data_chamada).label('hora'),
        func.count(models.HistoricoAtendimento.id).label('quantidade')
    ).group_by('hora').all()
    
    return [{"hora": f"{int(d.hora)}h", "quantidade": d.quantidade} for d in dados]