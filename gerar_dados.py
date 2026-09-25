import numpy as np
import pandas as pd

from config import DADOS, SEMENTE


rng = np.random.default_rng(SEMENTE)


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


def escolher(opcoes, pesos, n):
    return rng.choice(opcoes, n, p=pesos)


def apagar(df, coluna, fracao):
    """Simula valores ausentes, muito comuns em dados reais."""
    df.loc[rng.random(len(df)) < fracao, coluna] = np.nan


def gerar_credito(n=6000):
    """Dados do exercício: inadimplência em empréstimos."""

    d = pd.DataFrame({
        "id_contrato": [f"E{i:05d}" for i in range(1, n + 1)]
    })

    d["idade"] = np.clip(
        rng.normal(40, 12, n), 18, 80
    ).round()

    d["renda_mensal"] = np.clip(
        4200 * rng.lognormal(0, .6, n), 1300, 60000
    ).round(-1)

    d["tempo_emprego_anos"] = np.clip(
        rng.gamma(1.6, 3.5, n), 0, 40
    ).round(1)

    d["score_credito"] = np.clip(
        rng.normal(640, 110, n), 300, 1000
    ).round()

    d["dividas_ativas"] = rng.poisson(1.1, n)

    d["possui_imovel"] = escolher(
        ["sim", "nao"],
        [.4, .6],
        n
    )

    d["finalidade"] = escolher(
        ["pessoal", "veiculo", "reforma", "educacao", "negocio"],
        [.35, .25, .15, .1, .15],
        n
    )

    d["prazo_meses"] = escolher(
        [12, 24, 36, 48, 60],
        [.15, .3, .25, .15, .15],
        n
    )

    d["valor_emprestimo"] = np.clip(
        d.renda_mensal * rng.uniform(.5, 6, n),
        1000,
        200000
    ).round(-2)

    comprometimento = (
        d.valor_emprestimo
        * 1.33
        / d.prazo_meses
        / d.renda_mensal
    )

    z = (
        -2.2
        + 2.8 * np.clip(comprometimento, 0, 1.5)
        - .009 * (d.score_credito - 640)
        + .4 * d.dividas_ativas
        - .06 * d.tempo_emprego_anos
        - .35 * (d.possui_imovel == "sim")
        + .45 * (d.finalidade == "negocio")
        - .015 * (d.idade - 40)
        + rng.normal(0, .5, n)
    )

    d["inadimplente"] = (
        rng.random(n) < sigmoide(z)
    ).astype(int)

    apagar(d, "renda_mensal", .04)
    apagar(d, "tempo_emprego_anos", .03)

    return d


def main():
    DADOS.mkdir(exist_ok=True)

    df = gerar_credito()

    df.to_csv(
        DADOS / "credito.csv",
        index=False
    )

    print(f"data/credito.csv: {len(df)} linhas")


if __name__ == "__main__":
    main()