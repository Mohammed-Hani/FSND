from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate
from models import db
from flask_wtf.csrf import CSRFProtect


migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object('config')
#db = SQLAlchemy(app)
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    return app