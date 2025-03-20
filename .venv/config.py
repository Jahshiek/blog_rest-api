# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_cors import CORS
from routes.posts_route import posts_bp  # Import Blueprint here

def create_app():
    app = Flask(__name__)
    CORS(posts_bp, origins="*", supports_credentials=True)
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    return app

