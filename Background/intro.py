import streamlit as st
from PIL import Image

# Carga de imágenes
image_map = Image.open("images/mapa_mexico.png")  # Imagen del mapa de México
image_combined = Image.open("images/candidatos.png")  # Imagen combinada de candidatos y boletas

# Configuración de tamaños de imágenes (manual)
map_width = 500  # Ancho en píxeles para la imagen del mapa
map_height = 300  # Alto en píxeles (si deseas redimensionar proporcionalmente, este valor no es necesario)
combined_width = 400  # Ancho en píxeles para la imagen combinada
combined_height = 600  # Alto en píxeles (opcional)

# Título de la sección (independiente de las columnas)
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h2 style='color: #FAFAFA;'>La voz digital en las elecciones mexicanas 2024: Explorando patrones e influencia en X</h2>
    </div>
    """, unsafe_allow_html=True
)

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
    # Imagen del mapa dentro de la columna izquierda con tamaño configurado manualmente
    st.image(image_map, caption="Resultados electorales", width=map_width)

with col2:
    # Imagen combinada en la columna derecha con tamaño configurado manualmente
    st.image(image_combined, caption="Candidatos y boletas electorales", width=combined_width)