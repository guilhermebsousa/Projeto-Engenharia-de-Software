# Configuração do SQLAlchemy e criação do engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import DATABASE_URL # Importa a URL do banco de dados do arquivo de configuração

# Criação do engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, echo = False) # usar echo = True para debug

Base = declarative_base()