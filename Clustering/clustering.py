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

#Visualizaciones secundarias

# Definir una paleta de colores Vivid y asignarla manualmente a cada clúster
vivid_colors = px.colors.qualitative.Vivid
color_mapping = {0: vivid_colors[0], 1: vivid_colors[1], 2: vivid_colors[2]}  # Mapear clusters a colores

# Violin plot ajustado con colores manuales
violin_fig = px.violin(
    data,
    x="cluster",
    y="avg_text_len",
    color=data['cluster'].astype(str),  # Convertir los clusters a string para categorías
    box=True,  # Mostrar boxplot dentro del violin plot
    points=False,  # No mostrar puntos individuales
    labels={"cluster": "Clúster", "avg_text_len": "Longitud Promedio", "color": "Clúster"},
    color_discrete_map={str(key): value for key, value in color_mapping.items()}  # Usar colores asignados manualmente
)

# Ajustar diseño del violin plot
violin_fig.update_traces(
    scalegroup='one',  # Escalar los violines proporcionalmente
    width=0.6  # Aumentar el ancho de los violines
)

violin_fig.update_layout(
    template="plotly_dark",  # Tema oscuro
    xaxis_title="Clúster",
    yaxis_title="Longitud Promedio de Texto",
)

# Boxplot ajustado con colores manuales
boxplot_fig = go.Figure()

# Crear un boxplot para cada cluster, asignando colores manualmente
clusters = sorted(data['cluster'].unique())  # Asegurar un orden consistente
for cluster in clusters:
    cluster_data = data[data['cluster'] == cluster]
    boxplot_fig.add_trace(
        go.Box(
            y=cluster_data['influence_factor'],
            name=f"Clúster {cluster}",
            boxpoints='outliers',  # Mostrar solo los outliers
            whiskerwidth=0.8,  # Ajustar ancho de los bigotes
            marker=dict(size=5, color=color_mapping[cluster]),  # Usar colores asignados manualmente
            line=dict(width=1.5),  # Ancho de las líneas
        )
    )

# Ajustar diseño del boxplot
boxplot_fig.update_layout(
    xaxis_title="Clúster",
    yaxis_title="Factor de Influencia",
    template="plotly_dark",  # Tema oscuro
    height=600,  # Altura del gráfico
)

# Mostrar ambas visualizaciones en el mismo renglón en Streamlit
col1, col2 = st.columns([1.2, 1])  # Ajustar las proporciones de las columnas

with col1:
    st.subheader("Distribución de Longitud Promedio")
    st.plotly_chart(violin_fig, use_container_width=True)  # Visualización del violin plot

with col2:
    st.subheader("Distribución del Factor de Influencia")
    st.plotly_chart(boxplot_fig, use_container_width=True)  # Visualización del boxplot