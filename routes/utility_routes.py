from flask import Blueprint, jsonify
from models import db, Project, Execution

utility_bp = Blueprint('utility', __name__, url_prefix='/utility')

@utility_bp.route('/health')
def health_check():
    return jsonify({"status": "ok"}), 200

@utility_bp.route('/stats')
def stats():
    projects_count = Project.query.count()
    executions_count = Execution.query.count()
    return jsonify({
        "projects": projects_count,
        "executions": executions_count
    })