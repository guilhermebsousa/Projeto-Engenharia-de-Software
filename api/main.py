# api/main.py
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from api.schemas import SignupIn
from api.schemas import LoginIn, UserOut, ProductIn, ProductOut, MovementIn
from api.deps import get_db
from database.models.users import RoleEnum, User
from database.models.products import Product
from database.services import (
    authenticate_user, create_user, get_all_users,
    list_products, create_product, get_product_by_id,
    create_movement, get_by_barcode, update_product, delete_product,
    is_below_minimum_stock, get_all_movements, get_movements_by_period,
    get_user_by_username
)

# NOVO: criar tabelas
from database.database import Base, engine

# NOVO: leitor de código
from barcode_scanner.scanner import get_barcode

app = FastAPI(title="sTOK API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Startup: garante tabelas ----
@app.on_event("startup")
def _create_tables():
    Base.metadata.create_all(bind=engine)

# -------------------------
# ROTAS DE API
# -------------------------

# ---- AUTH ----
@app.post("/api/login", response_model=UserOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return UserOut(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role.value,
    )

@app.post("/api/signup", response_model=UserOut)
def signup(payload: SignupIn, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, payload.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = create_user(
        db,
        username=payload.username,
        password=payload.password,
        role=RoleEnum.OPERATOR,      # ou o role que desejar
        email=payload.email,
        full_name=payload.full_name
    )
    return UserOut(
        id=new_user.id,
        username=new_user.username,
        full_name=new_user.full_name,
        role=new_user.role.value,
        email=new_user.email,
    )


# Seed simples (dev)
@app.post("/api/users/seed", response_model=UserOut)
def seed_user(db: Session = Depends(get_db)):
    # evita duplicar
    existing = db.query(User).filter(User.username == "op_front").first()
    if existing:
        return UserOut(
            id=existing.id,
            username=existing.username,
            full_name=existing.full_name,
            role=existing.role.value,
        )
    u = create_user(db, username="op_front", password="123", role=RoleEnum.OPERATOR)
    return UserOut(
        id=u.id,
        username=u.username,
        full_name=u.full_name,
        role=u.role.value,
    )

# ---- PRODUCTS ----
@app.get("/api/users/{user_id}/products", response_model=list[ProductOut])
def get_products(user_id: str, search: str | None = None, db: Session = Depends(get_db)):
    prods = list_products(db, user_id=user_id, search=search)
    return [
        ProductOut(
            id=p.id,
            user_idF=p.user_idF,
            barcode=p.barcode,
            name=p.name,
            brand=p.brand,
            unit=p.unit,
            package_quantity=p.package_quantity,
            minimum_stock=p.minimum_stock,
            suggested_price=p.suggested_price,
            current_quantity=p.current_quantity,
            expiration_date=p.expiration_date,
        )
        for p in prods
    ]

@app.get("/api/users/{user_id}/products/{product_id}", response_model=ProductOut)
def get_single_product(user_id: str, product_id: str, db: Session = Depends(get_db)):
    # Chama a função de serviço que você já tem para buscar o produto
    p = get_product_by_id(db, product_id=product_id, user_id=user_id)
    
    # Se o produto não for encontrado, retorna um erro 404
    if not p:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Se encontrou, retorna os dados do produto
    return ProductOut(
        id=p.id,
        user_idF=p.user_idF,
        barcode=p.barcode,
        name=p.name,
        brand=p.brand,
        unit=p.unit,
        package_quantity=p.package_quantity,
        minimum_stock=p.minimum_stock,
        suggested_price=p.suggested_price,
        current_quantity=p.current_quantity,
        expiration_date=p.expiration_date,
    )

@app.post("/api/users/{user_id}/products", response_model=ProductOut, status_code=201)
def post_product(user_id: str, payload: ProductIn, db: Session = Depends(get_db)):
    p = create_product(db, user_idF=user_id, **payload.dict())
    return ProductOut(
        id=p.id,
        user_idF=p.user_idF,
        barcode=p.barcode,
        name=p.name,
        brand=p.brand,
        unit=p.unit,
        package_quantity=p.package_quantity,
        minimum_stock=p.minimum_stock,
        suggested_price=p.suggested_price,
        current_quantity=p.current_quantity,
        expiration_date=p.expiration_date,
    )

# Editar produto
@app.put("/api/users/{user_id}/products/{product_id}", response_model=ProductOut)
def put_product(user_id: str, product_id: str, payload: ProductIn, db: Session = Depends(get_db)):
    # Verifica se o produto existe antes de tentar atualizar
    db_product = get_product_by_id(db, product_id=product_id, user_id=user_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Chama a função de serviço para atualizar o produto no banco de dados
    updated_product = update_product(db, product_id=product_id, user_id=user_id, **payload.dict())
    
    # Retorna o produto atualizado
    return ProductOut(
        id=updated_product.id,
        user_idF=updated_product.user_idF,
        barcode=updated_product.barcode,
        name=updated_product.name,
        brand=updated_product.brand,
        unit=updated_product.unit,
        package_quantity=updated_product.package_quantity,
        minimum_stock=updated_product.minimum_stock,
        suggested_price=updated_product.suggested_price,
        current_quantity=updated_product.current_quantity,
        expiration_date=updated_product.expiration_date,
    )

# ---- MOVEMENTS ----
@app.post("/api/users/{user_id}/movements")
def post_movement(user_id: str, payload: MovementIn, db: Session = Depends(get_db)):
    m = create_movement(
        db,
        user_idF=user_id,
        product_idF=payload.product_idF,
        quantity=payload.quantity,
        type=payload.type,  # string "IN" | "OUT" | "LOSS" (tratado no service)
        purchase_price=payload.purchase_price,
        sale_price=payload.sale_price,
        note=payload.note,
        expiration_date=payload.expiration_date,
    )
    return {"id": m.id, "ok": True}

# ---- SCAN (NOVO) ----
@app.post("/api/users/{user_id}/scan")
def scan_barcode(user_id: str, db: Session = Depends(get_db)):
    code = get_barcode()  # abre webcam no servidor
    if not code:
        raise HTTPException(status_code=400, detail="Não foi possível ler o código")
    prod = get_by_barcode(db, barcode=code, user_id=user_id)
    if prod:
        return {
            "barcode": code,
            "product": {
                "id": prod.id,
                "name": prod.name,
                "brand": prod.brand,
                "unit": prod.unit,
                "package_quantity": prod.package_quantity,
                "minimum_stock": prod.minimum_stock,
                "suggested_price": prod.suggested_price,
                "current_quantity": prod.current_quantity,
            },
        }
    return {"barcode": code, "product": None}

# SERVIR O FRONTEND

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse(f"<pre>index.html não encontrado em:\n{index_path}</pre>", status_code=500)
    return FileResponse(str(index_path))
