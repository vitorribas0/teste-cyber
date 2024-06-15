import streamlit as st
import pandas as pd
import sqlite3

# Função para criar a tabela no SQLite com colunas dinâmicas
def create_table_from_df(df, table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Criação da tabela com colunas baseadas no DataFrame
    columns = df.columns
    columns_with_types = ', '.join([f'"{col}" TEXT' for col in columns])
    create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_with_types})'
    c.execute(create_table_query)
    
    conn.commit()
    conn.close()

# Função para inserir dados no SQLite
def insert_data_from_df(df, table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Inserindo dados do DataFrame na tabela
    for _, row in df.iterrows():
        placeholders = ', '.join(['?' for _ in row])
        columns = ', '.join([f'"{col}"' for col in df.columns])
        insert_query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'
        c.execute(insert_query, tuple(row))
    
    conn.commit()
    conn.close()

# Função para ler dados do SQLite
def read_data_from_db(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lendo dados da tabela
    c.execute(f'SELECT * FROM "{table_name}"')
    data = c.fetchall()
    
    conn.close()
    return data

# Configuração inicial
st.title('Upload de arquivo Excel e armazenamento seguro')

# Nome da tabela no banco de dados
table_name = 'dados_excel'

# Upload do arquivo Excel
file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

if file is not None:
    df = pd.read_excel(file)

    # Exibindo os dados do arquivo Excel
    st.write('**Dados do arquivo Excel:**')
    st.write(df)

    # Criando a tabela no SQLite com base no DataFrame
    create_table_from_df(df, table_name)

    # Inserindo os dados no SQLite
    insert_data_from_df(df, table_name)
    st.success('Dados inseridos com sucesso no banco de dados.')

# Botão para ler e exibir dados do banco de dados
if st.button('Mostrar Dados do Banco de Dados'):
    data = read_data_from_db(table_name)
    if data:
        st.write('**Dados no Banco de Dados:**')
        st.write(pd.DataFrame(data, columns=[desc[0] for desc in c.description]))

# Botão para excluir a tabela
if st.button('Excluir Tabela'):
    delete_table(table_name)
    st.success('Tabela excluída com sucesso.')
