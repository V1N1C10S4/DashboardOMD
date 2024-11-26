import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
import plotly.express as px

st.title("Análisis de Sentimientos")

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

st.write("""
Se teorizó que un pequeño grupo de usuarios acapara la mayor parte de la influencia en la plataforma de redes sociales X (antes Twitter). Este fenómeno sugiere que estos usuarios pueden compartir características comunes, como rasgos demográficos, patrones de compromiso o afiliaciones políticas, que merece la pena explorar.
""")

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Cargar los datos
url = 'https://drive.google.com/uc?id=1VVkIC0Us3_llEEOyK_sJebCk0b_MZQ9F'
df = pd.read_csv(url, nrows=5000)  # Carga las primeras 5000 filas

# Mostrar los primeros elementos
st.write("Primeros 5 elementos del dataset:")
st.dataframe(df.head())