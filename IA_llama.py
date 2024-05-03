import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")  # Configuração para layout de página amplo

# Inicialize o cliente OpenAI
client = OpenAI(
    api_key="LL-rZdxy5UFL4evTVeC6H1Jzuph00H08neiKQUGm3HSYOm1qMD4T8YxonRYedIH6856",
    base_url="https://api.llama-api.com"
)

# Histórico de conversa
conversation_history = []

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
pergunta = st.chat_input("Digite sua pergunta para a IA e pressione Enter:")

# Enviar a pergunta para a IA quando o usuário pressionar Enter
if pergunta:
    # Adicionar a pergunta ao histórico de conversa
    conversation_history.append(("🙎‍♂️:", pergunta))
    # Envie a pergunta para a IA e obtenha a resposta
    resposta = enviar_mensagem(pergunta)
    # Adicionar a resposta ao histórico de conversa
    conversation_history.append(("🤖:", resposta))

# Barra lateral
st.sidebar.title("🦙 LLAMA 2")  # Título na barra lateral
# Adicionando uma descrição na barra lateral
st.sidebar.markdown("Este é um projeto feito utilizando o 🦙 LLAMA 2.")

st.title("Chat com OpenAI")

# Exibir histórico de conversa
st.subheader("Histórico de Conversa")
for role, message in conversation_history:
    st.write(role, message)
