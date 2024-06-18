import streamlit as st
import pandas as pd
import base64
import os

# Aumentando o limite de upload para 2 GB (2048 MB)
st.set_option('deprecation.showfileUploaderEncoding', False)
MAX_UPLOAD_SIZE = 2048 * 1024 * 1024  # 2 GB em bytes

# Função para converter DataFrame para download em Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

# Função para salvar DataFrame em um arquivo CSV
def save_df_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Função para ler DataFrame de um arquivo CSV
def read_df_from_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame()

# Configuração inicial
st.title('Upload de arquivo Excel/PDF e inserir texto')

# Nome dos arquivos para armazenamento
csv_file_excel = 'dados_excel.csv'
pdf_directory = 'pdf_files'
csv_file_texto = 'dados_texto.csv'

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF', 'Inserir Texto']
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
                if not os.path.exists(pdf_directory):
                    os.makedirs(pdf_directory)
                file_path = os.path.join(pdf_directory, file.name)
                with open(file_path, 'wb') as f:
                    f.write(file.read())
                st.success('PDF inserido com sucesso.')
            if st.button('Limpar Dados do PDF'):
                pdf_files = os.listdir(pdf_directory)
                for pdf_file in pdf_files:
                    os.remove(os.path.join(pdf_directory, pdf_file))
                st.warning('Dados do PDF foram removidos.')

elif choice == 'Inserir Texto':
    st.title('Inserir Texto')

    # Campo de texto para entrada de dados
    text = st.text_area('Insira seu texto aqui')

    # Botão para salvar o texto
    if st.button('Salvar Texto'):
        df_texto = pd.DataFrame({'Texto': [text]})
        save_df_to_csv(df_texto, csv_file_texto)
        st.success('Texto salvo com sucesso.')

    # Botão para limpar o texto
    if st.button('Limpar Texto'):
        if os.path.exists(csv_file_texto):
            os.remove(csv_file_texto)
        st.warning('Texto foi removido.')

# Mostrar dados armazenados (deve estar sempre presente)
st.subheader('Dados Armazenados')

# Mostrar dados do Excel armazenados
if os.path.exists(csv_file_excel):
    df_excel = read_df_from_csv(csv_file_excel)
    if not df_excel.empty:
        st.write('**Dados do Excel Armazenados:**')
        st.write(df_excel)
    else:
        st.write('Nenhum dado do Excel foi armazenado ainda.')
else:
    st.write('Nenhum dado do Excel foi armazenado ainda.')

# Mostrar PDFs armazenados
pdf_files = os.listdir(pdf_directory)
if pdf_files:
    st.write('**PDFs Armazenados:**')
    for pdf_file in pdf_files:
        st.write(f'Nome do arquivo: {pdf_file}')
else:
    st.write('Nenhum PDF foi armazenado ainda.')

# Mostrar texto armazenado
if os.path.exists(csv_file_texto):
    df_texto = read_df_from_csv(csv_file_texto)
    if not df_texto.empty:
        st.write('**Texto Armazenado:**')
        st.write(df_texto)
    else:
        st.write('Nenhum texto foi armazenado ainda.')
else:
    st.write('Nenhum texto foi armazenado ainda.')
