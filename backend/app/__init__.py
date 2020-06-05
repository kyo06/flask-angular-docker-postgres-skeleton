from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from setting import config
from app.celery import create_celery
app_setting = config["development"]

db = SQLAlchemy()
migrate = Migrate()
api = Api()
celery = create_celery()


def create_app(app_name=app_setting):
    app = Flask(__name__)
    app.config.from_object(app_setting)

    CORS(app, origins='*')

    db.init_app(app)
    migrate.init_app(app, db)
    from app.celery import init_celery
    init_celery(celery, app)

    # from app.models.blog import Blog
    # # Init tables. Need the next two lines one time only. Run app after uncommenting once. Or use flask db init
    # # db.create_all()
    # # db.session.commit()

    from app.views import views
    views.register_view(api)
    api.init_app(app)

    # Register the blueprints here

    return app

import app.celery.celery_worker
