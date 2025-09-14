# database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from config import DATABASE_URL

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Criação do engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args) # usar echo = True para debug
Base = declarative_base()

