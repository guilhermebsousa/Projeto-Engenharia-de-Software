from sqlalchemy import Column, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import uuid
import enum

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"          # Pode tudo, gerencia usuários, produtos e relatórios -> dono do aplicativo
    OPERATOR = "OPERATOR"    # Pode movimentar estoque, cadastrar produtos, mas não gerencia usuários -> empresa

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    email = Column(String)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.OPERATOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="user")
    movements = relationship("Movement", back_populates="user")

    def is_admin(self):
        return self.role == RoleEnum.ADMIN

    def is_operator(self):
        return self.role == RoleEnum.OPERATOR

    def __repr__(self):
        return (
            f"<User(username={self.username}, role={self.role}, "
            f"is_active={self.is_active})>"
        )