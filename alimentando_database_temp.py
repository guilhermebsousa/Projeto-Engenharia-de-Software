# Exemplo de uso dos serviços para criar tabelas e inserir dados de teste
from database.database import engine, Base
from database.session import *
from database.models import *
from database.services import *
from config import ENV
import random
from database.models.users import RoleEnum

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

# Criar 2 usuários
usuarios = []
usuarios.append(create_user(db, username="op123", password="123", role=RoleEnum.OPERATOR))
usuarios.append(create_user(db, username="operador", password="op123", role=RoleEnum.OPERATOR))

marcas = [
    "Nestlé", "Coca-Cola", "Unilever", "PepsiCo", "Danone",
    "Colgate", "Palmolive", "Bunge", "Sadia", "Perdigão",
    "Heinz", "Ambev", "Italac", "Ypê", "Omo"
]

nomes = [
    "Leite", "Refrigerante", "Arroz", "Feijão", "Café",
    "Açúcar", "Óleo", "Sabonete", "Macarrão", "Farinha",
    "Biscoito", "Suco", "Manteiga", "Queijo", "Detergente",
    "Shampoo", "Creme dental", "Fralda", "Água mineral", "Cerveja"
]

unidades = {
    "Leite": "L",
    "Refrigerante": "L",
    "Arroz": "kg",
    "Feijão": "kg",
    "Café": "kg",
    "Açúcar": "kg",
    "Óleo": "L",
    "Sabonete": "un",
    "Macarrão": "kg",
    "Farinha": "kg",
    "Biscoito": "un",
    "Suco": "L",
    "Manteiga": "kg",
    "Queijo": "kg",
    "Detergente": "un",
    "Shampoo": "un",
    "Creme dental": "un",
    "Fralda": "un",
    "Água mineral": "L",
    "Cerveja": "L",
}

for user in usuarios:
    for i in range(50):
        nome = random.choice(nomes)
        marca = random.choice(marcas)
        barcode = f"{user.id[:4]}{i:04d}"  # barcode é gerado a partir do id do usuário + contador
        create_product(
            db,
            user_idF=user.id,
            barcode=barcode,
            name=f"{nome} {i}",
            brand=marca,
            unit=unidades.get(nome, "un"),  # pega a unidade correta, ou "un" se não tiver no dict
            package_quantity=random.randint(1, 10), # quantidade por embalagem em kg, unidade, litros, etc...
            minimum_stock=random.randint(5, 30),
            suggested_price=round(random.uniform(2.5, 50.0), 2),
            current_quantity=random.randint(0, 100),
        )

db.close()
print("✅ Usuários e produtos de teste criados com sucesso!")