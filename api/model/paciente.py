from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from model import Base


class Paciente(Base):
    __tablename__ = 'pacientes'

    id          = Column(Integer, primary_key=True)
    name        = Column("Name",     String(50))
    age         = Column("Age",      Integer)
    sex         = Column("Sex",      Integer)
    cp          = Column("CP",       Integer)
    trestbps    = Column("Trestbps", Integer)
    chol        = Column("Chol",     Integer)
    fbs         = Column("Fbs",      Integer)
    restecg     = Column("Restecg",  Integer)
    thalach     = Column("Thalach",  Integer)
    exang       = Column("Exang",    Integer)
    oldpeak     = Column("Oldpeak",  Float)
    slope       = Column("Slope",    Integer)
    ca          = Column("Ca",       Integer)
    thal        = Column("Thal",     Integer)
    outcome     = Column("Outcome",  Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, name: str, age: int, sex: int, cp: int,
                 trestbps: int, chol: int, fbs: int, restecg: int,
                 thalach: int, exang: int, oldpeak: float, slope: int,
                 ca: int, thal: int, outcome: int,
                 data_insercao: Union[DateTime, None] = None):
        self.name      = name
        self.age       = age
        self.sex       = sex
        self.cp        = cp
        self.trestbps  = trestbps
        self.chol      = chol
        self.fbs       = fbs
        self.restecg   = restecg
        self.thalach   = thalach
        self.exang     = exang
        self.oldpeak   = oldpeak
        self.slope     = slope
        self.ca        = ca
        self.thal      = thal
        self.outcome   = outcome

        if data_insercao:
            self.data_insercao = data_insercao