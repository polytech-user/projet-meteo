from tarification import client_result_average_best_method
import numpy as np
from datetime import datetime, timedelta

def analyse_retro(city : str, annee : int, CA: float, Cf: float, pl_pivot: float, years: int = 10):
    _, _, _ , liste_resultat = client_result_average_best_method(city, str(annee)+"-12-31",CA, Cf, pl_pivot,1)
    prime_predite, _, _, _ = client_result_average_best_method(city, str(annee-1)+"-12-31",CA, Cf, pl_pivot, years)
    
    liste_resultat = np.round(liste_resultat[1:],2)
    
    total_vrai = np.sum(liste_resultat)
    res_positif_vrai = np.sum(liste_resultat[liste_resultat >= 0])
    
    liste_resultat = liste_resultat.tolist()
    
    resultat_net_de_prime = res_positif_vrai - prime_predite
    
    if resultat_net_de_prime > total_vrai:
        message = f'S\'assurer pour cette année aurait été favorable. En effet, on constate un gain de {np.round(resultat_net_de_prime - total_vrai,2)}€'
    else:
        message = f'S\'assurer pour cette année aurait été défavorable. En effet, on constate une perte de {np.round(total_vrai-resultat_net_de_prime,2)}€'
    
    liste_resultat_non_nul = [r if r >= 0 else 0.0 for r in liste_resultat]
    
    start_date = datetime(annee, 1, 1)
    end_date = datetime(annee, 12, 31)
    delta = end_date - start_date
    
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
    # print(len(dates) == len(liste_resultat))
    return res_positif_vrai, total_vrai, prime_predite, resultat_net_de_prime, liste_resultat, liste_resultat_non_nul, dates, message
    
    
# analyse_retro('Nice', 2021, 1500, 1000, 5)