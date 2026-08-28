from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from app.models.produto import Produto

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

@router.post("/", response_model=CategoriaResponse)
def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    nova_categoria = Categoria(nome = categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    return categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(categoria_id: int, dados: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if categoria is None:
        raise HTTPException(
            status_code=404, 
            detail="Categoria não encontrada"
            )

    if dados.nome is not None:
        categoria.nome = dados.nome

    db.commit()
    db.refresh(categoria)

    return categoria

@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria_delete = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if categoria_delete is None:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
            )

    produtos_vinculados = db.query(Produto).filter(Produto.categoria_id == categoria_id).first()

    if produtos_vinculados is not None:
        raise HTTPException(
            status_code=400, 
            detail="Não é possivel excluir: existem produtos vinculados a essa categoria"
            )

    db.delete(categoria_delete)
    db.commit()

    return None



