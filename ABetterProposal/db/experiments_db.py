from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# Blueprint Configuration
db_bp = Blueprint('db_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

# this will be the experiment db dashboard page, only accessible for loggedin users
@db_bp.route('/experiment_db_dashboard')
def experiment_db_dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db dashboard page
        return render_template('experiment_db_dashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))

# this will be the experiment db proposals page, only accessible for loggedin users
@db_bp.route('/experiment_db_proposals')
def experiment_db_proposals():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db proposals page
        return render_template('experiment_db_proposals.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))

# this will be the experiment db plans page, only accessible for loggedin users
@db_bp.route('/experiment_db_plans')
def experiment_db_plans():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db plans page
        return render_template('experiment_db_plans.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))

# this will be the experiment db teams page, only accessible for loggedin users
@db_bp.route('/experiment_db_teams')
def experiment_db_teams():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the experimental db teams page
        return render_template('experiment_db_teams.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))