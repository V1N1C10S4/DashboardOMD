import streamlit as st
from PIL import Image

# Carga de imágenes
image_map = Image.open("images/mapa_mexico.png")  # Imagen del mapa de México
image_combined = Image.open("images/candidatos.png")  # Imagen combinada de candidatos y boletas

# Título de la sección (independiente de las columnas)
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h2 style='color: #FAFAFA;'>La voz digital en las elecciones mexicanas 2024: Explorando patrones e influencia en X</h2>
    </div>
    """, unsafe_allow_html=True
)

# Control de tamaño de imágenes
st.sidebar.markdown("### Ajuste de tamaño de imágenes")
map_width = st.sidebar.slider("Ancho de la imagen del mapa (%)", min_value=10, max_value=100, value=50)
map_height = st.sidebar.slider("Alto de la imagen del mapa (%)", min_value=10, max_value=100, value=50)
combined_width = st.sidebar.slider("Ancho de la imagen combinada (%)", min_value=10, max_value=100, value=50)
combined_height = st.sidebar.slider("Alto de la imagen combinada (%)", min_value=10, max_value=100, value=50)

# Diseño en columnas
col1, col2 = st.columns([1.5, 2])  # Ajustar proporciones para reducir el ancho de la columna izquierda

with col1:
    # Introducción con salto de línea entre párrafos
    st.markdown(
        """
        <div style='text-align: left; padding-top: 20px;'>
            <p style='font-size: 1.1em; color: #FAFAFA; text-align: justify;'>
                En un año decisivo para México, las elecciones presidenciales de 2024 también han tenido un impacto monumental en el ecosistema digital, 
                particularmente en la plataforma X (anteriormente Twitter). Este proyecto de análisis de datos profundiza en las dinámicas de interacción 
                de la comunidad en X, desentrañando patrones, anomalías y comportamientos influyentes detrás de los posts relacionados con las elecciones.
            </p>
            <br>
            <p style='font-size: 1.1em; color: #FAFAFA; text-align: justify;'>
                En su esencia, este dashboard no solo se centra en las elecciones como evento, sino en cómo las voces individuales y colectivas moldean 
                la narrativa pública en un acontecimiento de tal magnitud. Al identificar anomalías y comportamientos inusuales, buscamos extraer insights 
                clave que permitan comprender mejor a la sociedad en procesos históricos como este, con el potencial de transformar cómo entendemos la 
                influencia digital y sus efectos en la democracia.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    # Imagen del mapa dentro de la columna izquierda con tamaño dinámico
    st.image(image_map, caption="Resultados electorales", width=int(map_width * 10), use_column_width=False)

with col2:
    # Imagen combinada en la columna derecha con tamaño dinámico
    st.image(image_combined, caption="Candidatos y boletas electorales", width=int(combined_width * 10), use_column_width=False)