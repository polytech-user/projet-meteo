def CA_plt(CA : float, plt : float, pl_pivot : float) -> float:
    """
    Calcule le chiffre d'affaire à la date t, en cas de pluviométrie de niveau plt.

    Paramètres :
        CA (float) : Chiffre d'affaire initial.
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
        CA (float): Chiffre d'affaires.
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
