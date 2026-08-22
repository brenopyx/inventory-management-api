from app.models.movimentacao import TipoMovimentacao
from pydantic import BaseModel
from datetime import datetime

class MovimentacaoCreate(BaseModel):

    produto_id: int
    tipo: TipoMovimentacao
    quantidade: int
    motivo: str | None = None

class MovimentacaoResponse(BaseModel):

    id: int
    produto_id: int
    tipo: TipoMovimentacao
    quantidade: int
    motivo: str | None = None
    criado_em : datetime

    model_config = {"from_attributes": True}