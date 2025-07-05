import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🔥 GeoIgniter – Live Forest Fire Spread Simulation")
st.markdown("Click a point on the map to start fire simulation for the next 12 hours.")

# Grid size
H, W = 100, 100

# Simulated slope & LULC layers
slope = np.random.rand(H, W)
lulc = np.random.rand(H, W)

# Fire spread logic
def simulate_fire(start, slope, lulc, steps=12):
    fire_seq = [np.zeros_like(slope, dtype=np.uint8)]
    fire_seq[0][start] = 1

    for t in range(steps):
        prev = fire_seq[-1].copy()
        new = prev.copy()
        for i in range(1, H - 1):
            for j in range(1, W - 1):
                if prev[i, j] == 1:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if prev[ni, nj] == 0:
                                prob = 0.2 + 0.4 * slope[ni, nj] + 0.4 * lulc[ni, nj]
                                if np.random.rand() < prob:
                                    new[ni, nj] = 1
        fire_seq.append(new)
    return fire_seq

# Converts lat/lon to grid index (i, j)
def latlon_to_grid(lat, lon, bounds, H, W):
    lat_min, lon_min = bounds[0]
    lat_max, lon_max = bounds[1]

    i = int((lat_max - lat) / (lat_max - lat_min) * H)
    j = int((lon - lon_min) / (lon_max - lon_min) * W)

    return min(max(i, 0), H - 1), min(max(j, 0), W - 1)

# Map bounds
bounds = [[29.5, 77.5], [31.5, 80.0]]  # SouthWest, NorthEast

# Create interactive map
m = folium.Map(location=[30.5, 78.5], zoom_start=8)
m.add_child(folium.LatLngPopup())
output = st_folium(m, height=500, width=800, return_click_data=True)

# Handle click event
if output["last_clicked"] is not None:
    lat = output["last_clicked"]["lat"]
    lon = output["last_clicked"]["lng"]
    st.success(f"🔥 Fire started at ({lat:.4f}, {lon:.4f})")

    fire_i, fire_j = latlon_to_grid(lat, lon, bounds, H, W)
    fire_seq = simulate_fire((fire_i, fire_j), slope, lulc, steps=12)

    # Show simulation as images
    st.subheader("🕒 Fire Spread Over Time")
    for t, step in enumerate(fire_seq):
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(step, cmap="hot")
        ax.set_title(f"Hour {t}")
        ax.axis("off")
        st.pyplot(fig)
