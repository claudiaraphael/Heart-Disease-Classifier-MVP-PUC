from sklearn.model_selection import train_test_split
import numpy as np


class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador."""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """Divide o dataset em conjuntos de treino e teste usando holdout.

        Arguments:
            dataset:          DataFrame com features e target na última coluna
            percentual_teste: proporção dos dados reservada para teste (ex: 0.2)
            seed:             semente aleatória para reprodutibilidade

        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        X_train, X_test, y_train, y_test = self.__preparar_holdout(
            dataset, percentual_teste, seed
        )
        return (X_train, X_test, y_train, y_test)

    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """Método privado que executa a divisão holdout.

        Assume que a variável target está na última coluna.
        """
        dados = dataset.values
        X = dados[:, 0:-1]
        y = dados[:, -1]
        return train_test_split(X, y, test_size=percentual_teste, random_state=seed)

    def preparar_form(self, form):
        """Prepara os dados recebidos do frontend para uso no modelo.

        Converte os campos do formulário em um array numpy no formato
        esperado pelo pipeline de predição (1 linha × 13 features).

        Arguments:
            form: PacienteSchema com os campos do paciente

        Returns:
            numpy.ndarray: array de shape (1, 13)
        """
        X_input = np.array([
            form.age,
            form.sex,
            form.cp,
            form.trestbps,
            form.chol,
            form.fbs,
            form.restecg,
            form.thalach,
            form.exang,
            form.oldpeak,
            form.slope,
            form.ca,
            form.thal,
        ])
        # Reshape para que o pipeline entenda que é uma única amostra
        return X_input.reshape(1, -1)