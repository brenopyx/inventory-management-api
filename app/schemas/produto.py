from pydantic import BaseModel
from datetime import datetime
from app.schemas.categoria import CategoriaResponse

class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    descricao: str | None = None
    categoria_id: int

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    descricao: str | None = None
    categoria: CategoriaResponse
    criado_em: datetime

    model_config = {"from_attributes": True}

class EstoqueResponse(BaseModel):
    produto_id: int
    nome: str
    estoque_atual: int

class ProdutoUpdate(BaseModel):
    nome: str | None = None
    preco: float | None = None
    descricao: str | None = None
    categoria_id: int | None = None