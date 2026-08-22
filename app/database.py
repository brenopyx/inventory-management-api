from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os

# Conxao com o DataBase
load_dotenv()
conexao_db = os.getenv("DATABASE_URL")

engine = create_engine(conexao_db)
Sessao = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = Sessao()
    try:
        yield db
    finally:
        db.close()
        