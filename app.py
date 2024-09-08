import streamlit as st

## BRK Ambiental

# Páginas de navegação para BRK Ambiental

abastecimento_brk = st.Page(
    "brk/abastecimento_brk.py", title="Abastecimento BRK", icon=":material/directions_car:", default=True
)
ociosidade_brk = st.Page("brk/ociosidade_brk.py", title="Ociosidade BRK", icon=":material/schedule:")
eventos_brk = st.Page(
    "brk/eventos_brk.py", title="Eventos BRK", icon=":material/event:"
)

## Atlas Copco

# Páginas de navegação para Atlas Copco
abastecimento_atlas = st.Page(
    "atlas/abastecimento_atlas.py", title="Abastecimento Atlas", icon=":material/directions_car:"
)

ociosidade_atlas = st.Page("atlas/ociosidade_atlas.py", title="Ociosidade Atlas", icon=":material/schedule:")
eventos_atlas = st.Page(
    "atlas/eventos_atlas.py", title="Eventos Atlas", icon=":material/event:"
)

consolidador = st.Page("ferramentas/consolidador.py", title="Consolidador EXCEL", icon=":material/archive:")

comparador = st.Page("ferramentas/comparador.py", title="Comparador Coluna", icon=":material/archive:")

# Navegação
pg = st.navigation(
    {
        "BRK": [abastecimento_brk, ociosidade_brk, eventos_brk],
        "Atlas": [abastecimento_atlas, ociosidade_atlas, eventos_atlas],
        "Ferramentas": [consolidador, comparador]
    }
)

pg.run()
