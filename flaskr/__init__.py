import os

from flask import Flask
from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     # SQLALCHEMY_DATABASE_URI='postgres://postgres:mysecretpassword@localhost:5432/identity-service'
    # )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config, silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.secret_key = 'any random string'
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    @app.route('/hello')
    def hello():
        # from . import models
        # db.get_db().execute('INSERT INTO users ("id", "username", "email") VALUES (:id, :username, :email)', id=1,
        #                     username='keith', email='emailTemp')
        from sqlalchemy import Table, MetaData

        # users = Table('users', MetaData(bind=db.get_db()), autoload=True)

        # db.get_db().execute(users.insert(), id=2, username='admin', email='admin@localhost')
        userInfo = db.get_db().execute('select * from users').first()
        print(userInfo)
        return 'Hello, World!'

    return app
