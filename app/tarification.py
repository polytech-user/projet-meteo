import pandas as pd
import numpy as np
from pluie import get_daily_factor_and_proba, get_precipitation_x_years_ago, get_precipitation_x_years_ago_np
from calcul import R_plt_series, R_plt


# Méthode 1 : en utilisant les probabilités et en calculant l'espérance du résultat journalier du commmerce du client
def client_result_expectation(city : str, date : str, CA : float, Cf : float, pl_pivot : float, years: int = 10) -> pd.DataFrame:
    df_val_calcul = get_daily_factor_and_proba(city, date, pl_pivot, years)
    df_exp = pd.DataFrame(df_val_calcul['MM-DD'])
    df_exp['Produit_1ere_ligne'] = -Cf * df_val_calcul['Probabilité_plt_sup_pivot'] # Calcul de P(plt > pivot)*-Cf
    df_exp['Produit_2eme_ligne'] = (df_val_calcul['facteur'] * CA - Cf) * df_val_calcul['Probabilité_0_inf_plt_pivot']
    df_exp['Produit_3eme_ligne'] = (CA - Cf) * df_val_calcul['Probabilité_plt_eq_0']
    df_exp['Espérance'] = df_exp['Produit_1ere_ligne'] + df_exp['Produit_2eme_ligne'] + df_exp['Produit_3eme_ligne']
    total_expectation = df_exp['Espérance'].sum()
    # print(f"Espérance totale des résultats journaliers : {total_expectation}")
    negative_sum = df_exp[df_exp['Espérance'] < 0]['Espérance'].sum()
    # print(f"Somme des espérances négatives : {negative_sum}")
    return df_exp, total_expectation, negative_sum


# df, _, _ = client_result_expectation('Marseille','2014-01-01',150,100,0.5)
# print(df)
    

# Méthode 2 : on calcule les résultats journaliers des x dernières années et on fait la moyenne
def client_result_average(city: str, date: str, CA: float, Cf: float, pl_pivot: float, years: int = 10) -> pd.DataFrame:
    df_pluie = get_precipitation_x_years_ago(city, date, years)
    df_pluie['Résultat_jour'] = R_plt_series(CA, Cf, df_pluie['Précipitation'], pl_pivot)
    
    df_pluie['Année'] = df_pluie['Date'].str[:4].astype(int)
    
    annual_results = df_pluie.groupby('Année')['Résultat_jour'].sum().reset_index()
    annual_results.columns = ['Année', 'Résultat']
    
    min_year = df_pluie['Année'].min()
    annual_results['Poids'] = np.log(annual_results['Année'] - min_year + 1) + 1  # Poids logarithmiques
    annual_results['Résultat_Pondéré'] = annual_results['Résultat'] * annual_results['Poids']
    total_result_weighted_average = annual_results['Résultat_Pondéré'].sum() / annual_results['Poids'].sum()
    annual_results['Moyenne_Pondérée'] = total_result_weighted_average
    return annual_results, total_result_weighted_average
    
# print(client_result_average('Marseille', '2014-01-01', 150,100,0.5))
    

#Méthode qu'on va utilisée pour le calcul de la prime
def client_result_average_other_method(city: str, date: str, CA: float, Cf: float, pl_pivot: float, years: int = 10) -> pd.DataFrame:
    df_pluie = get_precipitation_x_years_ago(city, date, years)
    df_pluie['Résultat_jour'] = R_plt_series(CA, Cf, df_pluie['Précipitation'], pl_pivot)
    
    df_pluie['MM-DD'] = df_pluie['Date'].str[5:]
    df_pluie['Année'] = df_pluie['Date'].str[:4].astype(int)
    min_year = df_pluie['Année'].min()
    df_pluie['Poids'] = np.log(df_pluie['Année'] - min_year + 1) + 1 # Poids logarithmiques
    grouped = df_pluie.groupby('MM-DD').apply(
        lambda group: pd.Series({
            'Somme_Poids': np.sum(group['Résultat_jour'] * group['Poids']),
            'Total_Poids': np.sum(group['Poids'])
        })
    ).reset_index()
    
    grouped['Moyenne_Résultat_Pondérée'] = grouped['Somme_Poids'] / grouped['Total_Poids']
    result = grouped[['MM-DD', 'Moyenne_Résultat_Pondérée']]
    total_res = result['Moyenne_Résultat_Pondérée'].sum()
    # print(f"Somme des résultats journaliers : {total_res}")
    negative_sum = result[result['Moyenne_Résultat_Pondérée'] < 0]['Moyenne_Résultat_Pondérée'].sum()
    # print(f"Somme des résultats journaliers négatifs : {negative_sum}")
    positive_sum = result[result['Moyenne_Résultat_Pondérée'] >= 0]['Moyenne_Résultat_Pondérée'].sum()
    # print(f"Somme des résultats journaliers positifs : {positive_sum}")
    return result, total_res, negative_sum, positive_sum

# print(client_result_average_other_method('Marseille','2014-01-01',150,100,0.5))
    
    
def client_result_average_best_method(city: str, date: str, CA: float, Cf: float, pl_pivot: float, years: int = 10):
    dates, precipitations = get_precipitation_x_years_ago_np(city, date, years)
    R_plt_vectorized = np.vectorize(R_plt)
    liste_resultats_on_x_years = R_plt_vectorized(CA, Cf, precipitations, pl_pivot)
    total_positive_results = np.sum(liste_resultats_on_x_years[liste_resultats_on_x_years >= 0])
    total_negative_results = np.sum(liste_resultats_on_x_years[liste_resultats_on_x_years < 0])
    total_result = (total_positive_results + total_negative_results) / years
    positive_result = total_positive_results / years
    prime = total_negative_results / years
    prime = np.round(prime,2)
    return abs(prime), positive_result, total_result, liste_resultats_on_x_years
    
    
    
    
# print(client_result_average_best_method('Nice','2025-01-01',1000,100,10))

# prime_pred_2020, pospred2020, totpred2020 = client_result_average_best_method('Nice','2023-12-31',1000,500,5)
# primevraie2020, pos2020, tot2020 = client_result_average_best_method('Nice','2024-12-31',1000,500,5,1)

# print(f"La valeur de la prime prédite est {prime_pred_2020} €, le res pos est {pospred2020} et le total est {totpred2020}")
# print(f"La vraie valeur perdue est {primevraie2020} € ainsi que le res pos {pos2020} € et le total {tot2020} ")
# print(f"Soit un résultat net de prime de {pos2020 - prime_pred_2020}")