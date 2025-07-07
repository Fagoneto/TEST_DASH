import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text

# --- Configurações do banco de dados ---
user = "franciscoabraao"
password = "Clarice2006"
host = "localhost"
port = "5432"
database = "painel_comex"
engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

# --- Função para carregar os dados ---
def carregar_dados(tipo):
    query = text(f"""
        SELECT ano, SUM(kg) AS volume
        FROM pescados_dados_{tipo}
        GROUP BY ano
        ORDER BY ano
    """)
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df

# --- Dash App ---
app = dash.Dash(__name__)

# --- Layout ---
app.layout = html.Div([
    html.H1("Painel de Exportação e Importação de Pescado", style={"textAlign": "center"}),

    dcc.Tabs([
        dcc.Tab(label="Exportação", children=[
            dcc.Graph(
                id='grafico-expo',
                figure=px.bar(
                    carregar_dados("expo"),
                    x='ano',
                    y='volume',
                    title='Volume de Exportação por Ano',
                    labels={'volume': 'Volume (kg)', 'ano': 'Ano'}
                )
            )
        ]),

        dcc.Tab(label="Importação", children=[
            dcc.Graph(
                id='grafico-impo',
                figure=px.bar(
                    carregar_dados("impo"),
                    x='ano',
                    y='volume',
                    title='Volume de Importação por Ano',
                    labels={'volume': 'Volume (kg)', 'ano': 'Ano'}
                )
            )
        ])
    ])
])

if __name__ == '__main__':
    app.run(debug=True)

