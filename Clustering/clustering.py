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

import plotly.express as px
import pandas as pd

# Datos de prueba
df = pd.DataFrame({
    "x": [1, 2, 3, 4],
    "y": [10, 20, 30, 40],
    "z": ["A", "B", "C", "D"]
})

fig = px.scatter(df, x="x", y="y", color="z", title="Gráfico de prueba con Plotly")
fig.show()
