from flask import Blueprint, render_template

template_bp = Blueprint('template', __name__)

@template_bp.route('/templates/<string:name>')
def get_template(name):
    try:
        return render_template(f"{name}.html")
    except:
        return render_template('404.html')
