from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object('config')
#db = SQLAlchemy(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    return app