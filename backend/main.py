
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
UPLOAD_FOLDER = "static/images"
load_dotenv()

celery = Celery(
    __name__,
    backend='redis://localhost:6379',
    broker='redis://localhost:6379',
    include=['application.celery_tasks'],
    imports=('application.celery_tasks'),

)


def create_app():
    app = Flask(__name__)
    print("starting local development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY",'7cc6619eb68e5c5f5d2ee4fc')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['PDF_UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'pdfs')
    if not os.path.exists(app.config['PDF_UPLOAD_FOLDER']):
        os.makedirs(app.config['PDF_UPLOAD_FOLDER'])
    db.init_app(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'shruanalytics@gmail.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'shruanalytics@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ijjmuxkmwzvupfnw'
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = True
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

    celery.conf.beat_schedule = {
        'daily-visit': {
            'task': 'application.celery_tasks.daily_visit_reminder',
            # 'schedule': crontab(hour=0, minute=0),
            'schedule': 2
        },
        'monthly-report': {
            'task': 'application.celery_tasks.monthly_report',
            # 'schedule': crontab(day_of_month=1, hour=0, minute=0),
            'schedule': 5
        },

    }
    app.app_context().push()
    return app


app = create_app()
if not os.path.exists(os.path.join(app.instance_path, 'database.sqlite3')):
    db.create_all()
    # run only once to create admin user
    b = Bcrypt()
    password = b.generate_password_hash("subash").decode('utf-8')
    user = Users(email="admin@email.com", username="admin",
                 password=password, is_admin=True)
    db.session.add(user)
    db.session.commit()


jwt = JWTManager(app)

CORS(app)

cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://localhost:6379',
    'CACHE_DEFAULT_TIMEOUT': 300
})



# # CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
#

mail = Mail(app)

from application.controllers import *

if __name__ == '__main__':

    celery.conf.update(app.config)
    app.run(debug=True)
