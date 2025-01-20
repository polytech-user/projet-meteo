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



# Obtenir les valeurs des précipitations depuis x années
def get_precipitation_x_years_ago(city : str, date : str, years : int = 10) -> pd.DataFrame:
    year, month, day = date.split('-')
    year = str(int(year) - years)
    start_date = '-'.join([year,month,day])
    
    df = get_precipitation(city,start_date,date)
    
    return df
    

# df = get_precipitation_x_years_ago('Nice','2014-01-01')
# df_jan_1 = df[df['Date'].str.endswith('01-01')].head(11)
# print(df_jan_1)
# print(df)
# print(df.loc[df['Date'] == '2019-11-23'])
# max_precipitation_date = df.loc[df['Date'].idxmax(), 'Date']
# print(f"La date associée à la précipitation maximale est : {max_precipitation_date}")


# Calcule la moyenne pondérée des précipitations journalières sur x années (les années récentes ont plus de poids)
def daily_mean_precipitation_on_x_years(city : str, date: str, years: int = 10) -> pd.DataFrame:
    df = get_precipitation_x_years_ago(city, date, years)
    
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
    result = grouped[['MM-DD', 'Moyenne_Precipitation_Pondérée']]
           
    return result
    

# df = daily_mean_precipitation_on_x_years('Nice', '2014-01-01')
# print(df)
# # Filtrer les valeurs pour le mois de février
# df_february = df[df['Date'].str.startswith('02-')]
# print(df_february)


# Calcul des probabilités des 3 cas : plt > pivot, 0 < plt < pivot, et plt = 0 
def get_daily_proba_precipitation(city : str, date : str, pl_pivot : float, years: int = 10) -> pd.DataFrame:
    df_x_years_rain = get_precipitation_x_years_ago(city, date, years)
    df_x_years_rain['MM-DD'] = df_x_years_rain['Date'].str[5:]
    result = (
        df_x_years_rain.groupby("MM-DD")["Précipitation"]
        .agg(**{
            "Probabilité de plt > pivot": lambda x: ((x >= pl_pivot).sum())/years,
            "Probabilité de 0 < plt < pivot": lambda x: (((x > 0) & (x < pl_pivot)).sum())/years
        }).reset_index()
    )
    
    result["Probabilité de plt = 0"] = 1 - result["Probabilité de plt > pivot"] - result["Probabilité de 0 < plt < pivot"]
    
    return result
    
    
# print(get_daily_proba_precipitation('Nice','2014-01-01',2))

def get_daily_factor(city : str, date : str, pl_pivot : float, years : int = 10) -> pd.DataFrame:
    mean_plt = daily_mean_precipitation_on_x_years(city, date, years)
    mean_plt['facteur'] = (pl_pivot - mean_plt['Moyenne_Precipitation_Pondérée']) / pl_pivot
    return mean_plt

# print(get_daily_factor('Nice', '2014-01-01', 2))