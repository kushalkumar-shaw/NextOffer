import os
from flask import Flask
from flask_login import LoginManager
from config import config
from app.models import db, User

login_manager = LoginManager()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload and AI templates folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.template_folder, 'ai'), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.candidate import candidate_bp
    from app.routes.company import company_bp
    from app.routes.admin import admin_bp
    from app.routes.resume import resume_bp
    from app.routes.main import main_bp
    from app.routes.ai import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        from app.utils import seed_database
        seed_database()

    return app
