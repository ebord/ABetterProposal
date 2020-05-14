from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


# Blueprint Configuration
repo_bp = Blueprint('repo_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

# this will be the experiment repo page, only accessible for loggedin users
@repo_bp.route('/experiment_repo')
def experiment_repo():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('experiment_repo.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))
