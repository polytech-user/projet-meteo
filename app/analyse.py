from tarification import client_result_average_best_method
import numpy as np

def analyse_retro(city : str, annee : int, CA: float, Cf: float, pl_pivot: float, years: int = 10):
    _, _, _ , liste_resultat = client_result_average_best_method(city, str(annee)+"-12-31",CA, Cf, pl_pivot,1)
    prime_predite, _, _, _ = client_result_average_best_method(city, str(annee-1)+"-12-31",CA, Cf, pl_pivot, years)
    
    liste_resultat = liste_resultat[1:]
    
    total_vrai = np.sum(liste_resultat)
    res_positif_vrai = np.sum(liste_resultat[liste_resultat >= 0])
    
    liste_resultat = liste_resultat.tolist()
    
    resultat_net_de_prime = res_positif_vrai - prime_predite
    
    liste_resultat_non_nul = [r if r >= 0 else 0.0 for r in liste_resultat]
    return res_positif_vrai, total_vrai, prime_predite, resultat_net_de_prime, liste_resultat, liste_resultat_non_nul
    
    
# print(analyse_retro('Nice', 2024, 1500, 1000, 5))