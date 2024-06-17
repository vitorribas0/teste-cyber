import streamlit as st
import pandas as pd
import sqlite3
import base64

# Função para criar a tabela no SQLite com colunas dinâmicas
def create_table_from_pdf(table_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Criação da tabela para armazenar PDF
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
    c.execute('INSERT INTO "{table_name}" (file_name, file_data) VALUES (?, ?)', (file.name, sqlite3.Binary(pdf_content)))
    
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
st.title('Upload de arquivo PDF e armazenamento seguro')

# Nome da tabela no banco de dados
table_name = 'pdf_files'

# Sidebar com opções
menu = ['Página Principal', 'Ver PDFs Armazenados']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Página Principal':
    # Upload do arquivo PDF
    file = st.file_uploader('Carregue um arquivo PDF', type=['pdf'])

    if file is not None:
        # Criando a tabela no SQLite para armazenar PDFs
        create_table_from_pdf(table_name)

        # Inserindo o PDF no SQLite
        insert_pdf_into_db(file, table_name)
        st.success('PDF inserido com sucesso no banco de dados.')

    # Botão para ler e exibir dados do banco de dados
    if st.button('Mostrar PDFs Armazenados'):
        data = read_data_from_db(table_name)
        if data:
            # Exibir PDFs no Streamlit
            st.write('**PDFs Armazenados:**')
            for row in data:
                st.write(f'**Nome do arquivo:** {row[1]}')
                # Exibindo link para baixar o PDF
                pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(row[2]).decode("utf-8")}" download="{row[1]}">Baixar PDF</a>'
                st.markdown(pdf_link, unsafe_allow_html=True)
                st.write('---')

    # Botão para excluir a tabela
    if st.button('Excluir Tabela'):
        delete_table(table_name)
        st.success('Tabela excluída com sucesso.')

elif choice == 'Ver PDFs Armazenados':
    st.title('PDFs Armazenados no Banco de Dados')
    
    # Função para ler e exibir PDFs armazenados
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Lendo dados da tabela 'pdf_files'
    c.execute('SELECT * FROM pdf_files')
    data = c.fetchall()
    
    conn.close()
    
    if data:
        # Exibir PDFs no Streamlit
        st.write('**PDFs Armazenados:**')
        for row in data:
            st.write(f'**Nome do arquivo:** {row[1]}')
            # Exibindo link para baixar o PDF
            pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(row[2]).decode("utf-8")}" download="{row[1]}">Baixar PDF</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)
            st.write('---')
    else:
        st.write('Nenhum PDF foi armazenado ainda.')

