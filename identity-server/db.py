# import click
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table


def get_db():
    if 'db' not in g:
        # SQLALCHEMY_DATABASE_URI
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True,
                               pool_size=20, max_overflow=0, paramstyle='format')
        g.db = engine.connect()
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    print("DB init")
    app.teardown_appcontext(close_db)
