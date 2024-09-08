import streamlit as st
import pandas as pd
from io import BytesIO

# Função para carregar e processar o DataFrame
def load_dataframe(file):
    df = pd.read_excel(file, dtype=str)
    return df

# Função para encontrar dados não presentes em uma coluna
def find_missing_data(df1, df2, column1, column2):
    set1 = set(df1[column1].dropna())
    set2 = set(df2[column2].dropna())
    
    missing_in_df2 = set1 - set2
    missing_data = df1[df1[column1].isin(missing_in_df2)]
    
    return missing_data

# Função para criar um download de arquivo no Streamlit
def create_download_link(df, filename):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='MissingData')
    processed_file = output.getvalue()
    return st.download_button(label="Baixar Arquivo Atualizado",
                             data=processed_file,
                             file_name=filename,
                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# Upload dos arquivos Excel
uploaded_file1 = st.file_uploader("Escolha o primeiro arquivo Excel", type="xlsx", key="file1")
uploaded_file2 = st.file_uploader("Escolha o segundo arquivo Excel", type="xlsx", key="file2")

st.write("Primeiro forneça o arquivo completo, em segundo o faltante.")

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Carregar os DataFrames
    df1 = load_dataframe(uploaded_file1)
    df2 = load_dataframe(uploaded_file2)

    # Exibir nomes das colunas do primeiro e segundo arquivo lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Colunas do primeiro arquivo:")
        st.write(df1.columns.tolist())
    
    with col2:
        st.write("Colunas do segundo arquivo:")
        st.write(df2.columns.tolist())

    # Seleção de colunas para comparar
    column1 = st.selectbox("Selecione a coluna do primeiro arquivo para comparar", df1.columns)
    column2 = st.selectbox("Selecione a coluna do segundo arquivo para comparar", df2.columns)

    if column1 and column2:
        # Encontrar dados não presentes na coluna selecionada
        missing_data = find_missing_data(df1, df2, column1, column2)

        # Exibir os dados faltantes
        st.write("Dados que estão no primeiro arquivo e não no segundo arquivo:")
        st.dataframe(missing_data)

        # Criar o link para download do arquivo atualizado
        create_download_link(missing_data, 'dados_faltantes.xlsx')
