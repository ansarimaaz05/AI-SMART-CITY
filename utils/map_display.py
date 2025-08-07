import streamlit as st
import pandas as pd

def show_city_map(dataframe, lat_col="lat", lon_col=None, zoom=5):
    """
    Display a city map with latitude and longitude.
    Automatically handles 'lon' or 'lng' column names.
    """
    # Detect longitude column if not specified
    if lon_col is None:
        if "lon" in dataframe.columns:
            lon_col = "lon"
        elif "lng" in dataframe.columns:
            lon_col = "lng"
        elif "longitude" in dataframe.columns:
            lon_col = "longitude"
        else:
            st.warning("⚠️ No longitude column found ('lon' or 'lng').")
            return

    if lat_col in dataframe.columns and lon_col in dataframe.columns:
        # Rename to 'lon' so Streamlit st.map accepts it
        df = dataframe.rename(columns={lon_col: "lon"})
        st.map(df[[lat_col, "lon"]])
    else:
        st.warning("⚠️ Map cannot be displayed because latitude/longitude columns are missing.")
