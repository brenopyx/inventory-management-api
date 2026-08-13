from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

# Conxao com o DataBas
load_dotenv()
conexao_db = os.getenv("DATABASE_URL")

engine = create_engine(conexao_db)
Sessao = sessionmaker(engine)

class Base(DeclarativeBase):
    pass
