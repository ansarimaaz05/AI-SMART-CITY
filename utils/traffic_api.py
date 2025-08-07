import requests

def get_live_traffic(api_key, lat, lon, zoom=10):
    """
    Fetch live traffic data near given lat/lon from TomTom Traffic API.
    """
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    params = {
        "point": f"{lat},{lon}",
        "unit": "KMPH",
        "key": api_key
    }
    resp = requests.get(url, params=params)
    if resp.ok:
        data = resp.json()
        flow = data.get("flowSegmentData", {})
        return {
            "currentSpeed": flow.get("currentSpeed"),
            "freeFlowSpeed": flow.get("freeFlowSpeed"),
            "currentTravelTime": flow.get("currentTravelTime"),
            "freeFlowTravelTime": flow.get("freeFlowTravelTime"),
            "confidence": flow.get("confidence"),
        }
    else:
        return {"error": resp.text}
