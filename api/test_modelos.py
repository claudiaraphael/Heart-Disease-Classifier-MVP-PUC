from model import *

# Para rodar: pytest -v test_modelos.py

# Instanciação das classes auxiliares
carregador = Carregador()
avaliador  = Avaliador()
pipeline   = Pipeline()

# Caminhos dos dados de teste gerados no notebook
url_X_test = "./MachineLearning/data/X_test_heart_disease.csv"
url_y_test = "./MachineLearning/data/y_test_heart_disease.csv"

# Colunas do dataset Heart Disease (sem o target)
colunas = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal",
]

# Carregando os dados de teste
X_test_df = carregador.carregar_dados(url_X_test, colunas)
y_test_df = carregador.carregar_dados(url_y_test, ["target"])

X = X_test_df.values
y = y_test_df.values.ravel()


def test_modelo_svm():
    """Testa se o pipeline SVM atinge acurácia mínima de 80% no conjunto de teste.

    O threshold de 80% foi definido com base nos resultados da validação
    cruzada durante o treinamento, onde o SVM com StandardScaler atingiu
    consistentemente acurácia acima desse valor.

    Este teste garante que, caso o modelo seja substituído, o novo modelo
    só será implantado se atender ao mesmo requisito mínimo de desempenho.
    """
    pipeline_path = "./MachineLearning/pipelines/svm_heart_disease_pipeline.pkl"
    modelo_svm = pipeline.carrega_pipeline(pipeline_path)

    acuracia = avaliador.avaliar(modelo_svm, X, y)
    print(f"\nAcurácia do SVM no conjunto de teste: {acuracia:.4f}")

    assert acuracia >= 0.80, (
        f"Acurácia {acuracia:.4f} abaixo do threshold mínimo de 0.80. "
        "O modelo não atende aos requisitos de desempenho."
    )