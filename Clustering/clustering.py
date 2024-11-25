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

st.header("Clustering de datos")

def download_data():
    url = 'https://drive.google.com/uc?id=1b5glYHJkkH_cjw1yzLRDtLwMPRNdwu6x'
    output = 'encoded_cleansed_infotracer_by_user_for_clustering.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
data = pd.read_csv("encoded_cleansed_infotracer_by_user_for_clustering.csv")

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import plotly.express as px
import streamlit as st

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
    title="Clustering basado en PCA y KMeans",
    labels={'cluster': 'Cluster'},
    color_discrete_sequence=px.colors.qualitative.Vivid  # Colores vibrantes
)

# Agregar líneas de referencia en los ejes
fig.update_layout(
    shapes=[
        dict(type="line", x0=0, x1=0, y0=pca_df['PCA2'].min(), y1=pca_df['PCA2'].max(), line=dict(color="gray", width=1, dash="dash")),
        dict(type="line", y0=0, y1=0, x0=pca_df['PCA1'].min(), x1=pca_df['PCA1'].max(), line=dict(color="gray", width=1, dash="dash"))
    ]
)

# Configuración para Streamlit
st.title("Visualización Interactiva de Clustering")
st.plotly_chart(fig, use_container_width=True)

# Mostrar la varianza explicada por los componentes principales
explained_variance = pca.explained_variance_ratio_
st.write("Varianza explicada por cada componente principal:")
st.write(f"PCA1: {explained_variance[0]:.2%}, PCA2: {explained_variance[1]:.2%}")
