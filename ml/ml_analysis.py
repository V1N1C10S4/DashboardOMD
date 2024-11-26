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

uploaded_file = st.file_uploader("Sube tu archivo CSV")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
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
        title='Mes',
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

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

top_users_df = df[df['top_user_indicator'] == 1]

# Agrupar por sentimiento y sumar el número de interacciones
interaction_sum = top_users_df.groupby('predicted_sentiment')['num_interaction'].sum().reset_index()
print(interaction_sum)

# Crear la gráfica de barras
fig = go.Figure()

# Colores asignados
bar_colors = ['red', 'gray', 'green']

# Añadir las barras a la gráfica
fig.add_trace(go.Bar(
    x=interaction_sum['predicted_sentiment'],  # Eje X: Valores de sentimiento
    y=interaction_sum['num_interaction'],  # Eje Y: Total de interacciones
    marker_color=bar_colors,  # Colores personalizados
    name='Interacciones'
))

# Configurar el diseño de la gráfica
fig.update_layout(
    title={
        'text': 'Total de Interacciones por Valor de Sentimiento para Usuarios Destacados',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 18, 'color': 'black'}
    },
    xaxis=dict(
        title='Valor de Sentimiento',
        tickvals=[0, 1, 2],  # Valores en el eje X
        ticktext=['0', '1', '2'],  # Etiquetas en el eje X
        title_font=dict(size=14, color='black'),
        tickfont=dict(size=12, color='gray')
    ),
    yaxis=dict(
        title='Número Total de Interacciones',
        tickvals=[10_000_000, 20_000_000, 30_000_000, 40_000_000, 50_000_000],  # Valores en millones
        ticktext=['10M', '20M', '30M', '40M', '50M'],  # Etiquetas con sufijo 'M'
        range=[10_000_000, 50_000_000],  # Rango del eje Y
        title_font=dict(size=14, color='black'),
        tickfont=dict(size=12, color='gray'),
        gridcolor='lightgray',
        gridwidth=0.5
    ),
    template='simple_white',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    showlegend=False  # Ocultar leyenda
)

# Insertar logo en la esquina superior derecha
fig.add_layout_image(
    dict(
        x=1.1,
        y=1.15,
        xref="paper",
        yref="paper",
        sizex=0.15,
        sizey=0.15,
        xanchor="right",
        yanchor="top"
    )
)

# Mostrar la gráfica en Streamlit
import streamlit as st
st.plotly_chart(fig, use_container_width=True)