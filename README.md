Autores: Erick Ventura Gamberini - 03099001; Igor Ventura - 1722540; Fernando Alves Landim - 1794239; Pedro Paulo Camargo - 1860175

# Sistema de Previsão de Inadimplência com Machine Learning

Projeto acadêmico de Machine Learning desenvolvido para estimar a probabilidade de inadimplência em operações de crédito, utilizando algoritmos de classificação supervisionada.

A solução contempla análise exploratória de dados, pré-processamento, treinamento e avaliação de modelos, otimização do limiar de decisão com base em custos financeiros simulados e integração com uma aplicação web desenvolvida em Flask.

## 1. Objetivo

Desenvolver um sistema capaz de estimar a probabilidade de um cliente não cumprir suas obrigações financeiras, auxiliando na análise de risco de crédito.

O projeto também busca demonstrar como diferentes limiares de classificação influenciam os resultados do modelo e os custos associados aos erros de previsão.

**Importante:** trata-se de um projeto educacional baseado em dados sintéticos, sem validação para uso em decisões reais de concessão de crédito.

## 2. Tecnologias utilizadas

- Python
- Pandas e NumPy
- Scikit-learn
- Jupyter Notebook
- Flask
- Joblib
- Git e GitHub

## 3. Base de dados

Foi utilizado um conjunto de dados sintéticos com 6.000 registros de operações de crédito.

As variáveis incluem:

- Idade do cliente
- Renda mensal
- Tempo de emprego
- Score de crédito
- Quantidade de dívidas ativas
- Posse de imóvel
- Finalidade do empréstimo
- Prazo do contrato
- Valor do empréstimo

A variável-alvo é `inadimplente`, em que:

- `0`: cliente adimplente
- `1`: cliente inadimplente

Os dados foram divididos em 80% para treinamento e 20% para teste, preservando a proporção das classes.

## 4. Metodologia

O desenvolvimento foi dividido nas seguintes etapas:

1. Análise exploratória dos dados, incluindo distribuição das classes, valores ausentes e características das variáveis.
2. Pré-processamento com tratamento de valores ausentes, padronização de variáveis numéricas e codificação de variáveis categóricas.
3. Treinamento de três algoritmos: Regressão Logística, Random Forest e Árvore de Decisão.
4. Comparação por validação cruzada com a métrica ROC AUC.
5. Avaliação do modelo selecionado em um conjunto de teste separado.
6. Análise de diferentes limiares de decisão considerando custos de falsos positivos e falsos negativos.
7. Integração do modelo com uma interface web utilizando Flask.

## 5. Comparação dos modelos

| Modelo | ROC AUC médio (validação cruzada) |
|---|---:|
| Regressão Logística | 0,7613 |
| Random Forest | 0,7300 |
| Árvore de Decisão | 0,5760 |

A Regressão Logística apresentou o melhor desempenho médio e foi selecionada para a aplicação.

## 6. Otimização do limiar de decisão

O limiar padrão de classificação é 0,50. Entretanto, ele não necessariamente minimiza os custos financeiros associados aos erros de previsão.

Neste projeto, foram considerados os seguintes custos hipotéticos:

| Tipo de erro | Custo |
|---|---:|
| Falso positivo | R$ 1.500 |
| Falso negativo | R$ 8.000 |

A seleção do limiar foi realizada utilizando probabilidades obtidas por validação cruzada no conjunto de treinamento.

Entre os limiares avaliados, foi selecionado **0,16 (16%)**.

### Resultados no conjunto de teste

| Métrica | Limiar 50% | Limiar 16% |
|---|---:|---:|
| Acurácia | 80,75% | 64,08% |
| Precisão | 57,14% | 32,97% |
| Recall | 21,31% | 74,18% |
| Custo estimado | R$ 1.594.500 | R$ 1.056.000 |

A alteração do limiar produziu uma redução estimada de **33,77% nos custos simulados** no conjunto de teste.

Esse resultado representa uma comparação experimental sob hipóteses específicas de custo, não uma economia financeira comprovada em operações reais.

## 7. Aplicação web

Foi desenvolvida uma aplicação utilizando Flask para permitir que o usuário informe características de um cliente e de um contrato de crédito.

A aplicação retorna:

- Probabilidade estimada de inadimplência
- Classificação prevista
- Limiar de decisão utilizado

A classificação utiliza o limiar de 16%, definido na análise de custos.

## 8. Execução do projeto

### Clonar o repositório

```bash
git clone https://github.com/IgorVentura0517/Inadimplencia-ML
cd Inadimplencia-ML
```

### Criar e ativar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Instalar as dependências

```powershell
pip install -r requirements.txt
```

### Treinar o modelo

```powershell
python treinar.py
```

### Iniciar a aplicação

```powershell
python app.py
```

Acesse:

http://127.0.0.1:5000

## 9. Ética e LGPD

Modelos de análise de crédito podem reproduzir desigualdades presentes nos dados e produzir resultados injustos para determinados grupos.

Mesmo quando atributos sensíveis não são utilizados diretamente, outras variáveis podem atuar como indicadores indiretos dessas características.

O projeto considera a importância da proteção de dados pessoais, da transparência, da avaliação de vieses e da revisão de decisões automatizadas.

A discussão completa está disponível em `docs/etica_lgpd.md`.

## 10. Limitações e trabalhos futuros

- Utilização de dados sintéticos.
- Ausência de validação com dados reais.
- Necessidade de monitoramento de desempenho e possíveis vieses.
- Custos financeiros definidos hipoteticamente.
- Necessidade de validação adicional do limiar antes de qualquer aplicação real.
- Possibilidade de evolução para monitoramento contínuo e implantação em produção.

## 11. Organização do desenvolvimento

O projeto foi desenvolvido de maneira incremental, utilizando Git e GitHub para controle de versões e colaboração entre os integrantes da equipe.

As atividades foram organizadas em etapas, contemplando análise exploratória, modelagem, avaliação, integração da aplicação e análise de custos.

O desenvolvimento utilizou branches específicas para implementação de funcionalidades e documentação, com integração das alterações à branch principal por meio de Pull Requests.

Essa abordagem permitiu acompanhar a evolução do projeto, separar responsabilidades e manter um histórico das implementações.

## 11. Conclusão

O projeto demonstrou a construção de um fluxo completo de Machine Learning, desde a análise exploratória até a disponibilização de previsões em uma aplicação web.

Além da comparação de algoritmos, a análise de limiares evidenciou que a escolha do ponto de corte pode alterar significativamente o equilíbrio entre precisão, recall e custos financeiros simulados.

O resultado reforça a importância de avaliar modelos não apenas por métricas estatísticas, mas também pelas consequências práticas de suas decisões.