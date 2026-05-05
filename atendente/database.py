import os
from sqlalchemy import create_engine

# Recupera os dados do ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")

# Monta a URL garantindo que nada venha como 'None'
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Dica: Adicione este print (ele vai aparecer nos logs do Railway) 
# para você ver se a URL está sendo montada certa (NÃO MOSTRE A SENHA EM PRODUÇÃO)
print(f"DEBUG: Tentando conectar em {DB_HOST}:{DB_PORT} com o banco {DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)