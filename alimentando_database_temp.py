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
new_user = create_user(db, username="admin", email="admin@hotmail.com", password="admin123", role="ADMIN")

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

produtos = [
    ("White Rice", "Tio João", "kg", 5, 10, 25.90, 50),
    ("Carioca Beans", "Camil", "kg", 1, 20, 7.50, 100),
    ("Spaghetti Pasta", "Renata", "g", 500, 15, 4.80, 70),
    ("Soybean Oil", "Soya", "ml", 900, 12, 6.30, 40),
    ("Refined Sugar", "União", "kg", 1, 25, 5.20, 80),
    ("Roasted Coffee", "Pilão", "g", 500, 8, 18.90, 30),
    ("Whole Milk", "Italac", "ml", 1000, 30, 4.20, 120),
    ("Margarine", "Qualy", "g", 500, 10, 7.80, 35),
    ("Wheat Flour", "Dona Benta", "kg", 1, 12, 6.50, 45),
    ("Laundry Detergent", "Omo", "kg", 1, 15, 12.90, 60),
    ("Liquid Detergent", "Ypê", "ml", 500, 20, 2.50, 200),
    ("Fabric Softener", "Comfort", "ml", 2000, 10, 15.90, 25),
    ("Shampoo", "Pantene", "ml", 350, 8, 17.50, 40),
    ("Conditioner", "Pantene", "ml", 350, 8, 18.00, 40),
    ("Toilet Paper", "Neve", "un", 12, 15, 25.90, 60),
    ("Mineral Water", "Crystal", "ml", 1500, 30, 2.20, 150),
    ("Coca-Cola Soda", "Coca-Cola", "ml", 2000, 25, 9.80, 100),
    ("Guaraná Antarctica Soda", "Guaraná Antarctica", "ml", 2000, 25, 8.90, 90),
    ("Beer Can", "Skol", "ml", 350, 50, 3.50, 300),
    ("Red Wine", "Aurora", "ml", 750, 10, 22.90, 20),
    ("Mozzarella Cheese", "Itambé", "g", 500, 10, 23.50, 15),
    ("Sliced Ham", "Sadia", "g", 200, 10, 6.90, 30),
    ("Filled Cookie", "Nestlé", "g", 140, 20, 3.50, 60),
    ("Chocolate Bar", "Lacta", "g", 90, 15, 5.90, 40),
    ("Strawberry Yogurt", "Nestlé", "g", 170, 20, 2.90, 50),
    ("Butter", "Aviação", "g", 200, 8, 9.90, 25),
    ("Tomato Sauce", "Heinz", "g", 340, 12, 4.20, 45),
    ("Ketchup", "Heinz", "g", 380, 10, 8.50, 35),
    ("Mayonnaise", "Hellmanns", "g", 500, 10, 9.90, 40),
    ("Potato Sticks", "Elma Chips", "g", 120, 12, 6.90, 35),
    ("Snack", "Cheetos", "g", 100, 20, 4.50, 60),
    ("Sliced Bread", "Pullman", "g", 500, 10, 9.50, 30),
    ("Breakfast Cereal", "Nescau", "g", 300, 8, 12.50, 25),
    ("Saltine Crackers", "Bauducco", "g", 400, 15, 6.20, 50),
    ("Grape Juice", "Aurora", "ml", 1000, 10, 9.80, 30),
    ("Energy Drink", "Red Bull", "ml", 250, 15, 12.90, 40),
    ("Candy Mix", "Fini", "g", 100, 20, 3.20, 80),
    ("Chewing Gum", "Trident", "un", 10, 25, 2.50, 100),
    ("Ice Cream", "Kibon", "ml", 2000, 10, 25.00, 20),
    ("Frozen Chicken", "Seara", "kg", 1, 20, 12.90, 50),
    ("Ground Beef", "Friboi", "kg", 1, 15, 27.90, 40),
    ("Chicken Breast", "Sadia", "kg", 1, 15, 18.90, 40),
    ("Toscana Sausage", "Seara", "kg", 1, 12, 16.50, 30),
    ("Tilapia Fish", "Copacol", "g", 800, 8, 21.90, 20),
    ("French Bread", "Padaria Local", "g", 50, 100, 0.50, 500),
    ("Frozen Pizza", "Sadia", "g", 460, 10, 19.90, 25),
    ("Lasagna", "Perdigão", "g", 600, 10, 21.90, 25),
    ("Hot Dog Sausage", "Sadia", "g", 500, 15, 8.90, 40),
    ("Beef Hamburger", "Seara", "g", 672, 10, 24.90, 20),
    ("Aerosol Deodorant", "Rexona", "ml", 150, 15, 12.90, 40),
    ("Olive Oil", "Gallo", "ml", 500, 10, 29.90, 20),
    ("Cornmeal", "Yoki", "kg", 1, 12, 4.50, 40),
    ("Tapioca Flour", "Da Terrinha", "kg", 1, 10, 6.90, 30),
    ("Chimarrão Yerba Mate", "Barão", "g", 1000, 8, 18.90, 25),
    ("Black Tea", "Twinings", "g", 30, 10, 14.90, 15),
    ("Green Tea", "Leão", "g", 100, 12, 9.90, 20),
    ("Instant Noodles", "Nissin", "g", 80, 30, 2.20, 100),
    ("Cornflakes", "Kellogg's", "g", 300, 8, 11.90, 25),
    ("Instant Coffee", "Nescafé", "g", 200, 10, 15.90, 20),
    ("Chocolate Powder", "Nescau", "g", 400, 12, 9.50, 35),
    ("Honey", "Apis Flora", "g", 500, 8, 19.90, 15),
    ("Jam", "Queensberry", "g", 320, 10, 17.90, 20),
    ("Peanut Butter", "Amendocrem", "g", 500, 10, 14.90, 25),
    ("Granola", "Jasmine", "g", 1000, 8, 22.90, 20),
    ("Soy Sauce", "Sakura", "ml", 150, 12, 4.90, 35),
    ("Vinegar", "Castelo", "ml", 750, 15, 3.90, 40),
    ("Cachaça", "51", "ml", 965, 8, 15.90, 25),
    ("Whiskey", "Johnnie Walker", "ml", 1000, 5, 89.90, 10),
    ("Vodka", "Smirnoff", "ml", 1000, 6, 49.90, 15),
    ("Sparkling Water", "San Pellegrino", "ml", 750, 12, 8.90, 30),
    ("Soap Bar", "Lux", "g", 90, 20, 2.20, 80),
    ("Toothpaste", "Colgate", "g", 90, 20, 4.90, 60),
    ("Toothbrush", "Oral-B", "un", 1, 30, 7.50, 50),
    ("Sanitary Pads", "Always", "un", 8, 15, 6.90, 35),
    ("Paper Towel", "Scott", "un", 2, 12, 5.90, 40),
    ("Floor Cleaner", "Veja", "ml", 1000, 15, 7.90, 30),
    ("Disinfectant", "Lysoform", "ml", 500, 10, 9.50, 25),
    ("Bleach", "Qboa", "L", 2, 20, 6.90, 50),
    ("Steel Wool", "Bombril", "un", 8, 15, 3.50, 40),
    ("Matches", "Fiat Lux", "un", 10, 25, 1.50, 100),
    ("Charcoal", "Carvão Bom", "kg", 5, 10, 22.90, 20),
    ("Dog Food", "Pedigree", "kg", 15, 8, 79.90, 15),
    ("Cat Food", "Whiskas", "kg", 10, 10, 69.90, 12),
    ("Diapers", "Pampers", "un", 48, 10, 65.90, 20),
    ("Baby Wipes", "Huggies", "un", 48, 12, 15.90, 25),
    ("Sunblock", "Sundown", "ml", 200, 8, 39.90, 20),
    ("Body Lotion", "Nivea", "ml", 400, 10, 22.90, 25),
    ("Hand Soap", "Protex", "ml", 250, 15, 7.90, 30),
    ("Shaving Foam", "Gillette", "ml", 200, 10, 16.90, 20),
    ("Razor Blades", "Gillette", "un", 4, 12, 29.90, 15),
    ("Hair Gel", "Bozzano", "g", 300, 10, 12.90, 20),
    ("Dish Sponge", "Scotch-Brite", "un", 3, 20, 4.90, 50),
    ("Aluminum Foil", "Wyda", "m", 7.5, 15, 8.90, 25),
    ("Plastic Wrap", "Alpfilm", "m", 15, 12, 5.90, 30),
    ("Trash Bags", "Embalixo", "L", 50, 20, 18.90, 40),
    ("Light Bulb", "Philips", "un", 1, 20, 12.90, 30),
    ("Batteries AA", "Duracell", "un", 4, 15, 18.90, 35),
    ("Notebook", "Tilibra", "un", 1, 10, 15.90, 20),
    ("Ballpoint Pen", "BIC", "un", 5, 20, 7.50, 50)
]

# Criação automática dos 50 produtos
for i, produto in enumerate(produtos, start=1):
    barcode = f"1234567{i:03d}"  # código de barras único
    create_product(
        db,
        user_idF=new_user.id,
        barcode=barcode,
        name=produto[0],
        brand=produto[1],
        unit=produto[2],
        package_quantity=produto[3],
        minimum_stock=produto[4],
        suggested_price=produto[5],
        current_quantity=produto[6]
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

import random

movement_types = ["IN", "OUT", "LOSS"]

for _ in range(250):
    product = random.choice(produtos)  # escolhe um produto aleatório
    product_name = product[0]
    
    # Busca o registro do produto
    product_record = db.query(Product).filter(
        Product.name == product_name,
        Product.user_idF == new_user.id
    ).first()
    
    if not product_record:
        continue  # pula caso não encontre o produto
    
    product_id = product_record.id
    
    movement_type = random.choice(movement_types)
    
    if movement_type == "IN":
        quantity = random.randint(5, 50)  # entradas maiores
        purchase_price = round(random.uniform(product[5] * 0.8, product[5] * 1.2), 2)
        sale_price = None
    elif movement_type == "OUT":
        max_quantity = max(1, min(int(product_record.current_quantity), 20))
        quantity = random.randint(1, max_quantity)
        sale_price = round(random.uniform(product[5] * 1.0, product[5] * 1.5), 2)
        purchase_price = None
    else:  # LOSS
        max_quantity = max(1, min(int(product_record.current_quantity), 10))
        quantity = random.randint(1, max_quantity)
        purchase_price = None
        sale_price = None

    # Cria a movimentação
    try:
        create_movement(
            db,
            user_idF=new_user.id,
            product_idF=product_id,
            quantity=quantity,
            type=movement_type,
            purchase_price=purchase_price,
            sale_price=sale_price,
            note=f"Random {movement_type.lower()} movement"
        )
    except ValueError as e:
        print(f"Movimentação para {product_name} não realizada: {e}")

print("Dados de teste inseridos com sucesso na tabela tamporária!")

#barcode = get_product_by_scanner(db, new_user.id)

db.close()
