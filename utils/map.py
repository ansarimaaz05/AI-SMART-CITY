from traffic_api import get_live_traffic

st.markdown("### 🗺️ Live Traffic Map (TomTom API)")

api_key = "YOUR_TOMTOM_API_KEY"  # Replace with your TomTom key

cities = [
    ("Delhi", 28.7041, 77.1025),
    ("Mumbai", 19.0760, 72.8777),
    ("Bengaluru", 12.9716, 77.5946),
    ("Kolkata", 22.5726, 88.3639),
    ("Chennai", 13.0827, 80.2707)
]

traffic_points = []

for city, lat, lon in cities:
    traffic = get_live_traffic(api_key, lat, lon)
    if "error" not in traffic:
        st.write(f"**{city}** → 🚗 {traffic['currentSpeed']} km/h (Confidence: {traffic['confidence']})")
        traffic_points.append({"city": city, "lat": lat, "lon": lon, "speed": traffic["currentSpeed"]})
    else:
        st.error(f"{city}: {traffic['error']}")

if traffic_points:
    import pandas as pd
    traffic_df = pd.DataFrame(traffic_points)
    st.map(traffic_df[['lat', 'lon']])
