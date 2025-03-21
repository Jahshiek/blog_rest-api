# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_cors import CORS
from routes.posts_route import posts_bp  # Import Blueprint here
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_password= os.getenv("REDIS_PASSWORD")
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", 6379))

def create_app():
    app = Flask(__name__)
    CORS(posts_bp, origins="*", supports_credentials=True)

    #redis client setup
    try:
        redis_client = redis.Redis(host = redis_host, port = redis_port, password = redis_password, decode_responses=True)
        redis_client.ping()
    except redis.ConnectionError:
        print("⚠️ Redis server not available! Ensure Redis is running.")

    # limiter
    limiter = Limiter(
        key_func = get_remote_address,
        app=app,
        default_limits=["50 per day"],
        storage_uri=f"redis://:{redis_password}@{redis_host}:{redis_port}/0" 
    )


    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(posts_bp, url_prefix='/posts')
    
    return app

