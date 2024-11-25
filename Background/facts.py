import streamlit as st
from PIL import Image

# Cargar imagen
image = Image.open("images/mapa.webp")

# Configurar dos columnas
col1, col2 = st.columns([1, 2])

# Columna 1: Mostrar la imagen
with col1:
    st.image(image, use_column_width=True)

# Columna 2: Mostrar el texto formateado
with col2:
    st.markdown(
        """
        <h2 style='color: #4a4a4a;'>Datos importantes</h2>
        <h3 style='color: #6c757d;'>1. Conceptos clave de análisis</h3>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>EDA (Exploratory Data Analysis):</strong> 
            Es el proceso inicial en un análisis de datos que busca explorar, resumir y visualizar patrones, anomalías o relaciones en los datos sin hacer suposiciones previas. Es fundamental para descubrir insights clave y preparar los datos para análisis más avanzados.
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Clustering:</strong> 
            Es una técnica de aprendizaje no supervisado que agrupa datos en clusters o categorías basándose en similitudes. En este proyecto, se utiliza para identificar grupos de usuarios con patrones de interacción similares en redes sociales.
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Sentiment Analysis:</strong> 
            Método que clasifica textos según el tono emocional: positivo, negativo o neutro. En el análisis de elecciones, ayuda a identificar la percepción pública hacia los candidatos.
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Influence Factor:</strong> 
            Métrica que mide el impacto o nivel de influencia de un usuario en redes sociales, calculada a partir de interacciones como likes, retweets y comentarios. Usuarios con mayor factor de influencia suelen moldear la narrativa pública.
        </p>
        
        <h3 style='color: #6c757d;'>2. Descripción de candidatos y coaliciones</h3>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Claudia Sheinbaum (MORENA):</strong> Ex jefa de gobierno de la Ciudad de México, representa a la coalición de izquierda MORENA-PT-PVEM. Se enfoca en programas sociales y desarrollo sostenible.
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Xóchitl Gálvez (PAN-PRI-PRD):</strong> Ingeniera y empresaria, candidata de la coalición opositora de derecha-centro. Conocida por su discurso combativo y enfoque en infraestructura.
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            <strong>Jorge Álvarez Máynez (Movimiento Ciudadano):</strong> Representante del partido progresista, busca atraer votantes jóvenes y promover agendas de innovación y derechos civiles.
        </p>
        
        <h3 style='color: #6c757d;'>3. Contexto político y social</h3>
        <p style='font-size: 1.1em; color: #6c757d;'>
            México se encuentra en un momento crucial para su democracia. Las elecciones presidenciales de 2024 están marcadas por el impacto de las redes sociales, donde el 80% de los votantes activos interactúan con contenido político en plataformas como X, Facebook e Instagram. 
        </p>
        <p style='font-size: 1.1em; color: #6c757d;'>
            Históricamente, la participación electoral ha oscilado entre el 55% y el 63%, pero las campañas digitales han demostrado ser una herramienta poderosa para movilizar votantes, especialmente entre jóvenes de 18 a 29 años.
        </p>
        """,
        unsafe_allow_html=True
    )