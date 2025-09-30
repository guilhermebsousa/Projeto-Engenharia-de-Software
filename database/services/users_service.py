from database.models.users import User, RoleEnum
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

# Criar usuário
def create_user(db: Session, username: str, password: str, role: RoleEnum, email: str, full_name: Optional[str] = None):
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        password_hash=hashed_password,
        role=role,
        email=email,
        full_name=full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Buscar usuário por nome
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Autenticar usuário
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

# Listar todos os usuários
def get_all_users(db: Session):
    return db.query(User).all()

# Deletar usuário
def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
