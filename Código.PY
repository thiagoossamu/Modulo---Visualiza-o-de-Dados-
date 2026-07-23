import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('../Pycharm/ecommerce_estatistica.csv')
print(df.head())
print(df.columns)

# Análise dos dados
print('          Análise dos dados da E-Commerce              ')

total_produtos = len(df)
print(f' Total produtos: {total_produtos}')
total_vendas = df['Qtd_Vendidos_Cod'].sum()
print(f' Total de Unidades Vendidas: {total_vendas}')
preco_medio = df['Preço'].mean()
print(f'Preço Médio dos Produtos: {preco_medio}')
nota_media = df['Nota'].mean()
print(f'Avaliação média dos produtos: {nota_media}')
faturamento_total = (df['Preço']* df['Qtd_Vendidos_Cod']).sum()
print(f' Faturamento Bruto Estimando: {faturamento_total:,.2f}')

# Concentração por Marca
df['Faturamento_Item'] = df['Preço'] * df['Qtd_Vendidos_Cod']

fat_marca = df.groupby('Marca')['Faturamento_Item'].agg(['sum', 'count']).sort_values(by='sum', ascending=False)
fat_marca['share'] = (fat_marca['sum'] / faturamento_total) * 100
fat_marca['cum_share'] = fat_marca['share'].cumsum()

print('\n         Concentralção por Marca       ')
print(fat_marca.head(10).round(2))

# Gráfico de Histograma
plt.figure(figsize = (10,6))
plt.hist(df['Preço'], bins = 100, color = '#42f5ad', alpha = 0.8)
plt.title('Histograma - Distribuição de Preço dos Produtos')
plt.xlabel('Preço(R$)')
plt.xticks(ticks=range(0, int(df['Preço'].max())+ 50, 50))
plt.ylabel('Qtd. de Produtos')
plt.grid(True, linestyle = '--', alpha=0.7)
plt.show()

# Gráfico de Dispersão
sns.jointplot(x='Preço', y='Qtd_Vendidos_Cod',hue='Gênero', data=df, kind='scatter') # ('scatter, 'hist', 'hex', 'kde', 'reg', 'resid')
plt.show()

# Mapa de Calor
corr = df[['Preço', 'Desconto_MinMax']].corr()
plt.figure(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap='vlag')
plt.title('Correlação Preço e Desconto')
plt.tight_layout()
plt.show()

# Gráfico de Barra
plt.figure(figsize=(10, 6))
sns.barplot(x='Material', y='Preço', data=df, estimator='mean', errorbar=None,hue='Material', legend=False,palette='viridis')
plt.title('Preço Médio por Tipo de Material')
plt.xlabel('Material')
plt.ylabel('Preço Médio(R$)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Gráfico de Pizza
contagem_temporada = df['Temporada'].value_counts()
plt.figure(figsize=(8, 8))
explode=[0.05] * len(contagem_temporada)
plt.pie(contagem_temporada, labels=contagem_temporada.index, autopct='%1.1f%%', startangle=140, colors=['#e7f525','#eb790e','#c2108f','#19046b','#19c2ab','#07a607','#6311a6'],explode=explode, pctdistance=0.8)
plt.title('Distribuição Percentual de Produtos por Temporada')
plt.show()

# Gráfico de Densidade
plt.figure(figsize=(10, 8))
sns.kdeplot(data=df, x='Preço', hue='Temporada', fill=True,common_norm=False, alpha=0.4,palette='Set2',warn_singular=False,)
plt.title('Comparação da Densidade de Preços por Temporada')
plt.xlabel('Preço(R$)')
plt.ylabel('Densidade')
plt.grid(True, linestyle = '--', alpha=0.3)
plt.show()

# Gráfico de Regressão
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='N_Avaliações', y='Preço',  color='#8a880c', scatter_kws={'alpha': 0.5,'s':40,'color': '#351640'},
line_kws={'color':'#700629','linewidth':2.5})
plt.title('Relação entre Número de Avaliações e Preço', fontsize=12, fontweight='bold')
plt.xlabel('Número de Avaliações')
plt.ylabel('Preço(R$)')
plt.grid(True, linestyle = '--', alpha=0.3)
plt.tight_layout()
plt.show()
