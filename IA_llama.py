import streamlit as st
import xlsxwriter

st.title("Campo de texto e download em Excel")

texto_usuario = ""

texto = st.text_input(" Digite seu texto ")

if st.button("Download em Excel"):
    texto_usuario = texto
    wb = xlsxwriter.Workbook("texto.xlsx")
    ws = wb.add_worksheet()
    ws.write(0, 0, texto_usuario)
    wb.close()
    st.write("Arquivo baixado com sucesso!")
