import streamlit as st
import pandas as pd
import base64
import os

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
    save_df_to_csv(df, filename)

# Função para salvar PDF
def save_pdf(file, directory='pdf_files'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file.name)
    with open(file_path, 'wb') as f:
        f.write(file.read())
    return file_path

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

# Aumentando o limite de upload para 2 GB (2048 MB)
st.set_option('deprecation.showfileUploaderEncoding', False)
MAX_UPLOAD_SIZE = 2048 * 1024 * 1024  # 2 GB em bytes

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF', 'Inserir Texto e Baixar Excel']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

# Botão para limpar dados em cada menu
if choice == 'Inserir Excel':
    if st.button('Limpar Dados do Excel'):
        if os.path.exists(csv_file_excel):
            os.remove(csv_file_excel)
        st.warning('Dados do Excel foram removidos.')

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
                st.write('**Dados do Excel Inseridos:**')
                st.write(df)

elif choice == 'Inserir PDF':
    if st.button('Limpar Dados do PDF'):
        pdf_files = list_pdfs(pdf_directory)
        for pdf_file in pdf_files:
            os.remove(os.path.join(pdf_directory, pdf_file))
        st.warning('Dados do PDF foram removidos.')

    st.title('Inserir Arquivo PDF')
    # Upload do arquivo PDF
    file = st.file_uploader('Carregue um arquivo PDF', type=['pdf'])
    if file is not None:
        # Verifica o tamanho do arquivo PDF
        if len(file.getvalue()) > MAX_UPLOAD_SIZE:
            st.error(f'O arquivo selecionado excede o limite máximo de {MAX_UPLOAD_SIZE / (1024 * 1024)} MB.')
        else:
            if st.button('Inserir PDF'):
                file_path = save_pdf(file, pdf_directory)
                st.success('PDF inserido com sucesso.')
                st.write('**Link para Download do PDF Inserido:**')
                pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" download="{file.name}">Baixar PDF</a>'
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
        excel_data = pd.DataFrame({'Texto': [text]})
        b64 = base64.b64encode(excel_data.to_csv(index=False).encode()).decode()
        href = f'<a href="data:text/csv;base64,{b64}" download="{text_excel_file}">Clique aqui para baixar seu Excel</a>'
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
if pdf_files:
    st.write('PDFs Armazenados:')
    for pdf_file in pdf_files:
        st.write(f'Nome do arquivo: {pdf_file}')
        # Exibindo link para baixar o PDF
        pdf_link = f'<a href="data:application/pdf;base64,{base64.b64encode(open(os.path.join(pdf_directory, pdf_file), "rb").read()).decode()}" download="{pdf_file}">Baixar PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)
        st.write('---')
else:
    st.write('Nenhum PDF foi armazenado ainda.')

# Exibir textos inseridos
if os.path.exists(text_csv_file):
    with open(text_csv_file, 'r') as f:
        text_csv_content = f.read()
        st.write('**Texto armazenado em CSV:**')
        st.code(text_csv_content)

if os.path.exists(text_excel_file):
    df_text_excel = pd.read_csv(text_excel_file)
    if not df_text_excel.empty:
        st.write('**Texto armazenado em Excel:**')
        st.write(df_text_excel)
