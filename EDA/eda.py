import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go

# Simulated data for influence_factor based on statistical description provided earlier
np.random.seed(42)
influence_factor = np.concatenate([
    np.random.normal(loc=-10, scale=3, size=30000),
    np.random.normal(loc=0, scale=2, size=20000),
    np.random.normal(loc=5, scale=1, size=5000)
])

# Clean up extreme or unwanted values for the KDE calculation
influence_factor = influence_factor[~np.isinf(influence_factor)]

# Calculate KDE
density = gaussian_kde(influence_factor, bw_method='silverman')  # Matching seaborn default bandwidth
x_vals = np.linspace(influence_factor.min() - 2, influence_factor.max() + 2, 500)
y_vals = density(x_vals)

# Create Plotly figure
fig = go.Figure()

# Add KDE line
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    line=dict(color='blue', width=2),
    name="KDE"
))

# Update layout to replicate the original Seaborn style
fig.update_layout(
    title="Density of Influence Factor per User",
    xaxis_title="Influence Factor",
    yaxis_title="Density",
    template="plotly_white",
    height=600,
    xaxis=dict(range=[-20, 15], gridcolor="lightgrey"),
    yaxis=dict(gridcolor="lightgrey"),
    showlegend=True
)

# Display the figure
fig.show()