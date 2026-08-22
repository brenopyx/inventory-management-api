from fastapi import FastAPI
from app.routers import categorias, produtos, movimentacoes
from app.models import produto, categoria, movimentacao

app = FastAPI(title="Inventory Management API")

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)