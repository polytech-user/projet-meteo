from flask import render_template, request, jsonify, redirect, url_for, session
from bp import routes
from loader import Commune
from tarification import client_result_average_other_method
from pluie import get_precipitation
from datetime import datetime


@routes.route('/')
def home():
    return render_template('index.html')
   

@routes.route('/tarification', methods=['GET', 'POST'])
def tarification():
    if request.method == 'POST':
        chiffre_affaire = float(request.form['chiffre_affaire'])
        couts_fixes = float(request.form['couts_fixes'])
        pluviometrie = float(request.form['pluviometrie'])
        
        today = str(datetime.today().date())
        ville = request.form['ville']
        
        # Call the function with the parameters
        _, _, negative_sum, _  = client_result_average_other_method(ville, today, chiffre_affaire, couts_fixes, pluviometrie)
        
        # Store the negative_sum in the session
        print(negative_sum)
        session['negative_sum'] = negative_sum
        
        # Redirect to the result page without the negative_sum value in the URL
        return redirect(url_for('routes.resultat'))
    return render_template("tarification.html")

@routes.route('/resultat', methods=['GET', 'POST'])
def resultat():
    # Retrieve the negative_sum from the session
    negative_sum = session.get('negative_sum')
    return render_template('resultat.html', negative_sum=negative_sum)
        
# Route pour l'auto-complétion des villes
@routes.route('/autocomplete', methods=['GET'])
def autocomplete():
    # Récupérer la valeur tapée par l'utilisateur
    query = request.args.get('q', '').lower()  # 'query' est le paramètre envoyé par AJAX
    if query:
        if query.isdigit():  # Vérifie si la query est composée uniquement de chiffres
            # Recherche par code postal
            villes = Commune.query.filter(Commune.code_postal.ilike(f"{query}%")).limit(3).all()
        else:
            # Recherche les communes qui contiennent la chaîne saisie
            villes = Commune.query.filter(Commune.nom_commune.ilike(f"%{query}%")).limit(3).all()
        # Retourner les résultats sous forme de JSON
        return jsonify([{'id': ville.id, 'nom_commune': ville.nom_commune, 'code_postal': ville.code_postal} for ville in villes])
    return jsonify([])  # Si rien n'est tapé, retourner une liste vide


@routes.route('/test',methods=['GET', 'POST'])
def test():
    return render_template('testSearchCities.html')

