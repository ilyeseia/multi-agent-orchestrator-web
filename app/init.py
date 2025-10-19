from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://orchestrator:secure_password_123@db:5432/orchestrator_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.project import project_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(project_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
