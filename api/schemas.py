from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoginIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    full_name: Optional[str] = None
    role: str

class ProductIn(BaseModel):
    barcode: str
    name: str
    brand: Optional[str] = None
    unit: str
    package_quantity: Optional[float] = None
    minimum_stock: Optional[float] = 0
    suggested_price: Optional[float] = None
    current_quantity: Optional[float] = 0
    expiration_date: Optional[datetime] = None

class ProductOut(ProductIn):
    id: str
    user_idF: str

class MovementIn(BaseModel):
    product_idF: str
    type: str  # "IN" | "OUT" | "LOSS"
    quantity: float
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    note: Optional[str] = None
    expiration_date: Optional[datetime] = None
