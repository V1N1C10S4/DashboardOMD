# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import gdown
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go


def download_data():
    url = 'https://drive.google.com/uc?id=1b5glYHJkkH_cjw1yzLRDtLwMPRNdwu6x'
    output = 'encoded_cleansed_infotracer_by_user_for_clustering.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
data = pd.read_csv("encoded_cleansed_infotracer_by_user_for_clustering.csv")

# Seleccionar columnas relevantes para clustering
columns_for_clustering = [
    'influence_factor',
    'avg_text_len',
    'avg_time_elapsed_between_posts',
    'preferred_time_of_day',
    'top_mentioned_candidate_Claudia Sheinbaum',
    'top_mentioned_candidate_Jorge Álvarez Máynez',
    'top_mentioned_candidate_Xóchitl Gálvez'
]

# Filtrar el DataFrame con las columnas seleccionadas
clustering_data = data[columns_for_clustering]

# Escalar los datos
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Reducir dimensionalidad con PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Realizar KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(pca_data)

# Añadir etiquetas de clusters al DataFrame original
data['cluster'] = clusters

# Crear un DataFrame para los datos PCA transformados y las asignaciones de cluster
pca_df = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2'])
pca_df['cluster'] = clusters

# Visualización interactiva con Plotly
fig = px.scatter(
    pca_df,
    x='PCA1',
    y='PCA2',
    color=pca_df['cluster'].astype(str),  # Convertir cluster a cadena para una leyenda categórica
    title="Basado en PCA y KMeans",
    labels={'color': 'Clusters', 'PCA1': 'Componente principal 1', 'PCA2': 'Componente principal 2'},  # Cambiar el título del filtro de color
    color_discrete_sequence=px.colors.qualitative.Vivid  # Colores vibrantes
)

# Agregar líneas de referencia en los ejes
fig.update_layout(
    shapes=[
        dict(type="line", x0=0, x1=0, y0=pca_df['PCA2'].min(), y1=pca_df['PCA2'].max(), line=dict(color="gray", width=1, dash="dash")),
        dict(type="line", y0=0, y1=0, x0=pca_df['PCA1'].min(), x1=pca_df['PCA1'].max(), line=dict(color="gray", width=1, dash="dash"))
    ],
    xaxis_title="Componente principal 1 (PCA1)",
    yaxis_title="Componente principal 2 (PCA2)"
)

# Configuración para Streamlit
st.title("Clustering de usuarios en X")
st.plotly_chart(fig, use_container_width=True)

# Supongamos que 'data' es tu DataFrame principal

# Crear el violin plot interactivo usando Plotly
fig = go.Figure()

# Añadir trazas de violines para cada cluster
clusters = data['cluster'].unique()
for cluster in sorted(clusters):
    cluster_data = data[data['cluster'] == cluster]
    fig.add_trace(
        go.Violin(
            y=cluster_data['avg_text_len'],
            name=f"Cluster {cluster}",
            box_visible=True,  # Mostrar caja con estadísticas
            meanline_visible=True,  # Mostrar línea del promedio
            points="all",  # Mostrar todos los puntos
            line_color='black'
        )
    )

# Personalizar el diseño del gráfico
fig.update_layout(
    title={
        'text': "Distribución de la Longitud Promedio de Texto por Clúster",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Clusters",
    yaxis_title="Longitud Promedio de Texto",
    template="plotly_dark",  # Estilo oscuro para coincidir con tu tema
    showlegend=True,  # Mostrar leyenda
    height=600  # Ajustar altura del gráfico
)

# Añadir a Streamlit
st.title("Análisis de Longitud de Texto")
st.plotly_chart(fig, use_container_width=True)

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Crear el boxplot interactivo usando Plotly
boxplot_fig = go.Figure()

# Añadir trazas de boxplots para cada cluster
clusters = data['cluster'].unique()
for cluster in sorted(clusters):
    cluster_data = data[data['cluster'] == cluster]
    boxplot_fig.add_trace(
        go.Box(
            y=cluster_data['influence_factor'],
            name=f"Cluster {cluster}",
            boxpoints='all',  # Mostrar todos los puntos
            jitter=0.3,  # Añadir dispersión a los puntos
            whiskerwidth=0.8,  # Ajustar el ancho de los bigotes
            marker=dict(size=5),  # Tamaño de los puntos
            line=dict(width=1.5),  # Ancho de las líneas
            fillcolor='rgba(255, 255, 255, 0)'  # Transparencia
        )
    )

# Personalizar el diseño del gráfico
boxplot_fig.update_layout(
    title={
        'text': "Distribución del Factor de Influencia por Clúster",
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="Clusters",
    yaxis_title="Factor de Influencia",
    template="plotly_dark",  # Estilo oscuro para coincidir con el tema
    showlegend=False,  # Ocultar leyenda
    height=600,  # Ajustar altura del gráfico
)

# Mostrar ambas visualizaciones en el mismo renglón en Streamlit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Longitud Promedio")
    st.plotly_chart(fig, use_container_width=True)  # Visualización del violin plot

with col2:
    st.subheader("Distribución del Factor de Influencia")
    st.plotly_chart(boxplot_fig, use_container_width=True)  # Visualización del boxplot