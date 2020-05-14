from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


# Blueprint Configuration
tools_bp = Blueprint('tools_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

# this will be the experiment tools page, only accessible for loggedin users
@tools_bp.route('/experiment_tools')
def experiment_tools():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('experiment_tools.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('auth_bp.login'))