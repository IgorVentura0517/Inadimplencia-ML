import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dataset
df = pd.read_csv('data/credito.csv')

# Estilo visual padronizado
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

# Taxa de inadimplência média da carteira (usada como linha de referência)
taxa_media_inadimplencia = df['inadimplente'].mean() * 100

fig, ax = plt.subplots(figsize=(8, 5))

# Curvas de densidade (KDE)
sns.kdeplot(
    data=df[df['inadimplente'] == 0]['score_credito'], 
    label='Adimplente (0)', 
    fill=True, 
    alpha=0.4, 
    color='#2b5c8f', 
    ax=ax
)
sns.kdeplot(
    data=df[df['inadimplente'] == 1]['score_credito'], 
    label='Inadimplente (1)', 
    fill=True, 
    alpha=0.4, 
    color='#d95f02', 
    ax=ax
)

# Linhas de mediana
mediana_adimplente = df[df["inadimplente"] == 0]["score_credito"].median()
mediana_inadimplente = df[df["inadimplente"] == 1]["score_credito"].median()

ax.axvline(mediana_adimplente, color='#2b5c8f', linestyle='--', label=f'Mediana Adimplente: {mediana_adimplente:.0f}')
ax.axvline(mediana_inadimplente, color='#d95f02', linestyle='--', label=f'Mediana Inadimplente: {mediana_inadimplente:.0f}')

# Formatação de eixos e títulos
ax.set_title('Distribuição do Score de Crédito por Status de Inadimplência', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Score de Crédito')
ax.set_ylabel('Densidade')
ax.legend(frameon=True)

plt.tight_layout()
plt.savefig('grafico_1_score_credito.png', dpi=300)
plt.show()

#====================================================================================================================================

# Agregação e cálculo da taxa percentual
df_fin = df.groupby('finalidade')['inadimplente'].mean().reset_index()
df_fin['taxa_inadimplencia_%'] = df_fin['inadimplente'] * 100
df_fin = df_fin.sort_values(by='taxa_inadimplencia_%', ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))

bars = sns.barplot(
    data=df_fin,
    x='finalidade',
    y='taxa_inadimplencia_%',
    palette='Blues_r',
    ax=ax
)

# Linha de média geral
ax.axhline(taxa_media_inadimplencia, color='red', linestyle='--', label=f'Média Geral ({taxa_media_inadimplencia:.1f}%)')
ax.set_title('Taxa de Inadimplência por Finalidade do Empréstimo', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Finalidade')
ax.set_ylabel('Taxa de Inadimplência (%)')
ax.set_ylim(0, 30)

# Rótulos com as porcentagens no topo de cada barra
for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        ax.annotate(f'{altura:.1f}%', (p.get_x() + p.get_width() / 2., altura + 0.7),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig('grafico_2_finalidade.png', dpi=300)
plt.show()

#====================================================================================================================================

# Agregação por posse de imóvel
df_imovel = df.groupby('possui_imovel')['inadimplente'].mean().reset_index()
df_imovel['taxa_inadimplencia_%'] = df_imovel['inadimplente'] * 100

fig, ax = plt.subplots(figsize=(6, 5))

bars = sns.barplot(
    data=df_imovel,
    x='possui_imovel',
    y='taxa_inadimplencia_%',
    palette=['#e74c3c', '#2ecc71'],
    ax=ax
)

# Linha de média geral
ax.axhline(taxa_media_inadimplencia, color='gray', linestyle='--', label=f'Média Geral ({taxa_media_inadimplencia:.1f}%)')
ax.set_title('Taxa de Inadimplência por Posse de Imóvel', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Possui Imóvel?')
ax.set_ylabel('Taxa de Inadimplência (%)')
ax.set_ylim(0, 26)

# Rótulos nas barras
for p in ax.patches:
    altura = p.get_height()
    if altura > 0:
        ax.annotate(f'{altura:.1f}%', (p.get_x() + p.get_width() / 2., altura + 0.6),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig('grafico_3_possui_imovel.png', dpi=300)
plt.show()