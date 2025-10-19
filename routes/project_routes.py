 from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Project

project_bp = Blueprint('project', __name__, url_prefix='/projects')

@project_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        flash("Project created successfully.")
        return redirect(url_for('dashboard'))
    return render_template('project_new.html')

@project_bp.route('/<int:project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project_view.html', project=project)