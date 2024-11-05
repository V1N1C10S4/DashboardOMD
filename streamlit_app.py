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

# Configuración de las páginas
intro = st.Page(
    "Background/intro.py",
    title="Introduction",
    icon=":material/help:",
)

facts = st.Page(
    "Background/facts.py",
    title="Facts",
    icon=":material/help:",
)

visualization = st.Page(
    "Visualization/visualization.py",
    title="Interactive charts",
    icon=":material/help:",
)

ml = st.Page(
    "ml/ml_analysis.py",
    title="Sentiment analysis",
    icon=":material/healing:",
)

eda = st.Page(
    "EDA/eda.py",
    title="EDA",
    icon=":material/mag:",
)

about = st.Page(
    "Background/about.py",
    title="About Us",
    icon=":material/person_add:",
)

cr = st.Page(         
    "Background/example.py",
    title="Copyright",
    icon=":material/person_add:",
)

intro_pages = [intro, facts]
visualization_pages = [visualization]
ml_pages = [ml]
eda_pages = [eda]
about_pages = [about, cr]

# Logotipo con tamaño personalizado
st.logo("images/OMD2.png", icon_image="images/OMD2.png")

# Diccionario de navegación
page_dict = {
    "Introduction": intro_pages,
    "Data Analysis": eda_pages,
    "Visualization": visualization_pages,
    "Prediction": ml_pages,
    "About us": about_pages,
}

# Configuración de navegación
pg = st.navigation(page_dict)
pg.run()