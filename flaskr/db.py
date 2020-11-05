# import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
# from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # SQLALCHEMY_DATABASE_URI
        g.db = SQLAlchemy(current_app)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
