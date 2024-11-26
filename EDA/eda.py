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

# Example dataframe loading (you should replace this with your actual dataframe loading code)
# df = pd.read_csv("cleansed_infotracer.csv")

# Ensure datetime parsing
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Step 1: Data Cleaning (as provided)
df_unique_url = df.drop_duplicates(subset=['url'], keep='first').dropna(subset=['url', 'candidate_name'])
temp = df.drop_duplicates(subset=['url', 'candidate_name'], keep='first')
temp = temp.groupby(['url'], as_index=False).agg({'candidate_name': lambda x: ', '.join(set(x))})
temp = temp.dropna(subset=['url', 'candidate_name'])
df = pd.merge(df_unique_url, temp, on='url', how='left')
df.drop(columns=['candidate_name_x'], inplace=True)
df.rename(columns={'candidate_name_y': 'candidate_name'}, inplace=True)

# Step 2: Create posts_df
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').reset_index()
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Step 3: Calculate metrics
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts'].replace(0, np.nan)
posts_df['%_posts'] = (posts_df['num_posts'] / posts_df['num_posts'].sum()).replace(0, np.nan) * 100
posts_df['%_interaction'] = (posts_df['num_interaction'] / posts_df['num_interaction'].sum()).replace(0, np.nan) * 100
posts_df['influence_factor'] = np.log(
    (posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']).replace(0, np.nan) * 100
).fillna(0)

# Step 4: Filter out zero or invalid influence_factor values
filtered_influence_factors = posts_df[posts_df['influence_factor'] > 0]['influence_factor']

# Step 5: Generate KDE for filtered influence_factor
density = gaussian_kde(filtered_influence_factors)
x_vals = np.linspace(filtered_influence_factors.min(), filtered_influence_factors.max(), 500)
y_vals = density(x_vals)

# Step 6: Create Plotly visualization
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