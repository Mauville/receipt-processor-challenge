from flask import Flask

from routes.api_routes import api_blueprint

app = Flask(__name__)

# Add routes
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(port=5000)
