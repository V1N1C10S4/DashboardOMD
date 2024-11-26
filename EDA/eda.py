import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go

# Encabezado para la aplicación
st.title("Density of Influence Factor per User")

# Simulación de datos de ejemplo basada en las descripciones anteriores
np.random.seed(42)
influence_factor = np.concatenate([
    np.random.normal(loc=-10, scale=3, size=30000),
    np.random.normal(loc=0, scale=2, size=20000),
    np.random.normal(loc=5, scale=1, size=5000)
])

# Limpiar valores extremos o no deseados
influence_factor = influence_factor[~np.isinf(influence_factor)]

# Calcular KDE
density = gaussian_kde(influence_factor, bw_method='silverman')  # Simula el comportamiento de Seaborn
x_vals = np.linspace(influence_factor.min() - 2, influence_factor.max() + 2, 500)
y_vals = density(x_vals)

# Crear la figura en Plotly
fig = go.Figure()

# Añadir la línea KDE
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    line=dict(color='blue', width=2),
    name="KDE"
))

# Ajustar el diseño para replicar el estilo original
fig.update_layout(
    title="Density of Influence Factor per User",
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    template="plotly_white",  # Fondo blanco para emular la visualización original
    height=600,
    xaxis=dict(range=[-20, 15], gridcolor="lightgrey"),
    yaxis=dict(gridcolor="lightgrey"),
    showlegend=True
)

# Mostrar la figura en Streamlit
st.plotly_chart(fig, use_container_width=True)