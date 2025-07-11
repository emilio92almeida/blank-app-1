
# To install Streamlit, run:
# pip install streamlit

import streamlit as st
import random
import json
import matplotlib.pyplot as plt
import numpy as np

# Load specs
with open("specs.json", "r") as f:
    specs = json.load(f)

st.set_page_config(page_title="Port Terminal Digital Twin", layout="wide")
st.title("🚢 Port Terminal Simulation")

# User input for number of vessels
num_vessels = st.slider("Number of vessels to simulate", 1, 10, specs["number_of_vessels"])

results = []

for vessel_idx in range(num_vessels):
    st.subheader(f"Vessel {vessel_idx+1}")
    vessel_moves = st.slider(f"Vessel {vessel_idx+1} - Total container moves", specs["vessel_min_moves"], specs["vessel_max_moves"], specs["default_moves"], step=100)
    cranes_assigned = st.slider(f"Vessel {vessel_idx+1} - Cranes assigned (can be fractional)", float(specs["min_cranes"]), float(specs["max_cranes"]), float(specs["default_cranes"]), step=0.1)
    min_mph = st.slider(f"Vessel {vessel_idx+1} - Min crane moves/hour", specs["min_mph"], specs["default_max_mph"], specs["default_min_mph"])
    max_mph = st.slider(f"Vessel {vessel_idx+1} - Max crane moves/hour", specs["default_min_mph"], specs["max_mph"], specs["default_max_mph"])

    # Simulate productivity
    average_mph_per_crane = random.randint(min_mph, max_mph)
    total_mph = average_mph_per_crane * cranes_assigned
    time_required = vessel_moves / total_mph

    st.write(f"**Crane productivity (average):** {average_mph_per_crane} moves/hour")
    st.write(f"**Net Berth Productivity:** {total_mph:.2f} moves/hour")
    st.write(f"**Estimated time in port:** {time_required:.2f} hours")
    st.progress(min(time_required / specs["day_hours"], 1.0), text="Vessel processing progress")

    # Simulate hourly productivity
    hours = int(time_required) + 1
    hourly_productivity = [random.gauss(total_mph, total_mph * 0.1) for _ in range(hours)]
    hourly_productivity = [max(0, round(val, 2)) for val in hourly_productivity]

    # Plot
    fig, ax = plt.subplots()
    ax.plot(range(1, hours + 1), hourly_productivity, marker='o')
    ax.set_title(f"Vessel {vessel_idx+1} - Simulated Productivity Over Time")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Moves Completed")
    ax.grid(True)
    st.pyplot(fig)

    results.append((vessel_idx+1, cranes_assigned, average_mph_per_crane, total_mph, time_required))
