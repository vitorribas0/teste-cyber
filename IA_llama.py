import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")  # Configuração para layout de página amplo

st.title("Chat com OpenAI")

# Inicialize o cliente OpenAI
client = OpenAI(
    api_key="LL-rZdxy5UFL4evTVeC6H1Jzuph00H08neiKQUGm3HSYOm1qMD4T8YxonRYedIH6856",
    base_url="https://api.llama-api.com"
)

# Histórico de conversa
conversation_history = []

# Função para enviar mensagem e obter resposta
def enviar_mensagem(pergunta):
    global conversation_history
    # Adicionar a mensagem do usuário ao histórico
    conversation_history.append({"role": "user", "content": pergunta})
    # Enviar a mensagem para a IA e obter a resposta
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Olá! Sou um especialista em Python, Pandas, PySpark e AWS."},
            {"role": "user", "content": pergunta}
        ]
    )
    # Adicionar a resposta da IA ao histórico
    conversation_history.append({"role": "ai", "content": response.choices[0].message.content})
    return response.choices[0].message.content

# Input para o usuário na tela
st.write("Digite sua pergunta para a IA:")
pergunta = st.text_input("", key="pergunta")

# Enviar a pergunta para a IA quando o usuário pressionar Enter
if pergunta:
    # Envie a pergunta para a IA e obtenha a resposta
    resposta = enviar_mensagem(pergunta)
    st.write("Resposta da IA:")
    st.write(resposta)

# Exibir histórico de conversa
st.subheader("Histórico de Conversa")
for message in conversation_history:
    if message['role'] == 'user':
        st.text_input("Usuário:", message['content'], key=message['content'])
    elif message['role'] == 'ai':
        st.text_area("IA:", message['content'], key=message['content'])
