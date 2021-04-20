import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from . import db

def setLogger():
    path = os.path.join(os.getcwd(),'logs')
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)   
    LOGGER = logging.getLogger("")
    LOGFILE_NAME = 'logs/app.log'
    hdlr = RotatingFileHandler(LOGFILE_NAME, maxBytes=2000, backupCount=10)
    base_formatter = logging.Formatter(
        "%(asctime)s %(name)s:%(levelname)s %(message)s")
    hdlr.setFormatter(base_formatter)
    LOGGER.addHandler(hdlr)
    LOGGER.setLevel(logging.DEBUG)

def create_app(test_config=None):
    setLogger()
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

    from identity_server.provider import auth
    app.register_blueprint(auth.bp)
    @app.route('/hello')
    def hello():
        # from . import models
        # db.get_db().execute('INSERT INTO users ("id", "username", "email") VALUES (:id, :username, :email)', id=1,
        #                     username='keith', email='emailTemp')
        from sqlalchemy import Table, MetaData
        import json
        # users = Table('users', MetaData(bind=db.get_db()), autoload=True)

        # db.get_db().execute(users.insert(), id=4, username='admin2', email='admin2@localhost')
        userInfo = db.get_db().execute('select * from users')
        print(userInfo)
        # return 'Hello, World!'
        return json.dumps([dict(r) for r in userInfo])

    return app
