from pydantic import BaseModel

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str

    model_config = {"from_attributes": True}

class CategoriaUpdate(BaseModel):
    nome: str | None = None