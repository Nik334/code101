from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from application.models import *
from dotenv import load_dotenv
import os
from celery import Celery
from celery.schedules import crontab
from flask_caching import Cache
from flask_mail import Mail
from datetime import timedelta
import base64

app = None
UPLOAD_FOLDER="static/images"
load_dotenv()

def create_app():
    app=Flask(__name__)
    print("starting local development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

if not os.path.exists(os.path.join(app.instance_path, 'database.sqlite3')):
    db.create_all()
    b=Bcrypt()
    password=b.generate_password_hash("admin").decode('utf-8')
    user=Users(email="admin@email.com", username="admin",password=password, user_type="admin")
    db.session.add(user)
    db.session.commit()
    print("Admin created")
else:
    print("Database already exists")

jwt=JWTManager(app)

CORS(app)

from application.controllers import *

if __name__ == "__main__":
    app.run(debug=True)