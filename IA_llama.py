import streamlit as st
import pandas as pd
import sqlite3
import base64
from io import BytesIO

# Aumentando o limite de upload para 2 GB (2048 MB)
st.set_option('deprecation.showfileUploaderEncoding', False)
MAX_UPLOAD_SIZE = 2048 * 1024 * 1024 # 2 GB em bytes

# Função para verificar se a tabela existe no SQLite
def table_exists(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    result = c.fetchone()
    conn.close()
    return result is not None

# Função para criar a tabela no SQLite com colunas dinâmicas se não existir
def create_table_from_df(df, table_name):
    if not table_exists(table_name):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        columns = df.columns
        columns_with_types = ', '.join([f'"{col}" TEXT' for col in columns])
        create_table_query = f'CREATE TABLE "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_with_types})'
        c.execute(create_table_query)

        conn.commit()
        conn.close()

# Função para limpar dados da tabela no SQLite
def clear_table(table_name):
    if table_exists(table_name):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        c.execute(f'DELETE FROM "{table_name}"')

        conn.commit()
        conn.close()

# Função para inserir dados do Excel no SQLite
def insert_excel_data(file, table_name):
    df = pd.read_excel(file)

    create_table_from_df(df, table_name)

    clear_table(table_name)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    for _, row in df.iterrows():
        placeholders = ', '.join(['?' for _ in row])
        columns = ', '.join([f'"{col}"' for col in df.columns])
        insert_query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'
        c.execute(insert_query, tuple(row))

    conn.commit()
    conn.close()

# Função para ler dados do Excel do SQLite
def read_excel_data(table_name):
    if not table_exists(table_name):
        return []

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f'SELECT * FROM "{table_name}"')
    data = c.fetchall()

    conn.close()
    return data

# Função para criar tabela de PDFs
def create_table_for_pdfs(table_name):
    if not table_exists(table_name):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        c.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_data BLOB)')

        conn.commit()
        conn.close()

# Função para inserir PDF no SQLite
def insert_pdf_into_db(file, table_name):
    create_table_for_pdfs(table_name)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    pdf_content = file.read()

    c.execute(f'INSERT INTO "{table_name}" (file_name, file_data) VALUES (?, ?)', (file.name, sqlite3.Binary(pdf_content)))

    conn.commit()
    conn.close()

# Função para ler dados de PDF do SQLite
def read_pdfs_from_db(table_name):
    if not table_exists(table_name):
        return []

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f'SELECT * FROM "{table_name}"')
    data = c.fetchall()

    conn.close()
    return data

# Configuração inicial
st.title('Upload de arquivo Excel/PDF e armazenamento seguro')

# Nome das tabelas no banco de dados
table_name_excel = 'dados_excel'
table_name_pdf = 'pdf_files'

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

if choice == 'Inserir Excel':
    st.title('Inserir Arquivo Excel')

    # Upload do arquivo Excel
    file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

    if file is not None:
        # Verifica o tamanho do arquivo Excel
        if len(file.getvalue()) > MAX_UPLOAD_SIZE:
            st.error(f'O arquivo selecionado excede o limite máximo de {MAX_UPLOAD_SIZE / (1024 * 1024)} MB.')
        else:
