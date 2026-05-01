import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurações de Conexão
DB_USER = "root"
DB_PASS = ""  # <--- Troque pela sua senha real
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "senai_totem"

def create_db_if_not_exists():
    """Conecta no MySQL e cria o banco de dados se ele não existir"""
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        connection.commit()
    finally:
        connection.close()

# Executa a criação automática antes de qualquer coisa do SQLAlchemy
create_db_if_not_exists()

# URL do SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para as rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()