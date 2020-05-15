import os

from flask_bootstrap import Bootstrap
from flask import Flask, session, render_template, redirect, url_for, flash

from ABetterProposal.auth.auth import auth_bp
from ABetterProposal.admin.admin import admin_bp
from ABetterProposal.db.experiments_db import db_bp
from ABetterProposal.repo.experiments_repo import repo_bp
from ABetterProposal.tools.experiments_tools import tools_bp

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,template_folder='templates')
    bootstrap = Bootstrap(app)

    #app.config['EXPLAIN_TEMPLATE_LOADING'] = True

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

    # this will be the home page, only accessible for loggedin users
    @app.route('/')
    @app.route('/home')
    @app.route('/index')
    def home():
        # Check if user is loggedin
        if 'loggedin' in session:
            # User is loggedin show them the home page
            return render_template('home.html', username=session['username'])
        # User is not loggedin redirect to login page
        return redirect(url_for('auth_bp.login'))


    # add blueprint modules
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(db_bp)
    app.register_blueprint(repo_bp)
    app.register_blueprint(tools_bp)
    
    return app