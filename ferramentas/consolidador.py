import io
import streamlit as st
import pandas as pd

# Função para consolidar arquivos Excel
def consolidate_excel(files):
    dataframes = [pd.read_excel(io.BytesIO(file.read())) for file in files]
    consolidated_df = pd.concat(dataframes, ignore_index=True)
    return consolidated_df

st.write("Faça upload de múltiplos arquivos Excel para consolidá-los em um único arquivo.")

# Upload dos arquivos
uploaded_files = st.file_uploader("Escolha arquivos Excel", type="xlsx", accept_multiple_files=True)

if uploaded_files:
    # Consolida os arquivos
    consolidated_df = consolidate_excel(uploaded_files)
    
    # Exiba uma mensagem de sucesso
    st.success('Arquivos consolidados com sucesso!')

    # Exiba o DataFrame consolidado
    st.write(consolidated_df)

    # Salve o arquivo consolidado
    output = io.BytesIO()
    consolidated_df.to_excel(output, index=False)
    output.seek(0)

    # Exiba um link para download do arquivo consolidado
    st.download_button(
        label="Baixe o arquivo consolidado",
        data=output,
        file_name='consolidated_file.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
