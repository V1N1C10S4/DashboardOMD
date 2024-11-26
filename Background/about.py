import streamlit as st
import base64

# Función para convertir imágenes a base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Configuración del cuadro negro con texto
st.markdown("""
<div style="background-color: Lavender; padding: 20px; border-radius: 10px; text-align: center; width: 90%; margin: auto;">
    <div style="background-color: black; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style='text-align: center; color: white;'>¿Quiénes somos?</h1>
        <p style="color: white; font-size: 18px; margin: 20px;">
            Somos un grupo de estudiantes interdisciplinario del Tecnológico de Monterrey trabajando juntos para aportar de nuestros conocimientos y descubrimientos al resto de la comunidad universitaria y principalmente a México.
        </p>
    </div>
    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
        <div>
            <img src="data:image/png;base64,{}" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Vinicio Santoyo Cuevas<br>ITD</p>
        </div>
        <div>
            <img src="data:image/png;base64,{}" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Manuel Medina Juárez<br>LAF</p>
        </div>
        <div>
            <img src="data:image/png;base64,{}" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Gabriel Josué Tabango Espinoza<br>LEM</p>
        </div>
    </div>
    <div style="display: flex; justify-content: space-evenly; margin-top: 0px;"> <!-- Espacio reducido entre filas -->
        <div>
            <img src="data:image/png;base64,{}" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Andrés Emiliano Martínez Fuentes<br>IIS</p>
        </div>
        <div>
            <img src="data:image/png;base64,{}" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Luis Fernando González Cortés<br>IMD</p>
        </div>
    </div>
</div>
""".format(
    get_base64_image("images/Vinicio_Santoyo.jpg"),
    get_base64_image("images/Manuel_Medina.jpg"),
    get_base64_image("images/Gabriel_Tabango.jpg"),
    get_base64_image("images/Andres_Martinez.jpg"),
    get_base64_image("images/Luis_Fernando.png")
), unsafe_allow_html=True)