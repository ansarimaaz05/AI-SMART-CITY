import requests

def get_live_traffic(api_key, lat, lon):
    """
    Fetch live traffic data for a given latitude/longitude using TomTom Traffic API.
    Returns current speed, free flow speed, travel time, and confidence.
    """
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
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
            "confidence": flow.get("confidence")
        }
    else:
        return {"error": resp.text}
