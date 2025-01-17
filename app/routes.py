from flask import Flask, render_template

def init_routes(app: Flask):
    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route('/tarification')
    def about():
        return render_template("tarification.html")


