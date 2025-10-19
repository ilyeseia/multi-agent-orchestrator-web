from flask import Blueprint, jsonify
from models import User, Project, Execution

utility_bp = Blueprint('utility', __name__)

@utility_bp.route('/api/stats')
def stats():
    users_count = User.query.count()
    projects_count = Project.query.count()
    executions_count = Execution.query.count()
    return jsonify({
        'users': users_count,
        'projects': projects_count,
        'executions': executions_count
    })

@utility_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})
