import streamlit as st
import sqlite3
from openai import OpenAI

st.set_page_config(layout="wide")  # Configuração para layout de página amplo

# Inicialize o cliente OpenAI
client = OpenAI(
    api_key="LL-rZdxy5UFL4evTVeC6H1Jzuph00H08neiKQUGm3HSYOm1qMD4T8YxonRYedIH6856",
    base_url="https://api.llama-api.com"
)

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Criar a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS conversation_history 
             (role text, message text)''')

# Função para enviar mensagem e obter resposta
def enviar_mensagem(pergunta):
    # Enviar a mensagem para a IA e obter a resposta
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Olá! Sou um especialista em Python, Pandas, PySpark e AWS."},
            {"role": "user", "content": pergunta}
        ]
    )
    return response.choices[0].message.content

# Interface Streamlit para envio de pergunta
pergunta = st.chat_input("Digite sua pergunta para a IA:")

# Botão para limpar o histórico de conversas
if st.button("Limpar Histórico de Conversas"):
    c.execute("DELETE FROM conversation_history")
    conn.commit()

# Adicionar um input de documento
uploaded_file = st.file_uploader("Selecione um documento:", type=["pdf", "docx", "txt"])

# Se um arquivo for selecionado, exibir um botão para upload
if uploaded_file is not None:
    st.write("Você selecionou um arquivo!")
    if st.button("Upload do arquivo"):
        # Aqui você pode adicionar lógica para lidar com o upload de arquivo
        # Por exemplo, você pode salvar o arquivo em um diretório específico
        with open("uploads/" + uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.write("Arquivo upload com sucesso!")

# Enviar a pergunta para a IA quando o usuário enviar a mensagem
if pergunta:
    # Adicionar a pergunta ao histórico de conversa
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("", pergunta))
    conn.commit()
    # Envie a pergunta para a IA e obtenha a resposta
    resposta = enviar_mensagem(pergunta)
    # Adicionar a resposta ao histórico de conversa
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("", resposta))
    conn.commit()

# Barra lateral
st.sidebar.title("")  # Título na barra lateral
# Adicionando uma descrição na barra lateral
st.sidebar.markdown("Este é um projeto feito utilizando o .")

st.title("Chat com OpenAI")

# Carregar e exibir o histórico de conversa do banco de dados
for row in c.execute("SELECT * FROM conversation_history"):
    st.write(row[0], row[1])

# Fechar a conexão com o banco de dados
conn.close()
