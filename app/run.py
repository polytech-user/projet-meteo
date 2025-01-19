from loader import app
from routes import routes

if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(debug=True)
