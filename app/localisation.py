import requests
import json

# Utilisation de l'API de Nominatim
url = "https://nominatim.openstreetmap.org/search"

def get_coordinates(city):
        
    params = {
        "q": city,
        "format" : "json",
        "countrycode": "fr",  # Limiter aux résultats français
        "limit": 1,           # Obtenir un seul résultat
        
    }

    # Faire la requête à l'API
    response = requests.get(url, params=params, headers={"User-Agent" : "MyMeteoApp/1.0"})

    if response.status_code == 200:
        data = response.json()
        lat = data[0]["lat"]
        long = data[0]["lon"]
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code} - {response.reason}")
        
    return (lat, long)


