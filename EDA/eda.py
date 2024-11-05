# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import gdown

st.header("Exploratory Data Analysis")

def download_data():
    url = 'https://drive.google.com/uc?id=1BlXm5AwbroZKPYPxtXeBw3RzRyNiJEtd'
    output = 'cleansed_infotracer.csv'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

# Llama a la función antes de cargar los datos
download_data()

# Load data
data = pd.read_csv("cleansed_infotracer.csv")

# Display the first 5 rows to understand the structure
st.write("### First 5 Rows of Dataset")
st.write(data.head())

# Distribution of Number of Posts
st.write("### Distribution of Number of Posts")

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
Analyzing the distribution of the number of posts in the newly created `posts_df` to identify criteria for segmenting the top users.

#### Observations:
- Most users, likely casual users, have between 0 and ~250 total posts, from January 1st to July 31st.
- There is a lump between 1250 and 1500 total posts in the x-axis of a reduced number of users that have around 4x-5x times more posts than the casual user.
""")

# Visualization: Kernel Density Estimate (KDE) plot for the distribution of number of posts per user
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df, x='num_posts', weights='num_interaction')
plt.xlabel('Number of Posts')
plt.ylabel('Density')
plt.title('Density of Number of Posts per User')
st.pyplot(plt)

# Display description for visualization
st.write("""
#### Renmarks:
- The steepest slope happens from 0 to ~750 total posts, that most likely correspond to casual users.
- There is a less steep slope from ~750 to ~1700 total posts, most likely corresonding to non-casual users, and afterwards an almost horizontal slope.
""")

# Visualization: Commulative Density of number of posts per user
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df, x='num_posts', weights='num_interaction', cumulative=True)
plt.xlabel('Number of Posts')
plt.ylabel('Density')
plt.title('Cumulative Density of Number of Posts per User')
st.pyplot(plt)
