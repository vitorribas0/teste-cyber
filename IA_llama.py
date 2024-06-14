import streamlit as st
import sqlite3
from openai import OpenAI

st.title("Chat with OpenAI")

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

# Connect to SQLite database
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS conversation_history 
             (role text, message text)''')
conn.commit()

# Function to send message to AI chatbot
def send_message(message):
    response = client.chat.completions.create(
        model="llama-13b-chat",
        messages=[
            {"role": "system", "content": "Olá! Sou um especialista em Python, Pandas, PySpark e AWS."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# Chat input field
message = st.text_input("Typing...")
if st.button("Send"):
    # Add message to chat history
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("User:", message))
    conn.commit()
    # Send message to AI chatbot and retrieve response
    response = send_message(message)
    # Add response to chat history
    c.execute("INSERT INTO conversation_history VALUES (?, ?)", ("Bot:", response))
    conn.commit()

# Display chat history
c.execute("SELECT * FROM conversation_history")
for row in c.fetchall():
    st.write(row)

# Close connection to database
conn.close()
