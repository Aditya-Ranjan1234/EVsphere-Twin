import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    """Factory to create and configure the Flask application."""
    # Load environment variables from .env if present (useful for local dev)
    load_dotenv()
    app = Flask(__name__)

    # Basic configuration – secret key fallback for dev
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Register blueprints (routes)
    from .routes import main_bp
    from .api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app
