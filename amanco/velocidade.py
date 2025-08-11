import streamlit as st
import pandas as pd
import re
import io

# --- FUNÇÃO PRINCIPAL DE PROCESSAMENTO ---
def processar_arquivos(file_ok, file_vel):
    """
    Função que encapsula toda a lógica de processamento dos arquivos.
    Recebe os arquivos carregados e retorna o DataFrame final e logs do processo.
    """
    logs = []

    try:
        # Carrega o modelo a partir do arquivo carregado
        logs.append("Carregando arquivo modelo...")
        df_modelo = pd.read_excel(file_ok)
        colunas_modelo = df_modelo.columns.tolist()
        logs.append("✅ Modelo carregado.")

        # Lê os dados principais, pulando o cabeçalho falso
        logs.append("Carregando arquivo de velocidade...")
        df_raw = pd.read_excel(file_vel, skiprows=7)
        logs.append("✅ Arquivo de velocidade carregado.")

        # Lê tudo como texto para detectar as trocas de placa
        # É preciso "rebobinar" o arquivo para lê-lo novamente
        file_vel.seek(0) 
        df_full = pd.read_excel(file_vel, header=None)

        # Detecta linhas com placas
        placa_regex = r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}"
        placas_info = []
        for idx, val in df_full.iloc[:, 1].items():
            if isinstance(val, str) and re.match(placa_regex, val.strip().split()[0]):
                placa = val.strip().split()[0]
                placas_info.append((idx, placa))
        
        if not placas_info:
            st.error("Nenhuma placa encontrada no arquivo de velocidade. Verifique o formato do arquivo.")
            return None, logs

        # Mapeamento das placas por linha
        placas_idx = [x[0] for x in placas_info]
        placas_val = [x[1] for x in placas_info]
        placas_map = {}

        placa_pointer = 0
        for i in range(len(df_raw)):
            abs_idx = i + 8  # 7 puladas + 1 cabeçalho real
            if placa_pointer + 1 < len(placas_idx) and abs_idx >= placas_idx[placa_pointer + 1]:
                placa_pointer += 1
            placas_map[i] = placas_val[placa_pointer]

        # Renomeia colunas automaticamente com base em similaridade
        logs.append("Renomeando colunas...")
        colunas_encontradas = df_raw.columns.tolist()
        col_data = [c for c in colunas_encontradas if "data" in str(c).lower()][0]
        col_local = [c for c in colunas_encontradas if "local" in str(c).lower()][0]
        col_vel = [c for c in colunas_encontradas if "velocidade" in str(c).lower()][0]

        df_raw.rename(columns={
            col_data: 'Data & Hora',
            col_local: 'Endereço',
            col_vel: 'Velocidade'
        }, inplace=True)
        logs.append("✅ Colunas renomeadas.")

        # Adiciona colunas fixas
        df_raw['Veículo'] = df_raw.index.map(placas_map)
        df_raw['Apelido'] = df_raw['Veículo']
        df_raw['Infração'] = "Velocidade Máxima"
        df_raw['Valor Padrão'] = "110 Km/h"
        df_raw['Valor'] = ""
        df_raw['Condutor'] = ""
        df_raw['Ident.'] = ""

        # Garante todas as colunas do modelo
        for col in colunas_modelo:
            if col not in df_raw.columns:
                df_raw[col] = ""

        # Reordena colunas e faz cópia segura
        df_final = df_raw[colunas_modelo].copy()

        logs.append(f"📊 Total de linhas carregadas: {len(df_final)}")
        logs.append("⚙️  Iniciando conversão de dados...")

        # --- SEÇÃO DE CONVERSÃO DE DATA E VELOCIDADE CORRIGIDA ---
        df_final['Data & Hora'] = pd.to_datetime(df_final['Data & Hora'], errors='coerce')
        df_final.loc[df_final['Data & Hora'].notna(), 'Data & Hora'] = df_final['Data & Hora'].dt.strftime('%d/%m/%Y %H:%M')
        df_final['Velocidade'] = pd.to_numeric(
            df_final['Velocidade'].astype(str).str.extract(r'(\d+)', expand=False),
            errors='coerce'
        )
        
        # Relatório de perdas
        linhas_totais = len(df_final)
        sem_data = df_final['Data & Hora'].isna().sum()
        sem_vel = df_final['Velocidade'].isna().sum()

        logs.append("✔️ Conversão concluída.")
        logs.append(f"❗ Linhas sem data válida: {sem_data} ({sem_data/linhas_totais:.1%})")
        logs.append(f"❗ Linhas sem velocidade válida: {sem_vel} ({sem_vel/linhas_totais:.1%})")

        return df_final, logs

    except Exception as e:
        st.error(f"Ocorreu um erro durante o processamento: {e}")
        return None, logs

# --- INTERFACE DO STREAMLIT ---

st.set_page_config(page_title="Formatador de Relatório de Velocidade", layout="wide")

st.title("🚗 Formatador de Relatório de Velocidade Amanco")
st.markdown("""
Esta ferramenta automatiza a formatação de relatórios de velocidade, seguindo o padrão da Amanco. 
Faça o upload dos arquivos necessários para iniciar o processo.
""")

# Colunas para upload
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Arquivo Modelo (.xlsx)")
    st.info("Faça o upload do arquivo 'ok telemetria...' que serve como modelo de colunas.")
    file_ok = st.file_uploader("Selecione o arquivo modelo", type="xlsx", key="modelo")

with col2:
    st.subheader("2. Arquivo de Velocidade (.xlsx)")
    st.info("Faça o upload do relatório de velocidade bruto para ser processado.")
    file_vel = st.file_uploader("Selecione o arquivo de velocidade", type="xlsx", key="velocidade")

if file_ok and file_vel:
    st.success("Arquivos carregados com sucesso!")
    
    if st.button("🚀 Processar Arquivos", type="primary"):
        with st.spinner('Aguarde, processando os dados...'):
            df_final, logs = processar_arquivos(file_ok, file_vel)
        
        # Exibe os logs do processo
        st.subheader("📋 Log de Processamento")
        st.text_area("Detalhes da Execução", "\n".join(logs), height=300)

        if df_final is not None:
            st.subheader("✅ Processamento Finalizado!")
            st.markdown(f"O arquivo foi processado e resultou em **{len(df_final)}** linhas.")
            
            # Exibe uma prévia do DataFrame
            st.dataframe(df_final.head())
            
            # --- SEÇÃO DE DOWNLOAD ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Sheet1')
            
            # "Rebobina" o buffer para o início
            output.seek(0)
            
            st.download_button(
                label="📥 Baixar Arquivo Formatado",
                data=output,
                file_name="velocidade_amanco_formatado_final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Seção de instruções
st.markdown("---")
st.header("Instruções")
st.markdown("""
1.  **Carregue o Arquivo Modelo:** Utilize o primeiro campo para subir o seu arquivo `ok telemetria dezembro amanco.xlsx`.
2.  **Carregue o Arquivo de Velocidade:** No segundo campo, suba o arquivo `velocidade amanco.xlsx`.
3.  **Processe:** Clique no botão 'Processar Arquivos' para iniciar a formatação.
4.  **Visualize e Baixe:** Após o processamento, você verá os logs, uma prévia dos dados e um botão para baixar o arquivo final em formato Excel.
""")