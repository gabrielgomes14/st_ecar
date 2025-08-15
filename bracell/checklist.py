import pandas as pd
import streamlit as st
from io import BytesIO

# --- Função para processar os dados (lógica principal do seu script) ---
def processar_dados(df, nome_coluna_ignicao):
    """
    Processa o DataFrame para encontrar o primeiro e o último evento de ignição
    de cada veículo por dia.
    """
    try:
        # Garante que a coluna de data/hora está no formato correto
        df[nome_coluna_ignicao] = pd.to_datetime(df[nome_coluna_ignicao], dayfirst=True)
        
        # Cria uma coluna 'Data' apenas com a parte da data para agrupamento
        df["Data"] = df[nome_coluna_ignicao].dt.date
        
        # Agrupa os dados por veículo e por dia
        grupos_diarios = df.groupby(['Veículo', 'Data'])
        
        # Encontra os índices do primeiro e do último registro de ignição para cada grupo
        indices_min_ignicao = grupos_diarios[nome_coluna_ignicao].idxmin()
        indices_max_ignicao = grupos_diarios[nome_coluna_ignicao].idxmax()
        
        # Combina os índices e remove duplicatas
        indices_para_manter = pd.concat([indices_min_ignicao, indices_max_ignicao]).unique()
        
        # Filtra o DataFrame original para manter apenas as linhas desejadas
        df_resultado = df.loc[indices_para_manter]
        
        # Ordena o resultado para melhor visualização
        df_resultado = df_resultado.sort_values(by=['Veículo', 'Data', nome_coluna_ignicao])
        
        # Remove a coluna 'Data' auxiliar antes de exportar
        df_resultado_final = df_resultado.drop(columns=["Data"])
        
        return df_resultado_final, None  # Retorna o DataFrame e nenhuma mensagem de erro
        
    except Exception as e:
        return None, f"Ocorreu um erro: {e}" # Retorna None e a mensagem de erro

# --- Interface do Streamlit ---

st.set_page_config(layout="wide")
st.title("Análise de Ignição Diária de Veículos")

st.markdown("""
Esta aplicação analisa um arquivo Excel para extrair o **primeiro e o último registro de ignição** de cada veículo por dia.
""")

# 1. Upload do arquivo de entrada
arquivo_upload = st.file_uploader(
    "1. Escolha o arquivo Excel (.xlsx)", 
    type=["xlsx"]
)

if arquivo_upload:
    try:
        # Carrega o arquivo na memória
        df_original = pd.read_excel(arquivo_upload)
        
        st.subheader("Pré-visualização dos dados carregados")
        st.dataframe(df_original.head())

        # 2. Input para o nome da coluna de ignição
        st.markdown("---")
        st.subheader("Configurações da Análise")
        
        # Tenta adivinhar o nome da coluna, mas permite que o usuário altere
        opcoes_colunas = df_original.columns.tolist()
        nome_coluna_sugerido = 'Data Hora Ignição Ligada'
        # Define o índice da sugestão se ela existir na lista de colunas
        indice_sugerido = opcoes_colunas.index(nome_coluna_sugerido) if nome_coluna_sugerido in opcoes_colunas else 0

        nome_coluna_ignicao = st.selectbox(
            "2. Selecione a coluna que contém a data e hora da ignição:",
            opcoes_colunas,
            index=indice_sugerido
        )

        # 3. Botão para iniciar o processamento
        if st.button("Gerar Relatório de Ignição", type="primary"):
            with st.spinner("Processando os dados..."):
                # Chama a função de processamento
                df_resultado, erro = processar_dados(df_original.copy(), nome_coluna_ignicao)

            if erro:
                st.error(erro)
            else:
                st.success("Relatório gerado com sucesso!")
                st.subheader("Resultado da Análise")
                st.dataframe(df_resultado)

                # --- Opção para Download ---
                # Converte o DataFrame para um arquivo Excel em memória
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_resultado.to_excel(writer, index=False, sheet_name='Relatorio')
                
                # Prepara os dados para o botão de download
                dados_excel = output.getvalue()

                st.download_button(
                    label="📥 Baixar Relatório em Excel",
                    data=dados_excel,
                    file_name="relatorio_ignicao_diaria.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")