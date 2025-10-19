"""
Multi-Agent Orchestrator - Web Application
Flask-based interface for easy workflow management
"""

from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid

load_dotenv()

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///orchestrator.db')
app.config['JSON_SORT_KEYS'] = False

# Initialize Extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuration
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'https://n8n.tail7d68dd.ts.net/webhook/orchestrate-v2')
N8N_API_URL = os.getenv('N8N_API_URL', 'https://n8n.tail7d68dd.ts.net/api')

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    """User Model for Authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    api_key = db.Column(db.String(100), unique=True)
    
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_api_key(self):
        self.api_key = str(uuid.uuid4())
        return self.api_key


class Project(db.Model):
    """Project Model"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Project Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, running, success, failed
    
    # Scope
    frontend_features = db.Column(db.JSON)
    backend_features = db.Column(db.JSON)
    timeline = db.Column(db.String(100))
    budget = db.Column(db.String(100))
    
    # Requirements
    scalability = db.Column(db.String(500))
    performance = db.Column(db.String(500))
    availability = db.Column(db.String(100))
    security = db.Column(db.String(500))
    
    # Technologies
    preferred_tech = db.Column(db.JSON)
    constraints = db.Column(db.JSON)
    
    # Results
    prd_document = db.Column(db.JSON)
    architecture = db.Column(db.JSON)
    wireframes = db.Column(db.JSON)
    frontend_code = db.Column(db.JSON)
    backend_code = db.Column(db.JSON)
    test_report = db.Column(db.JSON)
    security_audit = db.Column(db.JSON)
    deployment_config = db.Column(db.JSON)
    release_notes = db.Column(db.JSON)
    
    # Execution Info
    execution_id = db.Column(db.String(100))
    coverage = db.Column(db.Float)
    vulnerabilities = db.Column(db.Integer)
    quality_passed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    executions = db.relationship('Execution', backref='project', lazy=True, cascade='all, delete-orphan')


class Execution(db.Model):
    """Execution History Model"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    execution_id = db.Column(db.String(100), unique=True)
    
    status = db.Column(db.String(50))
    phase = db.Column(db.String(100))
    progress = db.Column(db.Integer, default=0)
    
    request_data = db.Column(db.JSON)
    response_data = db.Column(db.JSON)
    error_message = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in seconds


# ==================== AUTHENTICATION ROUTES ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Validation
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create User
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.generate_api_key()
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user.id,
            'api_key': user.api_key
        }), 201
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User Login"""
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            login_user(user)
            return jsonify({
                'message': 'Login successful',
                'user_id': user.id,
                'api_key': user.api_key
            }), 200
        
        return jsonify({'error': 'Invalid email or password'}), 401
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User Logout"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


# ==================== PROJECT ROUTES ====================

@app.route('/api/projects', methods=['GET', 'POST'])
@login_required
def projects():
    """Get or Create Projects"""
    if request.method == 'POST':
        data = request.get_json()
        
        # Create Project
        project = Project(
            project_id=f"proj-{datetime.utcnow().timestamp()}-{uuid.uuid4().hex[:8]}",
            user_id=session.get('user_id'),
            name=data['projectName'],
            description=data.get('description'),
            frontend_features=data['scope'].get('frontend', []),
            backend_features=data['scope'].get('backend', []),
            timeline=data['scope'].get('timeline'),
            budget=data['scope'].get('budget'),
            scalability=data['requirements'].get('scalability'),
            performance=data['requirements'].get('performance'),
            availability=data['requirements'].get('availability'),
            security=data['requirements'].get('security'),
            preferred_tech=data.get('technologies', {}).get('preferred', []),
            constraints=data.get('technologies', {}).get('constraints', [])
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Execute Workflow
        execution_result = execute_workflow(data, project.id)
        
        if execution_result['success']:
            project.status = 'running'
            project.execution_id = execution_result['execution_id']
            db.session.commit()
            
            return jsonify({
                'message': 'Project created and workflow started',
                'project_id': project.id,
                'execution_id': execution_result['execution_id']
            }), 201
        else:
            db.session.delete(project)
            db.session.commit()
            return jsonify({'error': execution_result['error']}), 500
    
    # GET: Fetch user projects
    user_projects = Project.query.filter_by(user_id=session.get('user_id')).all()
    
    return jsonify([{
        'id': p.id,
        'project_id': p.project_id,
        'name': p.name,
        'status': p.status,
        'created_at': p.created_at.isoformat(),
        'coverage': p.coverage,
        'vulnerabilities': p.vulnerabilities,
        'quality_passed': p.quality_passed
    } for p in user_projects]), 200


@app.route('/api/projects/<int:project_id>')
@login_required
def get_project(project_id):
    """Get Project Details"""
    project = Project.query.filter_by(id=project_id, user_id=session.get('user_id')).first()
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({
        'id': project.id,
        'project_id': project.project_id,
        'name': project.name,
        'description': project.description,
        'status': project.status,
        'scope': {
            'frontend': project.frontend_features,
            'backend': project.backend_features,
            'timeline': project.timeline,
            'budget': project.budget
        },
        'requirements': {
            'scalability': project.scalability,
            'performance': project.performance,
            'availability': project.availability,
            'security': project.security
        },
        'technologies': {
            'preferred': project.preferred_tech,
            'constraints': project.constraints
        },
        'results': {
            'prd': project.prd_document,
            'architecture': project.architecture,
            'wireframes': project.wireframes,
            'frontend_code': project.frontend_code,
            'backend_code': project.backend_code,
            'tests': project.test_report,
            'security': project.security_audit,
            'deployment': project.deployment_config,
            'release_notes': project.release_notes
        },
        'quality': {
            'coverage': project.coverage,
            'vulnerabilities': project.vulnerabilities,
            'passed': project.quality_passed
        },
        'created_at': project.created_at.isoformat(),
        'completed_at': project.completed_at.isoformat() if project.completed_at else None
    }), 200


@app.route('/api/projects/<int:project_id>/executions')
@login_required
def get_executions(project_id):
    """Get Project Execution History"""
    project = Project.query.filter_by(id=project_id, user_id=session.get('user_id')).first()
    
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    executions = Execution.query.filter_by(project_id=project_id).all()
    
    return jsonify([{
        'id': e.id,
        'execution_id': e.execution_id,
        'status': e.status,
        'phase': e.phase,
        'progress': e.progress,
        'created_at': e.created_at.isoformat(),
        'completed_at': e.completed_at.isoformat() if e.completed_at else None,
        'duration': e.duration
    } for e in executions]), 200


# ==================== WEBHOOK EXECUTION ====================

def execute_workflow(project_data, project_id):
    """Execute n8n Workflow"""
    try:
        payload = {
            'projectName': project_data['projectName'],
            'description': project_data.get('description'),
            'scope': project_data.get('scope', {}),
            'requirements': project_data.get('requirements', {}),
            'technologies': project_data.get('technologies', {}),
            'targetAudience': project_data.get('targetAudience', '')
        }
        
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=3600,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Save Execution
            execution = Execution(
                project_id=project_id,
                execution_id=result.get('projectId'),
                status='success',
                request_data=payload,
                response_data=result
            )
            
            db.session.add(execution)
            
            # Update Project
            project = Project.query.get(project_id)
            project.status = 'success'
            project.completed_at = datetime.utcnow()
            project.prd_document = result.get('prd')
            project.architecture = result.get('architecture')
            project.wireframes = result.get('wireframes')
            project.frontend_code = result.get('frontend')
            project.backend_code = result.get('backend')
            project.test_report = result.get('tests')
            project.security_audit = result.get('security')
            project.deployment_config = result.get('deployment')
            project.release_notes = result.get('marketing')
            project.coverage = result.get('quality', {}).get('coverage')
            project.vulnerabilities = result.get('quality', {}).get('vulnerabilities')
            project.quality_passed = result.get('quality', {}).get('passed')
            
            db.session.commit()
            
            return {
                'success': True,
                'execution_id': result.get('projectId')
            }
        else:
            return {
                'success': False,
                'error': f'Workflow execution failed: {response.status_code}'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ==================== WEBHOOK CALLBACK ====================

@app.route('/webhook/callback', methods=['POST'])
def webhook_callback():
    """Receive updates from n8n Workflow"""
    data = request.get_json()
    
    project_id_str = data.get('projectId')
    project = Project.query.filter_by(project_id=project_id_str).first()
    
    if project:
        project.status = data.get('status', 'running')
        project.coverage = data.get('coverage')
        project.vulnerabilities = data.get('vulnerabilities')
        project.quality_passed = data.get('qualityPassed')
        
        if data.get('status') == 'success':
            project.completed_at = datetime.utcnow()
        
        db.session.commit()
    
    return jsonify({'message': 'Update received'}), 200


# ==================== DASHBOARD ROUTES ====================

@app.route('/')
@login_required
def dashboard():
    """Main Dashboard"""
    return render_template('dashboard.html')


@app.route('/project/new')
@login_required
def new_project():
    """Create New Project Form"""
    return render_template('project_new.html')


@app.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    """View Project Details"""
    project = Project.query.filter_by(id=project_id, user_id=session.get('user_id')).first()
    
    if not project:
        return render_template('404.html'), 404
    
    return render_template('project_view.html', project_id=project_id)


# ==================== TEMPLATE ROUTES ====================

@app.route('/templates')
def templates():
    """Project Templates"""
    templates_list = [
        {
            'name': 'E-commerce Platform',
            'description': 'Full-featured online store',
            'timeline': '12 weeks',
            'budget': '$80,000',
            'scope': {
                'frontend': ['Product Catalog', 'Shopping Cart', 'Checkout'],
                'backend': ['Product API', 'Order Processing', 'Payment']
            }
        },
        {
            'name': 'SaaS Application',
            'description': 'Subscription-based application',
            'timeline': '10 weeks',
            'budget': '$60,000',
            'scope': {
                'frontend': ['Dashboard', 'Settings', 'Reports'],
                'backend': ['REST API', 'Database', 'Authentication']
            }
        },
        {
            'name': 'Mobile App',
            'description': 'Cross-platform mobile application',
            'timeline': '8 weeks',
            'budget': '$50,000',
            'scope': {
                'frontend': ['UI/UX', 'Notifications', 'Offline'],
                'backend': ['Sync API', 'Push Notifications', 'DB']
            }
        }
    ]
    
    return jsonify(templates_list), 200


# ==================== UTILITY ROUTES ====================

@app.route('/api/health')
def health():
    """Health Check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/stats')
@login_required
def stats():
    """User Statistics"""
    user_projects = Project.query.filter_by(user_id=session.get('user_id')).all()
    
    total = len(user_projects)
    success = len([p for p in user_projects if p.status == 'success'])
    running = len([p for p in user_projects if p.status == 'running'])
    failed = len([p for p in user_projects if p.status == 'failed'])
    
    avg_coverage = sum([p.coverage for p in user_projects if p.coverage]) / success if success > 0 else 0
    
    return jsonify({
        'total_projects': total,
        'success': success,
        'running': running,
        'failed': failed,
        'average_coverage': round(avg_coverage, 2)
    }), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


# ==================== CLI COMMANDS ====================

@app.cli.command()
def init_db():
    """Initialize Database"""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def create_admin():
    """Create Admin User"""
    admin = User(
        username='admin',
        email='admin@orchestrator.dev'
    )
    admin.set_password('admin@123456')
    admin.generate_api_key()
    
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user created! API Key: {admin.api_key}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(
        debug=os.getenv('DEBUG', True),
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000))
    )
