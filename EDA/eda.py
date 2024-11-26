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
    x=[-7],  # Posición izquierda de la línea
    y=[max(density) * 0.8],  # Altura relativa para la etiqueta
    text=["Usuarios Comunes"],  # Texto para usuarios comunes
    mode="text",
    textfont=dict(size=18, color="white"),  # Estilo de la etiqueta
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=[0.3],  # Posición derecha de la línea
    y=[max(density) * 0.8],  # Altura relativa para la etiqueta
    text=["Usuarios Influyentes"],  # Texto para usuarios influyentes
    mode="text",
    textfont=dict(size=18, color="white"),  # Estilo de la etiqueta
    showlegend=False
))

# Mostrar en Streamlit
st.title("Análisis del Factor de Influencia")
st.plotly_chart(fig, use_container_width=True)

# Crear una segunda gráfica en Plotly adaptada al dashboard de Streamlit

# Filtrar y transformar los datos según el código proporcionado
treshold_influence_factor = -3.1165083206837174  # Umbral definido
top_users_df = posts_df[posts_df['influence_factor'] > treshold_influence_factor]

# Definir la columna 'top_user_indicator' en posts_df
posts_df['top_user_indicator'] = np.where(
    posts_df['influence_factor'] > treshold_influence_factor, 1, 0
)

results_df = posts_df.pivot_table(index='top_user_indicator',
                                  values=['num_posts', 'num_interaction'],
                                  aggfunc='sum')

temp = posts_df.pivot_table(index='top_user_indicator',
                            values='username',
                            aggfunc='count')

results_df = pd.merge(results_df, temp, on='top_user_indicator', how='left')
results_df.rename(columns={
    'num_interaction': 'total_interactions',
    'num_posts': 'total_posts',
    'username': 'total_users'
}, inplace=True)
results_df.rename(index={0: 'casual_user', 1: 'top_user'}, inplace=True)
results_df['%_interaction'] = (results_df['total_interactions'] / results_df['total_interactions'].sum() * 100).round(2)
results_df['%_posts'] = (results_df['total_posts'] / results_df['total_posts'].sum() * 100).round(2)
results_df['%_users'] = (results_df['total_users'] / results_df['total_users'].sum() * 100).round(2)
results_df.reset_index(inplace=True)

# Reorganizar los datos para el gráfico
melted_results = results_df.melt(
    id_vars=['top_user_indicator'],
    value_vars=['%_interaction', '%_posts', '%_users'],
    var_name='metric',
    value_name='value'
)

# Actualizar labels en el DataFrame
melted_results['top_user_indicator'] = melted_results['top_user_indicator'].replace({
    'casual_user': 'Usuarios comunes',
    'top_user': 'Usuario Influyente'
})

# Crear la gráfica en Plotly con barras agrupadas y colores Vivid
fig2 = go.Figure()

# Asignar colores de la paleta "Vivid"
vivid_colors = px.colors.qualitative.Vivid

# Traducir métricas de la leyenda
metric_translation = {
    '%_interaction': '% Interacción',
    '%_posts': '% Publicaciones',
    '%_users': '% Usuarios'
}

# Añadir barras agrupadas para cada métrica
for i, metric in enumerate(melted_results['metric'].unique()):
    filtered_data = melted_results[melted_results['metric'] == metric]
    fig2.add_trace(go.Bar(
        x=filtered_data['top_user_indicator'],
        y=filtered_data['value'],
        name=metric_translation.get(metric, metric),  # Traducir métrica
        text=filtered_data['value'],  # Mostrar los valores
        textposition='auto',
        marker_color=vivid_colors[i % len(vivid_colors)],  # Usar colores de la paleta "Vivid"
        textfont=dict(color='white')  # Asegurar que los porcentajes sean siempre blancos
    ))

# Configurar diseño de la gráfica
fig2.update_layout(
    xaxis_title="Grupo de Usuarios",
    yaxis_title="% del Total",
    barmode='group',  # Barras agrupadas
    template="simple_white",
    xaxis=dict(title_font=dict(size=14, weight='bold')),
    yaxis=dict(title_font=dict(size=14, weight='bold')),
    legend=dict(
        title="Métricas",
        orientation="v",  # Leyenda en vertical
        yanchor="top",    # Anclar en la parte superior
        y=1,              # Ubicar en el borde superior
        xanchor="right",  # Anclar a la derecha
        x=1.2             # Ubicar ligeramente fuera de la gráfica
    )
)

# Mostrar la gráfica en Streamlit
st.subheader("Comparación de Métricas por Grupo de Usuarios")
st.plotly_chart(fig2, use_container_width=True)