from pathlib import Path

PASTA = Path(__file__).resolve().parent
DADOS = PASTA / "data"
MODELOS = PASTA / "models"

SEMENTE = 42


def num(padrao, minimo, maximo):
    return {"tipo": "numero", "padrao": padrao, "min": minimo, "max": maximo}


def cat(*opcoes):
    return {"tipo": "categoria", "padrao": opcoes[0], "opcoes": list(opcoes)}


PROBLEMAS = {
    "credito": {
        "titulo": "Inadimplência de crédito",
        "tipo": "classificacao",
        "arquivo": "credito.csv",
        "alvo": "inadimplente",
        "limiar_decisao": 0.16,
        "resultado": "Probabilidade de inadimplência",
        "features": {
            "idade": num(40, 18, 80),
            "renda_mensal": num(4200, 1300, 60000),
            "tempo_emprego_anos": num(3, 0, 40),
            "score_credito": num(640, 300, 1000),
            "dividas_ativas": num(1, 0, 20),
            "possui_imovel": cat("sim", "nao"),
            "finalidade": cat("pessoal", "veiculo", "reforma", "educacao", "negocio"),
            "prazo_meses": num(36, 12, 60),
            "valor_emprestimo": num(15000, 1000, 200000),
        },
    },
}