# Definição das tabelas do banco de dados
from .products import Product
from .users import User
from .movements import Movement

__all__ = ["Product", "User", "Movement"]