from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db

app = FastAPI(
    title="Catalog API",
    description="API для каталога товаров",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Catalog API is running"}

@app.get("/products/all", response_model=List[schemas.Product])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить все товары"""
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/get/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Получить товар по ID"""
    return crud.get_product(db, product_id)

@app.get("/categories/", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    """Получить все категории"""
    return crud.get_categories(db)

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Создать новый товар"""
    return crud.create_product(db, product)

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    return crud.create_category(db, category)