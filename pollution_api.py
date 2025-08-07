import requests

def get_pollution(city_coords, api_key):
    data=[]
    for city,(lat,lon) in city_coords.items():
        resp = requests.get("http://api.openweathermap.org/data/2.5/air_pollution",
                            params={"lat":lat,"lon":lon,"appid":api_key})
        if resp.ok:
            components = resp.json().get("list", [])[0].get("components", {})
            data.append({"city": city, **components})
    return data
