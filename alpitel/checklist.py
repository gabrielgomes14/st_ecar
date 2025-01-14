import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from io import BytesIO

warnings.filterwarnings("ignore")

def verificar_e_consolidar_divergencias(file):
    OUTPUT_PATH = "relatorio_divergencias.xlsx"

    COLUMNS = [
        "Colaborador", "Executores",
        "Modelo de checklist", "Veículo",
        "Data", "Data de término",
        "Total por colaborador", "Controle de portaria"
    ]

    # Leitura da planilha
    df = pd.read_excel(file)

    # Verificar se todas as colunas esperadas estão presentes
    for column in COLUMNS:
        if column not in df.columns:
            raise KeyError(f"A coluna '{column}' não foi encontrada na planilha.")

    # Limpeza de dados
    df.columns = df.columns.str.strip()
    df["Colaborador"] = df["Colaborador"].fillna(method="ffill").astype(str).str.strip()
    df["Executores"] = df["Executores"].fillna("").astype(str).str.strip()
    df["Modelo de checklist"] = df["Modelo de checklist"].astype(str).str.strip()
    df["Controle de portaria"] = df["Controle de portaria"].fillna("").astype(str).str.strip()

    # Verificar erros de controle de portaria (nulos, inválidos)
    df["Erro de Controle de Portaria"] = df["Controle de portaria"].isna() | \
                                         (df["Controle de portaria"] == "-") | \
                                         (df["Controle de portaria"] == "")

    # Contar erros de execução do checklist por Colaborador
    def contar_erros_execucao(grupo):
        modelos = grupo["Modelo de checklist"].tolist()
        erros = sum(1 for i in range(1, len(modelos)) if modelos[i] == modelos[i - 1])
        return pd.Series({"Erro na execução do Checklist": erros})

    erros_execucao = df.groupby("Executores").apply(contar_erros_execucao).reset_index()

    # Contar erros de executores diferentes de colaboradores
    erros_executor = df[df["Executores"] != df["Colaborador"]].copy()
    erros_executor_counts = erros_executor.groupby("Executores").size().reset_index(name="Erro de Executor diferente de colaborador")

    # Contabilizar erros de controle de portaria por Executor
    erros_portaria_executor = df.groupby("Executores")["Erro de Controle de Portaria"].sum().reset_index()

    # Consolidar os erros por Colaborador
    consolidado_colaborador = erros_execucao \
        .merge(erros_portaria_executor, on="Executores", how="left") \
        .merge(erros_executor_counts, on="Executores", how="left")

    # Preencher NaN com 0
    consolidado_colaborador.fillna(0, inplace=True)

    # Converter as colunas de erro para inteiros
    for column in ["Erro na execução do Checklist", "Erro de Executor diferente de colaborador", "Erro de Controle de Portaria"]:
        consolidado_colaborador[column] = consolidado_colaborador[column].astype(int)

    # Calcular o total de erros por Colaborador
    consolidado_colaborador["Total de Erros Colaborador"] = consolidado_colaborador[[
        "Erro na execução do Checklist",
        "Erro de Executor diferente de colaborador",
        "Erro de Controle de Portaria"
    ]].sum(axis=1)

    # Ordenar os colaboradores pelo total de erros em ordem decrescente
    consolidado_colaborador.sort_values(by="Total de Erros Colaborador", ascending=False, inplace=True)


    # Preparar a estrutura para saída do Consolidado Colaborador
    total_erros_checklist = consolidado_colaborador["Erro na execução do Checklist"].sum()
    total_erros_executor = consolidado_colaborador["Erro de Executor diferente de colaborador"].sum()
    total_erros_portaria = consolidado_colaborador["Erro de Controle de Portaria"].sum()
    total_geral_erros = consolidado_colaborador["Total de Erros Colaborador"].sum()

    records_colaborador = []
    records_colaborador.append({
        "Rótulos de Linha": "TOTAL GERAL DE ERROS",
        "Contagem de Tipo de Erro": total_geral_erros
    })
    records_colaborador.append({
        "Rótulos de Linha": "TOTAL ERROS NA EXECUÇÃO DO CHECKLIST",
        "Contagem de Tipo de Erro": total_erros_checklist
    })
    records_colaborador.append({
        "Rótulos de Linha": "TOTAL ERROS DE EXECUTOR DIFERENTE",
        "Contagem de Tipo de Erro": total_erros_executor
    })
    records_colaborador.append({
        "Rótulos de Linha": "TOTAL ERROS DE CONTROLE DE PORTARIA",
        "Contagem de Tipo de Erro": total_erros_portaria
    })

    for _, row in consolidado_colaborador.iterrows():
        records_colaborador.append({
            "Rótulos de Linha": row["Executores"],
            "Contagem de Tipo de Erro": row["Total de Erros Colaborador"]
        })
        records_colaborador.append({
            "Rótulos de Linha": "  Erro na execução do Checklist",
            "Contagem de Tipo de Erro": row["Erro na execução do Checklist"]
        })
        records_colaborador.append({
            "Rótulos de Linha": "  Erro de Executor diferente de colaborador",
            "Contagem de Tipo de Erro": row["Erro de Executor diferente de colaborador"]
        })
        records_colaborador.append({
            "Rótulos de Linha": "  Erros de Controle de Portaria",
            "Contagem de Tipo de Erro": row["Erro de Controle de Portaria"]
        })

    df_final_colaborador = pd.DataFrame(records_colaborador)

    linhas_para_excluir = [4, 5, 6, 7]  # Ajustado para zero-based index
    df_final_colaborador = df_final_colaborador.drop(index=linhas_para_excluir)

    # Exportar para Excel com Abas Separadas
    with pd.ExcelWriter(OUTPUT_PATH, engine='xlsxwriter') as writer:
        # Consolidado por Colaborador
        df_final_colaborador.to_excel(writer, sheet_name='Consolidado_Colaborador', index=False)

    # Criar BytesIO para download do arquivo corrigido
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df_final_colaborador.to_excel(writer, sheet_name='Consolidado_Colaborador', index=False)
    excel_data.seek(0)

    return excel_data, df_final_colaborador

def plotar_grafico(df_final_colaborador):
    # Filtrar os dados necessários para o gráfico
    grafico_data = df_final_colaborador.iloc[:4].copy()
    grafico_data.set_index("Rótulos de Linha", inplace=True)

    # Criar o gráfico
    fig, ax = plt.subplots(figsize=(8, 4))  # Ajuste os valores para diminuir o tamanho
    grafico_data["Contagem de Tipo de Erro"].plot(kind='bar', ax=ax)
    ax.set_title("Total de Erros e Tipos de Erros")
    ax.set_ylabel("Contagem de Erros")
    ax.set_xlabel("Tipos de Erros")

    return fig

def plotar_grafico_adicional(df_final_colaborador):
    # Filtrar os dados necessários para o gráfico adicional
    indices = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
    grafico_adicional_data = df_final_colaborador.iloc[indices].copy()
    grafico_adicional_data.set_index("Rótulos de Linha", inplace=True)

    # Criar o gráfico adicional com o estilo da imagem fornecida
    fig, ax = plt.subplots(figsize=(8, 4))  # Ajuste os valores para diminuir o tamanho
    grafico_adicional_data["Contagem de Tipo de Erro"].plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_title("Comparativo 15 colaboradores com mais erros")
    ax.set_ylabel("Contagem de Erros")
    ax.set_xlabel("Colaboradores")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend(["Total de Erros"], loc='upper right')

    return fig

st.title("Análise de check-list")

uploaded_file = st.file_uploader("Escolha o arquivo Excel", type="xlsx")

if uploaded_file is not None:
    # Executar a função com o arquivo enviado
    excel_data, df_final_colaborador = verificar_e_consolidar_divergencias(uploaded_file)

    st.success("Relatório de divergências gerado com sucesso!")
    
    st.download_button(
        label="Download do arquivo corrigido",
        data=excel_data,
        file_name="relatorio_divergencias_corrigido.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Plotar e exibir o gráfico principal
    fig = plotar_grafico(df_final_colaborador)
    st.pyplot(fig)

    # Plotar e exibir o gráfico adicional
    fig_adicional = plotar_grafico_adicional(df_final_colaborador)
    st.pyplot(fig_adicional)
