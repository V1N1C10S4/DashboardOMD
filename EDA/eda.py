# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import gdown
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import gaussian_kde

st.header("Análisis Exploratorio de datos")

def download_data():
    url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
    output = 'cleansed_infotracer.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
df = pd.read_csv("cleansed_infotracer.csv")

# Suponiendo que `df` ya está cargado con los datos originales.

# Crear `posts_df` con conteo de posts únicos por usuario
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').sort_values(by='url', ascending=False).reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

# Crear DataFrame temporal `temp` con el total de interacciones por usuario
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').sort_values(by='num_interaction', ascending=False).reset_index()
temp.rename(columns={'num_interaction': 'num_interaction'}, inplace=True)

# Combinar `posts_df` y `temp` en un solo DataFrame
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Calcular métricas adicionales
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts']
posts_df['%_posts'] = posts_df['num_posts'] / posts_df['num_posts'].sum() * 100
posts_df['%_interaction'] = posts_df['num_interaction'] / posts_df['num_interaction'].sum() * 100
posts_df['influence_factor'] = np.log((posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']) * 100)

# Calcular el umbral del factor de influencia
earliest_date = df['datetime'].min()
latest_date = df['datetime'].max()
time_difference = latest_date - earliest_date
total_days = time_difference.days

expected_posts_per_day = 1
expected_interactions_per_post = 5
expected_total_posts = expected_posts_per_day * total_days
expected_total_interactions = expected_total_posts * expected_interactions_per_post
expected_engagement_rate = expected_interactions_per_post / expected_posts_per_day

treshold_influence_factor = np.log(
    expected_total_posts / posts_df['num_posts'].sum() * 100 *
    expected_total_interactions / posts_df['num_interaction'].sum() * 100 *
    expected_engagement_rate * 100
)

# Crear valores para la gráfica de densidad (KDE)
x_values = np.linspace(posts_df['influence_factor'].min(), posts_df['influence_factor'].max(), 1000)
kde = gaussian_kde(posts_df['influence_factor'])
density_values = kde(x_values)

# Crear la gráfica interactiva con Plotly
fig = go.Figure()

# Añadir la curva de densidad
fig.add_trace(go.Scatter(
    x=x_values,
    y=density_values,
    mode='lines',
    line=dict(color='blue', width=2),
    name='Densidad'
))

# Añadir la línea vertical del umbral
fig.add_trace(go.Scatter(
    x=[treshold_influence_factor, treshold_influence_factor],
    y=[0, max(density_values)],
    mode='lines',
    line=dict(color='darkgray', width=2, dash='dash'),
    name='Umbral del Factor de Influencia'
))

# Configuración de diseño
fig.update_layout(
    title={
        'text': "Densidad del Factor de Influencia por Usuario",
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title="Factor de Influencia",
    yaxis_title="Densidad",
    template="plotly_dark",
    showlegend=True,
    legend=dict(
        title="Leyenda",
        font=dict(size=12),
        bordercolor="Gray",
        borderwidth=1
    )
)

# Agregar líneas de referencia en el grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')

# Mostrar en Streamlit
st.title("Exploratory Data Analysis: Densidad del Factor de Influencia")
st.plotly_chart(fig, use_container_width=True)