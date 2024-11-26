import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
import plotly.express as px

# Cargar los datos
url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
df = pd.read_csv(url)

# Paso 1: Cálculo del número de posts por usuario
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').sort_values(by='url', ascending=False).reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

# Paso 2: Cálculo de las interacciones totales por usuario
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').sort_values(by='num_interaction', ascending=False).reset_index()
temp.rename(columns={'num_interaction': 'num_interaction'}, inplace=True)

# Paso 3: Unir los conteos de publicaciones e interacciones
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Paso 4: Cálculo de métricas derivadas
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts']
posts_df['%_posts'] = posts_df['num_posts'] / posts_df['num_posts'].sum() * 100
posts_df['%_interaction'] = posts_df['num_interaction'] / posts_df['num_interaction'].sum() * 100

# Paso 5: Calcular `influence_factor` y eliminar valores inválidos
posts_df['influence_factor'] = np.log((posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']) * 100)
posts_df = posts_df.replace([np.inf, -np.inf], np.nan).dropna(subset=['influence_factor'])  # Eliminar valores problemáticos

# Paso 6: Generar estimación de densidad usando KDE
influence_factor = posts_df['influence_factor']
kde = gaussian_kde(influence_factor)
x_range = np.linspace(influence_factor.min() - 5, influence_factor.max() + 5, 500)
density = kde(x_range)

# Paso 7: Crear la gráfica de densidad con Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_range,
    y=density,
    mode='lines',
    line=dict(color='dodgerblue', width=4),
    name='Density'
))

# Añadir la línea punteada para el threshold en -3.1165083206837174
fig.add_trace(go.Scatter(
    x=[-3.1165083206837174, -3.1165083206837174],
    y=[0, max(density)],
    mode='lines',
    line=dict(color='darkred', width=2, dash='dash'),
    name='Umbral'
))

# Configurar diseño traducido al español y eliminar gridlines
fig.update_layout(
    xaxis_title="Factor de Influencia",
    yaxis_title="Densidad",
    template="simple_white",
    xaxis=dict(
        showgrid=False,
        gridcolor="gray",  # Color tenue para las gridlines
        gridwidth=0.1,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        gridcolor="gray",  # Color tenue para las gridlines
        gridwidth=0.1,
        zeroline=False
    )
)

# Añadir etiquetas descriptivas
fig.add_trace(go.Scatter(
    x=[-6],  # Posición izquierda de la línea
    y=[max(density) * 0.8],  # Altura relativa para la etiqueta
    text=["Usuarios Comunes"],  # Texto para usuarios comunes
    mode="text",
    textfont=dict(size=18, color="white"),  # Estilo de la etiqueta
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=[0],  # Posición derecha de la línea
    y=[max(density) * 0.8],  # Altura relativa para la etiqueta
    text=["Usuarios Influyentes"],  # Texto para usuarios influyentes
    mode="text",
    textfont=dict(size=18, color="white"),  # Estilo de la etiqueta
    showlegend=False
))

# Mostrar en Streamlit
st.title("Análisis del Factor de Influencia")
st.plotly_chart(fig, use_container_width=True)