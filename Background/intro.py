import streamlit as st
from PIL import Image

# Load an image from local file
image = Image.open("images/votaciones2021.jpg")

# Display image with a caption
st.image(image, caption="Elecciones", use_column_width=True)

# Display formatted text below the image
st.markdown(
    """
    <div style='text-align: center; padding-top: 20px;'>
        <h2 style='color: #FAFAFA;'>Introducción</h2>
        <p style='font-size: 1.1em; color: #FAFAFA;'>
            En la escena política de México, la campaña para las elecciones presidenciales de 2024 está llena de estrategias que buscan influir en la percepción pública. Andrés Manuel López Obrador (AMLO), ex presidente de México, ha sido conocido por emplear tácticas que desvían la atención de las controversias y consolidan el apoyo a su partido, Morena. Esto ha dado pie a la hipótesis de que una cantidad limitada de usuarios en redes sociales desempeñará un rol desproporcionado en la actividad mediática, posiblemente porque algunos de ellos reciben incentivos para apoyar a la candidata de Morena, Claudia Sheinbaum. Esta narrativa de apoyo suele manifestarse desacreditando a sus oponentes y promoviendo a Sheinbaum. Al mismo tiempo, la oposición representada por Xóchitl Gálvez, se espera que lance su propia estrategia en redes, aunque con menos intensidad.
            Para explorar esta hipótesis, nos propusimos analizar la dinámica de publicaciones e interacciones en la red social X. Al observar el volumen de publicaciones y el nivel de interacción por usuario, buscamos detectar patrones de comportamiento que confirmen si, en efecto, un grupo específico de usuarios genera la mayor parte del contenido sobre las elecciones. Lo que encontramos es impresionante: hay usuarios tan activos que llegan a publicar hasta 250 veces al mes, acumulando más de medio millón de interacciones en un solo mes en esta plataforma.
            Para entender mejor estos patrones, agrupamos a los usuarios en tres categorías. En el primer grupo están quienes dominan el espacio digital, publican con frecuencia y reciben una gran cantidad de interacciones. En el segundo grupo se encuentran los usuarios que, aunque no publican tanto, logran captar la atención y acumulan interacciones importantes. Finalmente, en el tercer grupo se agrupan aquellos cuyos esfuerzos por publicar no logran generar casi ninguna reacción o bien, son usuarios muy casuales. Este análisis sugiere una fuerte correlación entre la frecuencia de publicación y el nivel de interacción.
            Además, estamos abordando un componente fundamental: el análisis del sentimiento. Entender la opinión pública en torno a los candidatos y temas de campaña nos permite ver cómo se ha transformado con el tiempo y, en última instancia, medir el pulso de la ciudadanía. Con este enfoque, buscamos no solo detectar patrones de actividad, sino también comprender el tono y la dirección de las conversaciones que están moldeando la política en México.

        </p>
    </div>
    """, unsafe_allow_html=True
)
