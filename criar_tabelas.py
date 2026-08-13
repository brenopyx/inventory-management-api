from app.database import Base, engine
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.movimentacao import Movimentacao

Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")