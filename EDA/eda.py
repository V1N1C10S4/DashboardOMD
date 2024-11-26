import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

# Header
st.header("Density of Influence Factor per User")

# Load data
url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
output = 'cleansed_infotracer.csv'
df = pd.read_csv(output)

# Streamlit header
st.header("Density of Influence Factor per User")

# Example dataframe loading (you should replace this with your actual dataframe loading code)
# df = pd.read_csv("cleansed_infotracer.csv")

# Ensure datetime parsing
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Step 1: Create posts_df
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').reset_index()
temp.rename(columns={'num_interaction': 'num_interaction'}, inplace=True)

posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Step 2: Calculate engagement rate and clean the data
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts'].replace(0, np.nan)

# Avoid zero percentages by replacing zeros with NaN
posts_df['%_posts'] = (posts_df['num_posts'] / posts_df['num_posts'].sum()).replace(0, np.nan) * 100
posts_df['%_interaction'] = (posts_df['num_interaction'] / posts_df['num_interaction'].sum()).replace(0, np.nan) * 100

# Step 3: Calculate the influence factor
posts_df['influence_factor'] = np.log(
    (posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']).replace(0, np.nan) * 100
).fillna(0)

# Remove invalid influence_factor values
posts_df = posts_df[posts_df['influence_factor'] > -np.inf]  # Filter out invalid or infinite values

# Step 4: Generate KDE for influence_factor
influence_factor = posts_df['influence_factor'].dropna()
density = gaussian_kde(influence_factor)
x_vals = np.linspace(influence_factor.min() - 5, influence_factor.max() + 5, 500)
y_vals = density(x_vals)

# Step 5: Create the Plotly visualization
fig = go.Figure()

# Add the KDE line
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    line=dict(color='blue', width=2),
    name="KDE"
))

# Update layout
fig.update_layout(
    title="Density of Influence Factor per User",
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    template="plotly_white",
    height=600,
    showlegend=True,
    xaxis=dict(range=[x_vals.min(), x_vals.max()])
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)