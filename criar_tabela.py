
import sys
import os
# Adiciona a pasta atendente ao caminho de busca do Python
sys.path.append(os.path.abspath("atendente"))

try:
    from database import engine
    from sqlalchemy import text

    sql_command = """
    CREATE TABLE IF NOT EXISTS historico_atendimento (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo VARCHAR(10) NOT NULL,
        nome VARCHAR(100) NOT NULL,
        guiche VARCHAR(50),
        data_chegada DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_chamada DATETIME,
        tempo_espera_segundos INT
    );
    """

    with engine.connect() as connection:
        connection.execute(text(sql_command))
        connection.commit() 
        print("Sucesso! Tabela historico_atendimento criada no banco senai_totem.")
except Exception as e:
    print(f"Erro: {e}")

