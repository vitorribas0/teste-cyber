import streamlit as st

# Criar um campo de texto
texto = st.text_input("Insira o texto:", "")

# Criar uma tabela para mostrar o texto
if texto:
    table = [[texto]]
    st.table(table)
