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
df = pd.read_csv(url)

# Mostrar los primeros 5 elementos del dataset
st.write("Primeros 5 elementos del dataset:")
st.dataframe(df.head())

# Asegurar que la columna 'datetime' está en formato datetime
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Agrupar por semana y calcular el promedio de sentimiento
sentiment_by_week = df.groupby(df['datetime'].dt.to_period('W'))['predicted_sentiment'].mean()

# Convertir el PeriodIndex a datetime para una mejor visualización en el eje X
sentiment_by_week.index = sentiment_by_week.index.to_timestamp()

# Crear la gráfica con Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sentiment_by_week.index,
    y=sentiment_by_week,
    mode='lines+markers',
    line=dict(color='lightblue', width=2),
    marker=dict(size=8),
    name='Promedio de Sentimiento'
))

# Configurar diseño de la gráfica
fig.update_layout(
    title='Tendencia del Sentimiento Promedio por Semana',
    xaxis=dict(
        title='Semana',
        titlefont=dict(size=14, weight='bold'),
        tickformat='%b %d',  # Mostrar el mes abreviado y el día
        tickangle=45,
        showgrid=True
    ),
    yaxis=dict(
        title='Sentimiento Promedio',
        titlefont=dict(size=14, weight='bold'),
        showgrid=True
    ),
    template='plotly_dark',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
    )
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)