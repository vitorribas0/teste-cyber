import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Error

# Função para criar uma conexão com o banco de dados SQLite
def create_connection(db_file):
    """ Cria uma conexão com o banco de dados SQLite especificado por db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
    return conn

# Função para criar uma tabela no banco de dados
def create_table(conn):
    """ Cria uma tabela no banco de dados SQLite """
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS dados (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nome TEXT NOT NULL,
                                    cpf TEXT NOT NULL,
                                    email TEXT
                                ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except Error as e:
        st.error(f"Erro ao criar a tabela: {e}")

# Função para inserir dados no banco de dados
def insert_data(conn, df):
    """ Insere os dados do DataFrame no banco de dados SQLite """
    try:
        df.to_sql('dados', conn, if_exists='append', index=False)
    except Error as e:
        st.error(f"Erro ao inserir dados no banco de dados: {e}")

# Função para obter dados do banco de dados
def get_data(conn):
    """ Obtém dados da tabela no banco de dados SQLite """
    try:
        df = pd.read_sql_query("SELECT * FROM dados", conn)
        return df
    except Error as e:
        st.error(f"Erro ao obter dados do banco de dados: {e}")
        return pd.DataFrame()

# Título da aplicação
st.title("Upload de Arquivo Excel e Inserção no Banco de Dados SQLite")

# Instrução para o usuário
st.write("Faça o upload de um arquivo Excel para inserir os dados no banco de dados SQLite.")

# Upload do arquivo
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Lendo o arquivo Excel
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Dados do arquivo enviado:")
        st.write(df)
        
        # Conectando ao banco de dados SQLite
        conn = create_connection("dados.db")
        
        if conn is not None:
            # Criando a tabela se não existir
            create_table(conn)
            
            # Inserindo os dados no banco de dados
            insert_data(conn, df)
            
            # Obtendo os dados do banco de dados para exibir
            st.success("Dados inseridos com sucesso no banco de dados SQLite.")
            st.write("Dados no banco de dados:")
            df_from_db = get_data(conn)
            st.write(df_from_db)
        else:
            st.error("Erro! Não foi possível criar a conexão com o banco de dados.")
            
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
else:
    st.write("Nenhum arquivo enviado.")
