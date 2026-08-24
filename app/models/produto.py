from sqlalchemy import ForeignKey, Integer, String, Float, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(40), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(200), nullable=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), insert_default=func.now())

    categoria: Mapped["Categoria"] = relationship(back_populates="produtos")
    movimentacoes: Mapped[list["Movimentacao"]] = relationship(back_populates="produto")