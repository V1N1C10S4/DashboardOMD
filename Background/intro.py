import streamlit as st
from PIL import Image

# Carga de imágenes
image_map = Image.open("images/mapa_mexico.png")  # Imagen del mapa de México
image_combined = Image.open("images/candidatos.png")  # Imagen combinada de candidatos y boletas

# Diseño en columnas
col1, col2 = st.columns([2, 1])  # Ajustar proporciones para dar más espacio al texto

with col1:
    # Título e introducción
    st.markdown(
        """
        <div style='text-align: left; padding-top: 20px;'>
            <h2 style='color: #FAFAFA;'>La voz digital en las elecciones mexicanas 2024: Explorando patrones e influencia en X</h2>
            <p style='font-size: 1.1em; color: #FAFAFA; text-align: justify;'>
                En un año decisivo para México, las elecciones presidenciales de 2024 también han tenido un impacto monumental en el ecosistema digital, 
                particularmente en la plataforma X (anteriormente Twitter). Este proyecto de análisis de datos profundiza en las dinámicas de interacción 
                de la comunidad en X, desentrañando patrones, anomalías y comportamientos influyentes detrás de los posts relacionados con las elecciones.
                En su esencia, este dashboard no solo se centra en las elecciones como evento, sino en cómo las voces individuales y colectivas moldean 
                la narrativa pública en un acontecimiento de tal magnitud. Al identificar anomalías y comportamientos inusuales, buscamos extraer insights 
                clave que permitan comprender mejor a la sociedad en procesos históricos como este, con el potencial de transformar cómo entendemos la 
                influencia digital y sus efectos en la democracia.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

with col2:
    # Imagen al costado
    st.image(image_combined, caption="Candidatos y boletas electorales", use_column_width=True)

# Mapa de México (debajo del texto e imagen combinada)
st.image(image_map, caption="Resultados electorales", use_column_width=True)