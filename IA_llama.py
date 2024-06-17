import streamlit as st
import pandas as pd
import sqlite3
import base64

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
        
        # Criação da tabela com colunas baseadas no DataFrame
        columns = df.columns
        columns_with_types = ', '.join([f'"{col}" TEXT' for col in columns])
        create_table_query = f'CREATE TABLE "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_with_types})'
        c.execute(create_table_query)
        
        conn.commit()
        conn.close()

# Função para inserir dados no SQLite se a tabela estiver vazia
def insert_data_from_df(df, table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Verificar se existem dados na tabela
    c.execute(f'SELECT COUNT(*) FROM "{table_name}"')
    count = c.fetchone()[0]
    
    if count == 0:
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

# Função para criar tabela de PDFs
def create_table_for_pdfs(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Criação da tabela para armazenar PDFs
    c.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_data BLOB)')
    
    conn.commit()
    conn.close()

# Função para inserir PDF no SQLite
def insert_pdf_into_db(file, table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lendo o conteúdo do arquivo PDF
    pdf_content = file.read()
    
    # Inserindo o PDF na tabela
    c.execute(f'INSERT INTO "{table_name}" (file_name, file_data) VALUES (?, ?)', (file.name, sqlite3.Binary(pdf_content)))
    
    conn.commit()
    conn.close()

# Função para ler dados de PDF do SQLite
def read_pdfs_from_db(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lendo dados da tabela de PDFs
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
menu = ['Página Principal', 'Inserir Excel', 'Inserir PDF', 'Ver Dados']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Página Principal':
    st.write('Selecione uma opção no menu para começar.')

elif choice == 'Inserir Excel':
    st.title('Inserir Arquivo Excel')

    # Upload do arquivo Excel
    file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

    if file is not None:
        df = pd.read_excel(file)

        # Criando a tabela no SQLite com base no DataFrame, se não existir
        create_table_from_df(df, table_name_excel)

        # Inserindo os dados no SQLite, se a tabela estiver vazia
        insert_data_from_df(df, table_name_excel)
        st.success('Dados do Excel inseridos com sucesso no banco de dados.')

    # Botão para mostrar dados do Excel
    if st.button('Mostrar Dados do Excel'):
        data_excel = read_data_from_db(table_name_excel)
        if data_excel:
            # Criar DataFrame a partir dos dados do Excel
            df_excel = pd.DataFrame(data_excel, columns=['ID'] + df.columns.tolist())

            # Exibir DataFrame no Streamlit
            st.write('**Dados do Excel Armazenados:**')
            st.write(df_excel)
        else:
            st.write('Nenhum dado do Excel foi armazenado ainda.')

elif choice == 'Inserir PDF':
    st.title('Inserir Arquivo PDF')

    # Upload do arquivo PDF
    file = st.file_uploader('Carregue um arquivo PDF', type=['pdf'])

    if file is not None:
        # Criando a tabela no SQLite para armazenar PDFs
        create_table_for_pdfs(table_name_pdf)

        # Inserindo o PDF no SQLite
        insert_pdf_into_db(file, table_name_pdf)
        st.success('PDF inserido com sucesso no banco de dados.')

    # Botão para mostrar PDFs armazenados
    if st.button('Mostrar PDFs Armazenados'):
        data_pdf = read_pdfs_from_db(table_name_pdf)
        if data_pdf:
            # Exibir PDFs no Streamlit
            st.write('**PDFs Armazenados:**')
            for row in data_pdf:
                st.write(f'**Nome do arquivo:** {row[1]}')
                # Exibindo link para baixar o PDF
                pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(row[2]).decode("utf-8")}" download="{row[1]}">Baixar PDF</a>'
                st.markdown(pdf_link, unsafe_allow_html=True)
                st.write('---')
        else:
            st.write('Nenhum PDF foi armazenado ainda.')

elif choice == 'Ver Dados':
    st.title('Ver Dados Armazenados')

    # Botão para mostrar dados do Excel
    if st.button('Mostrar Dados do Excel'):
        data_excel = read_data_from_db(table_name_excel)
        if data_excel:
            # Criar DataFrame a partir dos dados do Excel
            df_excel = pd.DataFrame(data_excel, columns=['ID'] + df.columns.tolist())

            # Exibir DataFrame no Streamlit
            st.write('**Dados do Excel Armazenados:**')
            st.write(df_excel)
        else:
            st.write('Nenhum dado do Excel foi armazenado ainda.')

    # Botão para mostrar PDFs armazenados
    if st.button('Mostrar PDFs Armazenados'):
        data_pdf = read_pdfs_from_db(table_name_pdf)
        if data_pdf:
            # Exibir PDFs no Streamlit
            st.write('**PDFs Armazenados:**')
            for row in data_pdf:
                st.write(f'**Nome do arquivo:** {row[1]}')
                # Exibindo link para baixar o PDF
                pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(row[2]).decode("utf-8")}" download="{row[1]}">Baixar PDF</a>'
                st.markdown(pdf_link, unsafe_allow_html=True)
                st.write('---')
        else:
            st.write('Nenhum PDF foi armazenado ainda.')

