import streamlit as st
import pandas as pd
import base64
from datetime import datetime

# Função para corrigir a planilha
def corrigir_planilha(df):
    # Remover espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Excluir linhas onde a coluna "Grupo" é "TO - EQUIPAMENTO" ou "TO - GERADOR"
    if 'Grupo' in df.columns:
        df = df[~df['Grupo'].isin(['TO - EQUIPAMENTO', 'TO - GERADOR'])]
    else:
        st.write("A coluna 'Grupo' não existe no DataFrame.")
    
    # Excluir linhas onde a coluna 'Modelo' é "Equipamento, Gerador"    
    if 'Modelo' in df.columns:
        df = df[~df['Modelo'].isin(['EQUIPAMENTO', 'GERADOR', 'Equipamento', 'equipamento', 'Gerador', 'gerador'])]
    else:
        st.write("A coluna 'Modelo' não existe")
        
    # Excluir linhas onde a coluna 'Fabricante' é "Equipamento, Gerador"    
    if 'Fabricante' in df.columns:
        df = df[~df['Fabricante'].isin(['EQUIPAMENTO', 'GERADOR', 'Equipamento', 'equipamento', 'Gerador', 'gerador'])]
    else:
        st.write("A coluna 'Fabricante' não existe")

    if 'Servico' in df.columns:
        # Remova espaços extras no início e no fim das strings na coluna 'Servico'
        df['Servico'] = df['Servico'].str.strip()

        # Lista de itens que são combustíveis
        combustiveis = ['Gasolina', 'Diesel', 'Diesel S500', 'Diesel S10', 'Gasolina Aditivada', 'Etanol', 'S10/50 ADITIVADO']
        
        # Substitua os valores 'Manutencao Preventiva' por 'Manutencao' e 'ARLA32' por 'ARLA 32'
        df['Servico'] = df['Servico'].replace({'Manutencao Preventiva': 'Manutencao', 'ARLA32': 'ARLA 32', 'S10/50 ADITIVADO': 'Diesel S10 aditivado'})

        # Converta os valores da coluna 'Quantidade' para float
        df['Quantidade'] = df['Quantidade'].str.replace(',', '.').astype(float)

        # Substitua os valores abaixo de 1 por 1 na coluna 'Quantidade'
        df.loc[(df['Quantidade'] < 1) & (~df['Servico'].isin(combustiveis)), 'Quantidade'] = 1
        
        # Limpe os valores da coluna 'UsoTotal' que não são combustíveis
        df.loc[~df['Servico'].isin(combustiveis), 'UsoTotal'] = None

        # Formate os valores da coluna "Quantidade"
        df['Quantidade'] = df['Quantidade'].apply(lambda x: f"{x:.2f}".replace('.', ','))

    else:
        st.write(f"A coluna 'Servico' não existe no DataFrame. As colunas disponíveis são: {', '.join(df.columns)}")

    # Remove a coluna "Unnamed: 31" se ela existir
    if "Unnamed: 31" in df.columns:
        df.drop("Unnamed: 31", axis=1, inplace=True)

    return df

# Função principal
def main():
    # Dicionário de mapeamento de cliente para cidade
    cliente_para_cidade = {
        "COMPANHIA SANEAMENTO DO TOCANTINS": "tocantins",
        "BRK AMBIENTAL CACHOEIRO DE ITAPEMIRIM S/A": "cachoeiro",
        "BRK AMBIENTAL STA GERTRUDES": "gertrudes",
        "SANEAQUA MAIRINQUE SA": "mairinque",
        "BRK AMBIENTAL MACAE SA": "macae_ro",
        "BRK AMBIENTAL - MACEIO": "maceio",
        "BRK AMBIENTAL MANSO S.A": "manso",
        "BRK AMBIENTAL MARANHAO": "maranhao",
        "BRK AMBIENTAL MAUA S.A.": "maua",
        "BRK AMBIENTAL PORTO FERREIRA": "porto ferreira",
        "BRK AMBIENTAL RIO CLARO S.A.": "rio claro",
        "BRK AMBIENTAL SUMARE": "sumare",
        "BRK AMBIENTAL LIMEIRA": "limeira",
        # Caso necessário, adicionar outras cidades
    }

    # Verifique se o arquivo foi carregado
    if uploaded_file is not None:
        # Carregue o arquivo CSV
        # Corrija e formate a planilha
        df_corrigido = corrigir_planilha(df)

        # Identificar a cidade na coluna "CLIENTE"
        if 'Cliente' in df_corrigido.columns:
            cliente = df_corrigido['Cliente'].iloc[0]  # Supondo que todas as linhas tenham o mesmo cliente na coluna "CLIENTE"
            cidade = cliente_para_cidade.get(cliente, cliente)  # Use o dicionário para obter a cidade ou o cliente se não encontrar
        else:
            st.error("A coluna 'CLIENTE' não foi encontrada na planilha.")
            return

        # Encontrar a menor e a maior data na coluna "DataHora"
        if 'DataHora' in df_corrigido.columns:
            df_corrigido['DataHora'] = pd.to_datetime(df_corrigido['DataHora'])
            data_inicio = df_corrigido['DataHora'].min()
            data_fim = df_corrigido['DataHora'].max()
        else:
            st.error("A coluna 'DataHora' não foi encontrada na planilha.")
            return

        # Formatando as datas
        data_inicio_str = data_inicio.strftime('%d-%m')
        data_fim_str = data_fim.strftime('%d-%m')
        data = f"{data_inicio_str} a {data_fim_str}"

        # Nome da planilha corrigida com base na cidade e data
        nome_planilha = f"{data} {cidade}.csv"

        # Exiba o DataFrame no Streamlit
        st.dataframe(df_corrigido)

        # Adicione um botão de download para baixar a planilha corrigida
        csv = df_corrigido.to_csv(index=False, sep=';', encoding='utf-8')
        b64 = base64.b64encode(csv.encode()).decode()  # codifique o arquivo para o formato base64
        href = f'<a href="data:file/csv;base64,{b64}" download="{nome_planilha}">\
                <button style="display:none;"></button></a>'
        st.markdown(href, unsafe_allow_html=True)

        # Adicione um botão de download alternativo
        st.download_button(
            label="Baixar planilha corrigida",
            data=csv,
            file_name=nome_planilha,
            mime="text/csv"
        )
       
    # Obtém todas as identificações únicas
    identificacoes = df_corrigido['Identificacao'].unique()

    # Adiciona a opção "Selecionar Todas" no início da lista de opções
    opcoes_identificacoes = ["Selecionar Todas"] + list(identificacoes)

    # Componente multiselect com a opção de selecionar todas
    identificacoes_selecionadas = st.multiselect("Selecione as Identificações", options=opcoes_identificacoes, default=["Selecionar Todas"])

    # Se "Selecionar Todas" estiver selecionado, seleciona automaticamente todas as identificações
    if "Selecionar Todas" in identificacoes_selecionadas:
        identificacoes_selecionadas = list(identificacoes)
        
    ##Pra que serve
    ##tantos códigos
    ##se a vida
    ##não é programada
    ##e as melhores coisas
    ##não têm lógica

    # Seleciona as colunas para o gráfico
    colunas_graficos = ['Quantidade', 'Valor', 'ValorUnitario', 'UsoTotal', 'Uso', 'UsoPorLitro']
    coluna_selecionada = st.selectbox("Selecione a coluna para o gráfico", options=colunas_graficos)

    if coluna_selecionada in df_corrigido.columns:
        # Filtra o DataFrame com base nas identificações selecionadas
        df_filtrado = df_corrigido[df_corrigido['Identificacao'].isin(identificacoes_selecionadas)]

        if coluna_selecionada != 'DataHora':
            # Converte a coluna selecionada para numérico, lidando com vírgulas e valores inválidos
            df_filtrado[coluna_selecionada] = pd.to_numeric(df_filtrado[coluna_selecionada].str.replace(',', '.'), errors='coerce')
            df_filtrado = df_filtrado.dropna(subset=[coluna_selecionada])

            # Agrupa por DataHora e Identificacao e realiza a agregação pela soma
            df_resumido = df_filtrado.groupby(['DataHora', 'Identificacao']).agg({coluna_selecionada: 'sum'}).reset_index()

            # Converte DataHora para string para uso no gráfico
            df_resumido['DataHora'] = df_resumido['DataHora'].dt.strftime('%Y-%m-%d')

            # Agrupa novamente para remover possíveis duplicatas
            df_resumido = df_resumido.groupby(['DataHora', 'Identificacao']).sum().reset_index()

            # Reorganiza os dados para o gráfico de barras
            chart_data = df_resumido.pivot_table(index='DataHora', columns='Identificacao', values=coluna_selecionada, fill_value=0)

            # Exibe o gráfico de barras
            st.bar_chart(
                chart_data,
                use_container_width=True
            )
        else:
            st.error("Por favor, selecione uma coluna diferente de 'DataHora' para o gráfico.")
    else:
        st.error(f"A coluna '{coluna_selecionada}' não está presente nos dados.")

uploaded_file = st.file_uploader("Por favor, forneça a planilha", type=['csv'])

if uploaded_file is not None:
    # Carregue o arquivo CSV
    df = pd.read_csv(uploaded_file, dtype="string", delimiter=";")
    main()
