from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
import os

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Heart Disease Classifier API", version="1.0.0")
app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
paciente_tag = Tag(
    name="Paciente",
    description="Adição, visualização, remoção e predição de doença cardíaca em pacientes",
)


# Rota home — redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    return redirect("/front/index.html")


# Rota para documentação OpenAPI
@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pacientes
@app.get(
    "/pacientes",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_pacientes():
    """Lista todos os pacientes cadastrados na base.

    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    session = Session()
    try:
        pacientes = session.query(Paciente).all()
        if not pacientes:
            return {"pacientes": []}, 200
        logger.debug(f"%d pacientes encontrados" % len(pacientes))
        return apresenta_pacientes(pacientes), 200
    finally:
        session.close()


# Rota de adição de paciente + predição
@app.post(
    "/paciente",
    tags=[paciente_tag],
    responses={
        "200": PacienteViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)
def predict(body: PacienteSchema):
    """Adiciona um novo paciente à base de dados e retorna o diagnóstico
    de doença cardíaca previsto pelo modelo de machine learning.

    O modelo é carregado de forma embarcada no back-end a partir do
    arquivo .pkl gerado no notebook de treinamento.
    """
    preprocessador = PreProcessador()
    pipeline = Pipeline()

    X_input = preprocessador.preparar_form(body)

    model_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "MachineLearning", "pipelines", "svm_heart_disease_pipeline.pkl"
    )
    modelo = pipeline.carrega_pipeline(model_path)
    outcome = int(modelo.predict(X_input)[0])

    paciente = Paciente(
        name=body.name,
        age=body.age,
        sex=body.sex,
        cp=body.cp,
        trestbps=body.trestbps,
        chol=body.chol,
        fbs=body.fbs,
        restecg=body.restecg,
        thalach=body.thalach,
        exang=body.exang,
        oldpeak=body.oldpeak,
        slope=body.slope,
        ca=body.ca,
        thal=body.thal,
        outcome=outcome,
    )
    logger.debug(f"Adicionando paciente: '{paciente.name}'")

    session = Session()
    try:
        if session.query(Paciente).filter(Paciente.name == body.name).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.name}': {error_msg}")
            return {"message": error_msg}, 409

        session.add(paciente)
        session.commit()
        logger.debug(f"Paciente adicionado: '{paciente.name}'")
        return apresenta_paciente(paciente), 200

    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.name}': {error_msg} — {type(e).__name__}: {e}")
        return {"message": error_msg}, 400

    finally:
        session.close()


# Rota de busca de paciente por nome
@app.get(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def get_paciente(query: PacienteBuscaSchema):
    """Busca um paciente cadastrado na base pelo nome.

    Args:
        name (str): nome do paciente

    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    paciente_nome = query.name
    logger.debug(f"Buscando paciente: '{paciente_nome}'")
    session = Session()
    try:
        paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
        if not paciente:
            error_msg = f"Paciente '{paciente_nome}' não encontrado na base :/"
            logger.warning(error_msg)
            return {"message": error_msg}, 404
        logger.debug(f"Paciente encontrado: '{paciente.name}'")
        return apresenta_paciente(paciente), 200
    finally:
        session.close()


# Rota de remoção de paciente por nome
@app.delete(
    "/paciente",
    tags=[paciente_tag],
    responses={"200": PacienteViewSchema, "404": ErrorSchema},
)
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base pelo nome.

    Args:
        name (str): nome do paciente

    Returns:
        msg: mensagem de sucesso ou erro
    """
    paciente_nome = unquote(query.name)
    logger.debug(f"Removendo paciente: '{paciente_nome}'")
    session = Session()
    try:
        paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
        if not paciente:
            error_msg = "Paciente não encontrado na base :/"
            logger.warning(f"Erro ao remover paciente '{paciente_nome}': {error_msg}")
            return {"message": error_msg}, 404
        session.delete(paciente)
        session.commit()
        logger.debug(f"Paciente removido: '{paciente_nome}'")
        return {"message": f"Paciente '{paciente_nome}' removido com sucesso!"}, 200
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)
