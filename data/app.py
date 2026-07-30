import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# 1. CARREGAMENTO DOS DADOS
# Caminho flexível: procura na pasta 'data/' ou na raiz
DATA_PATH = 'https://raw.githubusercontent.com/thiagoossamu/Modulo---Visualiza-o-de-Dados-/main/data/ecommerce_estatistica.csv'
df = pd.read_csv(DATA_PATH)


# 2. FUNÇÃO CONSTRUTORA DA APLICAÇÃO DASH
def cria_app(dataframe):
    app = Dash(__name__)
    app.title = "E-Commerce Dashboard Interativo"

    # Limites para o Slider de Preço
    preco_min = int(dataframe['Preço'].min())
    preco_max = int(dataframe['Preço'].max())

    # LAYOUT DA APLICAÇÃO
    app.layout = html.Div([
        html.H1('E-Commerce Dashboard Interativo', style={'textAlign': 'center', 'margin': '20px 0'}),

        html.Div([
            html.Div([
                html.Label('Filtrar por Gênero / Categoria:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='filtro-genero',
                    options=[{'label': g, 'value': g} for g in dataframe['Gênero'].dropna().unique()],
                    value=dataframe['Gênero'].dropna().unique()[0],
                    clearable=False
                )
            ], style={'width': '45%', 'display': 'inline-block', 'paddingRight': '20px'}),

            html.Div([
                html.Label('Filtrar Preço Máximo (R$):', style={'fontWeight': 'bold'}),
                dcc.Slider(
                    id='filtro-preco',
                    min=preco_min,
                    max=preco_max,
                    step=10,
                    value=preco_max,
                    marks={i: f'R${i}' for i in range(preco_min, preco_max + 1, int((preco_max - preco_min) / 4 or 1))}
                )
            ], style={'width': '45%', 'display': 'inline-block'})
        ], style={
            'padding': '20px',
            'backgroundColor': '#f8f9fa',
            'marginBottom': '20px',
            'borderRadius': '8px',
            'border': '1px solid #e9ecef'
        }),

        html.Br(),

        # Gráficos Dinâmicos Atualizados via Callback
        html.Div([
            html.Div(dcc.Graph(id='grafico-dispersao-dinamico'), style={'width': '50%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(id='grafico-barras-dinamico'), style={'width': '50%', 'display': 'inline-block'}),
        ]),

        html.Hr(style={'margin': '30px 0'}),
        html.H2("Análises Complementares"),

        dcc.Checklist(
            id='checklist-visibilidade',
            options=[
                {'label': ' Histograma ', 'value': 'fig1'},
                {'label': ' Mapa de Calor ', 'value': 'fig3'},
                {'label': ' Pizza ', 'value': 'fig5'},
                {'label': ' Densidade ', 'value': 'fig6'},
                {'label': ' Regressão ', 'value': 'fig7'}
            ],
            value=['fig1', 'fig3', 'fig5', 'fig6', 'fig7'],
            labelStyle={'display': 'inline-block', 'marginRight': '15px'}
        ),

        html.Br(),

        # Divs contendo os gráficos estáticos/alternados
        html.Div(dcc.Graph(id='fig1-histograma'), id='div-fig1'),
        html.Div(dcc.Graph(id='fig3-heatmap'), id='div-fig3'),
        html.Div(dcc.Graph(id='fig5-pizza'), id='div-fig5'),
        html.Div(dcc.Graph(id='fig6-violin'), id='div-fig6'),
        html.Div(dcc.Graph(id='fig7-regressao'), id='div-fig7')
    ], style={'padding': '0 30px', 'fontFamily': 'Arial, sans-serif'})

    # CALLBACK 1: Atualização dos Gráficos Interativos
    @app.callback(
        [Output('grafico-dispersao-dinamico', 'figure'),
         Output('grafico-barras-dinamico', 'figure')],
        [Input('filtro-genero', 'value'),
         Input('filtro-preco', 'value')]
    )
    def atualiza_graficos_interativos(genero_selecionado, preco_maximo):
        df_filtrado = dataframe[(dataframe['Gênero'] == genero_selecionado) & (dataframe['Preço'] <= preco_maximo)]

        fig_scatter = px.scatter(
            df_filtrado, x='Preço', y='Qtd_Vendidos_Cod',
            title=f'Preço vs Qtd Vendida ({genero_selecionado} - Até R${preco_maximo})',
            labels={'Qtd_Vendidos_Cod': 'Qtd Vendida', 'Preço': 'Preço (R$)'}
        )

        df_mat = df_filtrado.groupby('Material', as_index=False)['Preço'].mean()
        fig_bar = px.bar(
            df_mat, x='Material', y='Preço', color='Material',
            title=f'Preço Médio por Material ({genero_selecionado})'
        )
        fig_bar.update_layout(showlegend=False, xaxis_tickangle=-45)

        return fig_scatter, fig_bar

    # CALLBACK 2: Controle de Visibilidade dos Demais Gráficos
    @app.callback(
        [
            Output('div-fig1', 'style'), Output('div-fig3', 'style'),
            Output('div-fig5', 'style'), Output('div-fig6', 'style'),
            Output('div-fig7', 'style'),
            Output('fig1-histograma', 'figure'), Output('fig3-heatmap', 'figure'),
            Output('fig5-pizza', 'figure'), Output('fig6-violin', 'figure'),
            Output('fig7-regressao', 'figure')
        ],
        Input('checklist-visibilidade', 'value')
    )
    def visibilidade_e_carga_estatica(selected_values):
        graficos = ['fig1', 'fig3', 'fig5', 'fig6', 'fig7']
        estilos = [{} if g in selected_values else {'display': 'none'} for g in graficos]

        fig1 = px.histogram(dataframe, x='Preço', nbins=100, title='Histograma - Distribuição de Preço')

        corr = dataframe[['Preço', 'Desconto_MinMax']].corr()
        fig3 = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', title='Matriz de Correlação')

        contagem_temporada = dataframe['Temporada'].value_counts().reset_index()
        contagem_temporada.columns = ['Temporada', 'Quantidade']
        fig5 = px.pie(contagem_temporada, names='Temporada', values='Quantidade', title='Distribuição por Temporada')

        fig6 = px.violin(dataframe, x='Preço', color='Temporada', orientation='h', points=False,
                         title='Densidade de Preço por Temporada')

        fig7 = px.scatter(dataframe, x='N_Avaliações', y='Preço', trendline='ols', title='Avaliações vs Preço')

        return *estilos, fig1, fig3, fig5, fig6, fig7

    return app


# 3. EXECUÇÃO DO SERVIDOR
if __name__ == '__main__':
    app = cria_app(df)
    app.run(debug=True, port=8051)
    