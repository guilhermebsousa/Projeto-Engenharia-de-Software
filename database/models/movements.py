from sqlalchemy import Column, String, Float, Enum, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
import enum     

class MovementType(enum.Enum):
    IN = "IN"                    # entrada
    OUT = "OUT"                  # saida
    # TRANSFER = "TRANSFER"        # transferencia
    LOSS = "LOSS"                # perda
    # SALE = "SALE"                # venda

class Movement(Base):
    __tablename__ = "stock_movements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_idF = Column(String, ForeignKey("users.id"), nullable=False)         # Usuário (Mercado) que realizou a movimentação
    product_idF = Column(String, ForeignKey("products.id"), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float)
    # margin_pct = Column(Float) # Margem de lucro em porcentagem - usar???
    sale_price = Column(Float) 
    origin = Column(String) # Local de origem (para transferências)
    destination = Column(String) # Local de destino (para transferências)
    note = Column(Text) # Observações adicionais
    expiration_date = Column(DateTime) # Validade do lote movimentado
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="movements")
    product = relationship("Product", back_populates="movements")

    def __repr__(self):
        return (
            f"{self.user.full_name if self.user else 'Usuário desconhecido'} "
            f"{'recebeu' if self.type.value == 'in' else 'retirou'} "
            f"{self.quantity} unidades do {self.product.name} "
            f"com validade {self.expiration_date.strftime('%d/%m/%Y') if self.expiration_date else 'N/A'}."
        )