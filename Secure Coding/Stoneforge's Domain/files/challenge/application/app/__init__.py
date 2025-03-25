from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os, datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'magic_key')

    db.init_app(app)

    from app.models import User

    login_manager.init_app(app)
    login_manager.login_view = 'shop.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .blueprints.shop import shop
    app.register_blueprint(shop)

    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.datetime.now().year}

    return app
