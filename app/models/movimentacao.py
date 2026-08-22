from sqlalchemy import ForeignKey, Integer, String, Float, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
import enum


class TipoMovimentacao(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    tipo: Mapped[TipoMovimentacao] = mapped_column(nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str] = mapped_column(String(50), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), insert_default=func.now())

    produto: Mapped["Produto"] = relationship(back_populates="movimentacoes")