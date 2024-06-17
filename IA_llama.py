import streamlit as st
import pandas as pd
import base64

# Variável para armazenar o texto
text_var = ''

# Configuração inicial
st.title('Upload de arquivo Excel/PDF e armazenamento seguro')

# Nome das tabelas no banco de dados
table_name_excel = 'dados_excel'
table_name_pdf = 'pdf_files'

# Sidebar com botão para selecionar a funcionalidade desejada
menu = ['Inserir Excel', 'Inserir PDF', 'Inserir Texto']
choice = st.sidebar.selectbox('Escolha uma opção', menu)

if choice == 'Inserir Excel':
    st.title('Inserir Arquivo Excel')

    # Upload do arquivo Excel
    file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

    if file is not None:
        # Verifica o tamanho do arquivo Excel
        if len(file.getvalue()) > 2048 * 1024 * 1024:  # 2 GB
            st.error('O arquivo selecionado excede o limite máximo de 2 GB.')
        else:
            # Botão para inserir dados do Excel
            if st.button('Inserir Dados do Excel'):
                # Inserir dados do Excel no banco de dados
                st.success('Dados do Excel inseridos com sucesso no banco de dados.')

            # Botão para limpar dados do Excel
            if st.button('Limpar Dados do Excel'):
                # Limpar dados do Excel do banco de dados
                st.warning('Dados do Excel foram removidos do banco de dados.')

elif choice == 'Inserir PDF':
    st.title('Inserir Arquivo PDF')

    # Upload do arquivo PDF
    file = st.file_uploader('Carregue um arquivo PDF', type=['pdf'])

    if file is not None:
        # Verifica o tamanho do arquivo PDF
        if len(file.getvalue()) > 2048 * 1024 * 1024:  # 2 GB
            st.error('O arquivo selecionado excede o limite máximo de 2 GB.')
        else:
            # Botão para inserir PDF
            if st.button('Inserir PDF'):
                # Inserir PDF no banco de dados
                st.success('PDF inserido com sucesso no banco de dados.')

            # Botão para limpar dados do PDF
            if st.button('Limpar Dados do PDF'):
                # Limpar dados do PDF do banco de dados
                st.warning('Dados do PDF foram removidos do banco de dados.')

elif choice == 'Inserir Texto':
    st.title('Inserir Texto')

    global text_var

    # Campo de texto para inserir texto
    text_input = st.text_input('Insira o texto:')

    # Botão para guardar texto em uma variável
    if st.button('Guardar Texto'):
        text_var = text_input
        st.success('Texto guardado com sucesso!')

    # Botão para baixar Excel da variável
    if st.button('Baixar Excel'):
        if text_var:
            # Criar um DataFrame com a variável de texto
            df = pd.DataFrame({'Texto': [text_var]})

            # Converter o DataFrame em um arquivo Excel
            excel_file = df.to_excel('texto.xlsx', index=False)

            # Baixar o arquivo Excel
            st.markdown(f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(excel_file.getvalue()).decode("utf-8")}" download="texto.xlsx">Baixar Excel</a>', unsafe_allow_html=True)
        else:
            st.error('Nenhum texto foi guardado ainda.')

# Mostrar dados armazenados (deve estar sempre presente)
st.subheader('Dados Armazenados')

if choice == 'Inserir Excel':
    # Mostrar dados do Excel armazenados
    st.write('**Dados do Excel Armazenados:**')

elif choice == 'Inserir PDF':
    # Mostrar PDFs armazenados
    st.write('**PDFs Armazenados:**')

elif choice == 'Inserir Texto':
    # Mostrar texto armazenado
    if text_var:
        st.write('**Texto Armazenado:**')
        st.write(text_var)
    else:
        st.write('Nenhum texto foi guardado ainda.')
