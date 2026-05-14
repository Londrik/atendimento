import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Recupera os dados do ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")

# Monta a URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DEBUG: Tentando conectar em {DB_HOST}:{DB_PORT} com o banco {DB_NAME}")

# 1. Cria o motor de conexão com proteção contra timeouts (Pool de conexões resiliente)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,  # Fecha conexões com mais de 1 hora para evitar timeout do MySQL
    pool_pre_ping=True  # Testa a conexão antes de cada uso (Evita o erro "Server has gone away")
)

# 2. Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Cria a classe Base que o models.py está procurando
Base = declarative_base()

# Função para gerenciar as sessões do banco de dados nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()