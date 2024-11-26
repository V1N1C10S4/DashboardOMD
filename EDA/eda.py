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

# Asegurarse de que la columna datetime sea del tipo correcto
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Calcular métricas necesarias
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').reset_index()
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Evitar divisiones por cero y errores en logs
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts'].replace(0, np.nan)
posts_df['%_posts'] = (posts_df['num_posts'] / posts_df['num_posts'].sum()).fillna(0) * 100
posts_df['%_interaction'] = (posts_df['num_interaction'] / posts_df['num_interaction'].sum()).fillna(0) * 100

# Influence Factor
posts_df['influence_factor'] = np.log(
    (posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']).replace(0, np.nan) * 100
).fillna(0)

# Calcular el umbral
earliest_date = df['datetime'].min()
latest_date = df['datetime'].max()
total_days = (latest_date - earliest_date).days

expected_posts_per_day = 1
expected_interactions_per_post = 5

expected_total_posts = expected_posts_per_day * total_days
expected_total_interactions = expected_total_posts * expected_interactions_per_post
expected_engagement_rate = expected_interactions_per_post / expected_posts_per_day

threshold = np.log(
    (expected_total_posts / posts_df['num_posts'].sum() * 100) *
    (expected_total_interactions / posts_df['num_interaction'].sum() * 100) *
    (expected_engagement_rate * 100)
)

# Crear gráfico de densidad interactivo
fig = px.density_contour(
    posts_df,
    x='influence_factor',
    title="Density of Influence Factor per User",
    labels={'influence_factor': 'Influence Factor'},
    template="plotly_dark"
)

fig.add_trace(
    go.Scatter(
        x=[threshold, threshold],
        y=[0, 1],
        mode='lines',
        line=dict(color='gray', dash='dash', width=2),
        name='Threshold Influence Factor'
    )
)

fig.update_layout(
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    title_x=0.5,
    height=600,
    showlegend=True
)

# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)