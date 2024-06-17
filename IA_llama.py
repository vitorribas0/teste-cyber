import streamlit as st
import pandas as pd

# Criar um campo de texto
texto = st.text_input("Insira o texto:", "")

# Criar um DataFrame com o texto
df = pd.DataFrame({'Texto': [texto]})

# Criar um botão para baixar o arquivo Excel
if st.button('Baixar arquivo Excel'):
    df.to_excel('texto.xlsx', index=False)
    st.success('Arquivo Excel baixado com sucesso!')
else:
    st.write('')

# Mostrar o botão apenas se o campo de texto não estiver vazio
if texto:
    st.write('Mostrar botão')
else:
    st.write('')
