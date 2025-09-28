# database/services/movements_service.py
from database.models.movements import Movement, MovementType
from database.models.products import Product
from sqlalchemy.orm import Session

def create_movement(
    db: Session,
    user_idF: str,
    product_idF: str,
    quantity: float,
    type: str,  # "IN" | "OUT" | "LOSS"
    purchase_price: float = None,
    sale_price: float = None,
    origin: str = None,
    destination: str = None,
    note: str = None,
    expiration_date=None,
):
    product = db.query(Product).filter(
        Product.id == product_idF, Product.user_idF == user_idF
    ).first()
    if not product:
        raise ValueError("Produto não encontrado ou não pertence a este usuário")

    # Converte string para Enum
    try:
        mtype = MovementType[type]
    except KeyError:
        raise ValueError("Tipo de movimentação inválido. Use IN, OUT ou LOSS")

    # Atualiza estoque
    if mtype == MovementType.IN:
        if purchase_price is None:
            raise ValueError("Preço de compra é obrigatório para entradas")
        product.current_quantity = (product.current_quantity or 0) + quantity

    elif mtype == MovementType.OUT:
        if (product.current_quantity or 0) < quantity:
            raise ValueError("Estoque insuficiente para saída")
        if sale_price is None:
            raise ValueError("Preço de venda é obrigatório para saídas")
        product.current_quantity = (product.current_quantity or 0) - quantity

    elif mtype == MovementType.LOSS:
        if (product.current_quantity or 0) < quantity:
            raise ValueError("Estoque insuficiente para perda")
        product.current_quantity = (product.current_quantity or 0) - quantity

    movement = Movement(
        product_idF=product_idF,
        user_idF=user_idF,
        quantity=quantity,
        type=mtype,
        purchase_price=purchase_price,
        sale_price=sale_price,
        note=note,
        expiration_date=expiration_date,
    )

    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement

def get_all_movements(db: Session, user_id: str):
    # Corrige nome da coluna: user_idF
    return db.query(Movement).filter(Movement.user_idF == user_id).all()

def get_movements_by_period(db: Session, user_id: str, start_date, end_date):
    # Corrige campos: user_idF e created_at
    return db.query(Movement).filter(
        Movement.user_idF == user_id,
        Movement.created_at >= start_date,
        Movement.created_at <= end_date
    ).all()
