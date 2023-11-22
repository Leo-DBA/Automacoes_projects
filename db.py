import mysql.connector
from dotenv import load_dotenv
import pandas as pd
import os 

load_dotenv()

#acesso as variaveis
SENHA_DB = os.getenv("SENHA_DB")
HOST = os.getenv("HOST")


def conectar_mysql():
    config = {
        'user': 'dba_leo',
        'password': SENHA_DB,
        'host': HOST,
        'database': 'scrapping'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        print("Conectado com sucesso ao Mysql!")
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None, None
    
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


import pandas as pd

def read_data(cursor):
    try:
        retorna = """
        SELECT DISTINCT ACAO_SYMBOL, PRICE FROM ACOES
        order by PRICE desc; 
        """
        cursor.execute(retorna)
        resultado = cursor.fetchall()

        # Converta a lista de tuplas para um DataFrame
        columns = ["ação", "price"] 
        df = pd.DataFrame(resultado, columns=columns)

        return df
    except Exception as e:
        print(f"Ocorreu um erro ao ler os dados do banco: {e}")
        return None



