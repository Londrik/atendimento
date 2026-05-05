import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base # <--- Faltava este import
from sqlalchemy.orm import sessionmaker # <--- Faltava este import

# Recupera os dados do ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")

# Monta a URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DEBUG: Tentando conectar em {DB_HOST}:{DB_PORT} com o banco {DB_NAME}")

# 1. Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. Cria a fábrica de sessões (Faltava isso)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Cria a classe Base que o models.py está procurando (Faltava isso)
Base = declarative_base()