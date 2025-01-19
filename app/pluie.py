import requests
from localisation import get_coordinates, headers

# L'API utilisée pour récupérer les données historiques de la météo
url = "https://archive-api.open-meteo.com/v1/archive"

def get_precipitation(city : str, start_date : str , end_date : str) -> tuple:
    
    # Récupération des coordonnées de la ville nécessaires à la requête météo
    (lat, long), _ = get_coordinates(city)
    
    params = {
	"latitude": lat,
	"longitude": long,
	"start_date": start_date,
	"end_date": end_date,
	"daily": "precipitation_sum",
    
    }
    
    data = requests.get(url, params=params, headers=headers)
    
    if data.status_code == 200:
        data = data.json()
        liste_date = data["daily"]["time"]
        liste_précipitation = data["daily"]["precipitation_sum"]
        # print(f"Date : {liste_date}")
        # print(f"Précipitation : {liste_précipitation}")
        return liste_date, liste_précipitation
    else:
        print(f"Erreur dans la récupération des données des précipitations : Erreur {data.status_code} - Raison : {data.reason}")
        return None
    
    
# print(get_precipitation("Nice","2024-01-01","2025-01-01"))


