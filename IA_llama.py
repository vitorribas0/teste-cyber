import streamlit as st
import pandas as pd
import base64
import os
import requests
from io import BytesIO

# Função para salvar DataFrame em um arquivo CSV
def save_df_to_csv(df, filename):
    df.to_csv(filename, index=False)

# Função para salvar texto em um arquivo CSV
def save_text_to_csv(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

# Função para salvar texto em um arquivo Excel
def save_text_to_excel(text, filename):
    df = pd.DataFrame({'Texto': [text]})
    df.to_excel(filename, index=False)

# Função para salvar PDF a partir de uma URL
def save_pdf_from_url(url, directory='pdf_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.basename(url)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    else:
        st.error('Erro ao baixar o arquivo PDF.')
        return None

# Função para listar PDFs armazenados
def list_pdfs(directory='pdf_files'):
    if os.path.exists(directory):
        return [f for f in os.listdir(directory) if f.endswith('.pdf')]
    return []

# Função para limpar dados (excluir arquivos)
def clear_data(directory):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            os.remove(file_path)
        st.success(f'Dados em {directory} foram removidos com sucesso.')

# Configuração inicial
st.title('Upload de arquivo Excel/PDF e inserir texto')

# Nome dos arquivos e diretórios para armazenamento
csv_file_excel = 'dados_excel.csv'
pdf_directory = 'pdf_files'
text_csv_file = 'texto.csv'
text_excel_file = 'texto.xlsx'

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF', 'Inserir Texto e Baixar Excel']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

# Botão para limpar dados em cada menu
if choice == 'Inserir Excel':
    if st.button('Limpar Dados do Excel'):
        if os.path.exists(csv_file_excel):
            os.remove(csv_file_excel)
        st.warning('Dados do Excel foram removidos.')

    st.title('Inserir URL de Arquivo Excel')
    # Inserir URL do arquivo Excel
    url = st.text_input('Insira a URL de um arquivo Excel')
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se houve algum erro na requisição
            df = pd.read_excel(BytesIO(response.content))
            if st.button('Inserir Dados do Excel'):
                save_df_to_csv(df, csv_file_excel)
                st.success('Dados do Excel inseridos com sucesso.')
                st.write('**Dados do Excel Inseridos:**')
                st.write(df)
        except requests.exceptions.RequestException as e:
            st.error(f'Erro ao baixar o arquivo Excel: {e}')
        except Exception as e:
            st.error(f'Erro ao processar o arquivo Excel: {e}')

elif choice == 'Inserir PDF':
    if st.button('Limpar Dados do PDF'):
        pdf_files = list_pdfs(pdf_directory)
        for pdf_file in pdf_files:
            os.remove(os.path.join(pdf_directory, pdf_file))
        st.warning('Dados do PDF foram removidos.')

    st.title('Inserir URL de Arquivo PDF')
    # Inserir URL do arquivo PDF
    url = st.text_input('Insira a URL de um arquivo PDF')
    if url:
        file_path = save_pdf_from_url(url, pdf_directory)
        if file_path:
            st.success('PDF inserido com sucesso.')
            st.write('**Link para Download do PDF Inserido:**')
            pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" download="{os.path.basename(file_path)}">Baixar PDF</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)

elif choice == 'Inserir Texto e Baixar Excel':
    if st.button('Limpar Dados de Texto'):
        if os.path.exists(text_csv_file):
            os.remove(text_csv_file)
        if os.path.exists(text_excel_file):
            os.remove(text_excel_file)
        st.warning('Dados de texto foram removidos.')

    st.title('Inserir Texto e Baixar Excel')

    # Campo de texto para entrada de dados
    text = st.text_area('Insira seu texto aqui')

    # Botão para download do Excel com o texto
    if st.button('Baixar Excel com o texto'):
        save_text_to_excel(text, text_excel_file)
        with open(text_excel_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{text_excel_file}">Clique aqui para baixar seu Excel</a>'
        st.markdown(href, unsafe_allow_html=True)

    # Botão para salvar o texto em um arquivo CSV
    if st.button('Salvar Texto em CSV'):
        save_text_to_csv(text, text_csv_file)
        st.success(f'Texto salvo com sucesso em {text_csv_file}')
        st.write('**Texto Salvo em CSV:**')
        st.text(text)

# Mostrar dados armazenados (deve estar sempre presente)
st.subheader('Dados Armazenados')

# Mostrar PDFs armazenados
pdf_files = list_pdfs(pdf_directory)
if choice == 'Inserir PDF' and pdf_files:
    st.write('PDFs Armazenados:')
    for pdf_file in pdf_files:
        st.write(f'Nome do arquivo: {pdf_file}')
        # Exibindo link para baixar o PDF
        pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open(os.path.join(pdf_directory, pdf_file), "rb").read()).decode()}" download="{pdf_file}">Baixar PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)
        st.write('---')

# Exibir textos inseridos
if choice == 'Inserir Texto e Baixar Excel' and os.path.exists(text_csv_file):
    with open(text_csv_file, 'r') as f:
        text_csv_content = f.read()
        st.write('**Texto armazenado em CSV:**')
        st.code(text_csv_content)

if choice == 'Inserir Texto e Baixar Excel' and os.path.exists(text_excel_file):
    df_text_excel = pd.read_excel(text_excel_file)
    if not df_text_excel.empty:
        st.write('**Texto armazenado em Excel:**')
        st.write(df_text_excel)

if choice == 'Inserir Excel' and os.path.exists(csv_file_excel):
    df_excel = pd.read_csv(csv_file_excel)
    if not df_excel.empty:
        st.write('**Dados do Excel Armazenados:**')
        st.write(df_excel)

