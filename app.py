import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.feedback_analyzer import analyze_feedback

st.set_page_config(page_title="AI Smart City", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: #2E8B57;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #111;
            border-radius: 12px;
            padding: 10px;
            margin: 0 5px;
            color: #90ee90;
            font-weight: 600;
        }
        .stDataFrame thead tr th {
            background-color: #222;
            color: #90ee90;
        }
        textarea, .stTextInput, .stSelectbox {
            background-color: #111 !important;
            color: #90ee90 !important;
            border: 1px solid #2E8B57;
            border-radius: 6px;
        }
        .stButton button {
            background-color: #2E8B57;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 16px;
        }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔐 Secure Access Portal")
    with st.form(key="login_form"):
        username = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            valid_users = {
                "user@gmail.com": "user@123"
            }
            if username in valid_users and password == valid_users[username]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
    st.stop()

st.title("🌿 AI Smart City Dashboard")

if st.button("🔒 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

try:
    traffic_df = pd.read_csv("data/city_data.csv")
    pollution_df = pd.read_csv("data/air_quality_data.csv")

    city_df = pd.merge(traffic_df, pollution_df, left_on="city_ascii", right_on="location", how="inner")
    if "location" in city_df.columns:
        city_df.drop(columns=["location"], inplace=True)

    if "lng" in city_df.columns:
        city_df.rename(columns={"lng": "lon"}, inplace=True)

    for col in ['lat','lon','traffic_index','pm25','pm10','no2','so2','o3']:
        if col not in city_df.columns:
            city_df[col] = 0
        city_df[col] = pd.to_numeric(city_df[col], errors="coerce").fillna(0)

    st.success(f"✅ Loaded dataset with {len(city_df)} cities")
except Exception as e:
    st.error(f"⚠️ Could not load city data: {e}")
    city_df = pd.DataFrame()

try:
    feedback_df = pd.read_csv("data/citizen_feedback.csv")
except:
    feedback_df = pd.DataFrame()

tab1, tab2, tab3 = st.tabs(["🚦 Traffic & Mobility", "🌫 Air Quality", "🗣 Citizen Feedback"])

with tab1:
    st.markdown("### 🚦 Traffic & Pollution Map")

    if not city_df.empty:
        states = sorted(city_df['admin_name'].dropna().unique())
        states.insert(0, "All Over India")

        default_index = states.index("Maharashtra") if "Maharashtra" in states else 0
        selected_state = st.selectbox("Select a State", states, index=default_index)

        state_data = city_df if selected_state == "All Over India" else city_df[city_df['admin_name'] == selected_state]

        if not state_data.empty:
            st.dataframe(state_data[['city_ascii','admin_name','population','traffic_index','pm25']])

            if "show_map" not in st.session_state:
                st.session_state.show_map = False

            if st.button("🗺️ Show Map"):
                st.session_state.show_map = True

            if st.session_state.show_map:
                state_data['heat_weight'] = state_data['traffic_index'] * (state_data['pm25'].replace(0, 1))

                map_option = st.radio("Select Map Type", ["Heatmap", "Scatter Map", "Dot Map"])

                if map_option == "Heatmap":
                    layer = pdk.Layer(
                        "HeatmapLayer",
                        data=state_data,
                        get_position='[lon, lat]',
                        get_weight="heat_weight",
                        radiusPixels=50,
                        intensity=1,
                        threshold=0.1,
                    )
                else:
                    def get_color(pm25):
                        if pm25 <= 50:
                            return [0, 255, 0, 200]
                        elif pm25 <= 100:
                            return [255, 165, 0, 200]
                        else:
                            return [255, 0, 0, 200]

                    state_data['color'] = state_data['pm25'].apply(get_color)

                    if map_option == "Scatter Map":
                        layer = pdk.Layer(
                            "ScatterplotLayer",
                            data=state_data,
                            get_position='[lon, lat]',
                            get_radius="traffic_index * 100",
                            get_fill_color="color",
                            pickable=True,
                        )
                    else:
                        layer = pdk.Layer(
                            "ScatterplotLayer",
                            data=state_data,
                            get_position='[lon, lat]',
                            get_radius=20000,
                            get_fill_color="color",
                            pickable=True,
                        )

                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=pdk.ViewState(latitude=20.5937, longitude=78.9629, zoom=4),
                    tooltip={
                        "text": "{city_ascii}, {admin_name}\n"
                                "Traffic: {traffic_index}\n"
                                "PM2.5: {pm25}\nPM10: {pm10}\nNO₂: {no2}\nSO₂: {so2}\nO₃: {o3}"
                    }
                )
                st.pydeck_chart(r)

                st.markdown("""
                **Legend (PM2.5 Levels):**
                - 🟢 Green → Good (≤ 50)
                - 🟠 Orange → Moderate (51–100)
                - 🔴 Red → Unhealthy (> 100)
                """)
    else:
        st.warning("⚠️ No traffic data available.")

with tab2:
    st.markdown("### 🌫 Air Quality Data & Graphs")

    if not pollution_df.empty:
        st.write("#### 📋 Full Air Quality Data")
        st.dataframe(pollution_df)

        cities = sorted(pollution_df['location'].dropna().unique())
        selected_city = st.selectbox("Select a City to Analyze", cities, index=cities.index("Mumbai") if "Mumbai" in cities else 0)
        selected_data = pollution_df[pollution_df['location'] == selected_city]

        if not selected_data.empty and st.checkbox("📈 Show Graphs for Selected City"):
            st.bar_chart(selected_data.set_index('location')[['pm25','pm10','no2','so2','o3']])

        if st.checkbox("🌍 Compare PM2.5 Across All Cities"):
            st.bar_chart(pollution_df.set_index('location')[['pm25']])

        if st.checkbox("📊 Show Multi-Pollutant Comparison Across Cities"):
            st.bar_chart(pollution_df.set_index('location')[['pm25','pm10','no2','so2','o3']])
    else:
        st.warning("⚠️ Air quality data not available.")

with tab3:
    st.markdown("### 📬 Submit Feedback")
    feedback = st.text_area("Enter feedback or complaint:")
    if feedback:
        result = analyze_feedback(feedback)
        st.success("🔍 Feedback Analyzed")
        st.write("**Sentiment:**", result['sentiment'])
        st.write("**Tags:**", ", ".join(result['tags']))
        feedback_df = feedback_df._append({"feedback": feedback, "sentiment": result["sentiment"], "tags": ", ".join(result["tags"])}, ignore_index=True)
        feedback_df.to_csv("data/citizen_feedback.csv", index=False)

    if not feedback_df.empty:
        st.write("### 📊 Feedback Summary")
        st.bar_chart(feedback_df['sentiment'].value_counts())
        st.bar_chart(feedback_df['tags'].str.split(', ').explode().value_counts())
        st.dataframe(feedback_df)
    else:
        st.info("No feedback available yet.")
