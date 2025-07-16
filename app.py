import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils.data_loader import fetch_gaia_data
from utils.motion_animation import apply_proper_motion

# Streamlit config
st.set_page_config(page_title="GaiaGalaxyView", layout="wide")
st.title("🌌 GaiaGalaxyView")
st.markdown("Explore host stars in motion, space, and classification — powered by Gaia DR3.")

# Sidebar controls
st.sidebar.header("⚙️ Controls")
limit = st.sidebar.slider("Star Sample Size", 100, 5000, 1000)
show_motion = st.sidebar.checkbox("Show Proper Motion", True)
end_year = st.sidebar.slider("Animate to Year", 2025, 2125, 2125, step=10)
color_scheme = st.sidebar.selectbox("Color Scheme", ["Viridis", "Plasma", "Cividis"])

# Load data
with st.spinner("Fetching Gaia data..."):
    df = fetch_gaia_data(limit)

# Layout
tab1, tab2, tab3 = st.tabs(["🌍 3D Star Map", "🎞️ Motion Trails", "📊 CMD Diagram"])

# Tab 1: 3D Map
with tab1:
    st.subheader("🧭 3D Map of Host Stars")
    fig = go.Figure(go.Scatter3d(
        x=df['ra'], y=df['dec'], z=df['distance_pc'],
        mode='markers',
        marker=dict(size=2, color=df['phot_g_mean_mag'],
                    colorscale=color_scheme, opacity=0.7)
    ))
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Proper Motion
if show_motion:
    with tab2:
        st.subheader("🚀 Proper Motion Animation")
        animated_df = apply_proper_motion(df, 2025, end_year, 10)
        fig_motion = px.scatter_3d(animated_df, x='ra_shifted', y='dec_shifted', z='distance_pc',
                                   animation_frame='year',
                                   color='phot_g_mean_mag',
                                   color_continuous_scale=color_scheme,
                                   size_max=3, opacity=0.6)
        fig_motion.update_layout(height=700)
        st.plotly_chart(fig_motion, use_container_width=True)

# Tab 3: CMD Plot
with tab3:
    st.subheader("📈 Color-Magnitude Diagram")
    df['abs_mag'] = df['phot_g_mean_mag'] - 5 * (np.log10(df['distance_pc']) - 1)
    fig_cmd = px.scatter(df, x='bp_rp', y='abs_mag',
                         color='bp_rp',
                         color_continuous_scale=color_scheme,
                         labels={'bp_rp': 'BP-RP Color', 'abs_mag': 'Absolute Magnitude'},
                         height=700)
    fig_cmd.update_layout(yaxis_title="Absolute G Magnitude (mag)", xaxis_title="BP-RP Color Index")
    st.plotly_chart(fig_cmd, use_container_width=True)
