from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.movimentacao import Movimentacao, TipoMovimentacao
from app.schemas.movimentacao import MovimentacaoCreate, MovimentacaoResponse
from fastapi import HTTPException

def calcular_estoque_atual(db: Session, produto_id: int) -> int:
    resultado = db.query(
        func.sum(
            case(
                (Movimentacao.tipo == TipoMovimentacao.ENTRADA, Movimentacao.quantidade),
                (Movimentacao.tipo == TipoMovimentacao.SAIDA, -Movimentacao.quantidade)
            )
        )
    ).filter(Movimentacao.produto_id == produto_id).scalar()

    return resultado or 0


def registrar_movimentacao(db: Session, movimentacao: MovimentacaoCreate) -> Movimentacao:
    estoque_atual = calcular_estoque_atual(db, movimentacao.produto_id)

    if movimentacao.tipo == TipoMovimentacao.SAIDA:
        if movimentacao.quantidade > estoque_atual:
            raise HTTPException(status_code=400, detail = f"Estoque insuficiente. Disponível: {estoque_atual}, Solicitado: {movimentacao.quantidade}")

    nova_movimentacao = Movimentacao(
            produto_id = movimentacao.produto_id,
            tipo = movimentacao.tipo,
            quantidade = movimentacao.quantidade,
            motivo = movimentacao.motivo
        )
    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)
    return nova_movimentacao
    
