import streamlit as st
from PIL import Image

st.markdown("""
### Conclusiones

Este proyecto ha permitido explorar a profundidad cómo las interacciones digitales reflejan y amplifican los procesos democráticos en México. Al analizar el comportamiento de los usuarios en plataformas como X durante las elecciones presidenciales de 2024, se logró no solo identificar patrones clave de interacción, sino también destacar a los actores más influyentes y las anomalías que marcan la diferencia en el ecosistema digital.

El impacto de este estudio radica en su capacidad de desentrañar las dinámicas de una sociedad cada vez más interconectada. Los hallazgos presentados en este dashboard no solo ofrecen una visión innovadora sobre el poder de la narrativa pública en eventos históricos, sino que también abren la puerta a nuevas formas de entender cómo las redes sociales configuran la percepción colectiva y el debate democrático.

Más allá de los números, este análisis demuestra el potencial transformador de la analítica de datos en la toma de decisiones y en la promoción de la transparencia. Al estudiar patrones de comportamiento, identificar clusters de usuarios y explorar el sentimiento detrás de las interacciones más significativas, se pone de manifiesto cómo las herramientas digitales pueden usarse para potenciar la comprensión de los procesos sociales en el ámbito digital.

El conocimiento generado no solo nos invita a reflexionar sobre el presente, sino también a proyectar el futuro de la interacción digital en contextos de gran relevancia política. Este proyecto es un paso hacia la creación de soluciones más inclusivas y democráticas, donde el poder de la voz colectiva pueda ser comprendido, analizado y, en última instancia, mejor utilizado para construir una sociedad más equitativa.
""")

# Mostrar la imagen al final de la página
st.markdown("---")  # Línea divisoria opcional para separar el contenido de la imagen
st.image("images/Mexico.jpg", caption="México y su evolución digital", use_column_width=True)