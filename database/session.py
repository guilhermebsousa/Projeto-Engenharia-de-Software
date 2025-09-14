# Criar sessão para interagir com o banco de dados
from sqlalchemy.orm import sessionmaker
from .database import engine

# Criação de sessões para rodar queries
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Função para obter sessão dentro de um contexto
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()