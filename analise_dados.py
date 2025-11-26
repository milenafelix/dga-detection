import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Configurações visuais para ficar com cara de artigo científico
sns.set_theme(style="whitegrid")
ARQUIVO_DADOS = "dataset_mestrado.csv"

print("--- INICIANDO ANÁLISE ESTATÍSTICA ---")

# 1. Carregar os dados
try:
    df = pd.read_csv(ARQUIVO_DADOS)
    print(f"Dados carregados: {len(df)} linhas.")
except FileNotFoundError:
    print("ERRO: O arquivo 'dataset_mestrado.csv' não foi encontrado.")
    print("Rode o script 'coleta_dados.py' primeiro.")
    exit()

# 2. A Mágica Matemática: Entropia de Shannon
# Explicação: Mede o grau de "incerteza" ou "aleatoriedade" de uma string.
# 'google' = baixa entropia (repetição de letras, padrão).
# 'xkyz123' = alta entropia (tudo misturado).
def calcular_entropia(texto):
    if not isinstance(texto, str): return 0
    p, lns = Counter(texto), float(len(texto))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

print("Calculando entropia (pode levar alguns segundos)...")
df['entropia'] = df['domain_full'].apply(calcular_entropia)
df['tamanho'] = df['domain_full'].apply(len)

# Traduzir labels para o gráfico ficar legível
df['Categoria'] = df['label'].map({0: 'Legítimo (Humano)', 1: 'DGA (Malicioso)'})

# 3. Gerar os Gráficos
print("Gerando gráficos...")
plt.figure(figsize=(12, 6))

# Gráfico A: Histograma de Entropia (A prova de separação)
plt.subplot(1, 2, 1)
sns.histplot(data=df, x='entropia', hue='Categoria', kde=True, element="step", bins=30)
plt.title('Distribuição da Entropia de Shannon')
plt.xlabel('Nível de Entropia (Aleatoriedade)')
plt.ylabel('Quantidade de Domínios')

# Gráfico B: Boxplot (Comparação de Médias)
plt.subplot(1, 2, 2)
sns.boxplot(x='Categoria', y='entropia', data=df, palette="Set2")
plt.title('Comparação Direta: Legítimo vs Malicioso')
plt.ylabel('Nível de Entropia')

# Salvar
plt.tight_layout()
plt.savefig('figura_1_viabilidade.png', dpi=300) # dpi 300 é qualidade de impressão
print("\n--- CONCLUÍDO! ---")
print("Foi gerada uma imagem chamada 'figura_1_viabilidade.png'. Abra para ver!")
plt.show() # Tenta abrir a janela com o gráfico