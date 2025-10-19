from flask import Blueprint, jsonify, render_template

template_bp = Blueprint('template', __name__, url_prefix='/templates')

@template_bp.route('/list')
def list_templates():
    templates = ["base.html", "dashboard.html", "project_new.html", "project_view.html", "login.html", "register.html"]
    return jsonify(templates)