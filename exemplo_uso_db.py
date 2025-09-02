# Exemplo de uso dos serviços para criar tabelas e inserir dados de teste
from database.database import engine, Base
from database.session import *
from database.models import *
from database.services import *
from config import ENV

if ENV != "development":
    raise EnvironmentError("Este script não deve ser executado em ambiente de produção.")

print("Criando tabelas...")
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")

db = SessionLocal()

# Deletar valores de teste existentes
db.query(Movement).delete()
db.query(Product).delete()
db.query(User).delete()
db.commit()

# Criar usuário de teste
new_user = create_user(db, username="admin", password="admin123", role="ADMIN")

# Criar produto de teste
new_product = create_product(
    db,
    user_idF=new_user.id,
    barcode="123456789",
    name="Milk",
    brand="Nestle",
    unit="L",
    package_quantity=1,
    minimum_stock=10,
    suggested_price=4.50,
    current_quantity=20
)

# Criando uma movimentação de entrada de teste
new_movement = create_movement(
    db,
    user_idF=new_user.id,
    product_idF=new_product.id,
    type="IN",
    quantity=5,
    purchase_price=3.00,
    expiration_date=None
)

print("Dados de teste inseridos com sucesso na tabela tamporária!")

db.close()
