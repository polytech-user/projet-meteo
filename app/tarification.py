import pandas as pd
from pluie import get_daily_factor_and_proba, get_precipitation_x_years_ago
from calcul import R_plt_series


# Méthode 1 : en utilisant les probabilités et en calculant l'espérance du résultat journalier du commmerce du client
def client_result_expectation(city : str, date : str, CA : float, Cf : float, pl_pivot : float, years: int = 10) -> pd.DataFrame:
    df_val_calcul = get_daily_factor_and_proba(city, date, pl_pivot, years)
    df_exp = pd.DataFrame(df_val_calcul['MM-DD'])
    df_exp['Produit_1ere_ligne'] = -Cf * df_val_calcul['Probabilité_plt_sup_pivot'] # Calcul de P(plt > pivot)*-Cf
    df_exp['Produit_2eme_ligne'] = (df_val_calcul['facteur'] * CA - Cf) * df_val_calcul['Probabilité_0_inf_plt_pivot']
    df_exp['Produit_3eme_ligne'] = (CA - Cf) * df_val_calcul['Probabilité_plt_eq_0']
    df_exp['Espérance'] = df_exp['Produit_1ere_ligne'] + df_exp['Produit_2eme_ligne'] + df_exp['Produit_3eme_ligne']
    total_expectation = df_exp['Espérance'].sum()
    print(f"Espérance totale des résultats journaliers : {total_expectation}")
    return df_exp
# print(client_result_expectation('Nice','2014-01-01',200,100,10))
    

# Méthode 2 : on calcule les résultats journaliers des x dernières années et on fait la moyenne
def client_result_average(city: str, date: str, CA: float, Cf: float, pl_pivot: float, years: int = 10) -> pd.DataFrame:
    df_pluie = get_precipitation_x_years_ago(city, date, years)
    df_pluie['Résultat_jour'] = R_plt_series(CA, Cf, df_pluie['Précipitation'], pl_pivot)
    
    return df_pluie

print(client_result_average('Nice','2014-01-01',200,100,2))

    
    
