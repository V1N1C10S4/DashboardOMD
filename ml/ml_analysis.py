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
        titlefont=dict(size=16, color='white'),
        tickfont=dict(size=14, color='white')
    ),
    yaxis=dict(
        title='Sentimiento',
        titlefont=dict(size=16, color='white'),
        tickfont=dict(size=14, color='white'),
        tickvals=[0, 1, 2],  # Valores específicos en el eje Y
        ticktext=['Negativo', 'Neutral', 'Positivo'],  # Etiquetas personalizadas para 0, 1 y 2
        range=[0, 2],
        showgrid=False,  # Mantener las líneas de cuadrícula
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

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Separate data into top users and non-top users
top_users_df = df[df['top_user_indicator'] == 1]
non_top_users_df = df[df['top_user_indicator'] == 0]

# Group data by week for both groups and calculate average sentiment
top_users_sentiment = top_users_df.groupby(top_users_df['datetime'].dt.to_period('W'))['predicted_sentiment'].mean().reset_index()
non_top_users_sentiment = non_top_users_df.groupby(non_top_users_df['datetime'].dt.to_period('W'))['predicted_sentiment'].mean().reset_index()

# Convert PeriodIndex to datetime for better plotting
top_users_sentiment['datetime'] = top_users_sentiment['datetime'].dt.to_timestamp()
non_top_users_sentiment['datetime'] = non_top_users_sentiment['datetime'].dt.to_timestamp()

# Crear la gráfica de líneas con Plotly
fig = go.Figure()

# Añadir la línea para usuarios influyentes (top users)
fig.add_trace(go.Scatter(
    x=top_users_sentiment['datetime'],
    y=top_users_sentiment['predicted_sentiment'],
    mode='lines+markers',
    line=dict(color='#FFB400', width=2),  # Color Vivid (amarillo)
    marker=dict(size=6),
    name='Usuarios Influyentes'
))

# Añadir la línea para usuarios comunes (non-top users)
fig.add_trace(go.Scatter(
    x=non_top_users_sentiment['datetime'],
    y=non_top_users_sentiment['predicted_sentiment'],
    mode='lines+markers',
    line=dict(color='#4CC3D9', width=2, dash='dash'),  # Color Vivid (azul claro) con línea discontinua
    marker=dict(size=6),
    name='Usuarios Comunes'
))

# Configuración del diseño
fig.update_layout(
    title={
        'text': 'Tendencia del Sentimiento a lo Largo del Tiempo: Usuarios Influyentes vs Usuarios Comunes',
        'x': 0.5,  # Centrar el título
        'xanchor': 'center',
        'font': {'size': 18, 'color': 'white'}
    },
    xaxis=dict(
        title='Mes',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        tickformat='%b',  # Mostrar los meses abreviados
        showgrid=False
    ),
    yaxis=dict(
        title='Sentimiento Promedio',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        showgrid=True,
        gridcolor='gray',
        gridwidth=0.5
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de toda la gráfica transparente
    legend=dict(
        title='Tipo de Usuario',
        font=dict(size=12, color='white'),
        bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente para la leyenda
        bordercolor='gray',
        borderwidth=0.5
    )
)

# Mostrar la gráfica en Streamlit
st.header("Tendencia del Sentimiento por Usuarios Influyentes y Comunes")
st.plotly_chart(fig, use_container_width=True)

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Remover duplicados y calcular el sentimiento promedio por usuario
unique_users_df = df.groupby('username').agg({
    'predicted_sentiment': 'mean',
    'cluster': 'first'  # Mantener el cluster asignado por usuario
}).reset_index()

# Calcular el sentimiento promedio por cluster
sentiment_by_cluster = unique_users_df.groupby('cluster')['predicted_sentiment'].mean().reset_index()

# Crear la gráfica de barras con Plotly
fig = go.Figure()

# Añadir las barras para cada cluster
fig.add_trace(go.Bar(
    x=sentiment_by_cluster['cluster'].astype(str),  # Clusters tratados como categorías
    y=sentiment_by_cluster['predicted_sentiment'],  # Sentimiento promedio
    marker_color=['#FFB400', '#4CC3D9', '#7E57C2'],  # Colores Vivid (amarillo, azul claro, púrpura)
    text=sentiment_by_cluster['predicted_sentiment'],  # Etiquetas de valores
    textposition='auto',  # Mostrar etiquetas automáticamente
    name='Sentimiento Promedio'  # Nombre de la traza
))

# Configuración del diseño
fig.update_layout(
    title={
        'text': 'Sentimiento Promedio por Cluster',
        'x': 0.5,  # Centrar el título
        'xanchor': 'center',
        'font': {'size': 18, 'color': 'white'}
    },
    xaxis=dict(
        title='Cluster',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white')
    ),
    yaxis=dict(
        title='Sentimiento Promedio',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        range=[min(sentiment_by_cluster['predicted_sentiment']) - 0.1, 
               max(sentiment_by_cluster['predicted_sentiment']) + 0.1],
        showgrid=True,
        gridcolor='gray',
        gridwidth=0.5
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente para toda la gráfica
    showlegend=False  # Ocultar la leyenda
)

# Mostrar la gráfica en Streamlit
st.header("Sentimiento Promedio por Cluster")
st.plotly_chart(fig, use_container_width=True)

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Group data by week and cluster, calculating average sentiment for unique users
cluster_sentiment_unique = df.groupby([
    df['datetime'].dt.to_period('W'),
    df['cluster']
])['predicted_sentiment'].mean().reset_index()

# Convert PeriodIndex to datetime for better plotting
cluster_sentiment_unique['datetime'] = cluster_sentiment_unique['datetime'].dt.to_timestamp()

# Separate data for each cluster
cluster_0_unique = cluster_sentiment_unique[cluster_sentiment_unique['cluster'] == 0]
cluster_1_unique = cluster_sentiment_unique[cluster_sentiment_unique['cluster'] == 1]
cluster_2_unique = cluster_sentiment_unique[cluster_sentiment_unique['cluster'] == 2]

# Crear la gráfica de líneas con Plotly
fig = go.Figure()

# Añadir la línea para el Cluster 0
fig.add_trace(go.Scatter(
    x=cluster_0_unique['datetime'],
    y=cluster_0_unique['predicted_sentiment'],
    mode='lines+markers',
    line=dict(color='#7E57C2', width=2),  # Color Vivid (púrpura)
    marker=dict(size=6),
    name='Cluster 0'
))

# Añadir la línea para el Cluster 1
fig.add_trace(go.Scatter(
    x=cluster_1_unique['datetime'],
    y=cluster_1_unique['predicted_sentiment'],
    mode='lines+markers',
    line=dict(color='#00BFFF', width=2, dash='dash'),  # Color Vivid (azul cielo) con línea discontinua
    marker=dict(size=6),
    name='Cluster 1'
))

# Añadir la línea para el Cluster 2
fig.add_trace(go.Scatter(
    x=cluster_2_unique['datetime'],
    y=cluster_2_unique['predicted_sentiment'],
    mode='lines+markers',
    line=dict(color='#FFB400', width=2, dash='dot'),  # Color Vivid (amarillo) con línea de puntos
    marker=dict(size=6),
    name='Cluster 2'
))

# Configuración del diseño
fig.update_layout(
    title={
        'text': 'Tendencia del Sentimiento por Tiempo y Cluster (Usuarios Únicos)',
        'x': 0.5,  # Centrar el título
        'xanchor': 'center',
        'font': {'size': 18, 'color': 'white'}
    },
    xaxis=dict(
        title='Mes',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        tickformat='%b',  # Mostrar los meses abreviados
        showgrid=False
    ),
    yaxis=dict(
        title='Sentimiento Promedio',
        titlefont=dict(size=14, color='white'),
        tickfont=dict(size=12, color='white'),
        showgrid=True,
        gridcolor='gray',
        gridwidth=0.5
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo de toda la gráfica transparente
    legend=dict(
        title='Clusters',
        font=dict(size=12, color='white'),
        bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente para la leyenda
        bordercolor='gray',
        borderwidth=0.5
    )
)

# Mostrar la gráfica en Streamlit
st.header("Tendencia del Sentimiento por Cluster y Tiempo (Usuarios Únicos)")
st.plotly_chart(fig, use_container_width=True)
