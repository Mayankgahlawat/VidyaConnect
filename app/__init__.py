from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv # <-- ADD THIS LINE

# Load environment variables
load_dotenv() # <-- ADD THIS LINE

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # This will now work correctly
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Use the DATABASE_URL from environment, but default to the local one
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/vidyaconnect_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes
    app.register_blueprint(routes.main_bp) # For pages, no prefix
    app.register_blueprint(routes.api_bp, url_prefix='/api') # For data, with /api prefix

    return app

