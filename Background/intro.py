import streamlit as st
from PIL import Image

# Load images
image_flag = Image.open("images/bandera_mexico.jpg")  # Imagen de la bandera mexicana
image_combined = Image.open("images/candidatos_votaciones.png")  # Imagen combinada de candidatos y boletas

# Main title and text
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
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

# Layout for images
col1, col2 = st.columns(2)

with col1:
    st.image(image_flag, caption="Elecciones", use_column_width=True)

with col2:
    st.image(image_combined, caption="Candidatos y boletas electorales", use_column_width=True)