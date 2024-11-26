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

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Crear el gráfico de violín con Plotly
fig = px.violin(
    df,
    y='predicted_sentiment',
    box=True,  # Incluir un boxplot dentro del gráfico de violín
    points="all",  # Mostrar todos los puntos
    color_discrete_sequence=['lightcoral']  # Color personalizado
)

# Configurar el diseño de la gráfica
fig.update_layout(
    title={
        'text': 'Distribución General del Sentimiento (Violin Plot)',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 18, 'color': 'black'}
    },
    yaxis=dict(
        title='Valor de Sentimiento',
        tickvals=[0, 1, 2],  # Mostrar solo los valores 0, 1, 2
        ticktext=['0', '1', '2'],  # Etiquetas personalizadas
        title_font=dict(size=14, color='black'),
        tickfont=dict(size=12, color='gray')
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',  # Color tenue para la cuadrícula
        gridwidth=0.5,
        zeroline=False  # Eliminar la línea cero del eje X
    ),
    template='simple_white',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    height=500,  # Altura personalizada
    showlegend=False  # Ocultar leyenda
)

# Agregar un logotipo en la esquina superior derecha
fig.add_layout_image(
    dict(
        x=1.1,
        y=1.1,
        xref="paper",
        yref="paper",
        sizex=0.15,
        sizey=0.15,
        xanchor="right",
        yanchor="top"
    )
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)

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

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

