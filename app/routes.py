from flask import render_template, request, jsonify
from bp import routes
from loader import Commune


@routes.route('/')
def home():
    return render_template('index.html')
   

@routes.route('/tarification', methods=['GET', 'POST'])
def tarification():
    if request.method == 'POST':
        chiffre_affaire = request.form['chiffre_affaire']
        couts_fixes = request.form['couts_fixes']
        pluviometrie = request.form['pluviometrie']
        date_souscription = request.form['date_souscription']
        ville = request.form['ville']
        
        return render_template("tarification.html", message="Votre formulaire a bien été envoyé.")
    return render_template("tarification.html")
        
# Route pour l'auto-complétion des villes
@routes.route('/autocomplete', methods=['GET'])
def autocomplete():
    # Récupérer la valeur tapée par l'utilisateur
    query = request.args.get('q', '').lower()  # 'query' est le paramètre envoyé par AJAX
    if query:
        # Recherche les communes qui contiennent la chaîne saisie
        villes = Commune.query.filter(Commune.nom_commune.ilike(f"%{query}%")).limit(4).all()
        # Retourner les résultats sous forme de JSON
        return jsonify([{'id': ville.id, 'nom_commune': ville.nom_commune, 'code_postal': ville.code_postal} for ville in villes])
    return jsonify([])  # Si rien n'est tapé, retourner une liste vide


@routes.route('/test',methods=['GET', 'POST'])
def test():
    return render_template('testSearchCities.html')

