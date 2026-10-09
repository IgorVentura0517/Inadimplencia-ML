import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"data/credito.csv")
df_inad = df[df["inadimplente"] == 1]
df_renda_zero = df[df["renda_mensal"].isna()]

df_imovel = df.groupby('possui_imovel')['inadimplente'].mean().reset_index()
df_imovel['taxa_inadimplencia_%'] = df_imovel['inadimplente'] * 100

qtd = len(df)
cont_inad = len(df_inad)

colunas_para_testar = df.columns.difference(["inadimplente"])
colunas_zeradas = colunas_para_testar[(df[colunas_para_testar] == 0).any()]

prop = (cont_inad/qtd) * 100

score_inad = df.groupby("inadimplente")["score_credito"].describe()

# Qtd de contratos e inadimplentes
print(f"\n{'=' * 58}")
print(f"Qtd de contratos e inadimplentes")
print('=' * 58)

print(f'\n{len(df)} Contratos')
print(f'{len(df_inad)} Contratos')

# Inadimplentes e com valores zerados
print(f"\n{'=' * 58}")
print(f"Inadimplentes e com valores zerados")
print('=' * 58)

print(f'\nInadimplentes: {prop:.2f}%')
print(f'{len(df_renda_zero)} Contratos')

# Colunas com valores zerados
print(f"\n{'=' * 58}")
print(f"Colunas com Valores Zerados")
print('=' * 58)

print(f"\nColunas com valores nulos:", colunas_zeradas)
print(f"Qtd de colunas com valores nulos: {len(colunas_zeradas)}")

# Inadimplêntes por finalidade

bins = [299, 500, 600, 700, 800, 1000]
labels = ['300 a 500', '501 a 600', '601 a 700', '701 a 800', '801 a 1000']
df['faixa_score'] = pd.cut(df['score_credito'], bins=bins, labels=labels)

def exibir_concentracao(titulo, coluna):
    res = df.groupby(coluna, observed=False)['inadimplente'].agg(
        taxa=lambda x: f"{x.mean() * 100:.2f}%",
        concentracao=lambda x: f"{(x.sum() / cont_inad) * 100:.2f}%"
    ).rename(columns={
        'taxa': 'Taxa Inadimplência (%)',
        'concentracao': 'Concentração dos Inadimplentes (%)'
    })
    
    print(f"\n{'=' * 58}")
    print(f" {titulo.upper()}")
    print('=' * 58)
    print(res.to_string())

exibir_concentracao("Score de Crédito", 'faixa_score')
exibir_concentracao("Finalidade do Empréstimo", 'finalidade')
exibir_concentracao("Posse de Imóvel", 'possui_imovel')