# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import gdown
import numpy as np

st.header("Análisis Exploratorio de datos")

def download_data():
    url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
    output = 'cleansed_infotracer.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
data = pd.read_csv("cleansed_infotracer.csv")

# Description of the dataset
st.write("""
#### El conjunto de datos:
El conjunto de datos infotracer comprende una muestra de publicaciones relacionadas con las elecciones presidenciales mexicanas desde el 1 de enero de 2024 hasta el 31 de julio de 2024, a través de X (antes Twitter).
""")

# Description of the hypotesis
st.write("""
#### Hipotesis:
Se anticipa que una pequeña parte de los usuarios genere la mayoría de las publicaciones y concentre la mayor cantidad de interacciones dentro de nuestro conjunto de datos. Este fenómeno podría deberse a la influencia o popularidad de ciertos usuarios que capturan la atención de una gran audiencia, así como al alto nivel de actividad al publicar constantemente. Esta dinámica sugiere una distribución desigual de la actividad, en la que los usuarios no poseen un rol proporcionado en la generación de contenido y en la atracción de interacciones.
         
Este análisis exploratorio de datos (AED) sirve como etapa preliminar para un análisis más profundo (por ejemplo, modelado de temas, análisis de sentimientos). Su objetivo es identificar a los usuarios más activos (por ejemplo, por publicaciones, interacciones) en las redes sociales, segmentados por plataforma y candidato. Esta identificación de los principales usuarios guiará el proceso de segmentación de los datos, creando subconjuntos más pequeños y específicos para su posterior análisis.
""")

# Distribution of Number of Posts
st.write("### Distribución del número de publicaciones")

# Create a DataFrame `posts_df` with the count of unique posts (URLs) per user.
posts_df = data.pivot_table(index='username', values='url', aggfunc='count').sort_values(by='url', ascending=False).reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

# Create a temporary DataFrame `temp` with the total interactions per user.
temp = data.pivot_table(index='username', values='num_interaction', aggfunc='sum').sort_values(by='num_interaction', ascending=False).reset_index()
temp.rename(columns={'num_interaction': 'num_interaction'}, inplace=True)

# Merge the `posts_df` and `temp` DataFrames on `username`
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Display description for visualization
st.write("""
Analizar la distribución del número de posts en el recién creado `posts_df` para identificar criterios de segmentación de los principales usuarios.

#### Observaciones:
- La mayoría de los usuarios, probablemente usuarios ocasionales, tienen entre 0 y ~250 publicaciones totales, del 1 de enero al 31 de julio.
- En el eje de abscisas hay un grupo de entre 1.250 y 1.500 publicaciones totales de un número reducido de usuarios que tienen entre 4 y 5 veces más publicaciones que los usuarios ocasionales.
""")

# Visualization: Kernel Density Estimate (KDE) plot for the distribution of number of posts per user
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df, x='num_posts', weights='num_interaction')
plt.xlabel('Número de publicaciones')
plt.ylabel('Densidad')
plt.title('Densidad del número de publicaciones por usuario')
st.pyplot(plt)

# Display description for visualization
st.write("""
#### Observaciones:
- La pendiente más pronunciada se produce de 0 a ~750 publicaciones totales, que probablemente correspondan a usuarios ocasionales.
- Hay una pendiente menos pronunciada de ~750 a ~1700 publicaciones totales, que probablemente corresponda a usuarios no ocasionales, y después una pendiente casi horizontal.
""")

# Visualization: Commulative Density of number of posts per user
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df, x='num_posts', weights='num_interaction', cumulative=True)
plt.xlabel('Número de publicaciones')
plt.ylabel('Densidad')
plt.title('Densidad acumulada del número de publicaciones por usuario')
st.pyplot(plt)

# Logarithmic distribution of Number of Posts
st.write("### Logarítmico:")

posts_df['num_interaction'] = posts_df['num_interaction'].replace(0, 1)
posts_df['log_num_posts'] = np.log(posts_df['num_posts'])
posts_df['log_num_interaction'] = np.log(posts_df['num_interaction'])
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df, x='log_num_posts')
plt.xlabel('Log Número de publicaciones')
plt.ylabel('Densidad')
plt.title('Densidad del Log del número de publicaciones por usuario')
st.pyplot(plt)

# Display description for visualization
st.write("""
#### Observaciones:
- Entre los valores 0 y 1 en el logaritmo del número de publicaciones en el eje de abscisas, hay un intervalo en el que la pendiente se aproxima a 0, y después sigue creciendo hasta el valor de ~2 en el eje de abscisas.
- Este cambio abrupto en la pendiente podría ser un indicador de dónde cortar los datos.
""")