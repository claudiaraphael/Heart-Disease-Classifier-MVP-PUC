import pickle


class Pipeline:

    def __init__(self):
        """Inicializa o pipeline."""
        self.pipeline = None

    def carrega_pipeline(self, path):
        """Carrega o pipeline serializado gerado durante o treinamento.

        O pipeline já contém o scaler e o modelo encadeados,
        portanto não é necessário aplicar nenhuma transformação
        manual antes da predição.

        Arguments:
            path: caminho para o arquivo .pkl do pipeline

        Returns:
            pipeline carregado pronto para predição
        """
        with open(path, "rb") as file:
            self.pipeline = pickle.load(file)
        return self.pipeline