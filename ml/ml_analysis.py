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

# Configuración de Streamlit
st.title("Tendencia Promedio del Sentimiento por Semana")

# Calcular el sentimiento promedio por semana
# Asegúrate de que df tiene una columna datetime y sentiment antes de calcular esto
df['datetime'] = pd.to_datetime(df['datetime'])  # Asegurar formato datetime
df.set_index('datetime', inplace=True)
sentiment_by_week = df['sentiment'].resample('W').mean()  # Resample y cálculo

# Crear gráfica en Plotly
fig = go.Figure()

# Línea de sentimiento promedio
fig.add_trace(go.Scatter(
    x=sentiment_by_week.index,
    y=sentiment_by_week.values,
    mode='lines+markers',
    marker=dict(color='lightblue', size=6),
    line=dict(color='lightblue', width=2),
    name='Sentimiento Promedio'
))

# Configuración de diseño
fig.update_layout(
    title=dict(
        text="Tendencia Promedio del Sentimiento por Semana",
        font=dict(size=16, color='black', family='Arial'),
        x=0.5,  # Centrado
        xanchor='center'
    ),
    xaxis=dict(
        title='Mes',
        titlefont=dict(size=14, color='black'),
        tickformat='%b',  # Mes abreviado
        tickangle=45,
        tickfont=dict(size=10, color='gray')
    ),
    yaxis=dict(
        title='Sentimiento Promedio',
        titlefont=dict(size=14, color='black'),
        tickfont=dict(size=10, color='gray'),
        gridcolor='lightgray',
        gridwidth=0.5
    ),
    legend=dict(
        title='Leyenda',
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        font=dict(size=10)
    ),
    plot_bgcolor='white',
    margin=dict(l=20, r=20, t=50, b=20),
)

# Configuración de líneas de la cuadrícula (horizontal únicamente)
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=0.6, gridcolor='lightgray', zeroline=False)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)