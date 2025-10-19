from flask import Blueprint, render_template, request, redirect, url_for, session
from models import Project, db

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        project = Project(name=name, description=description, owner_id=session['user_id'])
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('dashboard.dashboard'))
    return render_template('project_new.html')

@project_bp.route('/projects/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_view.html', project=project)
