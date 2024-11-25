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
introduccion = st.Page(
    "Background/intro.py",
    title="Introducción",
    icon=":material/help:",
)

datos_importantes = st.Page(
    "Background/facts.py",
    title="Datos importantes",
    icon=":material/help:",
)

eda = st.Page(
    "EDA/eda.py",
    title="EDA",
    icon=":material/person_add:",
)

clustering = st.Page(
    "Clustering/clustering.py",
    title="Clustering",
    icon=":material/person_add:",
)

sentiment_analysis = st.Page(
    "ml/ml_analysis.py",
    title="Análisis de sentimientos",
    icon=":material/healing:",
)

conclusiones = st.Page(
    "Background/conclusions.py",
    title="Conclusiones",
    icon=":material/help:",
)

sobre_nosotros = st.Page(
    "Background/about.py",
    title="Sobre nosotros",
    icon=":material/person_add:",
)

derechos_autor = st.Page(
    "Background/copyright.py",
    title="Derechos de autor",
    icon=":material/person_add:",
)

# Organización de las páginas por subsección
introduccion_pages = [introduccion, datos_importantes]
analisis_datos_pages = [eda, clustering, sentiment_analysis]
conclusiones_pages = [conclusiones]
quienes_somos_pages = [sobre_nosotros, derechos_autor]

# Logotipo con tamaño personalizado
st.logo("images/OMD2.png", icon_image="images/OMD2.png")

# Diccionario de navegación en español
page_dict = {
    "Introducción": introduccion_pages,
    "Análisis de datos": analisis_datos_pages,
    "Conclusiones": conclusiones_pages,
    "Quiénes somos": quienes_somos_pages,
}

# Configuración de navegación
pg = st.navigation(page_dict)
pg.run()