
import sys
import os
sys.path.append(os.path.abspath("atendente"))
from database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS atendimentos;"))
        connection.execute(text("DROP TABLE IF EXISTS historico_atendimento;"))
        connection.commit()
        print("? Tabelas removidas com sucesso!")
except Exception as e:
    print(f"? Erro: {e}")

