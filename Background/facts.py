import streamlit as st
from PIL import Image

# Título principal fuera de las columnas
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h2 style='color: white;'>Datos importantes</h2>
    </div>
    """, unsafe_allow_html=True
)

# Espacio entre el título y las columnas
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Configurar dos columnas con espacio entre ellas
col1, _, col2 = st.columns([1, 0.2, 2])  # Añadir un espacio vacío entre las columnas

# Columna 1: Insertar tres imágenes con pies de imagen y espaciado vertical
with col1:
    # Primera imagen
    image1 = Image.open("images/Claudia_Sheinbaum.jpg")
    st.image(image1, use_column_width=True)
    st.markdown("<p style='text-align: center; color: white;'>Claudia Sheinbaum</p>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)  # Espacio vertical

    # Segunda imagen
    image2 = Image.open("images/Xochitl_Galvez.jpg")
    st.image(image2, use_column_width=True)
    st.markdown("<p style='text-align: center; color: white;'>Xóchitl Gálvez</p>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)  # Espacio vertical

    # Tercera imagen
    image3 = Image.open("images/Jorge_Alvarez_Maynez.jpg")
    st.image(image3, use_column_width=True)
    st.markdown("<p style='text-align: center; color: white;'>Jorge Álvarez Máynez</p>", unsafe_allow_html=True)

# Columna 2: Mostrar el texto formateado con espaciado ajustado
with col2:
    st.markdown(
        """
        <h3 style='color: white;'>1. Conceptos clave de análisis</h3>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>EDA (Exploratory Data Analysis):</strong> 
            Es el proceso inicial en un análisis de datos que busca explorar, resumir y visualizar patrones, anomalías o relaciones en los datos sin hacer suposiciones previas. Es fundamental para descubrir insights clave y preparar los datos para análisis más avanzados.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Clustering:</strong> 
            Es una técnica de aprendizaje no supervisado que agrupa datos en clusters o categorías basándose en similitudes. En este proyecto, se utiliza para identificar grupos de usuarios con patrones de interacción similares en redes sociales.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Sentiment Analysis:</strong> 
            Método que clasifica textos según el tono emocional: positivo, negativo o neutro. En el análisis de elecciones, ayuda a identificar la percepción pública hacia los candidatos.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Influence Factor:</strong> 
            Métrica clave que describe la contribución del usuario al número total de publicaciones, su contribución al total de interacciones y su tasa de compromiso (calcula la relación entre interacciones y publicaciones).
        </p>
        <br><br>

        <h3 style='color: white;'>2. Descripción de candidatos y coaliciones</h3>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Claudia Sheinbaum (MORENA):</strong> Ex jefa de gobierno de la Ciudad de México, representa a la coalición de izquierda MORENA-PT-PVEM. Se enfoca en programas sociales y desarrollo sostenible.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Xóchitl Gálvez (PAN-PRI-PRD):</strong> Ingeniera y empresaria, candidata de la coalición opositora de derecha-centro Fuerza y Corazón por México. Conocida por su discurso combativo y enfoque en infraestructura.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            <strong>Jorge Álvarez Máynez (Movimiento Ciudadano):</strong> Representante del partido progresista, busca atraer votantes jóvenes y promover agendas de innovación y derechos civiles.
        </p>
        <br><br>

        <h3 style='color: white;'>3. Contexto político y social</h3>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            México se encuentra en un momento crucial para su democracia. Las elecciones presidenciales de 2024 están marcadas por el impacto de las redes sociales, donde el 80% de los votantes activos interactúan con contenido político en plataformas como X, Facebook e Instagram. 
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            Históricamente, la participación electoral ha oscilado entre el 55% y el 63%, pero las campañas digitales han demostrado ser una herramienta poderosa para movilizar votantes, especialmente entre jóvenes de 18 a 29 años.
        </p>
        <p style='font-size: 1.1em; color: white; line-height: 1.8;'>
            Es por esto que las elecciones presidenciales de 2024 son un parteaguas en la historia democrática de México, con un escenario digital como protagonista central, tanto para los candidatos como para los votantes. Estas elecciones no solo decidieron quién liderará al país, sino también cómo evolucionará la democracia en la era de la información.
        </p>
        """,
        unsafe_allow_html=True
    )