from flask import Blueprint, jsonify
from .models import Task, db
from .celery import celery_app

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({"message": "Orchestrator Web App is running"})

@main_bp.route('/add_task/<name>')
def add_task(name):
    task = Task(name=name)
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": f"Task {name} added", "id": task.id})
