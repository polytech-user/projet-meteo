import requests
import pandas as pd
import numpy as np
from localisation import get_coordinates, headers

# L'API utilisée pour récupérer les données historiques de la météo
url = "https://archive-api.open-meteo.com/v1/archive"

def get_precipitation(city : str, start_date : str , end_date : str) -> pd.DataFrame:
    
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
        df = pd.DataFrame({
            "Date": liste_date,
            "Précipitation": liste_précipitation
        })
        return df
    else:
        print(f"Erreur dans la récupération des données des précipitations : Erreur {data.status_code} - Raison : {data.reason}")
        return None
    
    
# print(get_precipitation("Nice","2024-01-01","2025-01-01"))


def get_precipitation_10_years_ago(city : str, date : str) -> pd.DataFrame:
    year, month, day = date.split('-')
    year = str(int(year) - 10)
    start_date = '-'.join([year,month,day])
    
    df = get_precipitation(city,start_date,date)
    
    return df
    

df = get_precipitation_10_years_ago('Nice','2025-01-01')
print(df)
# print(df.loc[df['Date'] == '2019-11-23'])
# max_precipitation_date = df.loc[df['Date'].idxmax(), 'Date']
# print(f"La date associée à la précipitation maximale est : {max_precipitation_date}")

def daily_mean_precipitation_on_10_years(city : str, date: str) -> pd.DataFrame:
    df = get_precipitation_10_years_ago(city, date)
    
    df['MM-DD'] = df['Date'].str[5:]
    df['Année'] = df['Date'].str[:4].astype(int)
    
    min_year = df['Année'].min()
    df['Poids'] = np.log(df['Année'] - min_year + 1) + 1 # Poids logarithmiques
    grouped = df.groupby('MM-DD').apply(
        lambda group: pd.Series({
            'Somme_Poids': np.sum(group['Précipitation'] * group['Poids']),
            'Total_Poids': np.sum(group['Poids'])
        })
    ).reset_index()
    
    grouped['Moyenne_Precipitation_Pondérée'] = grouped['Somme_Poids'] / grouped['Total_Poids']
    result = grouped[['MM-DD', 'Moyenne_Precipitation_Pondérée']].rename(columns={
        'MM-DD': 'Date'
    })
    
    return result
    

# df = daily_mean_precipitation_on_10_years('Nice', '2025-01-01')
# print(df)
# print(df.loc[df['Année'] == 2020, 'Poids'])