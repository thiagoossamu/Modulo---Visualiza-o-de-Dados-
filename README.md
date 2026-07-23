Tecnologias Utilizadas
•	Python — Linguagem principal
•	Pandas — Manipulação e análise de dados
•	Matplotlib — Construção de gráficos
•	Seaborn — Visualização de dados estatísticos

Principais Análises Realizadas

1. Métricas Gerais de Desempenho (Kpis)
Calcula e exibe no console os indicadores básicos de saúde do catálogo:
•	Total de produtos cadastrados.
•	Unidades totais vendidas.
•	Preço médio e avaliação média dos produtos.
•	Faturamento Bruto Estimado (calculado via Prec\co×Qtd_Vendidos).
•	
2. Concentração de Mercado por Marca
Análise do princípio de Pareto (Curva ABC) focado nas marcas:
•	Faturamento acumulado e participação percentual (market share) das 10 principais marcas.

3. Visualizações Estatísticas e Gráficos
O script gera 7 gráficos complementares para investigar a estrutura dos dados:
Gráfico	Tipo 	Objetivo da Análise
Histograma de Preços	plt.hist	Avaliar a frequência e a assimetria na distribuição de preços do catálogo.
Dispersão com Marginais	sns.jointplot	Analisar a relação entre Preço e Vendas por Gênero.
Mapa de Calor (Heatmap)	sns.heatmap	Identificar a correlação entre o valor do Preço e a taxa de Desconto aplicada.
Gráfico de Barras	sns.barplot	Comparar o preço médio praticado para cada tipo de Material.
Gráfico de Pizza	plt.pie	Observar a distribuição percentual de produtos cadastrados por Temporada.
Gráfico de Densidade (KDE)	sns.kdeplot	Comparar como a faixa de preço varia entre diferentes temporadas.
Gráfico de Regressão	sns.regplot	Verificar se há tendência entre o volume de avaliações (reviews) e o preço do item.

 
 Como Executar o Projeto
Pré-requisitos
Certifique-se de ter o Python 3.x instalado em sua máquina e as bibliotecas necessárias:
Bash
pip install pandas matplotlib seaborn
Estrutura de Pastas Esperada
Garantir que o arquivo CSV esteja no diretório correto em relação ao script:
Plaintext
├── Pycharm/
│   └── ecommerce_estatistica.csv
└── seu_script.py
Execução
Rode o script diretamente via terminal ou pela sua IDE (PyCharm, VS Code, etc.):
Bash
python seu_script.py
Destaques de Código
•	Criação da variável de Faturamento por Item:
Python
df['Faturamento_Item'] = df['Preço'] * df['Qtd_Vendidos_Cod']
•	Cálculo da participação percentual e acumulada por marca:
Python
fat_marca['share'] = (fat_marca['sum'] / faturamento_total) * 100
fat_marca['cum_share'] = fat_marca['share'].cumsum()

