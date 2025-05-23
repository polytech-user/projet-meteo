import requests


# Utilisation de l'API de Nominatim pour récupérer les latitudes et longitudes des villes
url = "https://nominatim.openstreetmap.org/search"
# Définition d'un user-agent quelconque pour pouvoir utiliser l'API car l'user-agent de Python par défaut se fait bloquer
headers = {"User-Agent" : "MyMeteoApp/1.0"}

def get_coordinates(city : str) -> tuple:
        
    params = {
        "q": city,
        "format" : "json",
        "countrycode": "fr",  # Limiter aux résultats français
        "limit": 1,           # Obtenir un seul résultat
        
    }

    # Faire la requête à l'API
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        lat = data[0]["lat"]
        long = data[0]["lon"]
        name = data[0]["name"]
        return (lat, long), name
    else:
        print(f"Erreur lors de la récupération des données de ville : Erreur {response.status_code} - Raison : {response.reason}")
        return None
    

