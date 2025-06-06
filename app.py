import streamlit as st

## BRK Ambiental
abastecimento_brk = st.Page(
    "brk/abastecimento_brk.py", title="Abastecimentos", icon=":material/directions_car:"
)
ociosidade_brk = st.Page("brk/ociosidade_brk.py", title="Ociosidade", icon=":material/schedule:")
eventos_brk = st.Page("brk/eventos_brk.py", title="Eventos", icon=":material/event:")

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
checklist = st.Page("alpitel/checklist.py", title="Checklist", icon=":material/schedule:")

# Navegação
pg = st.navigation(
    {
        "BRK": [abastecimento_brk, ociosidade_brk, eventos_brk],
        "Alpitel": [checklist],
        "Volvo": [alugueis, gerador_multas],
        "Suporte": [guia]
    }
)

pg.run()
