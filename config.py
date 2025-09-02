from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

ENV = os.getenv("ENV", "development")

# URL para o banco de dados PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida. Verifique o arquivo .env ou as variáveis de ambiente.")