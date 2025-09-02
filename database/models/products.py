from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_idF = Column(String, ForeignKey("users.id"), nullable=False)  # Mercado: dono do produto
    barcode = Column(String, unique=False, nullable=False)             # Pode repetir entre mercados? -> Unique = False
    name = Column(String, nullable=False)
    brand = Column(String)
    unit = Column(String, nullable=False)
    package_quantity = Column(Float)
    minimum_stock = Column(Float, default=0)
    suggested_price = Column(Float)
    current_quantity = Column(Float, default=0)
    expiration_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    movements = relationship("Movement", back_populates="product")
    user = relationship("User", back_populates="products")

    def __repr__(self):
        return (
            f"<Product(name={self.name}, stock={self.current_quantity}, "
            f"owner={self.owner.username})>"
        )