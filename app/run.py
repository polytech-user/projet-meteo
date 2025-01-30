from loader import app
from routes import routes

if __name__ == "__main__":
    app.register_blueprint(routes)
    app.run(debug=True, host="0.0.0.0", port=5000)
