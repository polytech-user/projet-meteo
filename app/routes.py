from flask import render_template, request, jsonify, redirect, url_for, session, render_template_string
import numpy as np
import pandas as pd
from bp import routes
from loader import Commune
from tarification import client_result_average_other_method, client_result_average_best_method
from pdfmod import remplacer_texte_stylise_liste
from pluie import get_precipitation_x_years_ago_np, average_annual_precipitation
from analyse import analyse_retro
from datetime import datetime, timedelta



@routes.route('/')
def home():
    return render_template('index.html')
   

@routes.route('/tarification', methods=['GET', 'POST'])
def tarification():
    if request.method == 'POST':
        chiffre_affaire_str = request.form['chiffre_affaire']
        couts_fixes_str = request.form['couts_fixes']
        pluviometrie_str = request.form['pluviometrie']
        chiffre_affaire = float(chiffre_affaire_str)
        couts_fixes = float(couts_fixes_str)
        pluviometrie = float(pluviometrie_str)
        
        today = str((datetime.today().date() - timedelta(days=1)))
        ville = request.form['ville']
        print(today)
        # Call the function with the parameters
        prime, _, _, _ = client_result_average_best_method(ville, today, chiffre_affaire, couts_fixes, pluviometrie)
        prime_str = str(prime)
        
        # Stocke les valeurs en str pour le devis
        session['prime'] = prime
        session['prime_str'] = prime_str
        session['ville'] = ville
        session['CA_str'] = chiffre_affaire_str
        session['CF_str'] = couts_fixes_str
        session['pluvio_str'] = pluviometrie_str
        session['date'] = today
        
        
        # Redirect to the result page without the negative_sum value in the URL
        return redirect(url_for('routes.resultat'))
    return render_template("tarification.html")

@routes.route('/resultat', methods=['GET', 'POST'])
def resultat():
    # Retrieve the negative_sum from the session
    prime = session.get('prime')
    ville = session.get('ville')
    today = session.get('date')
    
    # dates = df['Date'].tolist()
    # precipitations = df['Précipitation'].tolist()
    dates, precipitations, averages = average_annual_precipitation(ville,today)
    dates = dates.tolist()
    precipitations = precipitations.tolist()
    precipitations = [p if not np.isnan(p) else 0.0 for p in precipitations]
   
            
    return render_template('resultat.html', negative_sum=prime, precipitations=precipitations, dates = dates, averages=averages)
        
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



@routes.route('/view')
def view_pdf():
    return render_template('view_pdf.html', filename="devis.pdf")

@routes.route('/generate_quote')
def generate_quote():
    prime = session.get('prime_str')
    chiffre_affaire_str = session.get('CA_str')
    couts_fixes_str = session.get('CF_str')
    pluviometrie_str = session.get('pluvio_str')
    ville = session.get('ville')
    today = session.get('date')
    year, month, day = today.split('-')
    today = '/'.join([day,month,year])
    remplacer_texte_stylise_liste("static/pdfs/devis_template.pdf","static/pdfs/devis.pdf",["$123","492","dd-mm-aaaa","Antibes", "1000 €", "700 €", "2 mm"],[prime + "€",prime + "€","le " + today,ville, chiffre_affaire_str + "€", couts_fixes_str + "€", pluviometrie_str + " mm"])
    return redirect(url_for('routes.view_pdf'))


@routes.route("/analyse-retrospective", methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        chiffre_affaire = float(request.form['chiffre_affaire'])
        couts_fixes = float(request.form['couts_fixes'])
        pluviometrie = float(request.form['pluviometrie'])

        annee = int(request.form['annee'])
        ville = request.form['ville']    
        
        session['CA'] = chiffre_affaire
        session['CF'] = couts_fixes
        session['pluvio'] = pluviometrie
        session['annee'] = annee
        session['ville'] = ville
        
        
        return redirect(url_for('routes.resanalyse'))
    
    return render_template('analyse.html')


@routes.route("/resultat-analyse", methods=['GET', 'POST'])
def resanalyse():
    chiffre_affaire = session.get('CA')
    couts_fixes = session.get('CF')
    pluviometrie = session.get('pluvio')
    annee = session.get('annee')
    ville = session.get('ville')
    
    
    res_positif_vrai, total_vrai, prime_predite, resultat_net_de_prime, liste_resultat, liste_resultat_non_nul, dates, mess = analyse_retro(ville, annee, chiffre_affaire, couts_fixes, pluviometrie)

    
    
    
    return render_template("resultat-analyse.html", res_positif_vrai=res_positif_vrai, total_vrai=total_vrai, prime_predite=prime_predite, resultat_net_de_prime=resultat_net_de_prime, liste_resultat=liste_resultat, liste_resultat_non_nul=liste_resultat_non_nul, dates=dates, annee=annee, mess=mess)