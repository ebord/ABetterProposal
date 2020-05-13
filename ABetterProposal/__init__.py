import os

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    # Change this to your secret key (can be anything, it's for extra protection)
    app.secret_key = os.urandom(24)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    #@app.route('/hello')
    #def hello():
    #    return 'Hello, World!'

    from . import model
    from . import tables
    from . import forms
    from . import routes
    
    return app