import os
import pandas as pd
import requests

def get_weather(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,windspeed_10m"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()     # erro se status != 200
        data = response.json()
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
        return pd.DataFrame()           # devolve dataframe vazio em vez de crashar

    df = pd.DataFrame({
        "time": data["hourly"]["time"],
        "temperature": data["hourly"]["temperature_2m"],
        "precipitation": data["hourly"]["precipitation"],
        "windspeed": data["hourly"]["windspeed_10m"]
    })
    return df


races = pd.DataFrame([
    {"season": 2021, "round": 1, "circuit": "SPA FRANCORCHAMPS",                    "start_date": "2021-05-01", "end_date": "2021-05-02", "lat": 50.4372, "lon": 5.9714},
    {"season": 2021, "round": 2, "circuit": "AUTODROMO DO ALGARVE",                 "start_date": "2021-06-13", "end_date": "2021-06-13", "lat": 37.2277, "lon": -8.6270},
    {"season": 2021, "round": 3, "circuit": "AUTODROMO NAZIONALE DI MONZA",         "start_date": "2021-07-18", "end_date": "2021-07-18", "lat": 45.6156, "lon": 9.2811},
    {"season": 2021, "round": 4, "circuit": "LE MANS",                              "start_date": "2021-08-21", "end_date": "2021-08-22", "lat": 47.9497, "lon": 0.2211},
    {"season": 2021, "round": 5, "circuit": "BAHRAIN INTERNATIONAL CIRCUIT 6 HOURS","start_date": "2021-10-30", "end_date": "2021-10-30", "lat": 26.0325, "lon": 50.5106},
    {"season": 2021, "round": 6, "circuit": "BAHRAIN INTERNATIONAL CIRCUIT 8 HOURS","start_date": "2021-11-06", "end_date": "2021-11-06", "lat": 26.0325, "lon": 50.5106},
    {"season": 2022, "round": 1, "circuit": "SEBRING",                              "start_date": "2022-03-17", "end_date": "2022-03-18", "lat": 27.4544, "lon": -81.3469},
    {"season": 2022, "round": 2, "circuit": "SPA FRANCORCHAMPS",                    "start_date": "2022-05-07", "end_date": "2022-05-07", "lat": 50.4372, "lon": 5.9714},
    {"season": 2022, "round": 3, "circuit": "LE MANS",                              "start_date": "2022-06-11", "end_date": "2022-06-12", "lat": 47.9497, "lon": 0.2211},
])

os.makedirs("data", exist_ok=True)

weather_list = []
for _, race in races.iterrows():
    df_w = get_weather(race["lat"], race["lon"], race["start_date"], race["end_date"])
    df_w["season"] = race["season"]
    df_w["round"] = race["round"]
    df_w["circuit"] = race["circuit"]
    weather_list.append(df_w)

df_weather = pd.concat(weather_list, ignore_index=True)

# Guardar para ser usado pelos outros ficheiros
df_weather.to_csv("data/weather.csv", index=False)
print(f"Dados meteorológicos guardados: {len(df_weather)} linhas")