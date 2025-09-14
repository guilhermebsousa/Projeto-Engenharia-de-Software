from sqlalchemy import Column, String, Float, Enum, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid
import enum     

class MovementType(enum.Enum):
    IN = "IN"                    # entrada
    OUT = "OUT"                  # saida
    LOSS = "LOSS"                # perda

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
    note = Column(Text) # Observações adicionais
    expiration_date = Column(DateTime) # Validade do lote movimentado
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    user = relationship("User", back_populates="movements")
    product = relationship("Product", back_populates="movements")

    def __repr__(self):
        owner = self.user.full_name or self.user.username if self.user else "Usuário"
        t = (self.type.value if hasattr(self.type, "value") else str(self.type)).upper()
        verbo = "recebeu" if t == "IN" else ("retirou" if t == "OUT" else "baixou (perda)")
        qtd = self.quantity
        nome = self.product.name if self.product else "Produto"
        val = self.expiration_date.strftime('%d/%m/%Y') if self.expiration_date else 'N/A'
        return f"{owner} {verbo} {qtd} unidades de {nome} (validade {val})."
