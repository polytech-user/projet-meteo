import pandas as pd
import numpy as np

def CA_plt(CA : float, plt : float, pl_pivot : float) -> float:
    """
    Calcule le chiffre d'affaire à la date t, en cas de pluviométrie de niveau plt.

    Paramètres :
        CA (float) : Chiffre d'affaire maximum journalier
        plt (float) : Niveau de pluviométrie à la date t.
        pl_pivot (float) : Niveau pivot de pluviométrie.

    Retourne :
        float : Chiffre d'affaire ajusté en fonction de la pluviométrie.
    """
    if plt >= pl_pivot:
        return 0
    elif plt > 0 and plt <= pl_pivot:
        f = (pl_pivot - plt) / pl_pivot
        return f*CA
    elif plt == 0:
        return CA
    

def R_plt(CA : float, Cf : float, plt : float, pl_pivot : float) -> float:
    """
    Calcule le résultat à la date t, en cas de pluviométrie de niveau plt.

    Paramètres :
        CA (float): Chiffre d'affaire journalier maximum.
        Cf (float): Coût fixe.
        plt (float): Niveau de pluviométrie à la date t.
        pl_pivot (float): Niveau pivot de pluviométrie.

    Retourne :
        float : Résultat ajusté en fonction de la pluviométrie.
    """
    if plt >= pl_pivot:
        return -Cf
    elif plt > 0 and plt <= pl_pivot:
        f = (pl_pivot - plt) / pl_pivot
        return f*CA - Cf
    elif plt == 0:
        return CA - Cf
    
    

def R_plt_series(CA: float, Cf: float, plt: pd.Series, pl_pivot: float) -> pd.Series:
    """
    Calcule le résultat pour chaque jour en fonction de la pluviométrie (vectorisé).

    Paramètres :
        CA (float): Chiffre d'affaires maximum.
        Cf (float): Coût fixe.
        plt (pd.Series): Niveau de pluviométrie pour chaque jour.
        pl_pivot (float): Niveau pivot de pluviométrie.

    Retourne :
        pd.Series : Résultats ajustés pour chaque jour.
    """
    conditions = [
        plt >= pl_pivot,
        (plt > 0) & (plt < pl_pivot),
        plt == 0
    ]
    valeurs = [
        -Cf,
        ((pl_pivot - plt) / pl_pivot) * CA - Cf,
        CA - Cf
    ]
    return np.select(conditions, valeurs)

    
    
    
