import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go

# Streamlit header
st.header("Density of Influence Factor per User")

# Cargar los datos
url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
df = pd.read_csv(url)

# Step 1: Calculate the number of posts per user
posts_df = df.pivot_table(index='username', values='url', aggfunc='count').sort_values(by='url', ascending=False).reset_index()
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

# Step 2: Calculate the total interactions per user
temp = df.pivot_table(index='username', values='num_interaction', aggfunc='sum').sort_values(by='num_interaction', ascending=False).reset_index()
temp.rename(columns={'num_interaction': 'num_interaction'}, inplace=True)

# Step 3: Merge the post counts and interaction sums for each user
posts_df = pd.merge(posts_df, temp, on='username', how='left')

# Step 4: Calculate derived metrics
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts']
posts_df['%_posts'] = posts_df['num_posts'] / posts_df['num_posts'].sum() * 100
posts_df['%_interaction'] = posts_df['num_interaction'] / posts_df['num_interaction'].sum() * 100
posts_df['influence_factor'] = np.log((posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']) * 100)

# Step 5: Create the KDE density plot using Plotly
fig = go.Figure()

# Add the KDE line for influence_factor
fig.add_trace(go.Histogram(
    x=posts_df['influence_factor'],
    histnorm='density',
    name='Density',
    marker=dict(color='blue', line=dict(width=1)),
    opacity=0.7
))

# Configure the layout
fig.update_layout(
    title="Density of Influence Factor per User",
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    template="simple_white",
    title_font=dict(size=18, color='#333333', family="Arial"),
    xaxis=dict(showgrid=True, gridcolor="LightGray", gridwidth=0.5, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="LightGray", gridwidth=0.5, zeroline=False)
)

# Streamlit visualization
st.title("Influence Factor Analysis")
st.plotly_chart(fig, use_container_width=True)