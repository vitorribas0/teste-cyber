import streamlit as st
import pandas as pd
import base64
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Criando uma conexão com o banco de dados SQLite usando SQLAlchemy
engine = create_engine('sqlite:///texto_db.sqlite', echo=False)
metadata = MetaData()

# Definindo a tabela texts
texts = Table('texts', metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String)
)

metadata.create_all(engine)

# Função para inserir texto na tabela
def insert_text(text):
    with engine.connect() as conn:
        insert_stmt = texts.insert().values(text=text)
        conn.execute(insert_stmt)

# Função para buscar todos os textos na tabela
def select_all_texts():
    with engine.connect() as conn:
        select_stmt = texts.select()
        result = conn.execute(select_stmt)
        return result.fetchall()

# Função para salvar DataFrame em um arquivo CSV
def save_df_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Função para salvar texto em um arquivo Excel
def save_text_to_excel(text, filename):
    df = pd.DataFrame({'Texto': [text]})
    save_df_to_csv(df, filename)

# Função para salvar PDF
def save_pdf(file, directory='pdf_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.name)
    with open(file_path, 'wb') as f:
        f.write(file.read())
    return file_path

# Função para ler lista de PDFs
def list_pdfs(directory='pdf_files'):
    if os.path.exists(directory):
        return [f for f in os.listdir(directory) if f.endswith('.pdf')]
    return []

# Configuração inicial
st.title('Manipulação de Dados: Excel, PDF e Texto')

# Nome dos arquivos e diretórios para armazenamento
csv_file_excel = 'dados_excel.csv'
pdf_directory = 'pdf_files'
text_csv_file = 'texto.csv'
text_excel_file = 'texto.xlsx'
db_file = 'texto_db.sqlite'

# Aumentando o limite de upload para 2 GB (2048 MB)
st.set_option('deprecation.showfileUploaderEncoding', False)
MAX_UPLOAD_SIZE = 2048 * 1024 * 1024 # 2 GB em bytes

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF', 'Inserir Texto', 'Ver Dados Armazenados']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = create_engine('sqlite:///texto_db.sqlite', echo=False)

if choice == 'Inserir Excel':
    st.title('Inserir Arquivo Excel')
    # Upload do arquivo Excel
    file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])
    if file is not None:
        # Verifica o tamanho do arquivo Excel
        if len(file.getvalue()) > MAX_UPLOAD_SIZE:
            st.error(f'O arquivo selecionado excede o limite máximo de {MAX_UPLOAD_SIZE / (1024 * 1024)} MB.')
        else:
            df = pd.read_excel(file)
            if st.button('Inserir Dados do Excel'):
                save_df_to_csv(df, csv_file_excel)
                st.success('Dados do Excel inseridos com sucesso.')
            if st.button('Limpar Dados do Excel'):
                if os.path.exists(csv_file_excel):
                    os.remove(csv_file_excel)
                st.warning('Dados do Excel foram removidos.')

elif choice == 'Inserir PDF':
    st.title('Inserir Arquivo PDF')
    # Upload do arquivo PDF
    file = st.file_uploader('Carregue um arquivo PDF', type=['pdf'])
    if file is not None:
        # Verifica o tamanho do arquivo PDF
        if len(file.getvalue()) > MAX_UPLOAD_SIZE:
            st.error(f'O arquivo selecionado excede o limite máximo de {MAX_UPLOAD_SIZE / (1024 * 1024)} MB.')
        else:
            if st.button('Inserir PDF'):
                save_pdf(file, pdf_directory)
                st.success('PDF inserido com sucesso.')
            if st.button('Limpar Dados do PDF'):
                pdf_files = list_pdfs(pdf_directory)
                for pdf_file in pdf_files:
                    os.remove(os.path.join(pdf_directory, pdf_file))
                st.warning('Dados do PDF foram removidos.')

elif choice == 'Inserir Texto':
    st.title('Inserir Texto')

    # Campo de texto para entrada de dados
    text = st.text_area('Insira seu texto aqui')

    # Botão para salvar o texto no banco de dados
    if st.button('Salvar Texto'):
        if text:
            insert_text(text)
            st.success('Texto inserido com sucesso.')

elif choice == 'Ver Dados Armazenados':
    st.title('Dados Armazenados')

    # Buscar todos os textos na tabela
    texts = select_all_texts()
    if texts:
        st.write('Textos Armazenados:')
        for text in texts:
            st.write(f'ID: {text[0]}, Texto: {text[1]}')
    else:
        st.write('Nenhum texto foi armazenado ainda.')

# Fechar a conexão com o banco de dados
if conn:
    conn.dispose()
