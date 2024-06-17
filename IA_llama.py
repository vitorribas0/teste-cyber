import streamlit as st

# Variável para armazenar o texto
text_var = ''

# Novo menu para inserir texto e guardar em uma variável
menu_text = ['Inserir Texto']
choice_text = st.sidebar.selectbox('Escolha uma opção', menu_text)

if choice_text == 'Inserir Texto':
    st.title('Inserir Texto')

    # Campo de texto para inserir texto
    text_input = st.text_input('Insira o texto:')

    # Botão para guardar texto em uma variável
    if st.button('Guardar Texto'):
        global text_var
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
