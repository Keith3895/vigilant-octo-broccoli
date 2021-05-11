import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask,session
from flask_session import Session,SqlAlchemySessionInterface
from .models import db

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
    LOGGER.setLevel(logging.ERROR)

def create_app(test_config=None):
    setLogger()
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_pyfile(test_config, silent=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.secret_key = 'any random string'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
    app.config['SESSION_KEY_PREFIX'] = ''
    app.config['SESSION_SQLALCHEMY'] = db
    # Session(app)
    @app.before_first_request
    def create_tables():
        # session.app.session_interface.db.create_all()
        db.create_all()
    db.init_app(app)
    
    
    # session = 
    
    SqlAlchemySessionInterface(app=app,db=db,table='session',key_prefix='')
    from .provider import oauth2, routes
    oauth2.config_oauth(app)
    app.register_blueprint(routes.bp)


    from .clients import gcp,linkedin,facebook
    app.register_blueprint(gcp.bp)
    app.register_blueprint(linkedin.bp)
    app.register_blueprint(facebook.bp)
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        

    return app
