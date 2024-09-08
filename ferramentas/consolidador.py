import pandas as pd
import streamlit as st
import base64
import io

def consolidar_arquivos(arquivos):
    # Lista para armazenar os DataFrames
    dfs = []
    
    # Ler cada arquivo e adicionar o DataFrame à lista
    for arquivo in arquivos:
        arquivo_bytes = arquivo.read()
        if arquivo.name.endswith('.csv'):
            # Ler arquivo CSV
            df = pd.read_csv(io.BytesIO(arquivo_bytes), dtype="string", delimiter=";")
        elif arquivo.name.endswith('.xlsx'):
            # Ler arquivo Excel
            df = pd.read_excel(io.BytesIO(arquivo_bytes))
        else:
            st.error(f"Formato de arquivo {arquivo.name} não suportado.")
            continue
        dfs.append(df)
    
    # Concatenar todos os DataFrames em um único DataFrame
    df_consolidado = pd.concat(dfs, ignore_index=True)
    
    return df_consolidado

def main():
    st.title("Consolidar Arquivos CSV e Excel")

    # Upload de múltiplos arquivos CSV e Excel
    uploaded_files = st.file_uploader("Por favor, forneça um ou mais arquivos CSV ou Excel", type=['csv', 'xlsx'], accept_multiple_files=True)

    if uploaded_files:
        # Consolidar arquivos
        df_consolidado = consolidar_arquivos(uploaded_files)

        # Exibir o DataFrame consolidado
        st.write("DataFrame Consolidado:")
        st.dataframe(df_consolidado)

        # Gerar o CSV consolidado
        csv = df_consolidado.to_csv(index=False, sep=';', encoding='utf-8')
        b64 = base64.b64encode(csv.encode()).decode()
        nome_planilha = "consolidado.csv"
        href = f'<a href="data:file/csv;base64,{b64}" download="{nome_planilha}">Baixar arquivo consolidado</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Adicionar botão de download
        st.download_button(
            label="Baixar arquivo consolidado",
            data=csv,
            file_name=nome_planilha,
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
