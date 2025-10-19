from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.auth_routes import auth_bp
from routes.project_routes import project_bp
from routes.dashboard_routes import dashboard_bp
from routes.template_routes import template_bp
from routes.utility_routes import utility_bp
import os

# تهيئة التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/orchestrator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# قاعدة البيانات و Migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# تسجيل Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(template_bp)
app.register_blueprint(utility_bp)

# صفحة الخطأ 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
