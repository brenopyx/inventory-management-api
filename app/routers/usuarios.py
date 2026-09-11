from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, LoginRequest
from app.security import hash_senha, verificar_senha, criar_token_acesso

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if usuario_existente is not None:
            raise HTTPException(
                status_code=400, 
                detail="Este e-mail já está registrado"
                )

    novo_usuario = Usuario(
        nome = usuario.nome,
        email = usuario.email,
        senha_hash = hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario is None or not verificar_senha(dados.senha, usuario.senha_hash):
         raise HTTPException(
              status_code=401,
              detail="Email ou senha incorretos"
         )

    token = criar_token_acesso({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
      