"""Compara algoritmos, avalia no teste e salva o modelo.  Uso: python treinar.py"""
import json

import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from config import DADOS, MODELOS, SEMENTE

FEATURES_NUMERICAS = [
    "idade",
    "renda_mensal",
    "tempo_emprego_anos",
    "score_credito",
    "dividas_ativas",
    "prazo_meses",
    "valor_emprestimo",
]
FEATURES_CATEGORICAS = ["possui_imovel", "finalidade"]
ALVO = "inadimplente"


def candidatos():
    return {
        "Regressão Logística": LogisticRegression(max_iter=1000, random_state=SEMENTE),
        "Árvore de Decisão": DecisionTreeClassifier(random_state=SEMENTE),
        "Random Forest": RandomForestClassifier(random_state=SEMENTE),
    }


def criar_pipeline(modelo):
    preprocessador = ColumnTransformer([
        ("numericas", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), FEATURES_NUMERICAS),
        ("categoricas", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]), FEATURES_CATEGORICAS),
    ])
    return Pipeline([("preprocessador", preprocessador), ("modelo", modelo)])


def dividir():
    df = pd.read_csv(DADOS / "credito.csv")
    X = df[FEATURES_NUMERICAS + FEATURES_CATEGORICAS]  # id e alvo ficam de fora
    y = df[ALVO]
    return train_test_split(X, y, test_size=0.20, stratify=y, random_state=SEMENTE)


def avaliar(modelo, X_teste, y_teste):
    prob = modelo.predict_proba(X_teste)[:, 1]
    prev = (prob >= 0.5).astype(int)
    precisao, revocacao, _ = precision_recall_curve(y_teste, prob)
    return {
        "acuracia": accuracy_score(y_teste, prev),
        "precisao": precision_score(y_teste, prev),
        "recall": recall_score(y_teste, prev),
        "f1": f1_score(y_teste, prev),
        "roc_auc": roc_auc_score(y_teste, prob),
        "pr_auc": auc(revocacao, precisao),
        "matriz_confusao": confusion_matrix(y_teste, prev).tolist(),
    }


def main():
    X_treino, X_teste, y_treino, y_teste = dividir()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMENTE)

    comparacao = {}
    for nome, modelo in candidatos().items():
        notas = cross_val_score(
            criar_pipeline(modelo), X_treino, y_treino, cv=cv, scoring="roc_auc", n_jobs=-1
        )
        comparacao[nome] = {"media": float(notas.mean()), "desvio": float(notas.std())}
        print(f"  {nome:<20} {notas.mean():.4f} ± {notas.std():.4f}")

    escolhido = max(comparacao, key=lambda n: comparacao[n]["media"])
    modelo = criar_pipeline(candidatos()[escolhido]).fit(X_treino, y_treino)
    teste = avaliar(modelo, X_teste, y_teste)
    print(f"  Escolhido: {escolhido} | teste: {teste}")

    MODELOS.mkdir(exist_ok=True)
    joblib.dump(modelo, MODELOS / "credito.joblib", compress=3)
    metricas = {
        "credito": {
            "modelo": escolhido,
            "metrica": "ROC AUC",
            "validacao_cruzada": comparacao,
            "teste": teste,
            "sklearn": sklearn.__version__,
        }
    }
    (MODELOS / "metricas.json").write_text(
        json.dumps(metricas, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
