 AI Smart City Dashboard

An intelligent and interactive web dashboard that visualizes **traffic data**, **air quality**, and **citizen feedback** using geospatial and AI-powered analytics. Built with **Streamlit** and **PyDeck**, this app demonstrates how smart cities can harness data for better governance, planning, and environmental monitoring.


 Features

Secure Login**: Only authorized users can access the dashboard.
Traffic & Pollution Map**: Visualize traffic congestion and PM2.5 levels across Indian cities using heatmaps, scatter maps, and dot maps.
Air Quality Dashboard**: View pollutant concentrations (PM2.5, PM10, NO₂, SO₂, O₃) per city and compare across cities.
Citizen Feedback Analyzer**: Submit complaints or suggestions and receive sentiment + tag analysis using AI.
Dynamic Graphs**: Interactive bar charts for pollutants and feedback sentiment breakdowns.


Technologies Used

 `Streamlit` – for web interface
 `Pandas` – for data manipulation
 `PyDeck` – for geospatial data visualization
 `NLP Model` – to analyze feedback sentiment and extract tags
 `CSV` – traffic, air quality, and feedback stored in local CSV files

 Folder Structure


AI-Smart-City/
│
├── app.py                      # Main Streamlit app
├── utils/
│   └── feedback_analyzer.py    # Logic for analyzing citizen feedback
├── data/
│   ├── city_data.csv           # Traffic & city-level data
│   ├── air_quality_data.csv    # Pollution data
│   └── citizen_feedback.csv    # Logged user feedback (generated)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

 Installation

 Prerequisites

* Python 3.8+
* pip (Python package manager)

Setup

```bash
# Clone the repo
git clone https://github.com/your-username/AI-Smart-City.git
cd AI-Smart-City

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

 Usernames for login 
user@gmail.com
user@123


 Map Legend

**PM2.5 Levels (Air Quality Index):**

* 🟢 **Green** – Good (≤ 50)
* 🟠 **Orange** – Moderate (51–100)
* 🔴 **Red** – Unhealthy (> 100)

---

## 💡 Use Cases

* Smart City Governance
* Urban & Environmental Research
* Public Feedback Management
* Educational or Demo Purposes

---

## 📜 License

This project is for educational and demo purposes only. All data is static and for simulation only.

---

## 👤 Author

Developed by **Ansari Maaz**

> Feel free to fork, modify, and share. Contributions are welcome!
