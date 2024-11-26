import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
import plotly.express as px
import os
import gdown

st.title("Análisis de Sentimientos")

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

st.write("""
Se teorizó que un pequeño grupo de usuarios acapara la mayor parte de la influencia en la plataforma de redes sociales X (antes Twitter). Este fenómeno sugiere que estos usuarios pueden compartir características comunes, como rasgos demográficos, patrones de compromiso o afiliaciones políticas, que merece la pena explorar.
""")

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

def download_data():
    url = 'https://drive.google.com/uc?id=15xmlau62Th5Vl3MF9DpfY_9Xrl8-jU7L'
    output = 'Sentiment_1.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
df1 = pd.read_csv("Sentiment_1.csv")

def download_data():
    url = 'https://drive.google.com/uc?id=1-7uTVd08Wh1a-YziQIeOGRxydbjZAwSb'
    output = 'Sentiment_2.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
df2 = pd.read_csv("Sentiment_2.csv")

# Combinar los dos DataFrames
df = pd.concat([df1, df2], ignore_index=True)


# Asegurar que la columna 'datetime' está en formato datetime
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Agrupar por semana y calcular el promedio de sentimiento
sentiment_by_week = df.groupby(df['datetime'].dt.to_period('W'))['predicted_sentiment'].mean()

top_users_df = df[df['top_user_indicator'] == 1]

# Agrupar por sentimiento y sumar el número de interacciones
interaction_sum = top_users_df.groupby('predicted_sentiment')['num_interaction'].sum().reset_index()
print(interaction_sum)

# Remover duplicados y calcular el sentimiento promedio por usuario
unique_users_df = df.groupby('username').agg({
    'predicted_sentiment': 'mean',
    'top_user_indicator': 'first'  # Mantener la etiqueta de top_user_indicator por usuario
}).reset_index()

# Dividir datos entre top users y non-top users
top_users = unique_users_df[unique_users_df['top_user_indicator'] == 1]
non_top_users = unique_users_df[unique_users_df['top_user_indicator'] == 0]

# Calcular el sentimiento promedio de cada grupo
avg_sentiment_top_users = top_users['predicted_sentiment'].mean()
avg_sentiment_non_top_users = non_top_users['predicted_sentiment'].mean()

# Preparar datos para la gráfica
sentiment_comparison = pd.DataFrame({
    'User Type': ['Top Users', 'Non-Top Users'],
    'Average Sentiment': [avg_sentiment_top_users, avg_sentiment_non_top_users]
})

# Crear la gráfica de barras con Plotly
fig = go.Figure()

# Añadir las barras
fig.add_trace(go.Bar(
    x=["Usuarios Influyentes", "Usuarios Comunes"],  # Etiquetas de eje X actualizadas
    y=sentiment_comparison['Average Sentiment'],  # Eje Y: Sentimiento promedio
    marker_color=['#FFB400', '#4CC3D9'],  # Colores Vivid (amarillo y azul claro)
    textposition='none',  # Ocultar los valores dentro de las barras
    name='Sentimiento Promedio'  # Nombre de la traza
))

# Configuración del diseño
fig.update_layout(
    xaxis=dict(
        title='Tipo de Usuario',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white')
    ),
    yaxis=dict(
        title='Sentimiento',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        tickvals=[0, 1, 2],  # Valores específicos en el eje Y
        ticktext=['Negativo', 'Neutral', 'Positivo'],  # Etiquetas personalizadas para 0, 1 y 2
        showgrid=True,  # Mantener las líneas de cuadrícula
        gridwidth=0.5,
        gridcolor='gray'
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de todo el gráfico transparente
    showlegend=False  # Ocultar la leyenda
)

# Mostrar la gráfica en Streamlit
st.header("Comparación de Sentimiento Promedio Usuarios Influyentes vs Usuarios Comunes")
st.plotly_chart(fig, use_container_width=True)