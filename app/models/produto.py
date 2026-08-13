from sqlalchemy import ForeignKey, Integer, String, Float, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(40), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), insert_default=func.now())
