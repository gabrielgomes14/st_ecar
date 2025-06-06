import pandas as pd
import smtplib
from email.message import EmailMessage
import streamlit as st

st.set_page_config(page_title="Envio de E-mails - Volvo", layout="wide")
st.title("📧 Cobrança Aluguéis - Volvo")

# Escolha do provedor
st.subheader("🔌 Escolha o provedor de e-mail")
provedor = st.selectbox("Selecione o provedor de e-mail", ["Gmail", "Outlook"])

# Definir servidor SMTP e porta com base no provedor
if provedor == "Gmail":
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    st.info("ℹ️ Para Gmail, você precisa gerar uma senha de aplicativo em: https://myaccount.google.com/apppasswords")
elif provedor == "Outlook":
    SMTP_SERVER = 'smtp.office365.com'
    SMTP_PORT = 587
    st.info("⚠️ Para Outlook, **você deve usar uma senha de aplicativo**, não a senha normal. Ative a verificação em duas etapas e gere a senha em: https://mysignins.microsoft.com/security-info")

st.success(f"🔐 Usando servidor: **{SMTP_SERVER}:{SMTP_PORT}**")

# Credenciais
st.subheader("🔐 Credenciais do Remetente")
EMAIL_REMETENTE = st.text_input("E-mail do remetente", value="", placeholder="exemplo@provedor.com")

# Armazenar a senha na sessão
if "senha_remetente" not in st.session_state:
    st.session_state["senha_remetente"] = ""

senha_input = st.text_input("Senha do aplicativo", type="password", value=st.session_state["senha_remetente"])
if senha_input:
    st.session_state["senha_remetente"] = senha_input
SENHA_REMETENTE = st.session_state["senha_remetente"]

# Botão para limpar a senha da sessão
if st.button("🔓 Limpar senha da sessão"):
    st.session_state["senha_remetente"] = ""
    st.success("Senha removida da sessão.")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("📄 Escolha a planilha Excel", type=["xlsx"])

if uploaded_file:
    if not EMAIL_REMETENTE or not SENHA_REMETENTE:
        st.warning("⚠️ Informe o e-mail e a senha do remetente para continuar.")
    else:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.strip()
            st.success("✅ Planilha carregada com sucesso!")

            coluna_email = 'email'
            df_filtrado = df[df[coluna_email].notna()]
            df_filtrado = df_filtrado[df_filtrado[coluna_email].astype(str).str.strip() != '']
            df_filtrado = df_filtrado[df_filtrado[coluna_email].astype(str).str.contains('@')]

            emails_editados = []
            assuntos_editados = []
            corpos_editados = []

            st.subheader("📝 Verifique, edite e envie os e-mails:")

            for idx, row in df_filtrado.iterrows():
                email_original = row[coluna_email]
                texto = row.get('Texto', 'Informação não disponível')
                vencimento = row.get('Vencimento líquido')
                montante = row.get('Montante em moeda interna')

                vencimento_str = "Data não disponível" if pd.isna(vencimento) else pd.to_datetime(vencimento).strftime('%d/%m/%Y')
                try:
                    montante_formatado = f"{float(montante):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except:
                    montante_formatado = "Valor indisponível"

                assunto_default = "Cobrança aluguel Volvo"
                corpo_default = f"""
Prezados(as),

Meu nome é Murilo, e sou representante da Ecar Fleet.

Segue abaixo os dados para cobrança:

Chassi: {texto}
Valor: R$ {montante_formatado}
Vencimento: {vencimento_str}

Atenciosamente,
Murilo – Ecar Fleet
"""

                st.markdown(f"### Registro {idx + 1}")
                novo_email = st.text_input(f"E-mail para {texto}", value=email_original, key=f"email_{idx}")
                novo_assunto = st.text_input("Assunto do e-mail", value=assunto_default, key=f"assunto_{idx}")
                novo_corpo = st.text_area("Corpo do e-mail (texto simples)", value=corpo_default, height=200, key=f"corpo_{idx}")

                emails_editados.append(novo_email)
                assuntos_editados.append(novo_assunto)
                corpos_editados.append(novo_corpo)

            if st.button("✉️ Enviar e-mails"):
                for idx, row in df_filtrado.iterrows():
                    try:
                        email = emails_editados[idx]
                        assunto = assuntos_editados[idx]
                        corpo_texto = corpos_editados[idx].replace("\n", "<br>")

                        msg = EmailMessage()
                        msg['Subject'] = assunto
                        msg['From'] = EMAIL_REMETENTE
                        msg['To'] = email
                        msg.set_content("Este e-mail requer visualização em HTML.")
                        msg.add_alternative(f"<html><body>{corpo_texto}</body></html>", subtype='html')

                        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                            smtp.set_debuglevel(1)  # 🔍 Ativa debug SMTP (pode remover depois)
                            smtp.starttls()
                            smtp.login(EMAIL_REMETENTE, SENHA_REMETENTE)
                            smtp.send_message(msg)

                        st.write(f"✅ E-mail enviado para {email}")
                    except Exception as e:
                        st.error(f"❌ Erro com {email}: {e}")
                st.success("📨 Todos os e-mails foram enviados com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao processar o arquivo: {e}")
