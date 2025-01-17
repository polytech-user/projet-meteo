from flask import Flask, render_template, request

def init_routes(app: Flask):
    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route('/tarification', methods=['GET', 'POST'])
    def tarification():
        if request.method == 'POST':
            chiffre_affaire = request.form['chiffre_affaire']
            couts_fixes = request.form['couts_fixes']
            pluviometrie = request.form['pluviometrie']
            date_souscription = request.form['date_souscription']
            ville = request.form['ville']
            print(date_souscription)
            return render_template("tarification.html", message="Votre formulaire a bien été envoyé.")
        return render_template("tarification.html")


