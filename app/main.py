from fastapi import FastAPI
from app.routers import categorias, produtos, movimentacoes, usuarios
from app.models import produto, categoria, movimentacao, usuario

app = FastAPI(title="Inventory Management API")

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(usuarios.router)