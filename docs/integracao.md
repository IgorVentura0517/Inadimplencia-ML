# Integração do modelo à aplicação (Issue #5)

## Estrutura

```
config.py            problemas, features e limites (fonte única)
treinar.py           treina, compara, avalia e salva o modelo em models/
app.py               API Flask
templates/index.html interface web (HTML e JavaScript)
static/style.css     estilos da interface
models/              credito.joblib e metricas.json (gerados, não versionados)
```

## Fluxo

```
TREINO:     data/credito.csv -> Pipeline -> validação cruzada -> teste -> models/
INFERÊNCIA: Navegador -> JSON -> API Flask -> modelo.predict_proba() -> Navegador
```

## Decisões de integração

- **`PROBLEMAS` como fonte única.** O problema `credito` é descrito uma vez em `config.py` (arquivo, alvo, features, limites e opções). O treino, a API e o formulário leem dali e não divergem entre si. As features numéricas e categóricas do pipeline são derivadas desse dicionário.
- **Mesmo pipeline da modelagem.** `treinar.py` usa o pré-processamento do notebook (mediana + `StandardScaler` nas numéricas; moda + `OneHotEncoder` nas categóricas), split 80/20 estratificado com `random_state=42` e validação cruzada de 5 folds por ROC AUC. A Regressão Logística é escolhida e reproduz os valores da Issue #2.
- **Pipeline completo salvo.** O `joblib` guarda o pré-processamento junto com o modelo, então a API aplica em produção exatamente as transformações aprendidas no treino, sem vazamento de dados.
- **Validação da entrada.** `validar()` em `app.py` confere tipo, limite e opção de cada campo. Erros retornam HTTP 400 com mensagem; problema inexistente retorna 404. Campos vazios são aceitos, pois o pipeline os imputa.
- **Primeira execução automática.** Se `models/credito.joblib` ou `models/metricas.json` não existirem, `app.py` gera os dados (se necessário) e treina antes de subir. Os dois arquivos são gerados e estão no `.gitignore`.
- **Probabilidade e classe.** A API devolve a probabilidade de inadimplência. A interface mostra o percentual e a classe prevista com corte em 0,5 (vermelho: inadimplente; verde: adimplente).
- **Métricas visíveis na interface.** A tela exibe a comparação por validação cruzada e as métricas no teste (acurácia, precisão, recall, F1, ROC AUC e matriz de confusão).

## Como executar

```bash
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

## Testes de previsão

| Cenário | Entrada | Probabilidade | Previsão |
|---|---|---|---|
| Risco baixo | 50 anos, renda R$ 15.000, 15 anos de emprego, score 850, sem dívidas, possui imóvel, pessoal, 36 meses, R$ 10.000 | 0,4% | adimplente |
| Risco alto | 22 anos, renda R$ 1.500, 0,5 ano de emprego, score 350, 6 dívidas, sem imóvel, negócio, 12 meses, R$ 60.000 | 99,1% | inadimplente |

Capturas: `docs/teste_risco_baixo.jpg` e `docs/teste_risco_alto.jpg`.

Validação da API:
- entrada fora dos limites ou com categoria inválida: HTTP 400 com a mensagem do campo;
- problema inexistente: HTTP 404;
- requisição sem campos: probabilidade calculada após imputação.
