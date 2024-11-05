# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.header("Exploratory Data Analysis")

# Step 1: Load the dataset
@st.cache
def load_data():
    return pd.read_csv("C:\\Users\\santo\\OneDrive\\Escritorio\\DashboardOMD\\DashboardOMD\\data\\cleansed_infotracer.csv")  # Ruta ajustada

# Load data
data = load_data()

# Display the first 5 rows to understand the structure
st.write("### First 5 Rows of Dataset")
st.write(data.head())

# Distribution of Number of Posts
st.write("### Distribution of Number of Posts")

# Create a DataFrame `posts_df` with the count of unique posts (URLs) per user.
# The pivot_table groups by `username`, counts occurrences of `url` for each user, and sorts in descending order.
posts_df = data.pivot_table(index='username', values='url', aggfunc='count').sort_values(by='url', ascending=False).reset_index()
# Rename the `url` column to `num_posts`
posts_df.rename(columns={'url': 'num_posts'}, inplace=True)

# Create a temporary DataFrame `temp` with the total interactions per user.
# This pivot_table groups by `username` and sums up the `num_interaction` values, sorting in descending order.
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

# Visualization: Kernel Density Estimate (KDE) plot for the distribution of number of posts per user, weighted by interactions
plt.figure(figsize=(10, 6))
sns.kdeplot(posts_df['num_posts'], weights=posts_df['num_interaction'])
plt.xlabel('Number of Posts')
plt.ylabel('Density')
plt.title('Density of Number of Posts per User')
st.pyplot(plt)

# Other exploratory sections here, like Species selection, if still relevant
# Additional analysis and visualizations can be added here.