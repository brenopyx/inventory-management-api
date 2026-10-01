from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import categorias, produtos, movimentacoes, usuarios
from app.models import produto, categoria, movimentacao, usuario

app = FastAPI(title="Inventory Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(usuarios.router)