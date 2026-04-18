from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente


class PacienteSchema(BaseModel):
    """Define como um novo paciente deve ser representado na requisição."""

    name:     str   = "João Silva"
    age:      int   = 52
    sex:      int   = 1
    cp:       int   = 0
    trestbps: int   = 125
    chol:     int   = 212
    fbs:      int   = 0
    restecg:  int   = 1
    thalach:  int   = 168
    exang:    int   = 0
    oldpeak:  float = 1.0
    slope:    int   = 2
    ca:       int   = 2
    thal:     int   = 3


class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado após inserção/consulta."""

    id:       int   = 1
    name:     str   = "João Silva"
    age:      int   = 52
    sex:      int   = 1
    cp:       int   = 0
    trestbps: int   = 125
    chol:     int   = 212
    fbs:      int   = 0
    restecg:  int   = 1
    thalach:  int   = 168
    exang:    int   = 0
    oldpeak:  float = 1.0
    slope:    int   = 2
    ca:       int   = 2
    thal:     int   = 3
    outcome:  Optional[int] = None


class PacienteBuscaSchema(BaseModel):
    """Define a estrutura para busca de paciente por nome."""

    name: str = "João Silva"


class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada."""

    pacientes: List[PacienteSchema]


class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado."""

    name: str = "João Silva"


def apresenta_paciente(paciente: Paciente):
    """Retorna a representação de um paciente seguindo PacienteViewSchema."""
    return {
        "id":       paciente.id,
        "name":     paciente.name,
        "age":      paciente.age,
        "sex":      paciente.sex,
        "cp":       paciente.cp,
        "trestbps": paciente.trestbps,
        "chol":     paciente.chol,
        "fbs":      paciente.fbs,
        "restecg":  paciente.restecg,
        "thalach":  paciente.thalach,
        "exang":    paciente.exang,
        "oldpeak":  paciente.oldpeak,
        "slope":    paciente.slope,
        "ca":       paciente.ca,
        "thal":     paciente.thal,
        "outcome":  paciente.outcome,
    }


def apresenta_pacientes(pacientes: List[Paciente]):
    """Retorna a representação de uma lista de pacientes."""
    result = []
    for paciente in pacientes:
        result.append({
            "id":       paciente.id,
            "name":     paciente.name,
            "age":      paciente.age,
            "sex":      paciente.sex,
            "cp":       paciente.cp,
            "trestbps": paciente.trestbps,
            "chol":     paciente.chol,
            "fbs":      paciente.fbs,
            "restecg":  paciente.restecg,
            "thalach":  paciente.thalach,
            "exang":    paciente.exang,
            "oldpeak":  paciente.oldpeak,
            "slope":    paciente.slope,
            "ca":       paciente.ca,
            "thal":     paciente.thal,
            "outcome":  paciente.outcome,
        })
    return {"pacientes": result}