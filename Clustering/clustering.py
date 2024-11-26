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

# Calcular el candidato más mencionado en cada clúster
data['top_candidate'] = data[['top_mentioned_candidate_Claudia Sheinbaum', 
                               'top_mentioned_candidate_Jorge Álvarez Máynez',
                               'top_mentioned_candidate_Xóchitl Gálvez']].idxmax(axis=1)

cluster_summary = data.groupby('cluster').agg(
    top_candidate = ('top_candidate', lambda x: x.value_counts().idxmax()),  # Candidato más mencionado
    avg_influence = ('influence_factor', 'mean'),
    avg_text_length = ('avg_text_len', 'mean'),
    avg_time_elapsed = ('avg_time_elapsed_between_posts', 'mean'),
    count = ('cluster', 'size')
).reset_index()

# Crear un DataFrame para los datos PCA transformados y las asignaciones de cluster
pca_df = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2'])
pca_df['cluster'] = clusters

# Asociar los datos agregados con cada clúster para las etiquetas
pca_df = pca_df.merge(cluster_summary, on='cluster')

# Crear visualización interactiva con etiquetas por clúster
fig = px.scatter(
    pca_df,
    x='PCA1',
    y='PCA2',
    color=pca_df['cluster'].astype(str),  # Convertir cluster a cadena para una leyenda categórica
    title="Basado en PCA y KMeans",
    labels={'color': 'Clusters', 'PCA1': 'Componente principal 1', 'PCA2': 'Componente principal 2'},
    color_discrete_sequence=px.colors.qualitative.Vivid,
    hover_data={  # Incluir datos agrupados en las etiquetas
        'cluster': False,
        'top_candidate': True,
        'avg_influence': ':.2f',
        'avg_text_length': ':.2f',
        'avg_time_elapsed': ':.2f',
        'count': True,
        'PCA1': False,  # Ocultar información a nivel individual
        'PCA2': False,   # Ocultar información a nivel individual
    }
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

# Añadir la columna 'cluster' al DataFrame
data['cluster'] = clusters

# Agrupar por clústeres y calcular estadísticas descriptivas
cluster_analysis = data.groupby('cluster').agg({
    'influence_factor': ['mean', 'std', 'min', 'max'],
    'avg_text_len': ['mean', 'std', 'min', 'max'],
    'avg_time_elapsed_between_posts': ['mean', 'std', 'min', 'max'],
    'preferred_time_of_day': ['mean', 'std', 'min', 'max'],
    'top_mentioned_candidate_Claudia Sheinbaum': ['mean'],
    'top_mentioned_candidate_Jorge Álvarez Máynez': ['mean'],
    'top_mentioned_candidate_Xóchitl Gálvez': ['mean']
}).reset_index()

# Renombrar columnas para mayor claridad
cluster_analysis.columns = [
    'Clúster',
    'Influencia Promedio', 'Desv. Estándar Influencia', 'Influencia Mínima', 'Influencia Máxima',
    'Longitud Texto Promedio', 'Desv. Estándar Longitud Texto', 'Longitud Texto Mínima', 'Longitud Texto Máxima',
    'Tiempo Promedio entre Posts', 'Desv. Estándar Tiempo entre Posts', 'Tiempo Mínimo entre Posts', 'Tiempo Máximo entre Posts',
    'Hora Preferida Promedio', 'Desv. Estándar Hora Preferida', 'Hora Preferida Mínima', 'Hora Preferida Máxima',
    '% Menciones Claudia Sheinbaum', '% Menciones Jorge Álvarez Máynez', '% Menciones Xóchitl Gálvez'
]

# Crear un DataFrame con los datos organizados por clúster
datos_clúster_organizados = []

for cluster_id in cluster_analysis['Clúster']:
    datos_clúster = data[data['cluster'] == cluster_id]
    total_usuarios = len(datos_clúster)
    influencia_promedio = cluster_analysis[cluster_analysis['Clúster'] == cluster_id]['Influencia Promedio'].values[0]
    longitud_texto_promedio = cluster_analysis[cluster_analysis['Clúster'] == cluster_id]['Longitud Texto Promedio'].values[0]
    tiempo_promedio = cluster_analysis[cluster_analysis['Clúster'] == cluster_id]['Tiempo Promedio entre Posts'].values[0]

    distribucion_menciones = datos_clúster[['top_mentioned_candidate_Claudia Sheinbaum',
                                            'top_mentioned_candidate_Jorge Álvarez Máynez',
                                            'top_mentioned_candidate_Xóchitl Gálvez']].mean()

    datos_clúster_organizados.append({
        'ID Clúster': cluster_id,
        'Total de Usuarios': total_usuarios,
        'Influencia Promedio': round(influencia_promedio, 2),
        'Longitud Texto Promedio': round(longitud_texto_promedio, 2),
        'Tiempo Promedio entre Posts': round(tiempo_promedio, 2),
        '% Menciones Claudia Sheinbaum': round(distribucion_menciones['top_mentioned_candidate_Claudia Sheinbaum'], 4),
        '% Menciones Jorge Álvarez Máynez': round(distribucion_menciones['top_mentioned_candidate_Jorge Álvarez Máynez'], 4),
        '% Menciones Xóchitl Gálvez': round(distribucion_menciones['top_mentioned_candidate_Xóchitl Gálvez'], 4)
    })

datos_clúster_df = pd.DataFrame(datos_clúster_organizados)

# Mostrar el DataFrame en Streamlit
st.header("Resumen del Análisis por Clúster")
st.write("A continuación se presenta un resumen de las métricas clave para cada clúster:")
st.dataframe(datos_clúster_df, use_container_width=True)

# Análisis detallado para cada clúster
st.subheader("Análisis Detallado por Clúster")
for _, fila in datos_clúster_df.iterrows():
    cluster_id = fila['ID Clúster']
    st.markdown(f"### Análisis del Clúster {cluster_id}")
    st.markdown(f"- **Total de Usuarios**: {fila['Total de Usuarios']}")
    st.markdown(f"- **Influencia Promedio**: {fila['Influencia Promedio']}")
    st.markdown(f"- **Longitud Promedio del Texto**: {fila['Longitud Texto Promedio']}")
    st.markdown(f"- **Tiempo Promedio entre Posts**: {fila['Tiempo Promedio entre Posts']} segundos")
    st.markdown("#### Distribución de Menciones por Candidato:")
    st.markdown(f"- **Claudia Sheinbaum**: {fila['% Menciones Claudia Sheinbaum']*100:.2f}%")
    st.markdown(f"- **Jorge Álvarez Máynez**: {fila['% Menciones Jorge Álvarez Máynez']*100:.2f}%")
    st.markdown(f"- **Xóchitl Gálvez**: {fila['% Menciones Xóchitl Gálvez']*100:.2f}%")

st.write("""
### Aspectos destacados de clústers por candidato:
Jorge Álvarez Maynez relacionado con el clúster 2 es el candidato más mencionado por un gran número de usuarios únicos, lo que significa que aunque sus menciones en general son pocas, al filtrar usuarios únicos es el que lidera la conversación, no genera una gran cantidad de influencia pero podemos concluir que es muy mencionado entre los usuarios más casuales de la red social X.
""")

st.write("""
El cluster 1 relacionado con Claudia Sheinbaum tiene mucha más influencia, a pesar de que el tiempo entre el post de cada publicación es el mayor entre los clusters así como la longitud media de las publicaciones.
""")

st.write("""
El cluster 0 uno relacionado con Xóchitl Gálvez presenta un comportamiento intermedio en comparación con los otros dos clusters.
""")

#Visualizaciones secundarias

# Añadir un espacio entre la gráfica de clustering y las gráficas de análisis de clusters
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# 0 -> naranja <- 2
# 1 -> azul <- 0
# 2 -> verde <- 1

# Definir una paleta de colores Vivid y asignarla manualmente a cada clúster
vivid_colors = px.colors.qualitative.Vivid
color_mapping = {2: vivid_colors[0], 0: vivid_colors[1], 1: vivid_colors[2]}  # Mapear clusters a colores

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
            name=f"{cluster}",
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
col1, col2 = st.columns([1, 1])  # Ajustar las proporciones de las columnas

with col1:
    st.subheader("Distribución de Longitud Promedio")
    st.plotly_chart(violin_fig, use_container_width=True)  # Visualización del violin plot

with col2:
    st.subheader("Distribución del Factor de Influencia")
    st.plotly_chart(boxplot_fig, use_container_width=True)  # Visualización del boxplot

st.write("""
### Frecuencia de publicación y longitud de texto como predictores de influencia:
En todos los grupos, los textos largos y las publicaciones menos frecuentes están vinculados a mayor influencia, mientras que mensajes breves y frecuentes corresponden a menor impacto. Este patrón resalta la importancia de priorizar calidad sobre cantidad para lograr un compromiso significativo.
""")

st.write("""
### Influencia concentrada en clusters pequeños y de alta calidad:
El grupo 1, el más pequeño, reúne a los usuarios más influyentes, quienes publican textos largos con menor frecuencia. Esto confirma que la calidad y la comunicación reflexiva e impactante tienen mayor influencia, mientras que los clusters más grandes, como el grupo 2, diluyen el impacto individual debido a publicaciones frecuentes y breves.
""")

# Añadir un espacio entre las gráficas de análisis de clusters y la visualización final
st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

# Calcular el DataFrame organizado (organized_cluster_df)
cluster_analysis = data.groupby('cluster').agg({
    'influence_factor': 'mean',
    'avg_text_len': 'mean',
    'avg_time_elapsed_between_posts': 'mean'
}).reset_index()

# Renombrar columnas
cluster_analysis.columns = [
    'Cluster ID', 'Average Influence', 'Average Text Length', 'Average Time Elapsed'
]

# Seleccionar las columnas relevantes para la comparación de promedios
cluster_means = cluster_analysis[['Cluster ID', 'Average Influence', 'Average Text Length', 'Average Time Elapsed']]

# Convertir el DataFrame a formato largo para graficar
cluster_means_melted = cluster_means.melt(
    id_vars='Cluster ID',  # Identificador único por clúster
    var_name='Metric',     # Nombre de la columna que indica la métrica
    value_name='Value'     # Nombre de la columna que almacena los valores
)

# Crear el gráfico de barras interactivo con Plotly
fig = px.bar(
    cluster_means_melted,
    x='Cluster ID',         # Eje x: ID del clúster
    y='Value',              # Eje y: valores promedio
    color='Metric',         # Diferenciar barras por métrica
    barmode='group',        # Agrupar barras por clúster
    labels={'Cluster ID': 'Clúster', 'Value': 'Valor Promedio', 'Metric': 'Métrica'},  # Etiquetas personalizadas
    color_discrete_sequence=px.colors.qualitative.Vivid  # Paleta de colores Vivid
)

# Ajustar diseño del gráfico
fig.update_layout(
    template="plotly_dark",  # Tema oscuro
    xaxis_title="Clúster",
    yaxis_title="Valor Promedio",
)

# Integrar el gráfico en Streamlit
st.title("Comparación de Promedios entre Clústeres")
st.plotly_chart(fig, use_container_width=True)

st.write("""
### Patrones de comportamiento diferenciados entre clusters:
- Clúster 0: Representa un equilibrio moderado en influencia, longitud de texto y frecuencia de publicación, posicionándose como un término medio en compromiso y alcance.
- Clúster 1: Enfocado en mensajes deliberados y significativos, con la mayor longitud de texto y menor frecuencia.
- Clúster 2: Caracterizado por publicaciones rápidas y frecuentes, con textos cortos que comprometen la calidad del impacto.
""")

st.write("""
### Implicaciones estratégicas:
Las estrategias de contenido deben priorizar publicaciones significativas y menos frecuentes para maximizar la influencia. Adaptar las tácticas según el comportamiento específico de cada cluster puede optimizar el alcance y resonancia del contenido en diferentes audiencias.
""")