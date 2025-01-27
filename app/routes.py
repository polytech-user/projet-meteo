from flask import render_template, request, jsonify, redirect, url_for, session, render_template_string
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, HoverTool
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
        session['negative_sum'] = negative_sum
        
        # Redirect to the result page without the negative_sum value in the URL
        return redirect(url_for('routes.resultat'))
    return render_template("tarification.html")

@routes.route('/resultat', methods=['GET', 'POST'])
def resultat():
    # Retrieve the negative_sum from the session
    prime = session.get('res')
    return render_template('resultat.html', prime=prime)
        
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


    
@routes.route('/test2')
def test2():
    # Données pour la courbe
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    labels = ["Point A", "Point B", "Point C", "Point D", "Point E"]
    
    source = ColumnDataSource(data={
        'x': x,
        'y': y,
        'label' : labels
    })
    
    # Création du graphique avec Bokeh
    plot = figure(title="Courbe interactive avec HoverTool",
                  x_axis_label='X-axis',
                  y_axis_label='Y-axis',
                  width=700, height=400)
    plot.line('x', 'y', source=source, legend_label="Ligne", line_width=2, color="blue")
    plot.circle('x', 'y', source=source, size=10, color="red")
    
    hover = HoverTool(tooltips=[
        ("","X: @x, Y: @y"),
        ("", "Point : @label")
        
    ], mode="vline")
    plot.add_tools(hover)
    
    # Convertir le graphique en composants HTML
    script, div = components(plot)

    # Rendu dans une page HTML
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graphique Bokeh</title>
            {{ resources|safe }}
        </head>
        <body>
            <h1>Graphique interactif avec Bokeh</h1>
            {{ div|safe }}
            {{ script|safe }}
        </body>
        </html>
    ''', script=script, div=div, resources=CDN.render())
