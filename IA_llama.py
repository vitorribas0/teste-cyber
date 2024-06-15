import streamlit as st
import pandas as pd
import sqlite3

# Função para criar a tabela no SQLite (apenas para exemplo)
def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    idade INTEGER
                )''')
    conn.commit()
    conn.close()

# Função para inserir dados no SQLite
def insert_data(nome, idade):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO dados (nome, idade) VALUES (?, ?)', (nome, idade))
    conn.commit()
    conn.close()

# Configuração inicial
st.title('Upload de arquivo Excel e armazenamento seguro')

# Upload do arquivo Excel
file = st.file_uploader('Carregue um arquivo Excel', type=['xls', 'xlsx'])

if file is not None:
    df = pd.read_excel(file)

    # Exibindo os dados do arquivo Excel
    st.write('**Dados do arquivo Excel:**')
    st.write(df)

    # Criando a tabela no SQLite (se ainda não existir)
    create_table()

    # Inserindo os dados no SQLite
    st.write('**Inserindo dados no banco de dados:**')
    for index, row in df.iterrows():
        insert_data(row['Nome'], row['Idade'])
        st.write(f"Nome: {row['Nome']}, Idade: {row['Idade']} - Inserido com sucesso!")

    st.success('Dados inseridos com sucesso no banco de dados.')

    # Mensagem final
    st.write('**Processo concluído com sucesso!**')

