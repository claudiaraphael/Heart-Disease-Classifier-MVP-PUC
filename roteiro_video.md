# Roteiro — Vídeo de Apresentação do MVP (3 minutos)

---

## [0:00 – 0:30] Abertura — O Problema

> *Fala direta para a câmera ou narração sobre a tela inicial da aplicação*

"Doenças cardíacas são a principal causa de morte no mundo. Identificar pacientes em risco com base em dados clínicos, de forma rápida e acessível, pode salvar vidas.

Este projeto é um MVP de Sistemas Inteligentes desenvolvido para a PUC-Rio. O objetivo é simples: dado um conjunto de dados clínicos de um paciente, o sistema responde com uma previsão — **baixo risco ou alto risco** de doença cardíaca."

---

## [0:30 – 1:15] A Aplicação — Demo ao Vivo

> *Gravação da tela mostrando o frontend rodando no navegador*

"A aplicação roda localmente com um backend em Flask e uma interface web simples. Aqui temos o formulário de entrada, com os 13 atributos clínicos do paciente — como idade, pressão arterial, colesterol, frequência cardíaca máxima, entre outros.

Vou preencher os dados de um paciente hipotético..."

> *Preenche o formulário e clica em 'Prever'*

"...e em menos de um segundo o modelo retorna a predição. Neste caso: **alto risco**. O resultado aparece destacado, e o registro do paciente é salvo automaticamente no banco de dados.

Aqui embaixo vemos o histórico de todos os pacientes cadastrados, com a classificação de risco de cada um. Há também um botão para alternar entre modo claro e escuro."

---

## [1:15 – 2:15] O Modelo de Machine Learning

> *Mostra o notebook ou slides com os gráficos de comparação*

"O modelo foi treinado com o dataset UCI Heart Disease, que reúne dados de quatro hospitais diferentes — Cleveland, Hungria, Suíça e Long Beach. São **1.025 pacientes** com 13 atributos clínicos e uma variável alvo binária: tem ou não tem doença cardíaca.

Para escolher o melhor modelo, foram avaliados quatro algoritmos:
- K-Nearest Neighbors
- Árvore de Decisão
- Naive Bayes
- **SVM com kernel RBF** — que foi o vencedor

Cada algoritmo foi testado com três estratégias de normalização e validação cruzada de 10 folds. O SVM com C igual a 100 e gamma igual a 0,1 alcançou **97,56% de acurácia na validação cruzada**.

No conjunto de teste separado, com 205 amostras que o modelo nunca viu durante o treinamento, o resultado foi de **100% de acurácia**."

---

## [2:15 – 2:45] Arquitetura e Testes

> *Mostra brevemente o VS Code com a estrutura de pastas ou um diagrama*

"A arquitetura segue uma separação clara de responsabilidades. O pipeline de machine learning — pré-processamento e modelo SVM — é salvo em um arquivo `.pkl` e carregado pela API Flask a cada predição.

A aplicação tem cobertura de testes com pytest: testes de endpoints da API e um teste específico que verifica se o modelo mantém ao menos 80% de acurácia no conjunto de teste. Isso garante que o pipeline serializado funciona corretamente em produção."

---

## [2:45 – 3:00] Encerramento

> *Volta para a tela da aplicação ou câmera*

"Este MVP demonstra como técnicas de machine learning podem ser integradas a uma aplicação web funcional para apoiar decisões clínicas. O modelo SVM escolhido se mostrou preciso, robusto e adequado para este tipo de dado estruturado.

Todo o código, notebook de experimentação e documentação estão disponíveis no repositório. Obrigada."

---

## Dicas de Gravação

- **Duração alvo por bloco:** abertura 30s / demo 45s / ML 60s / arquitetura 30s / encerramento 15s
- **Resolução recomendada:** 1080p, 30fps
- **Gravação de tela:** OBS Studio ou Loom
- **Tom:** técnico mas acessível — imagine explicar para um colega de engenharia que não conhece o projeto
- **Mostrar obrigatoriamente na demo:** formulário preenchido → resultado de predição → tabela de histórico
