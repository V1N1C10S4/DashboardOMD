import streamlit as st

# CSS para ajustar el tamaño del logo
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] img {
        width: 150px; /* Ajusta este tamaño según lo que necesites */
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logotipo con tamaño personalizado
st.image("images/OMD2.png")

# Configuración de las páginas
PAGES = {
    "Introduction": "Background/intro.py",
    "Facts": "Background/facts.py",
    "Interactive charts": "Visualization/visualization.py",
    "Sentiment analysis": "ml/ml_analysis.py",
    "Statistics": "EDA/eda.py",
    "About Us": "Background/about.py",
    "Copyright": "Background/example.py"
}

# Selector de página en la barra lateral
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Cargar el contenido de la página seleccionada
page = PAGES[selection]

with open(page, "r") as f:
    code = f.read()
    exec(code)