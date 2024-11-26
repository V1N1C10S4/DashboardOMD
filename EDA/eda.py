import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
posts_df['engagement_rate'] = posts_df['num_interaction'] / posts_df['num_posts'].replace(0, np.nan)
posts_df['%_posts'] = (posts_df['num_posts'] / posts_df['num_posts'].sum()).fillna(0) * 100
posts_df['%_interaction'] = (posts_df['num_interaction'] / posts_df['num_interaction'].sum()).fillna(0) * 100
posts_df['influence_factor'] = np.log(
    (posts_df['%_posts'] * posts_df['%_interaction'] * posts_df['engagement_rate']).replace(0, np.nan) * 100
).fillna(0)

# Plotting function
def plot_density_seaborn(posts_df):
    plt.figure(figsize=(10, 6))
    
    # Set seaborn style
    sns.set(style="whitegrid")
    
    # Create KDE plot
    sns.kdeplot(posts_df['influence_factor'], color='blue', linewidth=2)
    
    # Add labels and grid
    plt.title("Density of Influence Factor per User", fontsize=18, weight='bold', color='#333333')
    plt.xlabel("Influence Factor", fontsize=14, weight='bold')
    plt.ylabel("Density", fontsize=14, weight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    st.pyplot(plt)

# Call the plotting function
plot_density_seaborn(posts_df)