import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from db import conectar_mysql, fechar_conexao, read_data

api_key = '8dd4ae36'
acoes =  ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'B3SA3', 'ABEV3', 'MGLU3', 'WEGE3', 'GGBR4', 'LREN3']

st.set_page_config(layout='wide')

# Coletar dados de ações
compilada = pd.DataFrame()

for acao in acoes:
    url = f'https://api.hgbrasil.com/finance/stock_price?key={api_key}&symbol={acao}'
    r = requests.get(url)
    data = r.json()

    # Verificar se a resposta contém dados válidos
    if 'results' in data and isinstance(data['results'], dict) and acao in data['results']:
        # Seleciona apenas as colunas desejadas
        colunas_desejadas = ["symbol", "price", "change_percent", "change_price", "updated_at"]
        tabela = pd.json_normalize(data['results'][acao])[colunas_desejadas]
        compilada = pd.concat([compilada, tabela])

# Conectar ao banco de dados MySQL
conn, cursor = conectar_mysql()



# Inserir dados no banco de dados
if conn and cursor:
    try:
        for _, row in compilada.iterrows():
            query = """
                INSERT INTO acoes (acao_symbol, price, change_percent, change_price, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            data_to_insert = (
                row['symbol'], float(row['price']), float(row['change_percent']),
                float(row['change_price']), row['updated_at']
            )

            cursor.execute(query, data_to_insert)

        conn.commit()
        print("Insert executado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao inserir os dados no banco: {e}")
    finally:
        fechar_conexao(conn, cursor)
else:
    print("Não conseguimos conectar no MySQL!")



def fecth_data():
    conn, cursor = conectar_mysql()


    # ler os dados do banco
    s = read_data(cursor)

    fechar_conexao(conn,cursor)
    print("peguei os dados:", s)
    

    return s



def gera_dashs():
    st.title("Relatório Ações")
    

    data = fecth_data()

    if data is not None:
        st.write("Dados encontrados")
        st.write(data)

        print("Colunas disponíveis:", data.columns)


        # criando o grafico
        dash = px.scatter(data, x='ação', y='price', title='Preço das ações')
        st.plotly_chart(dash)
    else:
        st.write("Não encontramos nenhum dados na tabela!")


fecth_data()
gera_dashs()
