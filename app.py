import streamlit as st

## BRK Ambiental
checklist = st.Page(
    "bracell/checklist.py", title="entrada/saída", icon=":material/directions_car:"
)

## suporte
guia = st.Page(
    "suporte/guia.py", title="Guia de ajuda", icon=":material/directions_car:"
)

## Volvo
alugueis = st.Page(
    "volvo/alugueis.py", title="Alugueis", icon=":material/directions_car:", default=True
)

gerador_multas = st.Page("volvo/gerador_multas.py", title="Multas", icon=":material/schedule:")

## Alpitel
velocidade = st.Page("amanco/velocidade.py", title="Velocidade", icon=":material/schedule:")

# Navegação
pg = st.navigation(
    {
        "Bracell": [checklist],
        "Amanco": [velocidade],
        "Volvo": [alugueis, gerador_multas],
        "Suporte": [guia]
    }
)

pg.run()
