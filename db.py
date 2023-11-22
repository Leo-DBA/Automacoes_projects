import mysql.connector
from dotenv import load_dotenv
import os 


load_dotenv()

#acesso as variaveis
SENHA_DB = os.getenv("SENHA_DB")
HOST = os.getenv("HOST")


def conectar_mysql():
    config = {
        'user': 'root',
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



def selecao(cursor):
    #try:
        retorna ="""
        SELECT ACAO_SYMBOL, PRICE, CHANGE_PERCENT, CHANGE_PRICE FROM ACOES; 
        """
        cursor.execute(retorna)
        resultado = cursor.fetchall()

        #print(resultado)
        if resultado:
            return resultado


