import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# Header
st.header("Density of Influence Factor per User")

# Load data
url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
output = 'cleansed_infotracer.csv'
df = pd.read_csv(output)

# Ensure datetime is parsed correctly
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Preprocess the influence_factor
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').reset_index()
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Use established calculations
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts'].replace(0, np.nan)
posts_df['%_posts'] = (posts_df['num_posts'] / posts_df['num_posts'].sum()).fillna(0) * 100
posts_df['%_interaction'] = (posts_df['num_interaction'] / posts_df['num_interaction'].sum()).fillna(0) * 100
posts_df['influence_factor'] = np.log(
    (posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']).replace(0, np.nan) * 100
).fillna(0)

# Calculate KDE for influence_factor
influence_factor = posts_df['influence_factor'].dropna()
density = gaussian_kde(influence_factor)
x_vals = np.linspace(influence_factor.min(), influence_factor.max(), 500)  # Original range
y_vals = density(x_vals)

# Create the Plotly figure
fig = go.Figure()

# Add the KDE line
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    line=dict(color='blue', width=2),
    name="KDE"
))

# Update layout to match the original style
fig.update_layout(
    title="Density of Influence Factor per User",
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    template="plotly_white",  # Use light theme to match the original
    height=600,
    showlegend=True
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)