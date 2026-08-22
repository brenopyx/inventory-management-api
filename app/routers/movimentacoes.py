from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.movimentacao import Movimentacao
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from app.services.estoque_service import registrar_movimentacao

router = APIRouter(prefix="/movimentacaoes", tags=["Movimentacoes"])

@router.get("/", response_model=list[MovimentacaoResponse])
def listar_movimentacoes(produto_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Movimentacao)

    if produto_id is not None:
        query = query.filter(Movimentacao.produto_id == produto_id).all()

    return query

@router.post("/", response_model=MovimentacaoResponse)
def criar_movimentacao(movimentacao: MovimentacaoCreate, 
                       db: Session = Depends(get_db)):
    return registrar_movimentacao(db, movimentacao)

@router.get("/{movimentacao_id}", response_model=MovimentacaoResponse)
def buscar_movimentacao(movimentacao_id: int, db: Session = Depends(get_db)):
    movimentacao = db.query(Movimentacao).filter(Movimentacao.id == movimentacao_id).first()

    if movimentacao is None:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")

    return movimentacao
