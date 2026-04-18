from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import Base
from model.paciente import Paciente
from model.pipeline import Pipeline
from model.preprocessador import PreProcessador
from model.avaliador import Avaliador
from model.carregador import Carregador

# Garante que o diretório do banco de dados existe
db_path = "database/"
if not os.path.exists(db_path):
    os.makedirs(db_path)

# URL de acesso ao banco SQLite local
db_url = "sqlite:///%s/pacientes.sqlite3" % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)