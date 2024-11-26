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
sentiment_df = pd.read_csv(url)

# Asegurarse de que la columna de sentimiento esté configurada
sentiment_column = 'predicted_sentiment'  # Ajustar si el nombre es diferente

sentiment_df['datetime'] = pd.to_datetime(sentiment_df['datetime'], errors='coerce')

# Agrupar por semanas en lugar de días
sentiment_df['datetime'] = pd.to_datetime(sentiment_df['datetime'], errors='coerce')
sentiment_by_week = sentiment_df.groupby(sentiment_df['datetime'].dt.to_period('W'))[sentiment_column].mean()
#Graficar
# Agrupar por semana y calcular el sentimiento promedio
sentiment_by_week = sentiment_df.groupby(sentiment_df['datetime'].dt.to_period('W'))['predicted_sentiment'].mean()

# Convertir PeriodIndex a datetime para mejor formato
sentiment_by_week.index = sentiment_by_week.index.to_timestamp()

# Calcular sentimiento promedio por semana
sentiment_df.set_index('datetime', inplace=True)
sentiment_by_week = sentiment_df['sentiment'].resample('W').mean()

# Crear la gráfica en Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sentiment_by_week.index,
    y=sentiment_by_week.values,
    mode='lines+markers',
    marker=dict(color='lightblue', size=6),
    line=dict(color='lightblue', width=2),
    name='Sentimiento Promedio'
))

fig.update_layout(
    title="Tendencia Promedio del Sentimiento por Semana",
    xaxis=dict(title="Mes", tickformat="%b"),
    yaxis=dict(title="Sentimiento Promedio"),
    template="simple_white",
    margin=dict(l=20, r=20, t=50, b=20),
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)