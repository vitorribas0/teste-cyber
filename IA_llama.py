import streamlit as st
import xlsxwriter

# Título da página
st.title("Campo de texto e download em Excel")

# Variável para armazenar o texto digitado pelo usuário
 texto_usuario = ""

# Campo de texto
texto = st.text_input(" Digite seu texto ")

# Botão para baixar o arquivo Excel
if st.button("Download em Excel"):
    texto_usuario = texto

    # Criar um arquivo Excel
    wb = xlsxwriter.Workbook("texto.xlsx")
    ws = wb.add_worksheet()

    # Escrever o texto no arquivo Excel
    ws.write(0, 0, texto_usuario)

    # Fechar o arquivo Excel
    wb.close()

    # mensagem para indicar que o arquivo foi baixado
    st.write("Arquivo baixado com sucesso!")
