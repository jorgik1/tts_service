from flask import Flask
import flask_cors

def create_app():
    app = Flask(__name__)
    flask_cors.CORS(app)  # Enable CORS for all routes

    from .tts import tts_bp
    app.register_blueprint(tts_bp)

    return app