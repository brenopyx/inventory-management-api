from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao
from app.schemas.produto import ProdutoCreate, ProdutoResponse, EstoqueResponse, ProdutoUpdate
from app.services.estoque_service import calcular_estoque_atual

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome = produto.nome,
        preco = produto.preco,
        descricao = produto.descricao,
        categoria_id = produto.categoria_id
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto is None:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
            )

    return produto

@router.get("/{produto_id}/estoque", response_model=EstoqueResponse)
def consultar_estoque(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto is None:
        raise HTTPException(
            status_code = 404, 
            detail = "Produto não encontrado"
            )
    
    estoque_atual = calcular_estoque_atual(db, produto_id)

    return EstoqueResponse(
        produto_id = produto.id,
        nome = produto.nome,
        estoque_atual = estoque_atual
    )

@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto is None:
        raise HTTPException(
            status_code=404, 
            detail="Produto não encontrado"
            )

    if dados.nome is not None:
        produto.nome = dados.nome

    if dados.preco is not None:
        produto.preco = dados.preco

    if dados.descricao is not None:
        produto.descricao = dados.descricao

    if dados.categoria_id is not None:
            produto.categoria_id = dados.categoria_id

    db.commit()
    db.refresh(produto)

    return produto

@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_delete = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto_delete is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    movimentacao_vinculada = db.query(Movimentacao).filter(Movimentacao.produto_id == produto_id).first()

    if movimentacao_vinculada is not None:
        raise HTTPException(
            status_code=400, 
            detail="Não é possível excluir: existem movimentações vinculadas a esse produto"
            )

    produto_response = ProdutoResponse.model_validate(produto_delete)

    db.delete(produto_delete)
    db.commit()

    return None
