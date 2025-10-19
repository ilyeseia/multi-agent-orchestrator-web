from flask import Blueprint, render_template, session, redirect, url_for
from models import User, Project

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    projects = Project.query.filter_by(owner_id=user.id).all()
    return render_template('dashboard.html', user=user, projects=projects)
