import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔥 GeoIgniter – Live Forest Fire Spread Simulation")

st.markdown("Click a point on the map to start fire simulation for the next 12 hours.")

# Dummy slope and LULC maps (replace with np.load() if you have actual files)
H, W = 100, 100
slope = np.random.rand(H, W)
lulc = np.random.rand(H, W)

# Spread simulation function
def simulate_fire(start, slope, lulc, steps=12):
    fire_seq = [np.zeros_like(slope, dtype=np.uint8)]
    fire_seq[0][start] = 1

    for t in range(steps):
        prev = fire_seq[-1].copy()
        new = prev.copy()
        for i in range(1, H-1):
            for j in range(1, W-1):
                if prev[i, j] == 1:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i+di, j+dj
                            if prev[ni, nj] == 0:
                                prob = 0.2 + 0.4 * slope[ni, nj] + 0.4 * lulc[ni, nj]
                                if np.random.rand() < prob:
                                    new[ni, nj] = 1
        fire_seq.append(new)
    return fire_seq

# Map UI
m = folium.Map(location=[30.5, 78.5], zoom_start=8)
m.add_child(folium.LatLngPopup())

output = st_folium(m, height=500, width=800)

if output["last_clicked"] is not None:
    st.success("🔥 Fire started at clicked point. Running simulation...")

    # Mock coordinate conversion (real version needs lat/lon → i,j map)
    fire_i, fire_j = 50, 50  # center of dummy map
    fire_seq = simulate_fire((fire_i, fire_j), slope, lulc, steps=12)

    # Show simulation as images
    st.subheader("🕒 Fire Spread Over Time")
    for t, step in enumerate(fire_seq):
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(step, cmap="hot")
        ax.set_title(f"Hour {t}")
        ax.axis('off')
        st.pyplot(fig)
