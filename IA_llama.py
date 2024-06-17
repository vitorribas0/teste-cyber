```
import streamlit as st
import xlsxwriter

st.title("Campo de texto e resultado")

texto_usuario = ""

texto = st.text_input(" Digite seu texto ")

if st.button("Gerar documento"):
    texto_usuario = texto
    with st.expander("Resultado"):
        st.write(texto_usuario)
    st.write("O texto digitado será armazenado em um arquivo Excel.")
    st.write("Clique em 'Gerar documento' novamente para baixar o arquivo.")
