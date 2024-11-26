import streamlit as st
import pandas as pd
from io import BytesIO

def dividir_arquivo(arquivo, linhas_por_aba):
    # Carregar o arquivo Excel
    df = pd.read_excel(arquivo)
    num_abas = (len(df) // linhas_por_aba) + 1
    tabs = [f'Aba {i+1}' for i in range(num_abas)]
    tab = st.selectbox('Selecione a aba', tabs)
    aba_selecionada = int(tab.split(' ')[1]) - 1
    start_row = aba_selecionada * linhas_por_aba
    end_row = start_row + linhas_por_aba

    st.write(df.iloc[start_row:end_row])

    if st.button('Baixar arquivo dividido'):
        excel_bytes = dividir_em_arquivos(df, linhas_por_aba, num_abas)
        st.download_button(label='Baixar Excel', data=excel_bytes, file_name='arquivo_dividido.xlsx')

def dividir_em_arquivos(df, linhas_por_aba, num_abas):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i in range(num_abas):
            start_row = i * linhas_por_aba
            end_row = start_row + linhas_por_aba
            df.iloc[start_row:end_row].to_excel(writer, sheet_name=f'Aba {i+1}', index=False)
    output.seek(0)
    return output

st.title('Dividir Arquivo em Abas')
st.write('Carregue um arquivo Excel para dividi-lo em abas de 5000 linhas.')

uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
linhas_por_aba = 5000

if uploaded_file is not None:
    dividir_arquivo(uploaded_file, linhas_por_aba)