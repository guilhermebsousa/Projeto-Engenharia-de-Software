from sqlalchemy.orm import Session
from ..models.products import Product
from barcode_scanner import scanner

# Criar novo produto
def create_product(db: Session, user_idF: str, **data):
    product = Product(**data, user_idF=user_idF)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# Listar todos os produtos (opcionalmente filtrar por nome ou marca)
def list_products(db: Session, user_id: str, search: str = None):
    query = db.query(Product).filter(Product.user_idF == user_id)
    if search:
        search = f"%{search.lower()}%"
        query = query.filter(Product.name.ilike(search) | Product.brand.ilike(search))
    return query.all()

# Pegar produto por código de barras
def get_by_barcode(db: Session, barcode: str, user_id: str):
    return db.query(Product).filter(Product.barcode == barcode, Product.user_idF == user_id).first()

# Pegar produto por ID
def get_product_by_id(db: Session, product_id: str, user_id: str):
    return db.query(Product).filter(Product.id == product_id, Product.user_idF == user_id).first()

# UPDATE um produto existente
def update_product(db: Session, product_id: str, user_id: str, **data):
    product = get_product_by_id(db, product_id, user_id)
    if not product:
        return None  # Product not found

    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

# DELETE produto por ID
def delete_product(db: Session, product_id: str, user_id: str):
    product = get_product_by_id(db, product_id, user_id)
    if not product:
        return False  # Produto não encontrado

    db.delete(product)
    db.commit()
    return True

# Se tiver menos produtos que o minimo necessario, retorna True
def is_below_minimum_stock(db: Session, product_id: str, user_id: str):
    product = get_product_by_id(db, product_id, user_id)
    if not product:
        return None  # Produto não encontrado
    return product.current_quantity < product.minimum_stock


def get_product_by_scanner(db: Session, user_idF: str):
    barcode = scanner.get_barcode()
    if barcode:
        produto = get_by_barcode(db, barcode, user_idF)
        if produto:
            print(f"Produto: {produto.brand} {produto.name} {produto.package_quantity}{produto.unit}")
            print(f"Id: {produto.id}")
            return produto
        else:
            print("Produto não encontrado.")
            return False
    else:
        print("Nenhum código foi lido.")
    return None