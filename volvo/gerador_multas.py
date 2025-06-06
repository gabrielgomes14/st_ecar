import os
import pandas as pd
from fpdf import FPDF
import streamlit as st
from io import BytesIO
import tempfile
import shutil

st.set_page_config(page_title="Gerador de PDFs de Multas", layout="centered")

st.title("📄 Gerador de PDFs de Comunicados de Infração")
st.markdown("Envie os arquivos necessários abaixo para gerar automaticamente os comunicados em PDF.")

# Seção de upload com visual melhorado
with st.container():
    st.subheader("📂 Upload de Arquivos")
    st.markdown("Faça o upload da planilha de multas e do logo da empresa.")

    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_excel = st.file_uploader("📑 Planilha Excel (.xlsx)", type=["xlsx"], label_visibility="visible")
    with col2:
        uploaded_logo = st.file_uploader("🖼️ Logo da Empresa (.png/.jpg)", type=["png", "jpg", "jpeg"], label_visibility="visible")

# Geração dos PDFs
if uploaded_excel and uploaded_logo:
    df = pd.read_excel(uploaded_excel)
    logo_bytes = uploaded_logo.read()

    pasta_saida = tempfile.mkdtemp()
    progresso = st.progress(0)
    contador_emails = {}

    for index, row in df.iterrows():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
            tmp_logo.write(logo_bytes)
            logo_path = tmp_logo.name
        pdf.image(logo_path, x=10, y=8, w=50)
        pdf.ln(15)

        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(190, 12, txt="Comunicado de Infração de Trânsito", ln=True, align='C')

        def escrever_linha(titulo, valor):
            pdf.set_font("Arial", style='B', size=10)
            pdf.cell(50, 10, txt=titulo, border=1)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 10, txt=str(valor), border=1, ln=True)

        escrever_linha("Nº AIT:", row.get('N° AIT', 'N/A'))
        escrever_linha("Usuário (a):", row.get('Usuário (a)', 'N/A'))
        escrever_linha("Placa:", row.get('Placa', 'N/A'))
        escrever_linha("Infração:", row.get('Infração', 'N/A'))
        escrever_linha("Data da Infração:", row.get('Data/hora da infração', 'N/A'))
        escrever_linha("Local:", row.get('Local', 'N/A'))
        escrever_linha("Valor:", row.get('Valor', 'N/A'))

        pdf.ln(5)
        pdf.multi_cell(0, 5, txt=(
            "Recebemos uma notificação de infração de trânsito ocorrida na data acima mencionada e identificamos que "
            "o Sr.(a) é o(a) usuário(a) responsável por este veículo."
        ))
        pdf.ln(5)

        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(0, 10, txt="PAGAMENTO DA MULTA", ln=True)

        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, txt=f"Será debitado de sua folha de pagamento o valor de {row.get('Valor total', 'N/A')}, referente à infração.")

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.write(5, "IMPORTANTE: ")
        pdf.set_font("Arial", '', 10)
        pdf.write(5, (
            "A não identificação do infrator e/ou a entrega com atraso da notificação assinada mais os documentos anexos requeridos pelo Órgão gerador da multa, acarretará uma nova multa por não identificação do infrator "
        ))
        pdf.set_font("Arial", 'B', 10)
        pdf.write(5, "(NIC) ")
        pdf.set_font("Arial", '', 10)
        pdf.write(5, (
            "cujo valor será o da multa, multiplicado pelo número de infrações iguais cometidas no período de 12 meses (ART. 257, parágrafo 8 do CONTRAN)."
        ))

        pdf.ln(5)
        pdf.multi_cell(0, 5, txt=(
            "Caso a notificação para a indicação do condutor não seja entregue a tempo para o funcionário, a multa por não identificação será arcada pela empresa. "
            "O cumprimento do Código de Trânsito se faz necessário para evitarmos pendências e penalidades junto aos Órgãos de Trânsito (Municipal, Federal e Estadual)."
        ))

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, txt="ENCAMINHAMENTO DE RECURSO", ln=True)

        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, txt=(
            "Recurso junto ao DETRAN / CIRETRAN poderá ser movido pelo interessado:\n"
            "- Redigir uma carta apresentando defesa, contendo os dados do condutor do veículo e da multa;\n"
            "- Encaminhar à Junta Administrativa de Recursos de Infração do Município onde ocorreu a multa "
            "(antes de encaminhar o recurso, deve ser anexado ao processo, a cópia da procuração autenticada com assinatura de um procurador da Cia.)\n"
            "Site de CET para consulta: www.cetsp.com.br (somente para multas no município de São Paulo)\n"
            "Departamento de Trânsito de SBC: www.detsbc.gov.br (somente multas no município de SBC).\n"
            "Consulta de multas do estado de São Paulo: www.multacar.com.br (Municipal, Estadual e Federal)."
        ))

        pdf.ln(5)
        pdf.cell(0, 10, txt="De acordo,", ln=True)
        pdf.ln(10)
        pdf.cell(0, 10, txt="_____________________________________", ln=True)

        pdf.set_xy(130, pdf.get_y())
        pdf.cell(5, 5, border=1)
        pdf.cell(0, 5, txt="Me Identificarei", ln=True)

        pdf.set_xy(130, pdf.get_y())
        pdf.cell(5, 5, border=1)
        pdf.cell(0, 5, txt="Não me identificarei", ln=True)

        pdf.set_xy(130, pdf.get_y())
        pdf.cell(5, 5, border=1)
        pdf.cell(0, 5, txt="A notificação não chegou a tempo", ln=True)

        email_base = str(row.get('e-mail', f"sem_email_{index}")).strip().replace("/", "-").replace("\\", "-")
        contador_emails[email_base] = contador_emails.get(email_base, 0) + 1
        sufixo = f"_{contador_emails[email_base]}" if contador_emails[email_base] > 1 else ""
        nome_arquivo = os.path.join(pasta_saida, f"{email_base}{sufixo}.pdf")
        pdf.output(nome_arquivo)

        progresso.progress((index + 1) / len(df))

    shutil.make_archive(pasta_saida, 'zip', pasta_saida)
    with open(pasta_saida + ".zip", "rb") as f:
        st.download_button("📥 Baixar PDFs em ZIP", f, file_name="comunicados_multas.zip")

    st.success("✅ PDFs gerados com sucesso!")

else:
    st.info("🔄 Faça o upload da planilha e do logo para ativar a geração de PDFs.")
