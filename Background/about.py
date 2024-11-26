import streamlit as st

# Configurar la página "Sobre Nosotros"
st.markdown("""
<div style="background-color: white; padding: 20px; border-radius: 10px; text-align: center; width: 90%; margin: auto;">
    <h1 style='text-align: center; color: black;'>¿Quiénes somos?</h1>
    <p style="color: black; font-size: 18px; margin: 20px;">
        Somos un grupo de estudiantes interdisciplinario del Tecnológico de Monterrey trabajando juntos para aportar de nuestros conocimientos y descubrimientos al resto de la comunidad universitaria y principalmente a México.
    </p>
    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
        <div>
            <img src="images/Claudia_Sheinbaum.jpg" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Vinicio Santoyo Cuevas<br>ITD</p>
        </div>
        <div>
            <img src="images/Claudia_Sheinbaum.jpg" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Manuel Medina Juárez<br>ITD</p>
        </div>
        <div>
            <img src="images/Claudia_Sheinbaum.jpg" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Gabriel Josué Tabango Espinoza<br>ITD</p>
        </div>
    </div>
    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
        <div>
            <img src="images/Claudia_Sheinbaum.jpg" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Andrés Emiliano Martínez Fuentes<br>ITD</p>
        </div>
        <div>
            <img src="images/Claudia_Sheinbaum.jpg" style="border-radius: 50%; width: 150px;">
            <p style="color: black; font-size: 14px; font-weight: bold;">Luis Fernando González Cortés<br>ITD</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)