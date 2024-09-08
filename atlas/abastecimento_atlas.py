import streamlit as st
import pandas as pd
from io import BytesIO

# Função para processar o DataFrame
def process_dataframe(df):
    # Definir um dicionário de mapeamento para renomear as colunas
    rename_column = {
        'CODIGO EMISSORA': 'FORNECEDOR',
    }

    # Renomear as colunas
    df.rename(columns=rename_column, inplace=True)

    # Nome das colunas que você deseja atualizar
    column_servico = 'SERVICO'
    column_litros = 'LITROS'  # Nome real da coluna de litros

    # Atualizar a coluna 'LITROS' para '1,00' onde a coluna 'SERVICO' é 'Lavagem completa' ou 'Lavagem expressa'
    df[column_litros] = df.apply(
        lambda row: '1,00' if row[column_servico] in ['Lavagem completa', 'Lavagem expressa'] else row[column_litros],
        axis=1
    )

    coluna_para_preencher = 'FORNECEDOR'

    # Texto com o qual preencher as células em branco
    texto_para_preencher = 'Ticketlog'

    # Preencher células em branco da coluna com o texto especificado
    df[coluna_para_preencher] = df[coluna_para_preencher].fillna(texto_para_preencher)

    # Definir as colunas específicas das quais você deseja excluir a última linha
    colunas_para_atualizar = ['CODIGO TRANSACAO', 'LITROS', 'VALOR EMISSAO', 'FORNECEDOR']

    # Remover a última linha para as colunas especificadas
    for coluna in colunas_para_atualizar:
        df[coluna] = df[coluna].iloc[:-1]  # Remove a última linha

    return df

# Função para criar um download de arquivo no Streamlit
def create_download_link(df, filename):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_file = output.getvalue()
    return st.download_button(label="Baixar Planilha Atualizada",
                             data=processed_file,
                             file_name=filename,
                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

uploaded_file = st.file_uploader("Por favor, forneça a planilha extraída da Ticket", type="xlsx")

if uploaded_file is not None:
    # Carregar o arquivo Excel
    df = pd.read_excel(uploaded_file, dtype=str)

    # Processar o DataFrame
    df_updated = process_dataframe(df)

    # Exibir todas as linhas do DataFrame atualizado
    st.write("Dados Atualizados:")
    st.dataframe(df_updated, height=600)  # Ajuste a altura conforme necessário

    # Criar o link para download da planilha atualizada
    create_download_link(df_updated, 'RFCV_atualizado.xlsx')
