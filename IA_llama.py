import streamlit as st
import pandas as pd
import base64
import sqlite3

# Função para criar a conexão com o banco de dados SQLite
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Função para criar tabela de texto se não existir
def create_text_table(conn):
    sql_create_texts_table = """
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_texts_table)
    except sqlite3.Error as e:
        print(e)

# Função para inserir texto na tabela
def insert_text(conn, text):
    sql = '''
        INSERT INTO texts (text)
        VALUES (?);
    '''
    cur = conn.cursor()
    cur.execute(sql, (text,))
    conn.commit()
    return cur.lastrowid

# Função para buscar todos os textos na tabela
def select_all_texts(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM texts")
    rows = cur.fetchall()
    return rows

# Configuração inicial
st.title('Inserir Texto e Visualizar Dados')

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = create_connection('texto_db.sqlite')
if conn is not None:
    # Criar a tabela de textos se não existir
    create_text_table(conn)

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Texto', 'Ver Dados Armazenados']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

if choice == 'Inserir Texto':
    st.title('Inserir Texto')

    # Campo de texto para entrada de dados
    text = st.text_area('Insira seu texto aqui')

    # Botão para salvar o texto no banco de dados
    if st.button('Salvar Texto'):
        if text:
            text_id = insert_text(conn, text)
            st.success(f'Texto inserido com ID {text_id}')

elif choice == 'Ver Dados Armazenados':
    st.title('Dados Armazenados')

    # Buscar todos os textos na tabela
    texts = select_all_texts(conn)
    if texts:
        st.write('Textos Armazenados:')
        for text in texts:
            st.write(f'ID: {text[0]}, Texto: {text[1]}')
    else:
        st.write('Nenhum texto foi armazenado ainda.')

# Fechar a conexão com o banco de dados
if conn:
    conn.close()
