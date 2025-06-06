import streamlit as st

guia_gerar_senha = """
<style>
ul, ol {
    margin-left: 20px;
}
.guia-box {
    background-color: #f0f8ff;
    border-left: 6px solid #1e90ff;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-family: sans-serif;
}
.guia-box-outlook {
    background-color: #f3faff;
    border-left: 6px solid #0078d4;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    font-family: sans-serif;
}
.pass-box {
    background-color: #fff7e6;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: monospace;
    font-size: 16px;
    margin: 12px 0;
    display: inline-block;
}
</style>
"""

guia_gmail = """
<div class="guia-box">
<h2>🔐 Guia Prático: Como gerar uma <em>Senha de Aplicativo</em> no Gmail</h2>

<p>Para que este app possa enviar e-mails usando sua conta do <strong>Gmail</strong>, você precisa gerar uma <strong>senha de aplicativo</strong>. Ela é diferente da sua senha normal!</p>

<h4>✅ Passo a passo:</h4>
<ol>
    <li>👉 Acesse: <a href="https://myaccount.google.com/security" target="_blank">https://myaccount.google.com/security</a></li>
    <li>🔒 Ative a <strong>verificação em duas etapas</strong>, caso ainda não esteja ativada.</li>
    <li>🔑 Depois, entre em: <a href="https://myaccount.google.com/apppasswords" target="_blank">https://myaccount.google.com/apppasswords</a></li>
    <li>📋 Em "<strong>Selecionar aplicativo</strong>", escolha <em>Outro (nome personalizado)</em> e digite:
        <div class="pass-box">Streamlit Email</div>
    </li>
    <li>⚡ Clique em <strong>Gerar</strong>. Copie a senha gerada (blocos de 4 caracteres).</li>
    <li>✍️ Cole essa senha no campo <strong>Senha do aplicativo</strong> aqui no app.</li>
</ol>

<h4>💡 Dicas:</h4>
<ul>
    <li>Você verá a senha de aplicativo <strong>somente uma vez</strong>.</li>
    <li>Ela é segura e exclusiva para este tipo de envio via app.</li>
    <li>Se trocar de dispositivo ou app, será necessário gerar outra.</li>
</ul>
<div><h2>❓ Como fazer o envio dos <em>contratos de Alugueis</em> - Volvo no Gmail?</h2></div>

<h4>✅ Passo a passo:</h4>
<ol>
    <li>🛡️ Selecione o provedor de e-mail para o envio: <strong>Gmail ou outlook</strong></li>
    <li>📧 Agora em credenciais do remetente, informe o <strong>e-mail do remetente </strong></li>
    <li>🔑 Informe a senha do aplicativo. Caso de dúvidas, orientações no 
        <a href="http://localhost:8501/guia"><strong>guia prático</strong></a>
    </li>
    <li>🧾 Faça o upload do arquivo Excel</li>
    <li>✏️ Caso queira, você poderá editar e-mail, assunto do e-mail e o corpo do e-mail (texto simples)</li>
    <li>🎉 Agora, só enviar os e-mails e verificar no seu gmail o envio.</li>
</ol>

</div>
"""

guia_outlook = """
<div class="guia-box-outlook">
<h2>🔐 Guia Prático: Como gerar uma <em>Senha de Aplicativo</em> no Outlook</h2>

<p>Para que o app envie e-mails usando sua conta do <strong>Outlook / Hotmail / Office 365</strong>, siga estas instruções:</p>

<h4>✅ Passo a passo:</h4>
<ol>
    <li>🛡️ Acesse: <a href="https://security.microsoft.com/" target="_blank">https://security.microsoft.com/</a></li>
    <li>📲 Ative a <strong>verificação em duas etapas</strong> se ainda não estiver ativada: <br>
        <a href="https://account.microsoft.com/security" target="_blank">https://account.microsoft.com/security</a></li>
    <li>🔑 Depois, vá até: <a href="https://account.live.com/proofs/AppPassword" target="_blank">https://account.live.com/proofs/AppPassword</a></li>
    <li>🧾 Clique em <strong>Criar uma nova senha de aplicativo</strong>.</li>
    <li>📋 Copie a senha gerada e cole aqui no app no campo:
        <div class="pass-box">Senha do aplicativo</div>
    </li>
</ol>

<h4>💡 Importante:</h4>
<ul>
    <li>Você verá a senha gerada <strong>somente uma vez</strong>. Guarde temporariamente.</li>
    <li>Essa senha substitui sua senha tradicional quando usada por apps externos.</li>
    <li>Se trocar de dispositivo ou app, será necessário gerar outra.</li>
</ul>

<div><h2>❓ Como fazer o envio dos <em>contratos de Alugueis</em> - Volvo no Outlook?</h2></div>

<h4>✅ Passo a passo:</h4>
<ol>
    <li>🛡️ Selecione o provedor de e-mail para o envio: <strong>Gmail ou Outlook</strong></li>
    <li>📧 Agora em credenciais do remetente, informe o <strong>e-mail do remetente</strong></li>
    <li>🔑 Informe a senha do aplicativo. Caso de dúvidas, orientações no 
        <a href="http://localhost:8501/guia"><strong>guia prático</strong></a>
    </li>
    <li>🧾 Faça o upload do arquivo Excel</li>
    <li>✏️ Caso queira, você poderá editar e-mail, assunto do e-mail e o corpo do e-mail (texto simples)</li>
    <li>🎉 Agora, só enviar os e-mails e verificar no seu Outlook o envio.</li>
</ol>

</div>
"""

# Mostra o guia conforme o provedor selecionado
provedor = st.selectbox("Selecione o provedor de e-mail para ver o guia", ["Gmail", "Outlook"])

st.markdown(guia_gerar_senha, unsafe_allow_html=True)

if provedor == "Gmail":
    st.markdown(guia_gmail, unsafe_allow_html=True)
else:
    st.markdown(guia_outlook, unsafe_allow_html=True)

# --- Fim do conteúdo principal ---

# --- Bloco adicional com informações do repositório ---
st.markdown("""
---  
# Automação em Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Este repositório contém diversos scripts de automação desenvolvidos em Python para facilitar tarefas repetitivas e melhorar a eficiência do trabalho diário.

## Índice

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Sobre

Este projeto tem como objetivo fornecer uma coleção de scripts Python que automatizam tarefas comuns, como manipulação de arquivos, extração de dados, envio de emails, entre outros.

## Instalação

Para utilizar os scripts deste repositório, siga os passos abaixo:

1. Clone este repositório:
    ```sh
    git clone https://github.com/usuario/repositorio-de-automacao.git
    ```

2. Navegue até o diretório do projeto:
    ```sh
    cd repositorio-de-automacao
    ```

3. Crie um ambiente virtual e instale as dependências:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # No Windows use `venv\\Scripts\\activate`
    pip install -r requirements.txt
    ```

## Uso

Cada script possui uma funcionalidade específica. Para executar um script, basta navegar até o diretório correspondente e rodar o arquivo Python desejado:

```sh
python script_exemplo.py
""")