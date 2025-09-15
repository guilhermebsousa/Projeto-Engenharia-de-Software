from database.models.movements import Movement
from database.models.products import Product
from sqlalchemy.orm import Session
from barcode_scanner import scanner
from .products_service import get_by_barcode

# Registrar movimentação (entrada, saída, perda, etc.)
def create_movement(db: Session, user_idF: str, product_idF: str, quantity: int, type: str, purchase_price: float = None, sale_price: float = None, origin: str = None, destination: str = None, note: str = None, expiration_date = None):
    product = db.query(Product).filter(Product.id == product_idF, Product.user_idF == user_idF).first()
    if not product:
        raise ValueError("Produto não encontrado ou não pertence a este usuário")

    # Atualiza estoque
    if type == "IN":
        if purchase_price is None:
            raise ValueError("Preço de compra é obrigatório para entradas")
        product.current_quantity += quantity
    elif type == "OUT":
        if product.current_quantity < quantity:
            raise ValueError("Estoque insuficiente para saída")
        if sale_price is None:
            raise ValueError("Preço de venda é obrigatório para saídas (vendas)")
        product.current_quantity -= quantity
    elif type == "LOSS" and product.current_quantity >= quantity and sale_price is None:
        product.current_quantity -= quantity
    else:
        raise ValueError("Movimentação inválida ou estoque insuficiente")

    movement = Movement(
        product_idF=product_idF,
        user_idF=user_idF,
        quantity=quantity,
        type=type,
        purchase_price=purchase_price,
        sale_price=sale_price,
        note=note,
        expiration_date=expiration_date
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

# Listar todas as movimentações
def get_all_movements(db: Session, user_id: str):
    return db.query(Movement).filter(Movement.user_id == user_id).all()

# Obter movimentações por período
def get_movements_by_period(db: Session, user_id: str, start_date, end_date):
    return db.query(Movement).filter(
        Movement.user_id == user_id,
        Movement.date >= start_date,
        Movement.date <= end_date
    ).all()

def get_movements_by_scanner(db: Session, user_idF: str):
    barcode = scanner.get_barcode()
    if not barcode:
        print("Nenhum código foi lido.")
        return None

    produto = get_by_barcode(db, barcode, user_idF)
    if not produto:
        print("Produto não encontrado.")
        return None

    # Buscar movimentações relacionadas ao produto lido
    movements = db.query(Movement).filter(
        Movement.product_idF == produto.id,
        Movement.user_idF == user_idF
    ).all()

    if not movements:
        print(f"Nenhuma movimentação encontrada para {produto.name}.")
        return []

    print(f"Movimentações do produto: {produto.brand} {produto.name}")
    for mov in movements:
        print(f"- {mov.created_at} | {mov.type} | Qtd: {mov.quantity} | "
              f"Compra: {mov.purchase_price} | Venda: {mov.sale_price} | Nota: {mov.note}")

    return movements