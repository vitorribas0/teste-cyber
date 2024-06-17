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

# Função para excluir a tabela
def delete_table(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    conn.commit()
    conn.close()

# Configuração inicial
st.title('Upload de arquivo Excel e armazenamento seguro')

# Nome da tabela no banco de dados
table_name = 'dados_excel'

# Sidebar com botão para ir para a página de inserção de texto
menu = ['Página Principal', 'Inserir Texto']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Página Principal':
    # Upload do arquivo Excel
    file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

    if file is not None:
        df = pd.read_excel(file)

        # Criando a tabela no SQLite com base no DataFrame
        create_table_from_df(df, table_name)

        # Inserindo os dados no SQLite
        insert_data_from_df(df, table_name)
        st.success('Dados inseridos com sucesso no banco de dados.')

    # Botão para ler e exibir dados do banco de dados
    if st.button('Mostrar Dados do Banco de Dados'):
        data = read_data_from_db(table_name)
        if data:
            # Criar DataFrame a partir dos dados
            df_from_db = pd.DataFrame(data)

            # Exibir DataFrame no Streamlit
            st.write('**Dados no Banco de Dados:**')
            st.write(df_from_db)

    # Botão para excluir a tabela
    if st.button('Excluir Tabela'):
        delete_table(table_name)
        st.success('Tabela excluída com sucesso.')

elif choice == 'Inserir Texto':
    st.title('Inserir Texto para Armazenar no Banco de Dados')
    texto = st.text_area('Digite o texto que deseja armazenar:')
    
    if st.button('Salvar no Banco de Dados'):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        
        # Criando uma tabela específica para texto, se não existir
        c.execute('''CREATE TABLE IF NOT EXISTS textos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     texto TEXT
                     )''')
        
        # Inserindo o texto na tabela
        c.execute('INSERT INTO textos (texto) VALUES (?)', (texto,))
        
        conn.commit()
        conn.close()
        
        st.success('Texto armazenado com sucesso no banco de dados.')

