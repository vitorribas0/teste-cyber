import streamlit as st
import pandas as pd

def main():
    st.title("Upload de Dados Excel")

    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Dados do Excel:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

if __name__ == "__main__":
    main()
