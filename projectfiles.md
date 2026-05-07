
          # .gitignore,
          \${language}
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual Environment
venv/
env/
ENV/
.venv/

# Flask
instance/
.webassets-cache/

# Environment variables
.env
.env.*

# SQLite database
*.db
*.sqlite3

# Logs
*.log

# VS Code
.vscode/

# PyCharm
.idea/

# macOS
.DS_Store

# Windows
Thumbs.db

# Distribution / packaging
build/
dist/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Cache
.cache/

# Jupyter Notebook
.ipynb_checkpoints/

# Static generated files
static/uploads/
static/files/

# Temporary files
*.tmp
*.temp

# mypy
.mypy_cache/

# Flask session files
flask_session/

# WeasyPrint temp files
*.pdf
```
---


          # app/models.py,
          \${language}
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'candidate', 'company', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    candidate_profile = db.relationship('CandidateProfile', backref='user', uselist=False)
    company_profile = db.relationship('Company', backref='user', uselist=False)
    applications = db.relationship('Application', backref='candidate', foreign_keys='Application.candidate_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class CandidateProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    gender = db.Column(db.String(20))
    location = db.Column(db.String(120))
    bio = db.Column(db.Text)
    profile_pic = db.Column(db.String(255))
    resume_file = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    education = db.relationship('Education', backref='candidate', cascade='all, delete-orphan')
    experience = db.relationship('Experience', backref='candidate', cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='candidate', cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='candidate', cascade='all, delete-orphan')
    awards = db.relationship('Award', backref='candidate', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CandidateProfile {self.user.email}>'


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate_profile.id'), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    institution = db.Column(db.String(120), nullable=False)
    field = db.Column(db.String(120))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    grade = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate_profile.id'), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    is_current = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate_profile.id'), nullable=False)
    skill_name = db.Column(db.String(120), nullable=False)
    proficiency = db.Column(db.String(20), default='intermediate')  # beginner, intermediate, expert


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate_profile.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    tech_used = db.Column(db.String(255))
    link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Award(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate_profile.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    issuer = db.Column(db.String(120))
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120))
    website = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(120))
    size = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    jobs = db.relationship('Job', backref='company', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Company {self.company_name}>'


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    location = db.Column(db.String(120))
    job_type = db.Column(db.String(50))  # full-time, part-time, internship, remote
    experience_required = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    skills_required = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')  # active, closed
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applications = db.relationship('Application', backref='job', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20), default='applied')  # applied, shortlisted, rejected, hired
    cover_letter = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('candidate_id', 'job_id', name='unique_application'),)

    def __repr__(self):
        return f'<Application {self.candidate_id} - {self.job_id}>'
```
---


          # app/routes/admin.py,
          \${language}
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Company, Job, Application, CandidateProfile
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You must be logged in as admin to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_candidates = User.query.filter_by(role='candidate').count()
    total_companies = User.query.filter_by(role='company').count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(status='active').count()
    total_applications = Application.query.count()

    stats = {
        'total_users': total_users,
        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications
    }

    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html', stats=stats, recent_applications=recent_applications)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '').strip()

    query = User.query

    if role_filter:
        query = query.filter_by(role=role_filter)

    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)

    return render_template('admin/users.html', users=users, role_filter=role_filter)


@admin_bp.route('/user/<int:user_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Cannot deactivate your own account.', 'warning')
        return redirect(url_for('admin.users'))

    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {status} successfully!', 'success')

    return redirect(url_for('admin.users'))


@admin_bp.route('/jobs')
@login_required
@admin_required
def jobs():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '').strip()

    query = Job.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    jobs = query.order_by(Job.posted_at.desc()).paginate(page=page, per_page=20)

    return render_template('admin/jobs.html', jobs=jobs, status_filter=status_filter)


@admin_bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('admin.jobs'))


@admin_bp.route('/applications')
@login_required
@admin_required
def applications():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '').strip()

    query = Application.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    applications = query.order_by(Application.applied_at.desc()).paginate(page=page, per_page=20)

    return render_template('admin/applications.html', applications=applications, status_filter=status_filter)


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    total_candidates = User.query.filter_by(role='candidate').count()
    total_companies = User.query.filter_by(role='company').count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(status='active').count()

    total_applications = Application.query.count()
    hired = Application.query.filter_by(status='hired').count()
    shortlisted = Application.query.filter_by(status='shortlisted').count()

    data = {
        'candidates': total_candidates,
        'companies': total_companies,
        'jobs': total_jobs,
        'active_jobs': active_jobs,
        'applications': total_applications,
        'hired': hired,
        'shortlisted': shortlisted
    }

    return render_template('admin/reports.html', data=data)
```
---


          # app/routes/auth.py,
          \${language}
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, CandidateProfile, Company
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf import FlaskForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class CandidateRegistrationForm(RegistrationForm):
    pass


class CompanyRegistrationForm(RegistrationForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=120)])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'candidate':
            return redirect(url_for('candidate.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company.dashboard'))
        else:
            return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated.', 'warning')
                return redirect(url_for('auth.login'))

            login_user(user)
            next_page = request.args.get('next')

            if user.role == 'candidate':
                return redirect(next_page) if next_page else redirect(url_for('candidate.dashboard'))
            elif user.role == 'company':
                return redirect(next_page) if next_page else redirect(url_for('company.dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register/candidate', methods=['GET', 'POST'])
def register_candidate():
    if current_user.is_authenticated:
        return redirect(url_for('candidate.dashboard'))

    form = CandidateRegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            role='candidate'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        candidate_profile = CandidateProfile(user_id=user.id)
        db.session.add(candidate_profile)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_candidate.html', form=form)


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('company.dashboard'))

    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            role='company'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id=user.id,
            company_name=form.company_name.data
        )
        db.session.add(company)
        db.session.commit()

        flash('Company account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register_company.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))
```
---


          # app/routes/candidate.py,
          \${language}
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import db, CandidateProfile, Job, Application, Education, Experience, Skill, Project, Award
from app.utils import save_upload_file
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, Email
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from functools import wraps

candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidate')


def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'candidate':
            flash('You must be logged in as a candidate to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


class ProfileForm(FlaskForm):
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    location = StringField('Location', validators=[Optional(), Length(max=120)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Update Profile')


class EducationForm(FlaskForm):
    degree = StringField('Degree', validators=[DataRequired()])
    institution = StringField('Institution', validators=[DataRequired()])
    field = StringField('Field of Study', validators=[Optional()])
    start_year = IntegerField('Start Year', validators=[Optional()])
    end_year = IntegerField('End Year', validators=[Optional()])
    grade = StringField('Grade/GPA', validators=[Optional()])
    submit = SubmitField('Save')


class ExperienceForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    role = StringField('Job Title', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    is_current = BooleanField('Currently working here')
    submit = SubmitField('Save')


class SkillForm(FlaskForm):
    skill_name = StringField('Skill', validators=[DataRequired()])
    proficiency = SelectField('Proficiency', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')])
    submit = SubmitField('Add Skill')


class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    tech_used = StringField('Technologies Used', validators=[Optional()])
    link = StringField('Project Link', validators=[Optional()])
    submit = SubmitField('Save')


class AwardForm(FlaskForm):
    title = StringField('Award Title', validators=[DataRequired()])
    issuer = StringField('Issuer', validators=[Optional()])
    date = DateField('Date', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save')


@candidate_bp.route('/dashboard')
@login_required
@candidate_required
def dashboard():
    profile = current_user.candidate_profile
    applications = Application.query.filter_by(candidate_id=current_user.id).all()

    stats = {
        'applications_sent': len(applications),
        'shortlisted': len([a for a in applications if a.status == 'shortlisted']),
        'rejected': len([a for a in applications if a.status == 'rejected']),
        'hired': len([a for a in applications if a.status == 'hired'])
    }

    recent_applications = Application.query.filter_by(candidate_id=current_user.id).order_by(Application.applied_at.desc()).limit(5).all()

    return render_template('candidate/dashboard.html', profile=profile, stats=stats, recent_applications=recent_applications)


@candidate_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@candidate_required
def profile():
    profile = current_user.candidate_profile
    form = ProfileForm()

    if form.validate_on_submit():
        profile.phone = form.phone.data
        profile.location = form.location.data
        profile.bio = form.bio.data

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename:
                filename = save_upload_file(file, current_app.config['UPLOAD_FOLDER'])
                if filename:
                    profile.profile_pic = filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('candidate.profile'))

    form.phone.data = profile.phone
    form.location.data = profile.location
    form.bio.data = profile.bio

    return render_template('candidate/profile.html', profile=profile, form=form)


@candidate_bp.route('/education', methods=['GET', 'POST'])
@login_required
@candidate_required
def education():
    profile = current_user.candidate_profile
    form = EducationForm()

    if form.validate_on_submit():
        education = Education(
            candidate_id=profile.id,
            degree=form.degree.data,
            institution=form.institution.data,
            field=form.field.data,
            start_year=form.start_year.data,
            end_year=form.end_year.data,
            grade=form.grade.data
        )
        db.session.add(education)
        db.session.commit()
        flash('Education added successfully!', 'success')
        return redirect(url_for('candidate.education'))

    return render_template('candidate/education.html', education=profile.education, form=form)


@candidate_bp.route('/education/<int:edu_id>/delete', methods=['POST'])
@login_required
@candidate_required
def delete_education(edu_id):
    education = Education.query.get_or_404(edu_id)
    if education.candidate_id != current_user.candidate_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('candidate.education'))

    db.session.delete(education)
    db.session.commit()
    flash('Education deleted successfully!', 'success')
    return redirect(url_for('candidate.education'))


@candidate_bp.route('/experience', methods=['GET', 'POST'])
@login_required
@candidate_required
def experience():
    profile = current_user.candidate_profile
    form = ExperienceForm()

    if form.validate_on_submit():
        experience = Experience(
            candidate_id=profile.id,
            company=form.company.data,
            role=form.role.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            is_current=form.is_current.data
        )
        db.session.add(experience)
        db.session.commit()
        flash('Experience added successfully!', 'success')
        return redirect(url_for('candidate.experience'))

    return render_template('candidate/experience.html', experience=profile.experience, form=form)


@candidate_bp.route('/experience/<int:exp_id>/delete', methods=['POST'])
@login_required
@candidate_required
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    if exp.candidate_id != current_user.candidate_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('candidate.experience'))

    db.session.delete(exp)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('candidate.experience'))


@candidate_bp.route('/skills', methods=['GET', 'POST'])
@login_required
@candidate_required
def skills():
    profile = current_user.candidate_profile
    form = SkillForm()

    if form.validate_on_submit():
        skill = Skill(
            candidate_id=profile.id,
            skill_name=form.skill_name.data,
            proficiency=form.proficiency.data
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('candidate.skills'))

    return render_template('candidate/skills.html', skills=profile.skills, form=form)


@candidate_bp.route('/skill/<int:skill_id>/delete', methods=['POST'])
@login_required
@candidate_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.candidate_id != current_user.candidate_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('candidate.skills'))

    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('candidate.skills'))


@candidate_bp.route('/projects', methods=['GET', 'POST'])
@login_required
@candidate_required
def projects():
    profile = current_user.candidate_profile
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            candidate_id=profile.id,
            title=form.title.data,
            description=form.description.data,
            tech_used=form.tech_used.data,
            link=form.link.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('candidate.projects'))

    return render_template('candidate/projects.html', projects=profile.projects, form=form)


@candidate_bp.route('/project/<int:proj_id>/delete', methods=['POST'])
@login_required
@candidate_required
def delete_project(proj_id):
    project = Project.query.get_or_404(proj_id)
    if project.candidate_id != current_user.candidate_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('candidate.projects'))

    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('candidate.projects'))


@candidate_bp.route('/awards', methods=['GET', 'POST'])
@login_required
@candidate_required
def awards():
    profile = current_user.candidate_profile
    form = AwardForm()

    if form.validate_on_submit():
        award = Award(
            candidate_id=profile.id,
            title=form.title.data,
            issuer=form.issuer.data,
            date=form.date.data,
            description=form.description.data
        )
        db.session.add(award)
        db.session.commit()
        flash('Award added successfully!', 'success')
        return redirect(url_for('candidate.awards'))

    return render_template('candidate/awards.html', awards=profile.awards, form=form)


@candidate_bp.route('/award/<int:award_id>/delete', methods=['POST'])
@login_required
@candidate_required
def delete_award(award_id):
    award = Award.query.get_or_404(award_id)
    if award.candidate_id != current_user.candidate_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('candidate.awards'))

    db.session.delete(award)
    db.session.commit()
    flash('Award deleted successfully!', 'success')
    return redirect(url_for('candidate.awards'))


@candidate_bp.route('/applications')
@login_required
@candidate_required
def applications():
    applications = Application.query.filter_by(candidate_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('candidate/applications.html', applications=applications)


@candidate_bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
@candidate_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)

    existing_application = Application.query.filter_by(
        candidate_id=current_user.id,
        job_id=job_id
    ).first()

    if existing_application:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('candidate.applications'))

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter', '')
        application = Application(
            candidate_id=current_user.id,
            job_id=job_id,
            cover_letter=cover_letter,
            status='applied'
        )
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('candidate.applications'))

    return render_template('candidate/apply.html', job=job)
```
---


          # app/routes/company.py,
          \${language}
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import db, Company, Job, Application, User, CandidateProfile
from app.utils import save_upload_file
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, URL
from flask_wtf import FlaskForm
from functools import wraps
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/company')


def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'company':
            flash('You must be logged in as a company to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


class CompanyProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[Optional()])
    website = StringField('Website', validators=[Optional(), URL(require_tld=False)])
    location = StringField('Location', validators=[Optional()])
    size = SelectField('Company Size', choices=[
        ('', 'Select Size'),
        ('10-50', '10-50'),
        ('50-200', '50-200'),
        ('200-500', '200-500'),
        ('500-1000', '500-1000'),
        ('1000+', '1000+')
    ], validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Update Profile')


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[Optional()])
    salary_min = FloatField('Salary Min', validators=[Optional()])
    salary_max = FloatField('Salary Max', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    job_type = SelectField('Job Type', choices=[
        ('', 'Select Type'),
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote')
    ], validators=[DataRequired()])
    experience_required = StringField('Experience Required', validators=[Optional()])
    skills_required = StringField('Required Skills (comma-separated)', validators=[Optional()])
    deadline = DateField('Application Deadline', validators=[Optional()])
    submit = SubmitField('Post Job')


@company_bp.route('/dashboard')
@login_required
@company_required
def dashboard():
    company = current_user.company_profile
    total_jobs = Job.query.filter_by(company_id=company.id).count()
    active_jobs = Job.query.filter_by(company_id=company.id, status='active').count()

    total_applications = db.session.query(Application).join(Job).filter(Job.company_id == company.id).count()
    shortlisted = db.session.query(Application).join(Job).filter(
        Job.company_id == company.id,
        Application.status == 'shortlisted'
    ).count()

    stats = {
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'shortlisted': shortlisted
    }

    recent_jobs = Job.query.filter_by(company_id=company.id).order_by(Job.posted_at.desc()).limit(5).all()

    return render_template('company/dashboard.html', company=company, stats=stats, recent_jobs=recent_jobs)


@company_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    company = current_user.company_profile
    form = CompanyProfileForm()

    if form.validate_on_submit():
        company.company_name = form.company_name.data
        company.industry = form.industry.data
        company.website = form.website.data
        company.location = form.location.data
        company.size = form.size.data
        company.description = form.description.data

        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename:
                filename = save_upload_file(file, current_app.config['UPLOAD_FOLDER'])
                if filename:
                    company.logo = filename

        db.session.commit()
        flash('Company profile updated successfully!', 'success')
        return redirect(url_for('company.profile'))

    form.company_name.data = company.company_name
    form.industry.data = company.industry
    form.website.data = company.website
    form.location.data = company.location
    form.size.data = company.size
    form.description.data = company.description

    return render_template('company/profile.html', company=company, form=form)


@company_bp.route('/jobs', methods=['GET', 'POST'])
@login_required
@company_required
def jobs():
    company = current_user.company_profile
    company_jobs = Job.query.filter_by(company_id=company.id).order_by(Job.posted_at.desc()).all()
    return render_template('company/jobs.html', jobs=company_jobs)


@company_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
@company_required
def post_job():
    company = current_user.company_profile
    form = JobForm()

    if form.validate_on_submit():
        job = Job(
            company_id=company.id,
            title=form.title.data,
            description=form.description.data,
            requirements=form.requirements.data,
            salary_min=form.salary_min.data,
            salary_max=form.salary_max.data,
            location=form.location.data,
            job_type=form.job_type.data,
            experience_required=form.experience_required.data,
            skills_required=form.skills_required.data,
            deadline=form.deadline.data,
            status='active'
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('company.jobs'))

    return render_template('company/post_job.html', form=form)


@company_bp.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
@company_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    form = JobForm()
    if form.validate_on_submit():
        job.title = form.title.data
        job.description = form.description.data
        job.requirements = form.requirements.data
        job.salary_min = form.salary_min.data
        job.salary_max = form.salary_max.data
        job.location = form.location.data
        job.job_type = form.job_type.data
        job.experience_required = form.experience_required.data
        job.skills_required = form.skills_required.data
        job.deadline = form.deadline.data
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('company.jobs'))

    form.title.data = job.title
    form.description.data = job.description
    form.requirements.data = job.requirements
    form.salary_min.data = job.salary_min
    form.salary_max.data = job.salary_max
    form.location.data = job.location
    form.job_type.data = job.job_type
    form.experience_required.data = job.experience_required
    form.skills_required.data = job.skills_required
    form.deadline.data = job.deadline

    return render_template('company/edit_job.html', form=form, job=job)


@company_bp.route('/job/<int:job_id>/toggle', methods=['POST'])
@login_required
@company_required
def toggle_job_status(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    job.status = 'closed' if job.status == 'active' else 'active'
    db.session.commit()
    flash(f'Job status changed to {job.status}!', 'success')
    return redirect(url_for('company.jobs'))


@company_bp.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
@company_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('company.jobs'))


@company_bp.route('/job/<int:job_id>/applications')
@login_required
@company_required
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
    return render_template('company/job_applications.html', job=job, applications=applications)


@company_bp.route('/application/<int:app_id>/candidate')
@login_required
@company_required
def view_candidate(app_id):
    application = Application.query.get_or_404(app_id)
    job = application.job
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    candidate_user = User.query.get(application.candidate_id)
    candidate_profile = candidate_user.candidate_profile

    return render_template('company/candidate_profile.html', application=application, candidate_user=candidate_user, candidate_profile=candidate_profile)


@company_bp.route('/application/<int:app_id>/update-status', methods=['POST'])
@login_required
@company_required
def update_application_status(app_id):
    application = Application.query.get_or_404(app_id)
    job = application.job
    if job.company_id != current_user.company_profile.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('company.jobs'))

    new_status = request.form.get('status')
    if new_status in ['applied', 'shortlisted', 'rejected', 'hired']:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}!', 'success')

    return redirect(url_for('company.job_applications', job_id=job.id))
```
---


          # app/routes/main.py,
          \${language}
from flask import Blueprint, render_template, request
from app.models import Job, Company
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    featured_jobs = Job.query.filter_by(status='active').order_by(Job.posted_at.desc()).limit(6).all()

    total_jobs = Job.query.filter_by(status='active').count()
    total_companies = Company.query.count()

    return render_template(
        'index.html',
        featured_jobs=featured_jobs,
        total_jobs=total_jobs,
        total_companies=total_companies
    )


@main_bp.route('/jobs', methods=['GET', 'POST'])
def browse_jobs():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    location = request.args.get('location', '').strip()
    job_type = request.args.get('job_type', '').strip()

    query = Job.query.filter_by(status='active')

    if search:
        query = query.filter(
            or_(
                Job.title.ilike(f'%{search}%'),
                Job.description.ilike(f'%{search}%')
            )
        )

    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))

    if job_type:
        query = query.filter_by(job_type=job_type)

    jobs = query.order_by(Job.posted_at.desc()).paginate(page=page, per_page=10)

    return render_template(
        'jobs/browse.html',
        jobs=jobs,
        search=search,
        location=location,
        job_type=job_type
    )


@main_bp.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    company = job.company
    return render_template('jobs/detail.html', job=job, company=company)
```
---


          # app/routes/resume.py,
          \${language}
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import CandidateProfile
from io import BytesIO
from functools import wraps
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

resume_bp = Blueprint('resume', __name__, url_prefix='/resume')


def candidate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'candidate':
            flash('You must be logged in as a candidate to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def prepare_resume_data():
    profile = current_user.candidate_profile
    return {
        'name': current_user.name,
        'email': current_user.email,
        'phone': profile.phone or '',
        'location': profile.location or '',
        'bio': profile.bio or '',
        'education': profile.education,
        'experience': profile.experience,
        'skills': profile.skills,
        'projects': profile.projects,
        'awards': profile.awards
    }


@resume_bp.route('/builder')
@login_required
@candidate_required
def builder():
    resume_data = prepare_resume_data()
    return render_template('resume/builder.html', resume_data=resume_data)


@resume_bp.route('/preview/<template>', methods=['GET', 'POST'])
@login_required
@candidate_required
def preview(template):
    resume_data = prepare_resume_data()

    if template not in ['classic', 'modern', 'creative']:
        flash('Invalid template selected.', 'danger')
        return redirect(url_for('resume.builder'))

    template_file = f'resume/templates/{template}_resume.html'
    return render_template(template_file, resume_data=resume_data)


@resume_bp.route('/download/<template>')
@login_required
@candidate_required
def download(template):
    resume_data = prepare_resume_data()

    if template not in ['classic', 'modern', 'creative']:
        flash('Invalid template selected.', 'danger')
        return redirect(url_for('resume.builder'))

    buffer = BytesIO()
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0A1628'),
        spaceAfter=6,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=6,
        borderBottomWidth=1,
        borderBottomColor=colors.HexColor('#2563EB')
    )

    elements = []

    # Header
    elements.append(Paragraph(resume_data['name'], title_style))
    contact_info = f"{resume_data['email']}"
    if resume_data['phone']:
        contact_info += f" | {resume_data['phone']}"
    if resume_data['location']:
        contact_info += f" | {resume_data['location']}"
    elements.append(Paragraph(f"<font size=9>{contact_info}</font>", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Professional Summary
    if resume_data['bio']:
        elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        elements.append(Paragraph(resume_data['bio'], styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

    # Experience
    if resume_data['experience']:
        elements.append(Paragraph("EXPERIENCE", heading_style))
        for exp in resume_data['experience']:
            exp_text = f"<b>{exp.role}</b> | {exp.company}"
            elements.append(Paragraph(exp_text, styles['Normal']))
            dates = f"{exp.start_date.strftime('%b %Y')} - "
            dates += f"{exp.end_date.strftime('%b %Y')}" if exp.end_date else "Present"
            elements.append(Paragraph(f"<font size=9>{dates}</font>", styles['Normal']))
            if exp.description:
                elements.append(Paragraph(exp.description, styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))

    # Education
    if resume_data['education']:
        elements.append(Paragraph("EDUCATION", heading_style))
        for edu in resume_data['education']:
            edu_text = f"<b>{edu.degree}</b>"
            if edu.field:
                edu_text += f" in {edu.field}"
            elements.append(Paragraph(edu_text, styles['Normal']))
            elements.append(Paragraph(edu.institution, styles['Normal']))
            if edu.start_year:
                year_text = f"{edu.start_year}"
                if edu.end_year:
                    year_text += f" - {edu.end_year}"
                elements.append(Paragraph(f"<font size=9>{year_text}</font>", styles['Normal']))
            elements.append(Spacer(1, 0.08*inch))

    # Skills
    if resume_data['skills']:
        elements.append(Paragraph("SKILLS", heading_style))
        skills_text = ", ".join([f"{s.skill_name} ({s.proficiency})" for s in resume_data['skills']])
        elements.append(Paragraph(skills_text, styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

    # Projects
    if resume_data['projects']:
        elements.append(Paragraph("PROJECTS", heading_style))
        for proj in resume_data['projects']:
            elements.append(Paragraph(f"<b>{proj.title}</b>", styles['Normal']))
            if proj.description:
                elements.append(Paragraph(proj.description, styles['Normal']))
            if proj.tech_used:
                elements.append(Paragraph(f"<font size=9><i>Tech: {proj.tech_used}</i></font>", styles['Normal']))
            elements.append(Spacer(1, 0.08*inch))

    # Awards
    if resume_data['awards']:
        elements.append(Paragraph("AWARDS & ACHIEVEMENTS", heading_style))
        for award in resume_data['awards']:
            award_text = f"<b>{award.title}</b>"
            if award.issuer:
                award_text += f" | {award.issuer}"
            elements.append(Paragraph(award_text, styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))

    # Generate PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    doc.build(elements)

    buffer.seek(0)
    filename = f"resume_{current_user.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
```
---


          # app/routes/__init__.py,
          \${language}

```
---


          # app/routes/__pycache__/admin.cpython-314.pyc,
          \${language}
+
    X��i  �                   �\  � ^ RI HtHtHtHtHtHtHt ^ RIH	t	H
t
 ^ RIHtHtHtHtHtHt ^ RIHt ]! R]RR7      tR t]P/                  R	4      ]	]R
 4       4       4       t]P/                  R4      ]	]R 4       4       4       t]P/                  RR.R7      ]	]R 4       4       4       t]P/                  R4      ]	]R 4       4       4       t]P/                  RR.R7      ]	]R 4       4       4       t]P/                  R4      ]	]R 4       4       4       t]P/                  R4      ]	]R 4       4       4       tR# )�    )�	Blueprint�render_template�request�redirect�url_for�flash�jsonify)�login_required�current_user)�db�User�Company�Job�Application�CandidateProfile��wraps�adminz/admin)�
url_prefixc                 �0   a � \        S 4      V 3R  l4       pV# )c                  �   <� \         P                  '       d   \         P                  R 8w  d!   \        RR4       \	        \        R4      4      # S! V / VB # )r   z3You must be logged in as admin to access this page.�warningz
auth.login)r   �is_authenticated�roler   r   r   )�args�kwargs�fs   *,��0C:\Coding\Projects\NextOffer\app\routes\admin.py�decorated_function�*admin_required.<locals>.decorated_function
   sG   �� ��,�,�,��0A�0A�W�0L��G��S��G�L�1�2�2��$�!�&�!�!�    r   )r   r   s   f r   �admin_requiredr"   	   s!   �� �
�1�X�"� �"�
 �r!   z
/dashboardc                  �  � \         P                  P                  4       p \         P                  P                  R R7      P                  4       p\         P                  P                  RR7      P                  4       p\        P                  P                  4       p\        P                  P                  RR7      P                  4       p\
        P                  P                  4       pRV RVRVRVR	VR
V/p\
        P                  P                  \
        P                  P                  4       4      P                  ^
4      P                  4       p\        RWgR7      # )�	candidate�r   �company�active��status�total_users�total_candidates�total_companies�
total_jobs�active_jobs�total_applicationszadmin/dashboard.html)�stats�recent_applications)r   �query�count�	filter_byr   r   �order_by�
applied_at�desc�limit�allr   )r*   r+   r,   r-   r.   r/   r0   r1   s           r   �	dashboardr:      s  � � �*�*�"�"�$�K��z�z�+�+��+�=�C�C�E���j�j�*�*�	�*�:�@�@�B�O������"�J��)�)�%�%�X�%�6�<�<�>�K�$�*�*�0�0�2�� 	�{��,��?��j��{��0��E� &�+�+�4�4�[�5K�5K�5P�5P�5R�S�Y�Y�Z\�]�a�a�c���1��h�hr!   z/usersc                  �  � \         P                  P                  R ^\        R7      p \         P                  P                  RR4      P	                  4       p\
        P                  pV'       d   VP                  VR7      pVP                  \
        P                  P                  4       4      P                  V ^R7      p\        RW1R7      # )�page��typer   � r%   �r<   �per_pagezadmin/users.html)�users�role_filter)r   r   �get�int�stripr   r2   r4   r5   �
created_atr7   �paginater   )r<   rC   r2   rB   s       r   rB   rB   ,   s�   � � �<�<���F�A�C��0�D��,�,�"�"�6�2�.�4�4�6�K��J�J�E�����[��1���N�N�4�?�?�/�/�1�2�;�;��PR�;�S�E��-�U�T�Tr!   z/user/<int:user_id>/toggle�POST)�methodsc                 �  � \         P                  P                  V 4      pVP                  \        P                  8X  d!   \        R R4       \        \        R4      4      # VP                  '       * Vn        \        P                  P                  4        VP                  '       d   RMRp\        RV R2R4       \        \        R4      4      # )z#Cannot deactivate your own account.r   zadmin.users�	activated�deactivatedzUser z successfully!�success)r   r2   �
get_or_404�idr   r   r   r   �	is_activer   �session�commit)�user_id�userr)   s   &  r   �toggle_user_statusrV   =   s�   � � �:�:� � ��)�D��w�w�,�/�/�!��3�Y�?����.�/�/����'�D�N��J�J���� �N�N�N�[��F�	�E�&���
(�)�4��G�M�*�+�+r!   z/jobsc                  �  � \         P                  P                  R ^\        R7      p \         P                  P                  RR4      P	                  4       p\
        P                  pV'       d   VP                  VR7      pVP                  \
        P                  P                  4       4      P                  V ^R7      p\        RW1R7      # )r<   r=   r)   r?   r(   r@   zadmin/jobs.html)�jobs�status_filter)r   r   rD   rE   rF   r   r2   r4   r5   �	posted_atr7   rH   r   )r<   rY   r2   rX   s       r   rX   rX   O   s�   � � �<�<���F�A�C��0�D��L�L�$�$�X�r�2�8�8�:�M��I�I�E�����}��5���>�>�#�-�-�,�,�.�/�8�8�d�R�8�P�D��,�4�U�Ur!   z/job/<int:job_id>/deletec                 ��   � \         P                  P                  V 4      p\        P                  P                  V4       \        P                  P                  4        \        R R4       \        \        R4      4      # )zJob deleted successfully!rN   z
admin.jobs)
r   r2   rO   r   rR   �deleterS   r   r   r   )�job_id�jobs   & r   �
delete_jobr_   `   sU   � � �)�)�
�
�v�
&�C��J�J���c���J�J����	�
%�y�1��G�L�)�*�*r!   z/applicationsc                  �  � \         P                  P                  R ^\        R7      p \         P                  P                  RR4      P	                  4       p\
        P                  pV'       d   VP                  VR7      pVP                  \
        P                  P                  4       4      P                  V ^R7      p\        RW1R7      # )r<   r=   r)   r?   r(   r@   zadmin/applications.html)�applicationsrY   )r   r   rD   rE   rF   r   r2   r4   r5   r6   r7   rH   r   )r<   rY   r2   ra   s       r   ra   ra   k   s�   � � �<�<���F�A�C��0�D��L�L�$�$�X�r�2�8�8�:�M����E�����}��5���>�>�+�"8�"8�"=�"=�"?�@�I�I�t�^`�I�a�L��4�<�m�mr!   z/reportsc                  �  � \         P                  P                  R R7      P                  4       p \         P                  P                  RR7      P                  4       p\        P                  P                  4       p\        P                  P                  RR7      P                  4       p\
        P                  P                  4       p\
        P                  P                  RR7      P                  4       p\
        P                  P                  RR7      P                  4       pRV RVR	VR
VRVRVRV/p\        RVR7      # )r$   r%   r&   r'   r(   �hired�shortlisted�
candidates�	companiesrX   r.   ra   zadmin/reports.html)�data)r   r2   r4   r3   r   r   r   )r+   r,   r-   r.   r/   rc   rd   rg   s           r   �reportsrh   |   s  � � �z�z�+�+��+�=�C�C�E���j�j�*�*�	�*�:�@�@�B�O������"�J��)�)�%�%�X�%�6�<�<�>�K�$�*�*�0�0�2�����'�'�w�'�7�=�=�?�E��#�#�-�-�]�-�C�I�I�K�K� 	�&��_��
��{��*����{��D� �/�d�;�;r!   N)�flaskr   r   r   r   r   r   r	   �flask_loginr
   r   �
app.modelsr   r   r   r   r   r   �	functoolsr   �__name__�admin_bpr"   �router:   rB   rV   rX   r_   ra   rh   � r!   r   �<module>rq      s  �� X� X� X� 4� L� L� ��W�h�8�<��� 
�������i� � � �i�, 
�������U� � � �U� 
���,�v�h��?���,� � � @�,� 
�������V� � � �V� 
���*�V�H��=���+� � � >�+� 
���� ���n� � � !�n� 
���
����<� � � �<r!   
```
---


          # app/routes/__pycache__/auth.cpython-314.pyc,
          \${language}
+
    X��iA  �                   ��  � ^ RI HtHtHtHtHtHt ^ RIHtH	t	H
t
Ht ^ RIHtHtHtHt ^ RIHtHtHtHt ^ RIHtHtHtHtHt ^ RIHt ]! R]RR	7      t ! R
 R]4      t  ! R R] 4      t! ! R R] 4      t" ! R R]4      t#]PI                  RRR.R7      R 4       t%]PI                  RRR.R7      R 4       t&]PI                  RRR.R7      R 4       t']PI                  R4      ]
R 4       4       t(R# )�    )�	Blueprint�render_template�request�redirect�url_for�flash)�
login_user�logout_user�login_required�current_user)�db�User�CandidateProfile�Company)�StringField�PasswordField�SubmitField�SelectField)�DataRequired�Email�EqualTo�ValidationError�Length)�	FlaskForm�authz/auth)�
url_prefixc            	       ��   a � ] tR t^t o ]! R]! 4       ]! ^^xR7      .R7      t]! R]! 4       ]! 4       .R7      t	]
! R]! 4       ]! ^R7      .R7      t]
! R]! 4       ]! R4      .R7      t]! R	4      tR
 tRtV tR# )�RegistrationFormz	Full Name��min�max��
validatorsr   �Password)r    zConfirm Password�password�Registerc                �   � \         P                  P                  VP                  R 7      P	                  4       pV'       d   \        R4      hR# )��emailzEmail already registered.N)r   �query�	filter_by�data�firstr   )�selfr)   �users   && �/C:\Coding\Projects\NextOffer\app\routes\auth.py�validate_email�RegistrationForm.validate_email   s:   � ��z�z�#�#�%�*�*�#�5�;�;�=���!�"=�>�>� �    � N)�__name__�
__module__�__qualname__�__firstlineno__r   r   r   �namer   r)   r   r%   r   �confirm_passwordr   �submitr1   �__static_attributes__�__classdictcell__)�__classdict__s   @r0   r   r      s}   �� � ��{����1�RU�@V�/W�X�D���\�^�U�W�,E�F�E��Z�\�^�V�PQ�]�4S�T�H�$�%7�\�^�U\�]g�Uh�Di�j����$�F�?� ?r3   r   c                   �   � ] tR t^tRtR# )�CandidateRegistrationFormr4   N)r5   r6   r7   r8   r<   r4   r3   r0   r@   r@      s   � �r3   r@   c            	       �H   � ] tR t^t]! R]! 4       ]! ^^xR7      .R7      tRtR# )�CompanyRegistrationFormzCompany Namer   r"   r4   N)	r5   r6   r7   r8   r   r   r   �company_namer<   r4   r3   r0   rB   rB      s   � ��~�<�>�6�VW�]`�Ka�:b�c�Lr3   rB   c                   �r   � ] tR t^ t]! R]! 4       ]! 4       .R7      t]! R]! 4       .R7      t	]
! R4      tRtR# )�	LoginFormr   r"   r$   �Loginr4   N)r5   r6   r7   r8   r   r   r   r)   r   r%   r   r;   r<   r4   r3   r0   rE   rE       s2   � ���\�^�U�W�,E�F�E��Z�\�^�4D�E�H���!�Fr3   rE   z/login�GET�POST)�methodsc                  �@  � \         P                  '       dg   \         P                  R 8X  d   \        \	        R4      4      # \         P                  R8X  d   \        \	        R4      4      # \        \	        R4      4      # \        4       p V P                  4       '       Edv   \        P                  P                  V P                  P                  R7      P                  4       pV'       Ed   VP                  V P                  P                  4      '       d�   VP                  '       g!   \!        RR4       \        \	        R4      4      # \#        V4       \$        P&                  P)                  R	4      pVP                  R 8X  d(   V'       d   \        V4      # \        \	        R4      4      # VP                  R8X  d(   V'       d   \        V4      # \        \	        R4      4      # V'       d   \        V4      # \        \	        R4      4      # \!        R
R4       \+        RV R7      # )�	candidate�candidate.dashboard�company�company.dashboardzadmin.dashboardr(   z"Your account has been deactivated.�warning�
auth.login�nextzInvalid email or password.�dangerzauth/login.html��form)r   �is_authenticated�roler   r   rE   �validate_on_submitr   r*   r+   r)   r,   r-   �check_passwordr%   �	is_activer   r	   r   �args�getr   )rT   r/   �	next_pages      r0   �loginr]   &   s�  � ��$�$�$�����+��G�$9�:�;�;����)�+��G�$7�8�9�9��G�$5�6�7�7��;�D���� � ��z�z�#�#�$�*�*�/�/�#�:�@�@�B���4�D�'�'����(:�(:�;�;��>�>�>��:�I�F���� 5�6�6��t�����(�(��0�I��y�y�K�'�.7�x�	�*�e�X�g�Nc�Fd�=e�e����i�'�.7�x�	�*�c�X�g�Na�Fb�=c�c�.7�x�	�*�a�X�g�N_�F`�=a�a��.��9��,�4�8�8r3   z/register/candidatec                  ��  � \         P                  '       d   \        \        R 4      4      # \	        4       p V P                  4       '       Ed   \        V P                  P                  V P                  P                  RR7      pVP                  V P                  P                  4       \        P                  P                  V4       \        P                  P                  4        \!        VP"                  R7      p\        P                  P                  V4       \        P                  P%                  4        \'        RR4       \        \        R4      4      # \)        RV R7      # )	rL   rK   �r9   r)   rV   )�user_idz,Account created successfully! Please log in.�successrP   zauth/register_candidate.htmlrS   )r   rU   r   r   r@   rW   r   r9   r,   r)   �set_passwordr%   r   �session�add�flushr   �id�commitr   r   )rT   r/   �candidate_profiles      r0   �register_candidateri   G   s�   � ��$�$�$��� 5�6�7�7�$�&�D���� � ��������*�*�/�/��
��
 	���$�-�-�,�,�-�
�
�
���t��
�
�
����,�T�W�W�=��
�
�
���(�)�
�
�
�����<�i�H����-�.�.��9��E�Er3   z/register/companyc                  ��  � \         P                  '       d   \        \        R 4      4      # \	        4       p V P                  4       '       Ed!   \        V P                  P                  V P                  P                  RR7      pVP                  V P                  P                  4       \        P                  P                  V4       \        P                  P                  4        \!        VP"                  V P$                  P                  R7      p\        P                  P                  V4       \        P                  P'                  4        \)        RR4       \        \        R4      4      # \+        RV R7      # )	rN   rM   r_   )r`   rC   z4Company account created successfully! Please log in.ra   rP   zauth/register_company.htmlrS   )r   rU   r   r   rB   rW   r   r9   r,   r)   rb   r%   r   rc   rd   re   r   rf   rC   rg   r   r   )rT   r/   rM   s      r0   �register_companyrk   a   s�   � ��$�$�$��� 3�4�5�5�"�$�D���� � ��������*�*�/�/��
��
 	���$�-�-�,�,�-�
�
�
���t��
�
�
������G�G��*�*�/�/�
�� 	�
�
���w��
�
�
�����D�i�P����-�.�.��7�d�C�Cr3   z/logoutc                  �V   � \        4        \        R R4       \        \        R4      4      # )z&You have been logged out successfully.�infoz
main.index)r
   r   r   r   r4   r3   r0   �logoutrn   ~   s$   � � �M�	�
2�F�;��G�L�)�*�*r3   N))�flaskr   r   r   r   r   r   �flask_loginr	   r
   r   r   �
app.modelsr   r   r   r   �wtformsr   r   r   r   �wtforms.validatorsr   r   r   r   r   �	flask_wtfr   r5   �auth_bpr   r@   rB   rE   �router]   ri   rk   rn   r4   r3   r0   �<module>rw      s  �� O� O� M� M� :� :� H� H� T� T� �
�F�H��
9��
?�y� 
?�	� 0� 	�d�.� d�"�	� "� 	���x�%����1�9� 2�9�@ 	���$�u�f�o��>�F� ?�F�2 	���"�U�F�O��<�D� =�D�8 	���y���+� � �+r3   
```
---


          # app/routes/__pycache__/candidate.cpython-314.pyc,
          \${language}
+
    X��i�0  �                   �d  � ^ RI HtHtHtHtHtHtHt ^ RIH	t	H
t
 ^ RIHtHtHtHtHtHtHtHtHt ^ RIHt ^ RIHtHtHtHtHtHtHt ^ RIH t H!t!H"t"H#t# ^ RI$H%t% ^ RI&H't' ^ R	I(H)t) ]! R
]*RR7      t+R t, ! R R]%4      t- ! R R]%4      t. ! R R]%4      t/ ! R R]%4      t0 ! R R]%4      t1 ! R R]%4      t2]+Pg                  R4      ]	],R 4       4       4       t4]+Pg                  RRR.R7      ]	],R  4       4       4       t5]+Pg                  R!RR.R7      ]	],R" 4       4       4       t6]+Pg                  R#R.R7      ]	],R$ 4       4       4       t7]+Pg                  R%RR.R7      ]	],R& 4       4       4       t8]+Pg                  R'R.R7      ]	],R( 4       4       4       t9]+Pg                  R)RR.R7      ]	],R* 4       4       4       t:]+Pg                  R+R.R7      ]	],R, 4       4       4       t;]+Pg                  R-RR.R7      ]	],R. 4       4       4       t<]+Pg                  R/R.R7      ]	],R0 4       4       4       t=]+Pg                  R1RR.R7      ]	],R2 4       4       4       t>]+Pg                  R3R.R7      ]	],R4 4       4       4       t?]+Pg                  R54      ]	],R6 4       4       4       t@]+Pg                  R7RR.R7      ]	],R8 4       4       4       tAR9# ):�    )�	Blueprint�render_template�request�redirect�url_for�flash�current_app)�login_required�current_user)	�db�CandidateProfile�Job�Application�	Education�
Experience�Skill�Project�Award)�save_upload_file)�StringField�TextAreaField�SelectField�IntegerField�
FloatField�SubmitField�BooleanField)�DataRequired�Optional�Length�Email)�	FlaskForm)�	DateField��wraps�	candidatez
/candidate)�
url_prefixc                 �0   a � \        S 4      V 3R  l4       pV# )c                  �   <� \         P                  '       d   \         P                  R 8w  d!   \        RR4       \	        \        R4      4      # S! V / VB # )r%   z9You must be logged in as a candidate to access this page.�warningz
auth.login)r   �is_authenticated�roler   r   r   )�args�kwargs�fs   *,��4C:\Coding\Projects\NextOffer\app\routes\candidate.py�decorated_function�.candidate_required.<locals>.decorated_function   sG   �� ��,�,�,��0A�0A�[�0P��M�y�Y��G�L�1�2�2��$�!�&�!�!�    r#   )r.   r0   s   f r/   �candidate_requiredr3      s!   �� �
�1�X�"� �"�
 �r2   c                   �   � ] tR t^t]! R]! 4       ]! ^R7      .R7      t]! R]! 4       ]! ^xR7      .R7      t]	! R]! 4       ]! RR7      .R7      t
]! R4      tRtR	# )
�ProfileForm�Phone)�max��
validators�Location�Bioi�  zUpdate Profile� N)�__name__�
__module__�__qualname__�__firstlineno__r   r   r   �phone�locationr   �bior   �submit�__static_attributes__r<   r2   r/   r5   r5      sS   � ���X�Z��B��,H�I�E��:�8�:�v�#��2O�P�H�
��8�:�v�$�7G�*H�
I�C��)�*�Fr2   r5   c                   ��   � ] tR t^t]! R]! 4       .R7      t]! R]! 4       .R7      t]! R]! 4       .R7      t	]
! R]! 4       .R7      t]
! R]! 4       .R7      t]! R]! 4       .R7      t]! R4      tR	tR
# )�EducationForm�Degreer8   �InstitutionzField of Studyz
Start YearzEnd Yearz	Grade/GPA�Saver<   N)r=   r>   r?   r@   r   r   �degree�institutionr   �fieldr   �
start_year�end_year�grader   rD   rE   r<   r2   r/   rG   rG      so   � ���|�~�.>�?�F��m���8H�I�K��(�h�j�\�B�E��l��
�|�D�J��J�H�J�<�@�H������=�E��� �Fr2   rG   c                   ��   � ] tR t^)t]! R]! 4       .R7      t]! R]! 4       .R7      t]! R]! 4       .R7      t	]! R]
! 4       .R7      t]! R]
! 4       .R7      t]! R4      t]! R4      tR	tR
# )�ExperienceForm�Companyr8   z	Job Titlez
Start DatezEnd Date�DescriptionzCurrently working hererJ   r<   N)r=   r>   r?   r@   r   r   �companyr+   r"   �
start_dater   �end_dater   �descriptionr   �
is_currentr   rD   rE   r<   r2   r/   rR   rR   )   sj   � ��)���0@�A�G��{���/?�@�D��<�\�^�4D�E�J������=�H���8�:�,�G�K��6�7�J��� �Fr2   rR   c                   �^   � ] tR t^3t]! R]! 4       .R7      t]! R. ROR7      t]	! R4      t
RtR# )	�	SkillFormr   r8   �Proficiency)�choicesz	Add Skillr<   N))�beginner�Beginner)�intermediate�Intermediate)�expert�Expert)r=   r>   r?   r@   r   r   �
skill_namer   �proficiencyr   rD   rE   r<   r2   r/   r[   r[   3   s0   � ��W�,�.�1A�B�J��m�  6H�  I�K���%�Fr2   r[   c                   �   � ] tR t^9t]! R]! 4       .R7      t]! R]! 4       .R7      t	]! R]! 4       .R7      t
]! R]! 4       .R7      t]! R4      tRtR# )	�ProjectFormzProject Titler8   rT   zTechnologies UsedzProject LinkrJ   r<   N)r=   r>   r?   r@   r   r   �titler   r   rX   �	tech_used�linkr   rD   rE   r<   r2   r/   rg   rg   9   sN   � ���\�^�4D�E�E���8�:�,�G�K��/�X�Z�L�I�I��~�8�:�,�?�D��� �Fr2   rg   c                   �   � ] tR t^At]! R]! 4       .R7      t]! R]! 4       .R7      t]	! R]! 4       .R7      t
]! R]! 4       .R7      t]! R4      tRtR# )	�	AwardFormzAward Titler8   �Issuer�DaterT   rJ   r<   N)r=   r>   r?   r@   r   r   rh   r   �issuerr"   �dater   rX   r   rD   rE   r<   r2   r/   rl   rl   A   sM   � ���<�>�2B�C�E���x�z�l�;�F��V����5�D���8�:�,�G�K��� �Fr2   rl   z
/dashboardc                  ��  � \         P                  p \        P                  P	                  \         P
                  R 7      P                  4       pR\        V4      R\        V Uu. uF  q"P                  R8X  g   K  VNK  	  up4      R\        V Uu. uF  q"P                  R8X  g   K  VNK  	  up4      R\        V Uu. uF  q"P                  R8X  g   K  VNK  	  up4      /p\        P                  P	                  \         P
                  R 7      P                  \        P                  P                  4       4      P                  ^4      P                  4       p\        RWVR7      # u upi u upi u upi )��candidate_id�applications_sent�shortlisted�rejected�hiredzcandidate/dashboard.html)�profile�stats�recent_applications)r   �candidate_profiler   �query�	filter_by�id�all�len�status�order_by�
applied_at�desc�limitr   )rx   �applications�ary   rz   s        r/   �	dashboardr�   I   s7  � � �,�,�G��$�$�.�.�L�O�O�.�L�P�P�R�L� 	�S��.��s�|�Q�|�!�x�x�=�7P�A�A�|�Q�R��C�L�K�L�q�H�H�
�4J���L�K�L����E��A���W�1D�a�a��E�F�	�E� &�+�+�5�5�<�?�?�5�S�\�\�]h�]s�]s�]x�]x�]z�{�  B�  B�  CD�  E�  I�  I�  K���5�w�i|�}�}�� R��K��Es$   �"E%�9E%�E*�&E*�<E/�E/z/profile�GET�POST)�methodsc                  �(  � \         P                  p \        4       pVP                  4       '       Ed   VP                  P
                  V n        VP                  P
                  V n        VP                  P
                  V n        R \        P                  9   da   \        P                  R ,          pV'       dB   VP                  '       d0   \        V\        P                  R,          4      pV'       d   W0n        \        P                   P#                  4        \%        RR4       \'        \)        R4      4      # V P                  VP                  n        V P                  VP                  n        V P                  VP                  n        \+        RWR7      # )�profile_pic�UPLOAD_FOLDERzProfile updated successfully!�successzcandidate.profilezcandidate/profile.html)rx   �form)r   r{   r5   �validate_on_submitrA   �datarB   rC   r   �files�filenamer   r	   �configr�   r   �session�commitr   r   r   r   )rx   r�   �filer�   s       r/   rx   rx   \   s  � � �,�,�G��=�D���� � ��
�
������=�=�-�-����h�h�m�m����G�M�M�)��=�=��/�D������+�D�+�2D�2D�_�2U�V���*2�'�
�
�
�����-�y�9��� 3�4�5�5��m�m�D�J�J�O� �)�)�D�M�M���K�K�D�H�H�M��3�W�P�Pr2   z
/educationc            
      �t  � \         P                  p \        4       pVP                  4       '       d�   \	        V P
                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  R 7      p\        P                  P                  V4       \        P                  P!                  4        \#        RR4       \%        \'        R4      4      # \)        RV P*                  VR7      # ))rs   rK   rL   rM   rN   rO   rP   zEducation added successfully!r�   �candidate.educationzcandidate/education.html)�	educationr�   )r   r{   rG   r�   r   r~   rK   r�   rL   rM   rN   rO   rP   r   r�   �addr�   r   r   r   r   r�   )rx   r�   r�   s      r/   r�   r�   z   s�   � � �,�,�G��?�D���� � �� ����;�;�#�#��(�(�-�-��*�*�/�/����+�+��]�]�'�'��*�*�/�/�
�	� 	�
�
���y�!�
�
�
�����-�y�9��� 5�6�7�7��5��AR�AR�Y]�^�^r2   z/education/<int:edu_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )�Unauthorized action.�dangerr�   zEducation deleted successfully!r�   )r   r|   �
get_or_404rs   r   r{   r~   r   r   r   r   r�   �deleter�   )�edu_idr�   s   & r/   �delete_educationr�   �   s�   � � ���*�*�6�2�I�����!?�!?�!B�!B�B��$�h�/��� 5�6�7�7��J�J���i� ��J�J����	�
+�Y�7��G�1�2�3�3r2   z/experiencec            
      �t  � \         P                  p \        4       pVP                  4       '       d�   \	        V P
                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  R 7      p\        P                  P                  V4       \        P                  P!                  4        \#        RR4       \%        \'        R4      4      # \)        RV P*                  VR7      # ))rs   rU   r+   rV   rW   rX   rY   zExperience added successfully!r�   �candidate.experiencezcandidate/experience.html)�
experiencer�   )r   r{   rR   r�   r   r~   rU   r�   r+   rV   rW   rX   rY   r   r�   r�   r�   r   r   r   r   r�   )rx   r�   r�   s      r/   r�   r�   �   s�   � � �,�,�G���D���� � �� ����L�L�%�%���������+�+��]�]�'�'��(�(�-�-����+�+�
�
� 	�
�
���z�"�
�
�
�����.�	�:��� 6�7�8�8��6�7�CU�CU�\`�a�ar2   z/experience/<int:exp_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )r�   r�   r�   z Experience deleted successfully!r�   )r   r|   r�   rs   r   r{   r~   r   r   r   r   r�   r�   r�   )�exp_id�exps   & r/   �delete_experiencer�   �   s�   � � �
�
�
%�
%�f�
-�C�
���<�9�9�<�<�<��$�h�/��� 6�7�8�8��J�J���c���J�J����	�
,�i�8��G�2�3�4�4r2   z/skillsc                  ��  � \         P                  p \        4       pVP                  4       '       d�   \	        V P
                  VP                  P                  VP                  P                  R 7      p\        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # \!        RV P"                  VR7      # ))rs   rd   re   zSkill added successfully!r�   �candidate.skillszcandidate/skills.html)�skillsr�   )r   r{   r[   r�   r   r~   rd   r�   re   r   r�   r�   r�   r   r   r   r   r�   )rx   r�   �skills      r/   r�   r�   �   s�   � � �,�,�G��;�D���� � �� ������+�+��(�(�-�-�
��
 	�
�
���u��
�
�
�����)�9�5��� 2�3�4�4��2�7�>�>�PT�U�Ur2   z/skill/<int:skill_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )r�   r�   r�   zSkill deleted successfully!r�   )r   r|   r�   rs   r   r{   r~   r   r   r   r   r�   r�   r�   )�skill_idr�   s   & r/   �delete_skillr�   �   �   � � �K�K�"�"�8�,�E����\�;�;�>�>�>��$�h�/��� 2�3�4�4��J�J���e���J�J����	�
'��3��G�.�/�0�0r2   z	/projectsc                  �   � \         P                  p \        4       pVP                  4       '       d�   \	        V P
                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  R 7      p\        P                  P                  V4       \        P                  P                  4        \        RR4       \!        \#        R4      4      # \%        RV P&                  VR7      # ))rs   rh   rX   ri   rj   zProject added successfully!r�   �candidate.projectszcandidate/projects.html)�projectsr�   )r   r{   rg   r�   r   r~   rh   r�   rX   ri   rj   r   r�   r�   r�   r   r   r   r   r�   )rx   r�   �projects      r/   r�   r�   �   s�   � � �,�,�G��=�D���� � �� ����*�*�/�/��(�(�-�-��n�n�)�)������
�� 	�
�
���w��
�
�
�����+�Y�7��� 4�5�6�6��4�w�?O�?O�VZ�[�[r2   z/project/<int:proj_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )r�   r�   r�   zProject deleted successfully!r�   )r   r|   r�   rs   r   r{   r~   r   r   r   r   r�   r�   r�   )�proj_idr�   s   & r/   �delete_projectr�     s�   � � �m�m�&�&�w�/�G����|�=�=�@�@�@��$�h�/��� 4�5�6�6��J�J���g���J�J����	�
)�9�5��G�0�1�2�2r2   z/awardsc                  �   � \         P                  p \        4       pVP                  4       '       d�   \	        V P
                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  R 7      p\        P                  P                  V4       \        P                  P                  4        \        RR4       \!        \#        R4      4      # \%        RV P&                  VR7      # ))rs   rh   ro   rp   rX   zAward added successfully!r�   �candidate.awardszcandidate/awards.html)�awardsr�   )r   r{   rl   r�   r   r~   rh   r�   ro   rp   rX   r   r�   r�   r�   r   r   r   r   r�   )rx   r�   �awards      r/   r�   r�     s�   � � �,�,�G��;�D���� � �� ����*�*�/�/��;�;�#�#�������(�(�-�-�
�� 	�
�
���u��
�
�
�����)�9�5��� 2�3�4�4��2�7�>�>�PT�U�Ur2   z/award/<int:award_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )r�   r�   r�   zAward deleted successfully!r�   )r   r|   r�   rs   r   r{   r~   r   r   r   r   r�   r�   r�   )�award_idr�   s   & r/   �delete_awardr�   +  r�   r2   z/applicationsc                  ��   � \         P                  P                  \        P                  R 7      P                  \         P                  P                  4       4      P                  4       p \        RV R7      # )rr   zcandidate/applications.html�r�   )
r   r|   r}   r   r~   r�   r�   r�   r   r   r�   s    r/   r�   r�   :  sS   � � �$�$�.�.�L�O�O�.�L�U�U�Va�Vl�Vl�Vq�Vq�Vs�t�x�x�z�L��8�|�T�Tr2   z/apply/<int:job_id>c                 �  � \         P                  P                  V 4      p\        P                  P	                  \
        P                  V R 7      P                  4       pV'       d!   \        RR4       \        \        R4      4      # \        P                  R8X  d�   \        P                  P                  RR4      p\        \
        P                  V VRR7      p\        P                   P#                  V4       \        P                   P%                  4        \        R	R
4       \        \        R4      4      # \'        RVR7      # ))rs   �job_idz&You have already applied for this job.r)   zcandidate.applicationsr�   �cover_letter� �applied)rs   r�   r�   r�   z#Application submitted successfully!r�   zcandidate/apply.html)�job)r   r|   r�   r   r}   r   r~   �firstr   r   r   r   �methodr�   �getr   r�   r�   r�   r   )r�   r�   �existing_applicationr�   �applications   &    r/   �	apply_jobr�   B  s�   � � �)�)�
�
�v�
&�C�&�,�,�6�6�!�_�_�� 7� � �e�g� �
 ��6�	�B��� 8�9�:�:��~�~����|�|�'�'���;��!�%����%��	
�� 	�
�
���{�#�
�
�
�����3�Y�?��� 8�9�:�:��1�s�;�;r2   N)B�flaskr   r   r   r   r   r   r	   �flask_loginr
   r   �
app.modelsr   r   r   r   r   r   r   r   r   �	app.utilsr   �wtformsr   r   r   r   r   r   r   �wtforms.validatorsr   r   r   r    �	flask_wtfr!   �wtforms.fieldsr"   �	functoolsr$   r=   �candidate_bpr3   r5   rG   rR   r[   rg   rl   �router�   rx   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r<   r2   r/   �<module>r�      s�  �� \� \� \� 4� k� k� k� &� p� p� p� D� D� � $� ���h�<�H���+�)� +�!�I� !�!�Y� !�&�	� &�!�)� !�!�	� !� ���L�!���~� � � "�~�  ���J�����8���Q� � � 9�Q�6 ���L�5�&�/��:���_� � � ;�_�, ���4�v�h��G���	4� � � H�	4� ���M�E�6�?��;���b� � � <�b�, ���5��x��H���	5� � � I�	5� ���I��v���7���V� � � 8�V�$ ���2�V�H��E���	1� � � F�	1� ���K�%����9���\� � � :�\�( ���3�f�X��F���	3� � � G�	3� ���I��v���7���V� � � 8�V�( ���2�V�H��E���	1� � � F�	1� ���O�$���U� � � %�U�
 ���)�E�6�?��C���<� � � D�<r2   
```
---


          # app/routes/__pycache__/company.cpython-314.pyc,
          \${language}
+
    X��i')  �                   ��  � ^ RI HtHtHtHtHtHtHt ^ RIH	t	H
t
 ^ RIHtHtHtHtHtHt ^ RIHt ^ RIHtHtHtHtHtHtHt ^ RIHtHtHtH t  ^ RI!H"t" ^ RI#H$t$ ^ R	I%H%t% ]! R
]&RR7      t'R t( ! R R]"4      t) ! R R]"4      t*]'PW                  R4      ]	](R 4       4       4       t,]'PW                  RRR.R7      ]	](R 4       4       4       t-]'PW                  RRR.R7      ]	](R 4       4       4       t.]'PW                  RRR.R7      ]	](R 4       4       4       t/]'PW                  RRR.R7      ]	](R 4       4       4       t0]'PW                  RR.R7      ]	](R  4       4       4       t1]'PW                  R!R.R7      ]	](R" 4       4       4       t2]'PW                  R#4      ]	](R$ 4       4       4       t3]'PW                  R%4      ]	](R& 4       4       4       t4]'PW                  R'R.R7      ]	](R( 4       4       4       t5R)# )*�    )�	Blueprint�render_template�request�redirect�url_for�flash�current_app)�login_required�current_user)�db�Company�Job�Application�User�CandidateProfile)�save_upload_file)�StringField�TextAreaField�SelectField�
FloatField�SubmitField�	DateField�IntegerField)�DataRequired�Optional�Length�URL)�	FlaskForm��wraps)�datetime�companyz/company)�
url_prefixc                 �0   a � \        S 4      V 3R  l4       pV# )c                  �   <� \         P                  '       d   \         P                  R 8w  d!   \        RR4       \	        \        R4      4      # S! V / VB # )r"   z7You must be logged in as a company to access this page.�warningz
auth.login)r   �is_authenticated�roler   r   r   )�args�kwargs�fs   *,��2C:\Coding\Projects\NextOffer\app\routes\company.py�decorated_function�,company_required.<locals>.decorated_function   sG   �� ��,�,�,��0A�0A�Y�0N��K�Y�W��G�L�1�2�2��$�!�&�!�!�    r   )r+   r-   s   f r,   �company_requiredr0      s!   �� �
�1�X�"� �"�
 �r/   c                   ��   � ] tR t^t]! R]! 4       .R7      t]! R]! 4       .R7      t]! R]! 4       ]	! RR7      .R7      t
]! R]! 4       .R7      t]! R. RO]! 4       .R	7      t]! R
]! 4       .R7      t]! R4      tRtR# )�CompanyProfileFormzCompany Name��
validators�Industry�WebsiteF)�require_tld�LocationzCompany Size��choicesr4   �DescriptionzUpdate Profile� N))� zSelect Size)�10-50r>   )�50-200r?   )�200-500r@   )�500-1000rA   )�1000+rB   )�__name__�
__module__�__qualname__�__firstlineno__r   r   �company_namer   �industryr   �website�locationr   �sizer   �descriptionr   �submit�__static_attributes__r<   r/   r,   r2   r2      s�   � ��~�<�>�:J�K�L��:�8�:�,�?�H��)���S�U�=S�0T�U�G��:�8�:�,�?�H��~� 0� �:�,� �D�  ��8�:�,�G�K��)�*�Fr/   r2   c                   �l  � ] tR t^)t]! R]! 4       .R7      t]! R]! 4       .R7      t]! R]	! 4       .R7      t
]! R]	! 4       .R7      t]! R]	! 4       .R7      t]! R]	! 4       .R7      t]! R. RO]! 4       .R	7      t]! R
]	! 4       .R7      t]! R]	! 4       .R7      t]! R]	! 4       .R7      t]! R4      tRtR# )�JobFormz	Job Titler3   zJob Description�Requirementsz
Salary Minz
Salary Maxr8   zJob Typer9   zExperience Requiredz!Required Skills (comma-separated)zApplication DeadlinezPost Jobr<   N))r=   zSelect Type)z	full-timez	Full-time)z	part-timez	Part-time)�contract�Contract)�
internship�
Internship)�remote�Remote)rC   rD   rE   rF   r   r   �titler   rL   r   �requirementsr   �
salary_min�
salary_maxrJ   r   �job_type�experience_required�skills_requiredr   �deadliner   rM   rN   r<   r/   r,   rP   rP   )   s�   � �����0@�A�E�� 1�|�~�>N�O�K� ��X�Z�L�I�L��L�h�j�\�B�J��L�h�j�\�B�J��:�8�:�,�?�H��:� 0�  �>�"�$�H� &�&;����U��!�"E�S[�S]�R^�_�O��/�X�Z�L�I�H���$�Fr/   rP   z
/dashboardc                  ��  � \         P                  p \        P                  P	                  V P
                  R 7      P                  4       p\        P                  P	                  V P
                  RR7      P                  4       p\        P                  P                  \        4      P                  \        4      P                  \        P                  V P
                  8H  4      P                  4       p\        P                  P                  \        4      P                  \        4      P                  \        P                  V P
                  8H  \        P                  R8H  4      P                  4       pRVRVRVRV/p\        P                  P	                  V P
                  R 7      P                  \        P                  P!                  4       4      P#                  ^4      P%                  4       p\'        RWVR7      # )	��
company_id�active)rb   �status�shortlisted�
total_jobs�active_jobs�total_applicationszcompany/dashboard.html)r"   �stats�recent_jobs)r   �company_profiler   �query�	filter_by�id�countr   �sessionr   �join�filterrb   rd   �order_by�	posted_at�desc�limit�allr   )r"   rf   rg   rh   re   ri   rj   s          r,   �	dashboardrx   >   sj  � � �*�*�G����$�$��
�
�$�;�A�A�C�J��)�)�%�%����H�%�M�S�S�U�K����)�)�+�6�;�;�C�@�G�G����Za�Zd�Zd�Hd�e�k�k�m���*�*�"�"�;�/�4�4�S�9�@�@����'�*�*�$����m�+�� �e�g� � 	�j��{��0��{�	�E� �)�)�%�%����%�<�E�E�c�m�m�FX�FX�FZ�[�a�a�bc�d�h�h�j�K��3�W�_j�k�kr/   z/profile�GET�POST)�methodsc                  �l  � \         P                  p \        4       pVP                  4       '       EdV   VP                  P
                  V n        VP                  P
                  V n        VP                  P
                  V n        VP                  P
                  V n        VP                  P
                  V n	        VP                  P
                  V n
        R \        P                  9   da   \        P                  R ,          pV'       dB   VP                  '       d0   \        V\        P                   R,          4      pV'       d   W0n        \$        P&                  P)                  4        \+        RR4       \-        \/        R4      4      # V P                  VP                  n        V P                  VP                  n        V P                  VP                  n        V P                  VP                  n        V P                  VP                  n        V P                  VP                  n        \1        RWR7      # )�logo�UPLOAD_FOLDERz%Company profile updated successfully!�successzcompany.profilezcompany/profile.html)r"   �form)r   rk   r2   �validate_on_submitrG   �datarH   rI   rJ   rK   rL   r   �files�filenamer   r	   �configr}   r   rp   �commitr   r   r   r   )r"   r�   �filer�   s       r,   �profiler�   X   s{  � � �*�*�G���D���� � �#�0�0�5�5����=�=�-�-����,�,�+�+����=�=�-�-����y�y�~�~���"�.�.�3�3����W�]�]�"��=�=��(�D������+�D�+�2D�2D�_�2U�V���#+�L�
�
�
�����5�y�A��� 1�2�3�3�$�1�1�D���� �)�)�D�M�M�����D�L�L�� �)�)�D�M�M���\�\�D�I�I�N�#�/�/�D�����1�7�N�Nr/   z/jobsc                  �  � \         P                  p \        P                  P	                  V P
                  R 7      P                  \        P                  P                  4       4      P                  4       p\        RVR7      # )ra   zcompany/jobs.html)�jobs)r   rk   r   rl   rm   rn   rs   rt   ru   rw   r   )r"   �company_jobss     r,   r�   r�   |   sY   � � �*�*�G��9�9�&�&�'�*�*�&�=�F�F�s�}�}�GY�GY�G[�\�`�`�b�L��.�\�B�Br/   z	/post-jobc                  �
  � \         P                  p \        4       pVP                  4       '       EdG   \	        V P
                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                  P                  VP                   P                  R R7      p\"        P$                  P'                  V4       \"        P$                  P)                  4        \+        RR4       \-        \/        R4      4      # \1        RVR7      # )rc   )rb   rX   rL   rY   rZ   r[   rJ   r\   r]   r^   r_   rd   zJob posted successfully!r   �company.jobszcompany/post_job.html)r�   )r   rk   rP   r�   r   rn   rX   r�   rL   rY   rZ   r[   rJ   r\   r]   r^   r_   r   rp   �addr�   r   r   r   r   )r"   r�   �jobs      r,   �post_jobr�   �   s  � � �*�*�G��9�D���� � ���z�z��*�*�/�/��(�(�-�-��*�*�/�/����+�+����+�+��]�]�'�'��]�]�'�'� $� 8� 8� =� =� �0�0�5�5��]�]�'�'��
�� 	�
�
���s��
�
�
�����(�)�4����/�0�0��2��>�>r/   z/job/<int:job_id>/editc                 ��  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        4       pVP                  4       '       EdM   VP                  P                  Vn        VP                  P                  Vn        VP                  P                  Vn        VP                   P                  Vn        VP"                  P                  Vn        VP$                  P                  Vn        VP&                  P                  Vn        VP(                  P                  Vn        VP*                  P                  Vn        VP,                  P                  Vn        \.        P0                  P3                  4        \        RR4       \        \        R4      4      # VP                  VP                  n        VP                  VP                  n        VP                  VP                  n        VP                   VP                   n        VP"                  VP"                  n        VP$                  VP$                  n        VP&                  VP&                  n        VP(                  VP(                  n        VP*                  VP*                  n        VP,                  VP,                  n        \5        RW!R7      # )�Unauthorized action.�dangerr�   zJob updated successfully!r   zcompany/edit_job.html)r�   r�   )r   rl   �
get_or_404rb   r   rk   rn   r   r   r   rP   r�   rX   r�   rL   rY   rZ   r[   rJ   r\   r]   r^   r_   r   rp   r�   r   )�job_idr�   r�   s   &  r,   �edit_jobr�   �   s�  � � �)�)�
�
�v�
&�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0��9�D���� � ��J�J�O�O��	��*�*�/�/����,�,�1�1������-�-������-�-����}�}�)�)����}�}�)�)���"&�":�":�"?�"?���"�2�2�7�7����}�}�)�)���
�
�
�����)�9�5����/�0�0��i�i�D�J�J�O��O�O�D���� �-�-�D�����>�>�D�O�O���>�>�D�O�O�����D�M�M�����D�M�M��$'�$;�$;�D���!� #� 3� 3�D�������D�M�M���2��G�Gr/   z/job/<int:job_id>/togglec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # VP                  R8X  d   RMRVn
        \        P                  P                  4        \        RVP                   R2R4       \        \        R4      4      # )r�   r�   r�   rc   �closedzJob status changed to �!r   )r   rl   r�   rb   r   rk   rn   r   r   r   rd   r   rp   r�   �r�   r�   s   & r,   �toggle_job_statusr�   �   s�   � � �)�)�
�
�v�
&�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0� �Z�Z�8�3���C�J��J�J����	�"�3�:�:�,�a�
0�)�<��G�N�+�,�,r/   z/job/<int:job_id>/deletec                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V4       \        P                  P                  4        \        RR4       \        \        R4      4      # )r�   r�   r�   zJob deleted successfully!r   )r   rl   r�   rb   r   rk   rn   r   r   r   r   rp   �deleter�   r�   s   & r,   �
delete_jobr�   �   s�   � � �)�)�
�
�v�
&�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0��J�J���c���J�J����	�
%�y�1��G�N�+�,�,r/   z/job/<int:job_id>/applicationsc                 �  � \         P                  P                  V 4      pVP                  \        P
                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  V R7      P                  \        P                  P                  4       4      P                  4       p\!        RWR7      # )r�   r�   r�   �r�   zcompany/job_applications.html)r�   �applications)r   rl   r�   rb   r   rk   rn   r   r   r   r   rm   rs   �
applied_atru   rw   r   )r�   r�   r�   s   &  r,   �job_applicationsr�   �   s�   � � �)�)�
�
�v�
&�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0��$�$�.�.�f�.�=�F�F�{�G]�G]�Gb�Gb�Gd�e�i�i�k�L��:��_�_r/   z#/application/<int:app_id>/candidatec                 �p  � \         P                  P                  V 4      pVP                  pVP                  \
        P                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  VP                  4      pVP                  p\        RWVR7      # )r�   r�   r�   zcompany/candidate_profile.html)�application�candidate_user�candidate_profile)r   rl   r�   r�   rb   r   rk   rn   r   r   r   r   �get�candidate_idr�   r   )�app_idr�   r�   r�   r�   s   &    r,   �view_candidater�   �   s�   � � �#�#�.�.�v�6�K�
�/�/�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0��Z�Z�^�^�K�$<�$<�=�N�&�8�8���;��  HY�  Z�  Zr/   z'/application/<int:app_id>/update-statusc                 ��  � \         P                  P                  V 4      pVP                  pVP                  \
        P                  P                  8w  d!   \        R R4       \        \        R4      4      # \        P                  P                  R4      pVR	9   d5   W1n        \        P                   P#                  4        \        RV R2R4       \        \        RVP                  R7      4      # )
r�   r�   r�   rd   zApplication status updated to r�   r   zcompany.job_applicationsr�   )�appliedre   �rejected�hired)r   rl   r�   r�   rb   r   rk   rn   r   r   r   r   r�   r�   rd   r   rp   r�   )r�   r�   r�   �
new_statuss   &   r,   �update_application_statusr�     s�   � � �#�#�.�.�v�6�K�
�/�/�C�
�~�~��5�5�8�8�8��$�h�/����/�0�0����!�!�(�+�J��D�D�'��
�
�
�����.�z�l�!�<�i�H��G�6�s�v�v�F�G�Gr/   N)6�flaskr   r   r   r   r   r   r	   �flask_loginr
   r   �
app.modelsr   r   r   r   r   r   �	app.utilsr   �wtformsr   r   r   r   r   r   r   �wtforms.validatorsr   r   r   r   �	flask_wtfr   �	functoolsr    r!   rC   �
company_bpr0   r2   rP   �routerx   r�   r�   r�   r�   r�   r�   r�   r�   r�   r<   r/   r,   �<module>r�      s�  �� \� \� \� 4� L� L� &� m� m� m� B� B� � � ��y�(�z�B�
��+�� +�"%�i� %�* ���,����l� � �  �l�. ���*�u�f�o��6���O� � � 7�O�B ���'�E�6�?��3���C� � � 4�C� ���+��v���7���?� � � 8�?�6 ���*�U�F�O��D���!H� � � E�!H�H ���,�v�h��?���	-� � � @�	-� ���,�v�h��?���	-� � � @�	-� ���2�3���`� � � 4�`� ���7�8���
Z� � � 9�
Z� ���;�f�X��N���H� � � O�Hr/   
```
---


          # app/routes/__pycache__/main.cpython-314.pyc,
          \${language}
+
    X��i�  �                   ��   � ^ RI HtHtHt ^ RIHtHt ^ RIHt ]! R]	4      t
]
P                  R4      R 4       t]
P                  RRR	.R
7      R 4       t]
P                  R4      R 4       tR# )�    )�	Blueprint�render_template�request)�Job�Company)�or_�main�/c                  ��  � \         P                  P                  R ^\        R7      p \        P
                  P                  RR7      P                  \        P                  P                  4       4      P                  ^4      P                  4       p\        P
                  P                  RR7      P                  4       p\        P
                  P                  4       p\        RVVVR7      # )�page��type�active��statusz
index.html)�featured_jobs�
total_jobs�total_companies)r   �args�get�intr   �query�	filter_by�order_by�	posted_at�desc�limit�all�countr   r   )r   r   r   r   s       �/C:\Coding\Projects\NextOffer\app\routes\main.py�indexr!      s�   � ��<�<���F�A�C��0�D��I�I�'�'�x�'�8�A�A�#�-�-�BT�BT�BV�W�]�]�^_�`�d�d�f�M����$�$�H�$�5�;�;�=�J��m�m�)�)�+�O���#��'�	� �    z/jobs�GET�POST)�methodsc            
      �  � \         P                  P                  R ^\        R7      p \         P                  P                  RR4      P	                  4       p\         P                  P                  RR4      P	                  4       p\         P                  P                  RR4      P	                  4       p\
        P                  P                  RR7      pV'       d^   VP                  \        \
        P                  P                  RV R24      \
        P                  P                  RV R24      4      4      pV'       d3   VP                  \
        P                  P                  RV R24      4      pV'       d   VP                  VR	7      pVP                  \
        P                  P!                  4       4      P#                  V ^
R
7      p\%        RVVVVR7      # )r   r   �search� �location�job_typer   r   �%)r*   )r   �per_pagezjobs/browse.html)�jobsr'   r)   r*   )r   r   r   r   �stripr   r   r   �filterr   �title�ilike�descriptionr)   r   r   r   �paginater   )r   r'   r)   r*   r   r-   s         r    �browse_jobsr4      s`  � ��<�<���F�A�C��0�D��\�\���h��+�1�1�3�F��|�|���
�B�/�5�5�7�H��|�|���
�B�/�5�5�7�H��I�I���x��0�E�������	�	���!�F�8�1��.����%�%��&���m�4��
�� ����S�\�\�/�/�!�H�:�Q��@�A��������2���>�>�#�-�-�,�,�.�/�8�8�d�R�8�P�D�������� r"   z/job/<int:job_id>c                 �r   � \         P                  P                  V 4      pVP                  p\	        R WR7      # )zjobs/detail.html)�job�company)r   r   �
get_or_404r7   r   )�job_idr6   r7   s   &  r    �
job_detailr:   :   s-   � �
�)�)�
�
�v�
&�C��k�k�G��-�3�H�Hr"   N)�flaskr   r   r   �
app.modelsr   r   �
sqlalchemyr   �__name__�main_bp�router!   r4   r:   � r"   r    �<module>rB      s�   �� 5� 5� #� �
�F�H�
%�� 	���s��� �� 	���w�����0�� 1��B 	���"�#�I� $�Ir"   
```
---


          # app/routes/__pycache__/resume.cpython-314.pyc,
          \${language}
+
    "��iu  �                   �  � ^ RI HtHtHtHtHtHtHt ^ RIH	t	H
t
 ^ RIHt ^ RIHt ^ RIHt ^ RIHt ^ RIHt ^ RIHt ^ R	IHtHtHtHtHt ^ R
IHtHt ^ RIH t  ]! R]!RR7      t"R t#R t$]"PK                  R4      ]	]#R 4       4       4       t&]"PK                  RRR.R7      ]	]#R 4       4       4       t']"PK                  R4      ]	]#R 4       4       4       t(R# )�    )�	Blueprint�render_template�request�redirect�url_for�flash�	send_file)�login_required�current_user)�CandidateProfile)�BytesIO��wraps)�datetime)�letter)�colors)�SimpleDocTemplate�Table�
TableStyle�	Paragraph�Spacer)�getSampleStyleSheet�ParagraphStyle)�inch�resumez/resume)�
url_prefixc                 �0   a � \        S 4      V 3R  l4       pV# )c                  �   <� \         P                  '       d   \         P                  R 8w  d!   \        RR4       \	        \        R4      4      # S! V / VB # )�	candidatez9You must be logged in as a candidate to access this page.�warningz
auth.login)r   �is_authenticated�roler   r   r   )�args�kwargs�fs   *,��1C:\Coding\Projects\NextOffer\app\routes\resume.py�decorated_function�.candidate_required.<locals>.decorated_function   sG   �� ��,�,�,��0A�0A�[�0P��M�y�Y��G�L�1�2�2��$�!�&�!�!�    r   )r%   r'   s   f r&   �candidate_requiredr*      s!   �� �
�1�X�"� �"�
 �r)   c                  �b  � \         P                  p R \         P                  R\         P                  RV P                  ;'       g    RRV P
                  ;'       g    RRV P                  ;'       g    RRV P                  RV P                  RV P                  R	V P                  R
V P                  /
# )�name�email�phone� �location�bio�	education�
experience�skills�projects�awards)r   �candidate_profiler,   r-   r.   r0   r1   r2   r3   r4   r5   r6   )�profiles    r&   �prepare_resume_datar9      s�   � ��,�,�G���!�!���#�#�����$�$�"��G�$�$�*�*���w�{�{� � �b��W�&�&��g�(�(��'�.�.��G�$�$��'�.�.�� r)   z/builderc                  �0   � \        4       p \        R V R7      # )zresume/builder.html��resume_data)r9   r   r;   s    r&   �builderr=   *   s   � � &�'�K��0�k�J�Jr)   z/preview/<template>�GET�POST)�methodsc                 �   � \        4       pV R9  d!   \        RR4       \        \        R4      4      # RV  R2p\	        W!R7      # )�classic�Invalid template selected.�danger�resume.builderzresume/templates/z_resume.htmlr;   �rB   �modern�creative)r9   r   r   r   r   )�templater<   �template_files   &  r&   �previewrK   2   sJ   � � &�'�K��8�8��*�H�5��� 0�1�2�2�'��z��>�M��=�B�Br)   z/download/<template>c                 �z  � \        4       pV R:9  d!   \        RR4       \        \        R4      4      # \	        4       p\        4       p\        RVR,          ^\        P                  ! R4      ^^R7      p\        RVR	,          ^\        P                  ! R
4      ^^^\        P                  ! R
4      R7      p. pVP                  \        VR,          V4      4       VR,           pVR,          '       d   VRVR,           2,          pVR,          '       d   VRVR,           2,          pVP                  \        RV R2VR,          4      4       VP                  \        ^R\        ,          4      4       VR,          '       dk   VP                  \        RV4      4       VP                  \        VR,          VR,          4      4       VP                  \        ^R\        ,          4      4       VR,          '       EdI   VP                  \        RV4      4       VR,           EF  pRVP                   RVP                   2p	VP                  \        W�R,          4      4       VP                  P!                  R4       R2p
Y�P"                  '       d   VP"                  P!                  R4       MR,          p
VP                  \        RV
 R2VR,          4      4       VP$                  '       d-   VP                  \        VP$                  VR,          4      4       VP                  \        ^R\        ,          4      4       EK"  	  VR,          '       EdF   VP                  \        R V4      4       VR,           EF  pRVP&                   R!2pVP(                  '       d   VR"VP(                   2,          pVP                  \        W�R,          4      4       VP                  \        VP*                  VR,          4      4       VP,                  '       d\   VP,                   pVP.                  '       d   VRVP.                   2,          pVP                  \        RV R2VR,          4      4       VP                  \        ^R#\        ,          4      4       EK  	  VR$,          '       d�   VP                  \        R%V4      4       R&P1                  VR$,           Uu. uF  q�P2                   R'VP4                   R(2NK   	  up4      pVP                  \        W�R,          4      4       VP                  \        ^R\        ,          4      4       VR),          '       Ed   VP                  \        R*V4      4       VR),           F�  pVP                  \        RVP6                   R!2VR,          4      4       VP$                  '       d-   VP                  \        VP$                  VR,          4      4       VP8                  '       d1   VP                  \        R+VP8                   R,2VR,          4      4       VP                  \        ^R#\        ,          4      4       K�  	  VR-,          '       d�   VP                  \        R.V4      4       VR-,           F�  pRVP6                   R!2pVP:                  '       d   VRVP:                   2,          pVP                  \        VVR,          4      4       VP                  \        ^R/\        ,          4      4       K�  	  \=        V\>        R0\        ,          R0\        ,          R17      pVPA                  V4       VPC                  ^ 4       R2\D        PF                  PI                  R3R44       R4\J        PL                  ! 4       P!                  R54       R62p\O        VR7R8VR97      # u upi );rB   rC   rD   rE   �CustomTitle�Heading1z#0A1628)�parent�fontSize�	textColor�
spaceAfter�	alignment�CustomHeading�Heading2z#2563EB)rO   rP   rQ   �spaceBeforerR   �borderBottomWidth�borderBottomColorr,   r-   r.   z | r0   z<font size=9>z</font>�Normalg�������?r1   zPROFESSIONAL SUMMARYg�������?r3   �
EXPERIENCEz<b>z</b> | z%b %Yz - �Presentr2   �	EDUCATIONz</b>z in g{�G�z�?r4   �SKILLSz, z (�)r5   �PROJECTSz<font size=9><i>Tech: z</i></font>r6   zAWARDS & ACHIEVEMENTSg�������?g      �?)�pagesize�	topMargin�bottomMargin�resume_� �_z%Y%m%dz.pdfzapplication/pdfT)�mimetype�as_attachment�download_namerF   )(r9   r   r   r   r   r   r   r   �HexColor�appendr   r   r   r"   �company�
start_date�strftime�end_date�description�degree�field�institution�
start_year�end_year�join�
skill_name�proficiency�title�	tech_used�issuerr   r   �build�seekr   r,   �replacer   �nowr	   )rI   r<   �buffer�styles�title_style�heading_style�elements�contact_info�exp�exp_text�dates�edu�edu_text�	year_text�s�skills_text�proj�award�
award_text�doc�filenames   &                    r&   �downloadr�   @   s  � � &�'�K��8�8��*�H�5��� 0�1�2�2��Y�F� �"�F� !���j�!���/�/�)�,����K� #���j�!���/�/�)�,���� �/�/�)�4�	�M� �H� �O�O�I�k�&�1�;�?�@�!�'�*�+�L��7����#�k�'�2�3�4�4���:����#�k�*�5�6�7�7���O�O�I��l�^�7�C�V�H�EU�V�W��O�O�F�1�c�$�h�'�(� �5������	�"8�-�H�I����	�+�e�"4�f�X�6F�G�H�����q�#�d�(�+�,� �<� � ����	�,��>�?��|�,�,�C��S�X�X�J�g�c�k�k�]�;�H��O�O�I�h�x�0@�A�B��~�~�.�.�w�7�8��<�E��L�L�L����-�-�g�6�7�i�W�E��O�O�I��e�W�G�&D�f�X�FV�W�X��������	�#�/�/�6�(�;K� L�M��O�O�F�1�c�$�h�/�0� -� �;������	�+�}�=�>��{�+�+�C��S�Z�Z�L��-�H��y�y�y��d�3�9�9�+�.�.���O�O�I�h�x�0@�A�B��O�O�I�c�o�o�v�h�7G�H�I��~�~�~�"�~�~�.�	��<�<�<��3�s�|�|�n�!5�5�I����	�M�)��G�*L�f�U]�N^� _�`��O�O�F�1�d�4�i�0�1� ,� �8������	�(�M�:�;��i�i�k�Zb�Nc� d�Nc��L�L�>��A�M�M�?�!�!D�Nc� d�e�����	�+�h�/?�@�A�����q�#�d�(�+�,� �:������	�*�m�<�=��
�+�+�D��O�O�I��D�J�J�<�t�&<�f�X�>N�O�P��������	�$�*:�*:�F�8�<L� M�N��~�~�~����	�,B�4�>�>�BR�R]�*^�`f�go�`p� q�r��O�O�F�1�d�4�i�0�1� ,� �8������	�"9�=�I�J� ��*�*�E��u�{�{�m�4�0�J��|�|�|���E�L�L�>�2�2�
��O�O�I�j�&��2B�C�D��O�O�F�1�d�4�i�0�1� +� �F�V�s�4�x�VY�Z^�V^�
_�C��I�I�h��
�K�K��N���*�*�2�2�3��<�=�Q�x�|�|�~�?V�?V�W_�?`�>a�ae�f�H���"���	� ��A !es   �$^8N))�flaskr   r   r   r   r   r   r	   �flask_loginr
   r   �
app.modelsr   �ior   �	functoolsr   r   �reportlab.lib.pagesizesr   �reportlab.libr   �reportlab.platypusr   r   r   r   r   �reportlab.lib.stylesr   r   �reportlab.lib.unitsr   �__name__�	resume_bpr*   r9   �router=   rK   r�   � r)   r&   �<module>r�      s�   �� Z� Z� Z� 4� '� � � � *�  � V� V� D� $��h��Y�?�	���  �������K� � � �K�
 ���&�����@���C� � � A�C� ���'�(���v� � � )�vr)   
```
---


          # app/routes/__pycache__/__init__.cpython-314.pyc,
          \${language}
+
    X��i    �                   �   � R # )N� r   �    �3C:\Coding\Projects\NextOffer\app\routes\__init__.py�<module>r      s   �r   
```
---


          # app/static/css/style.css,
          \${language}
:root {
    --primary-color: #054ADA;
    --secondary-color: #4267B2;
    --dark-color: #054ADA;
    --accent-color: #FF9900;
    --light-bg: #f5f7fa;
    --text-dark: #1a1a1a;
}

* {
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--light-bg);
    color: var(--text-dark);
}

.navbar {
    box-shadow: 0 2px 8px rgba(5, 74, 218, 0.15);
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%) !important;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
}

/* Cards */
.card {
    transition: all 0.3s ease;
    border-radius: 12px;
}

.hover-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(5, 74, 218, 0.15) !important;
}

.card.border-0 {
    border-radius: 12px;
}

/* Buttons */
.btn {
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
    border: none;
}

.btn-primary {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(5, 74, 218, 0.4);
    background: linear-gradient(135deg, #043aa8 0%, #3855a0 100%);
    color: white;
}

.btn-success {
    background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%);
    color: white;
}

.btn-success:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(255, 153, 0, 0.4);
    background: linear-gradient(135deg, #e68a00 0%, #cc7700 100%);
    color: white;
}

.btn-outline-primary {
    color: #054ADA;
    border-color: #054ADA;
}

.btn-outline-primary:hover {
    background-color: #054ADA;
    border-color: #054ADA;
    color: white;
}

.btn-warning {
    background-color: #FF9900;
    border-color: #FF9900;
    color: white;
}

.btn-warning:hover {
    background-color: #e68a00;
    border-color: #e68a00;
    color: white;
}

/* Forms */
.form-control, .form-select {
    border-radius: 6px;
    border: 2px solid #e0e0e0;
    padding: 0.75rem;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    border-color: #054ADA;
    box-shadow: 0 0 0 3px rgba(5, 74, 218, 0.1);
}

/* Badges */
.badge {
    padding: 0.5rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
}

.badge.bg-primary {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%) !important;
}

/* Hero Section */
.hero-section {
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
}

.search-form {
    margin-top: 1.5rem;
}

/* Tables */
.table {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
}

.table thead th {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
    color: white;
    font-weight: 600;
    border: none;
    padding: 1rem;
}

.table tbody td {
    padding: 1rem;
    border-color: #e5e7eb;
    vertical-align: middle;
}

.table tbody tr:hover {
    background-color: rgba(5, 74, 218, 0.05);
}

/* Pagination */
.pagination {
    gap: 0.25rem;
}

.pagination .page-link {
    border: none;
    color: #054ADA;
    border-radius: 4px;
    margin: 0 2px;
    font-weight: 500;
}

.pagination .page-link:hover {
    background-color: rgba(5, 74, 218, 0.1);
    color: #054ADA;
}

.pagination .page-item.active .page-link {
    background-color: #054ADA;
    color: white;
}

/* Alerts */
.alert {
    border-radius: 8px;
    border: none;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
}

.alert-danger {
    background-color: #f8d7da;
    color: #721c24;
}

.alert-info {
    background-color: #d1ecf1;
    color: #0c5460;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
}

/* Sidebar */
.sidebar-nav {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
    border-radius: 12px;
    padding: 1.5rem;
    color: white;
}

.sidebar-nav .nav-link {
    color: rgba(255, 255, 255, 0.8);
    border-radius: 6px;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
}

.sidebar-nav .nav-link:hover,
.sidebar-nav .nav-link.active {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
}

/* Footer */
footer {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
    margin-top: auto;
    color: white;
    border-top: 3px solid #FF9900;
}

/* Spinner */
.spinner-border {
    color: #054ADA;
}

/* Loading Overlay */
.loading-overlay {
    background: rgba(5, 74, 218, 0.1);
}

/* Profile Cards */
.profile-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(5, 74, 218, 0.1);
}

.profile-header {
    text-align: center;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid rgba(5, 74, 218, 0.1);
}

.profile-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #054ADA;
}

/* Section Headers */
.section-header {
    border-left: 4px solid #054ADA;
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

.section-header h3 {
    color: #054ADA;
    margin-bottom: 0;
    font-weight: 700;
}

/* Status Badges */
.status-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.status-applied {
    background: #e3f2fd;
    color: #054ADA;
}

.status-shortlisted {
    background: #fff3e0;
    color: #FF9900;
}

.status-rejected {
    background: #ffebee;
    color: #c62828;
}

.status-hired {
    background: #e8f5e9;
    color: #2e7d32;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.3s ease-in-out;
}

/* Glassmorphism */
.glass-effect {
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(5, 74, 218, 0.1);
    border-radius: 12px;
}

/* Cursor */
.cursor-pointer {
    cursor: pointer;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #054ADA;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4267B2;
}

/* Responsive */
@media (max-width: 768px) {
    .navbar-collapse {
        padding-top: 1rem;
    }

    .hero-section h1 {
        font-size: 2rem;
    }

    .card {
        margin-bottom: 1rem;
    }

    .sidebar-nav {
        margin-bottom: 1.5rem;
    }
}

/* Links */
a {
    color: #054ADA;
    transition: all 0.3s ease;
}

a:hover {
    color: #FF9900;
}

/* Input Focus */
input:focus, textarea:focus, select:focus {
    outline: none;
}

/* Label */
label {
    color: var(--text-dark);
    font-weight: 500;
}

/* Dividers */
.divider {
    border-top: 2px solid rgba(5, 74, 218, 0.1);
    margin: 1.5rem 0;
}

/* Card Headers */
.card-header {
    background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);
    color: white;
    border: none;
    border-radius: 12px 12px 0 0 !important;
}
```
---


          # app/static/js/main.js,
          \${language}
// Close alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fade-in');
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form && !form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
    }
    form.classList.add('was-validated');
}

// Show loading spinner on form submit
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitBtn = form.querySelector('[type="submit"]');
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        submitBtn.disabled = true;
    }
});

// Confirm delete actions
function confirmDelete(message = 'Are you sure?') {
    return confirm(message);
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0
    }).format(amount);
}

// Search functionality
function setupSearch() {
    const searchInput = document.querySelector('[data-search]');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const items = document.querySelectorAll('[data-search-item]');
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
}

// Initialize tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// Setup search
setupSearch();

// Logout confirmation
function confirmLogout() {
    return confirm('Are you sure you want to logout?');
}

// Print resume
function printResume() {
    window.print();
}
```
---


          # app/static/uploads/28ae14de-4cf7-416f-819e-927a1ee9ff61_men.jpg,
          \${language}
�PNG

   IHDR  d  �   c�i    IDATx��i�e�u����Lwx��S���bh�� ��&	����ȱ+�����O��Q+����QU�R*�%Uٱ]�dq�(J� &@w����7���L{��������@�}�z�}���s��{��ַ����a�=����  )��RZ���c����\�It�o"*DDr�]S�F�
K� �Qo�e�|p��j� �Y�D�@X �}��������H"���" DJi�iOk�kݵ 	  	�$����Hmhppd0�|�CMLl%���IM������u7���<�~P��ۍV;�I3s���kkWggqrbj���>��R��C�:�ZP��iDj4��+���{��<ω0�� �$i4 000�J��zn���@�RF�:i��K���)kdmm��}/�8�t:�19)�5 ��A�i��9Mc��Y�)� J���~����z�ga
iV�G�q����w�v�잘��}nn��k猱Y��Ap��a ��dllleees���yT�����@�g�������5�Їj�ӧO_x���:`���ND�g���G����fK@��L��9z�A�����Vk���n�OLE�H��q��ճ��Z�m�/����/�����i�D^���9"V�ب׳4.Wʑﹱg-+P����5�@ �`D���퇂��D�X7GX$�(oye�ԙW���4o�[���ŋ�J��_?�裏v�ь�8{������_ߚ���Ĥƴ;y�q��,�b�sw�ߡo��o2�W�~�Mk׶���G~�cy�z�pc�o�������m�$���_�n|n��E�9k�8ݦs|�;�ݝ���SXlﳆ�h@D��|��}��<7do� ���l� ���q�h�k��5���V���6��:[�̋�K����� [ �YD����0"�p���e�ܘ8��V�!Q�������`pxhhp0����UA�4뛛���a����NZ�)�jZ�f5)��<E ���<O�f#"���i��y�c�0  F+bE677�ˣ�G��;1���̳Ϭ,-��w��Qٵk�f�94<\�V��y���s�}�������K��9Q���Xs��3S�=���ٳ@������]뫫T��ݽ��3˳ע��8�A�����������O�dy~���i��d-�$Ϯ/�GQ4�{zff�6�Σ��������ү�������?�o�����ij�4��o��5�a�A�'���9'z��n;���w%,�����o�L�0#"t��:�;�]�����p����kODD��GQ)� ԭ�%"j��i���N(��+++ 466a��WZ��\�\�z��h�Z Ё���1�nw� �<m-3s!��s���<fa6 ��""�b��8��,��4�V�FF�S����	_&ϳvlLx>�q��t���B��֞R@@��#?�� ���v'�Z��4�ֈJ0
�aX*��(����h$�a�9[�����;���j�����?���{�188�i��##"rm����������Z푏|dc}�R�����eoxx��LT��?>11���}nuu��C�q""�M^�:t8˲�g_��I
��eoxߞ�#����{Z����g����6ϟ}�{��^�D山��3S֚����}������_�#'�x~����~�W��'����� (*E��#�F�'�������*&������� R$,��Y  @D��ޮ�����,Y�M�o �:~k�I �)�}/�(�R�g���<#"�z�� ���h����P�Ѩ��ۿ�򕹗_:�����:���YX(�#kM����BDc�5�)�D�{QAD
� ��v����Ԕ�t�ݲ ~D咧=aI�$MӨR�}/�3�LD~V�e h��l!*���R�i ��,�;bM�iOs.�-�:�R�H�ۭ��#�a�T�MN��y�g��v�sd�����챍�����N3�Z�I�$�2 @����޵���]ӗ�\y���A�񉉡�GN<��n������?���'O~���i���;�����_X^]/���h�R	����#��S�N���ed�s`ߋ�^��m�
y���kW��^�z�|%*ONM~�1����.-�ϟ��w����:�ڣ����lZc�%���<7�h�Q� x���n"9�	 ���2t�����*l-[���Zy;w���
����mJ$�ҚE�o^a��؛ITx��ٯ���w��H����֙��޺F�۾� ���6�y�EF `��F@DE �h��BԽ� "�ɡXfE�k�|��^�aj�#����]�(�($ DD%,�a F�G��_g{�����WϜ9s���(��BD�Bk�c� @��ġR>"Zf�� ����6yn,#��l����v=�&MS/�(�}�w�������"i" h�<�8 �0�|Ml�$I��f�g	I�X�0	�4k�;�f�<�eβ��3��]��+��vf/_��ޣÃ/^�}dx��j���;��������o҄j����xЈ��?��Ǐ�cO>��w_}�����J��߁��������Y�s��F�5�kfﾽL����Ӿ����i����wݷ�V���E���{cc_}���}�꩗@���}���+��'�?��'���嵍�����������/��-��b�E|߷y�o�F)w-��G����p�ÒEzc�E���.@Y�<7H�<�]�O17���O��C�Q��;��A���omO~��5�~I��������~ "�BO+�S��yZ{�Ҥ5*��e�
 (� "�v @�FGF��D�����f�W<�q*��"ҽ�s�3 x���b�f ��~����u�)˓������kkk@880�G! �i�%�G~����I�fB����^�ic������VY��4����Y�yZ���=|����N�c����j��q�٨K�VGG��Ҿ���y� 
[�����޽�O�:500��l�a�$I���ؽg��k�._��XX?x�Zسg���KKKK�+O<�D���?���Ν=���r�؃��/��E�ч���H����RA�Yo:����w?։�gN>m��s�@��K�_xa�ڕt�U�3��i<�2�����g����k�񑑇~��W��&��|�׺����$I�42�[��+�;Ͳ+��w���2o��oe�w���w�$��a�6	 JD
�c�ׯzvNſ�D
J�]�f�`�F�H�p;�Q�8��/{-�E��ܯVn]�H�BǘUZ���u!&*�Z+F0 ���k!( P�� x}s���Ckk����g�.�1��мI�@���, EψȲɲL@�VZ#)pj�eVH h��M��Ւ�Q�tZ�fmxxp�����u"533��A��$�j�Z�e�z=3y�����͍�kOa��h�6�8��T)M&K�ύ X)�N�%I,HD*�RHۀAell��ݣ��O�������`�P�P��9��w<�[c����q@���[^^��:������@25=)$�K��f����a��]�JD��?�ML<t��${�@�'�J���`�6888�?�tڇʕ0�O>�L����/|2I�/}�Kןy� �����x}eѤ��#G867��ZY={�j������LN���/<��o=z`����j�R*�*a�/-,n�e�B�C�m_�tGja;!D B$!₂� ��6Yb�ퟤ���P��ڎ�uw������>�x;q�!�}�HۄI��q�u�K��Ɛ�MҾ�����u��V���VR�=[|/�5�1n ���;]��ٙPy���~@J���{�5)�(��D3�( D�lE�&��#<������~��j5�X` b���"Œ�l��5ä)���fFEniβܘ4MSQ�ݒ]�""�<�QT��Rf�W�
�����z}��Au�fA�VW۝"V�� l�o�6=���o'��z��
�Q�Ř�ZFD�\5�5&����=���� ������y~��l��L����X��<�53s��驩�c���ʫg.�=땢��a ���Q�v~v v���h5�]�fs����~0<<�$�5v~~�|?����4��W��j�v���/�����a����+i�w�{&&^y���f�hP�266F�r��_���dyf$������=����F�t���[���3���O~��ݏ<ǭW^9�kj�7:�� ��q��00�F B7G��-����v���%晴;x+�VΝ[��,�G��r?��QNn��T4"R����Xp�d���YG���d )�;}V�ޥ�n�/��WN��8�#��n�ea$ҀH�
P!�� ��]) �a�+�R9���@��"b���5
�B�a����J��W�y��?���ҋ��ۂ�O� Bi�rW@:�"3�i
,��I �yn� "
+"`k�ɭ�����J�+eEZD�<�<O) �<ϳ,#"�Bˬ, s�wZME:��T�e6O:�v��,��b����X��J����<�̅oX{^�T({
�4)GA��$I ��f��s^_]�4[��k����ܥK@l�����/-��Y
 �������fks��ő���ƴ6�ATJ��k��22V�	�N�����Q������ZM{��>���s�����Zexhd|b�#�R�Z�\��A�:/��z�=�4��k��߷��;�NMO�������s�^[YY;w��c�VV����4M���En|���Po��9�n�?�Cۭ,Bh�]d�����9[F������D����C�v�c�zK��m,���������oS~8����q���:����n��n���Q|#5o[�}����6��E�	>7�8��O���d)��j�ܻI�?����t_B�8�0t�b���^w'p�q�,W��� �Ax~�COi_#��E �S+0:2NZ��m�+��q�C�����h:nЭކef�"B�H����hLnL.�Jo�*0[4���$y�X�"�?�,I�̰�V�J�8��V��5A�4��M���o�ZI�dY�]�e7�,O�ņ �㌍�{��-�FDP�֞Rd-k��G,�;��曛�Y��yf�[��5�'��~���;q�ԩSZ����LZi��,/)�����h4+�3G��ݷ�W����r}9N�0��{Py��W777���;����>�n�������@��\^X�^�z���,�⸵��684�h��kkI�������a�n6��kC��v{qe��j\��c6�ճ����yAuZ���4-y�V�[@��� D���E�b104��.@�1ώ�ַ%���#Gw��oD�p��(�D"�  �'~DD)���b.��?�
� TN^1:>��^�d)��8l�M��sH�g�j��7�����a�لJ�Q�Q�Z�T*^�������c6��5	h"A0~P�f��u4<<�jR�w���Q�4HƵ�4��7<a�����y��� H! �n [k@�؁fy&�z~�� 7i��1Q��RU�U��z�IL�0�@���fw�4e�*�4��V�g�]��f�p;$t�n V
��}�'�yn��-�ij��y�$I�n9妐߭(52:155�tZ���"vbt��0���gggg�&��7U�RY^^n��#�#J�K/��j4����؁��Պ5�G�������4Mw��;1>>2:�i�/_�\�׿��S |�轚 �J���'����� cV7֕RQT����CI���g����F&J�V������������':~}~yiec��y�aT^��K�N����<�m
�O�s�(�@�R���>�ˏ���Z�y���V��Y��m^���X�C�������o�'ԏW۾�m ޴8�[�hNd�z�6-Y ��'�N��[�a��KA���H.ޑ�f`��PW�����JQ�G��=��=O#��%`A"Ԃ$�"b��y��T���?��8�����5P� Ȍ黗H(y��W��s�c���� ��='@w��p�%i����zTZ�^���YoY�RP��H��-f�y�(�t�i��I��s�	�eKݤ� �T�HXy��*�"�:ϭ�hXk�eDʲ,I�<MQ� �"DT��y��@%
��N���]ӝ4a���������Ջ���k���'�&wMM�Rc#C����}?��^�J�ᡑo���R��������=a��������^ O}��O�Z����ڗ��E�#c��s�FD:t�����s���̹s����WO�`��塑��F���76^<��cO|pa��s?x����F�$�s���[E�����2�"t���Ŵ"`v�T��F�OB̥P"��bo̼�Y��;�JX�7�7g����./e��CDB@BAD�qn!>�����ٯ��!@��cf��q�n����ѓ��<�K^�,� `�oV�H!iE�W^�G%�=���}�Q��H,���[�X�Gؒ����Ϭ( ������GJ+k,I_�P�R���TIcrDt��bESԥ^�u��, ���k�܈���0=�	��4NӸT���lD��u��̳���7٤�ϫ ���,�t��[s	\�\�<7�噱Ji	�ͭecr(�"�=�y��� "��_9�22T+���Fj̮�6�k�^.W�#�#���}�؃��9�J��������������H�ٜ�r���9<61:42�k�R.��p��܋/�^9|��:�zz�Q_����۵k�Ŋ@�imll���ɿ�ڗ��f��&K$ˀ9�Z�_:�NΝ9��ʮ]��#Ǐ_o4���layyق�6πE臫����7��ޠ��<FD�k#! �.��-�eRJ����#�H���""�f��Y���FP�~��7�;�Y_�f�]�ٳO�,�`���MW'�
�����x��p��-v��QM~�(H��ҋ����R��H�G��^� ��Ӟ5�"��)s��L @H��6����O������iy:PZ�X��b�ν�]�i���=I"��E�[ �` k, �e�= �t:q���?24��N�$��4�6I�,I�-)T(,��)(V`�)�C�,�:�~EQyn�^�,�D
 ��q�dY600P�� ��� 1�;�819������>>9�e��Q�T�/��5�CCK�Ky�ؿ�64����m���#����vg���������R��F���|�E������Vk׮]�vguy�����A� ��LY
b�-�ƨ1ۤU/��ӓ��ˍ�����}odt�T�,..<���F�r���6�{w���l���M��%% �e�t�u���'fnr�'����"k���=U�v���e����~RS��q���^UT!�P��0 ���VUR�X$�GBttQBD)� �]�DoB7��֑�	>=)}�ؽsn�2�&r��vr���(�JQ)C��=����l��	I)@ �������������y
 �ݢʶ��.c��#4u)��ޭ���[kAز�<�%���,I8�2c�ry��iwĂ�i�r}s�-[f``��rbإ�Z!j� Z��P�����8M�<Ϙ��J��v:�֊��ek-U*Ս��,ˆ��`�т��)����4}�̫yn����ՙ�]�C����ٹ$IDdhx�T
�]�V�%Il����_��LL����{76��}��׮�M?
/�;��%Hb�T��9ˠ � �|a�v:�b�=�����c'�N<����y��W7{�=��3���7�������ki��4�T+�q'f�oZ 	v�,�;gQ+E�ht� W�'���l	Q)�L����mlc���g7H�;�n��on'�~rx}���P�[k�tSy�n�Ů7��q�w��iz�n�m��y��?�c�����("����Jk���.�lI�vj$ 
t������� x��N�xڻ�Д����Zűu��� D`dfk-)���4��$�0��3o�oDA�����$I<�w�w���;�����-D�[�-�V�| `�4ME��n�4���i�i��1��]�@'M]]f�V�a���V*��������������)��*���C����++�l�&500���dT.ǝ�R�]�>?7��h9rdzz�n�L    IDAT�64�Y�^�|��I��{����j�{���`-�:+K�W.��:�A$I�G!���LV��w���|����ċ�N}�/�������?y�{O����_�L�٘����$�V�H�&��ב�-b����dg�Gd՝��Z�l�k�'�"��[�����M�ܷ�7�?�� 	e�I�ԋ��c��ZPZm��䮼T(�=���sVq���bk��{Ƿ,N��6 [��;3{j��9E˅���޸=�	�����Z������0P����&"@ �J��j��V6�j��i���_~kmm}��"��;� |_��)�N������#Co�WT�d,P,�N-<�΍,Z�"�P�sk�! ����y���.|��)�ɬ�Q�D8g ���{��ɭ��W#* �� y�����"6O3�[6���RZk��Zkf�Z;J��c�w��4�V��8�<m�<�c�M�R��e����*�����"E�J)�����ik?�p��y�C�x�\�fY���K�N����Y][���#��<����1�%׮^Y��6:R�ȇ?:<2�8�������Ҩo�������5�n�G��w���W���o|�w�4��[��7���������W�ޗ�����X[�ַ�s��~��Z�6�0_�TQ �Fc��J~��Oҥw��,�	����BB� ����U"FD� 2�{7�۟^q{��zo�ލ>#��w����y�=�3���*�����g[Td���n�
n�p��	 �U������ׇS�>oe����&wsjUhW����t��n�� �6����[*�������XP��</�QT	���<��\+�[� "���(����=��s��6����ML�4KR�"S���"��E�&*RZk���!��H��'D��C���,I�4uҎ�F^�$ �� #_kϩ��cra�D��+�]6zg+�Q�f�}��=�݌O$�J)D6�0Kר� ���<S���V��֖��j���0M�N�`�4MG�ƢR��.�K,����޳w�޽�:x��ť0,�=������r6�}�Z{��Sˋa�}��O��f��Z]Z]^X^ZZ\Y��C��#F���{��G�\Z����ف������yyy�_�ѿ��'��V��fctl��������_��/����gN���3�MOO����H[�X�Z}z㟙]"��dDM,ݕe�'���b�$<�ۄe?��WD��SW����꺥D9f0*d�H���"ƿ��8h�
��1���}~۫� l߷�3�E��a}��4��J�H��a�"�� C�S"����0�J�����ի���Z�<����I�j��pNJ�7�Y�@�=��^�M�����")@�j�l,�p"/�يB�JA��֘ey�Į���`1z�^�4"*ENL:� Zi�.q���	J��U�մF�V�.A�Vyn�; =�+W*D��y�,VD<O��(M�᱑�\}��kq�<��O鍍��|�[޳��������g���=3>>���^�r�����?������]��;����뤑m&NJ��a��s�����������W<���_�����w����/}��,�.\����c���l�<r`o҉O>�T�:X
}�1I���;�8KD�[C�7��g4!��8�Vl�&���&s�;P�v���|�67����yW|�>�m~�[h�.����Ҫ�,�����]�0�n��z�`����ۢ'<Pn����������|ߏ�(
C��J���j��e@�l��ɞ���nnn�:u*���yc���d�Dd�"�C7��X{�ӕֲ "��Tn�""Y�a� (�N躥S
	M
Py~EJiM��q��i�e"����b�MӔ�P"D�DN^���N�Xk��Z�>"�8f�6fS��Ji���s�)�� I�<��Y)BE������ X���ڵk��n�7 P)�O�>���{Ϯ˗.��`;�/�?���T)�>�яNOM]�x�~����^Р�F�0�J�<|��ޫ|���~}~i|�A�o���d���~���/�:��s�=���?��cWggM��f}�Z\_]=x�`���vG�A@Hw�tn�>e��@X�^����YD���H+OA�I�v�q�`o�n�(��ؚZN�#`��ǃ��r��(Db-C�a!����Q�T�	 p�v�.p���M��t'�շ��z��%�������ۀl� n�V���v�.{���\Q��A��J9C�n5��Oǖ������z�R�"l��9_�~�'��<W�z:-w�i��v�s�t�4#��˩���n��~K, ��NI&"g�wTU�s�Fb6igY��9�U.&]! +$O�X��1&7�:����)xC ��E����i`c@��z�]�[ٙňAD`�=��cs ����l�4�Lfr���Z)�lj��I���	s^.����*��I3�?hh�6<2"�F�%�=}rϞ=�:�������ⷾ��._�;qu|*��,�%K,�}�>�g����k�/,��.�W^>{��~�7/^�[���N�_���=~�؉�c#�K�C��s�WO<tߟ}�Kg^|q��쉇޹{f�Z� Kn���Y��-1�H��ý:�Rt�wnrk-"jAA$�5"
w]!n����%�$Q�nl������[��'���z�k'�����{�����6�o�����;�/0")�?,��0����`I)Bww���J#�4�[��+��ET 9t�"K��`a��3�.~�%����f��9D���y�i��X.����0I�,˒$1Y D
I;w���&I��ݸ�����1b�ef�����i��Xg�E����H�����X�=�RkA�Mn�K���Kg&g6�ݕ��� s�'����&7[������8�jׯ__�7x��4M���Ç����}�c�0��/���+W���-+�љi6�X;2P>��6��鹋���^�:m�Qm�蓟��.ON?��s��y�ff�n����`��Z?�裾�S{vʹ7��-���n�~8��W���f��֙,ҭ� w0��`; ��e!�����)�[Z)r�=E��HɈ��J��-s˨�k ���RҼ�݃c�`r?��V�<��
�0*��J����5ROң��x�D�A����O���/�����WN*�v��k-��:��vQ+T� �5l�X�̾糰56�y���[BDҤ�P)EH��ղ��2 R����J��,��[�UDdfkm��)n���S����Zg@v�<g�(*i�  Mcw�֊�㸭�p|||nn>3�����Ç�66;�����@u���q�����r��/}�C��@����v�ʕ�ׯA0<2��Y_��<�g�z���N��n-//o�׀�_-��>x����Ї���o�����z
b�����??<2<66vm��#�~t~q1������v�J��#��������h�Y���Fo�ʲ݋�R$�*$�l%FGD̍ "E��֞��R �$��o#�v��'�Y�&�O���BG~H,�֙����GQ�AP��J jq
{�X*��V���\���Ơ���-��Ȩ�e?��"lY��y�-�����֨�X��;�V�G�|�WZ���&N��1��#�P�ЁX�Fs���4�0s�oc��r� ��.�2�:M�u�����j0ݟ[��v�K��
�SJ�`�N�c�}��|_�@D�A�Z���������iEt��y�{QXNl'˓��#G��}�����{����K�������\�۔4�\�����7���(*���p�b��N�Ҿ�G�G�'��������>��o��_��r��;FFǁ(,��p׮]׮]k���}�C����k���Ǿ�������4��W��`�k��-2�X)^e18ٺ�Y`�煡ֲ�F�r�~�";���@��o��g{`)���hK����QuK�Q��
=c�8�$��T�[�U��}�C�k� ��6ݏ�8� �r�P�G���	��RX�H�/�(*���Ԟ��R�"�gJ �m�N�ZX]]�ܿ�B��A����+z1�H!	]�L+B�z7*�.1{��K7�r�}O
�B`Ak�q<Y�1s�e��.�:��
Y�})��µ�5�9J0"�s��mO��3��.����ܠ���K~D�����"[�bV�"@f�5�a)���@�4M�䄂^�PF�j~�z�T���0��[��˹�j��yi9,U&�=8{u j��f�UR��k���=68P	�`sc��ɧV�}������@��޳7,�/���w��$N2�_��W^{�я~dd������ҩS�����W��ō�������{�7�-����}��\<|a������,��	��Y�!�X�]^�.M\�qd�U��v�Z?�U�6���&�l��G}��?z$���N�����H���!o���by�o�
b��@�����ƽ��Hҍ9  �Py:�R)
�@k�<��<R]B-2 #�1Y�ٴ�*�:w�1P��<�c�s���*I��o��SUJ�R�Zdq9�H+���+���.[ioO �%o���5��F9�[!�e�DD��\.='8�����쵰]�$٪�%�5�m��7�R���众 �l˩����e�[�ǧ���{��k����}��Wʕv�}��W6��P����5���z��o�<<255y�#�weee����z��W�^Z[[_�~ٮ/��3���b'�T9���ٹųg���ƴ�ο����_.�����W.]x���WW�����V���]{v__�t��[qc��,�ݿ]Yj̍�:��c2��{��[o���4���*�(,{�d�.9e�����)ĢXAO�p- RO�욀
�ڢ����Di_��ד��ft�`�#m������R��|����S���8�$��W�+��ɧ2�Ձr}�M�i�X�Oo�F\�%.�@��r�w�Xa1�Z67��H$ӓd�j{X�͏��}�\.A�,._]�e�$�*����4�;��~֏Sa���"J�Q������㤭�P���z�\�l�Z
p�R-�Q�Ɨ/�o,.a��H��]�����fHML�w:��/.,./.=����Ϟ=[�����S��������K���ݧ��{����q�ʕ��������g_[��O<�X���|�W�\y��'殭�-OLN��������1���/2��{q��c- H���s�r�!R�Č ]�s[B/I
�.6�}u�~�����T�ͫg�S E�;.�'ǸeA�Y�a���~G�"5�/�[�mRd%�n�o%z+��v[�%� �֎����@U�1q�f39�+��F���(�[����[�ӱ[U{ݸ�0�^f6�z/  8l�e�]�wT��T��1gbuz�R�]�v��r��ȮZ{*�)���[�n��4f��]����5�Z�"S�Ȗ
�#(Ac,�4��A+��y����P���:;>>>s�F�t�B�\�91311�{!"������Z[�$�(�J����2�����__[{��+��i7W�^������>?<�w�=�N�Is{��kk��P�T)��}��z��������ο���W/����kx��������XE�';Տ���V/\����m;J�o#��v��Xz�D�aV"���n�[!�����[tB���-Q���SVz��n<"}��]%tD?굃 RHpN�Bw-E�[�1�y}�,t9��D��Fa�\*�J� �D��&"�G.K+@��������K/� q'���w,��*r�쩰��3��bx�NI���(�:�B��8O4n��B�����"�EN�) Z�H�c��EeMDD���(��#���Z&®3ۊ5Jkk�k�(�e
��R*�BDt,"��%�#b�v���?::����uE,s��V7���+�Ki'^X�___��<������	D���h�[�w�N�xnnnbrlxhxia~�:���'��O��+3=��#'O~o����������+W�X�����K�/��t�xBD�F�:�@��j�P	�����?�I��1���"h �";�y�J�̂H�r��=.""��5��[Lu���Q�1���{��v�s�ӆ����G��N[dv��7[5�J��r��E��(�W�����O����ZZ��]I�;�q5]��m�qwK�Z)$r>�J�R*��RT*�<�"��v�e@�����@����׾���y��ԯ�HaQ}}ʈ"��(���J�W��X.�4���T[��<O��@yn�8.r�)E�O�[K��|�V��
�R����Z��h��"�.�R��@�ڜ���t�N���U�$Y�>w��aw#��"�^ߨ�7��T���� :}�4���]�vmnn���o6�����i���}�������_��J�ڱ|���;�£�?1:9�efpp��'� ������'s����##�i��9u��ų�<p���G���+�Ht������#�e9[&��$$]6�Oag;x3q'a���i��n����=�$"+����
ze~�
��RD�Q,;���܍H�~΍b�������w�e�!s:iσ��\)W*�0��R�H��ﻢ!�
b�G'J�c���ŗ_8G~q��]��v��@�2�I�E;�<,�H�k��t�q�ꊢ�ҋ���}��l�,�� �(*�+a*E.��K�]a|�i��T._`��z�����G�u�Ty  08Py��ט����(U*ׯ�I2>2�: ("�,` ��gΜim��ruxxx��/^����ǟ��>�C�C��Ѩ���{�}�{'�8=x���=s�P؞���'~�����ɉ����mnn\�~��Ç�9���~�Z.�~p�«���7�������Q�����z�X�밥���/��(t	�ܪ�("fyv�݂��^�<�7Y��ԡ�]�nϷ��*��oY��k?���:��ι�7��5�"#�������	�v)2��+��[R�un{�57|��
���=/CW�9|I�iOX��FЀ���e�<����V0K�zZ6!v+c�t]�=��Xl��kV%f�w~E�u��u6F��++�y��d��Kh����+�L��5������.G��iz!ֽ���tK�t~~�Z�FQd�lcm%�ā�+��������0�˥rǇj�[��_,�J�F��h�w�}k�ըR�r�
"&�΃�=�k��o��FMp����p3���S/�����D�F}ph`nnnph�Z-?u�ۏ��с(2I;<z����Y|�}�~��z����!���FR�]�L�>�,�B�"Er��;���[�^�^` #c�e�Y�r�(�@(��"�����
�#f���	�%��n�Uoo�귍��c�@�
���Pӧ}���-��Yŭ ���Ϲ�5B��^P.EQɉ�@{� ���1��ck���ZD@l��v�u�����'�^Z;'?n�I�+�(�����M�[�*ADdL*�uP��P9aw�=nc Q�"g���wqD���(�Z�� ��0�eT�����#tJG��Σ�,�9C��(�NLv�X!8��i�=O��Dl���1&M�j�Z�J���<������H���Y�,�$q ^Љ�djj2��fksff�ؼ�ٲ"Bx�ޙ#�?{o�kɕ���i�8��)&39�X�b��A��eٖ�ju�-�a���`����,v��F�V0`�.7�v�TR�JRbqL�9��D��k�a����df2I��y�c�k���ݹu����ۻ} �������%������˟��<) a�.�_��������ܹ�}qQ��ƍ��|���W����k?�w����_��?��o�Ư/�6�����65�L���~���������޾��FD^�#y={�Vf�Ѳ9ǳZV�t��p�����g[O3;���pЩ���6���W�<o��x4��F�[5�Мj�MNBk�K��>��f�x��?�S1dG2z�F� $9"��M��@�[)����>hV���k/�$$E%$%6�o��0��}r�:��^�~�����Y�TM-A�� FD5�N޽���TA�EUտ�{�'"G��	����Ŏ733���H��)'W!D�"�)�y�\ZV 	e��(ư�����.��e�i    IDATm�\.�1k25n��U�,���r� �=p����:X�h�i	wԮщ۞��AB�̀Ȕr���-���.ބ& 2����1���m �������R:<:P��lVUU�w7n�ؿ�;��_z��[��ޟ��������wytt���������_��/mο��K�������[o����ݫ�/}�˯�����~���?�������i�zVHf�OD+	�a�xH�z 2PV�����@𰥟s;��d��a�nǝ�HM�R���U�1���X"R��Ґ��b�����0� ��&0�8uC��<k=�U�0���)�Qy*�)���>u]�	""��@	�/^���X���a�&5(��9�iGp|�X��A7r]�rL+��gCc�;��U�Q٠����Х@�0d� ���1F����� ֍SӱY�b
!�X�����r���{�9D�ۣ��at�g��_r9's1q�mK�� B�)�m��`B��H)�4��B������ԧ��!]����߻����{uUŦ�/���;����������{k���ͷw��{�g_~���������/~�ÿ�����.U�/~��o�Y�q�X�������.��o���� �"@FS��k(g�ɻ㬃��@��y���aa��Z"��E���8�f�m��؃����3e��,���#��O������'�:�o�'Գ�x�FG��0���\C`UgS�U�%���Y>�S�f�#��1D��::i����	qoOB�뚉$������ŭ�wn�8�!f�Y�>��5D,%_D�<r� b�
�v$3*��s� �g� ж��޾�q]כ���c 1FfvV��i��]ׅRʠY��ܹ�u���z�o�C^G���X�P���q)����m���̇J�	.1�S�`��ol��˥�(Q�<<���{w�ީcuq���b�R�۷ߖ�����[w����._���7~������������µ-Ŀ��O�~��׾��[�n���+�?�cܹ�����ܙ��n���ٙ�6�,�}��d�O����N����Q͔ȉ~�[��ܞ)��*�{(BYU�KņV�״~�~ ��m  f�9F4`D��j�t*}�I�y�U�"p9v=��,�+�~�4��a�FP��$0���$�U��z��g�f���.:�D���0&"Ysj�&V/\}�w�w�@� X8�	�fx����G����������MX�f`l����..j�Be�@;��eEQ4�WM	�c]��,ƘS��n��"BU=:Z�m��U���:��� TUD��U����f`jhhf
�`��-� ��>Ȉf�FD���r`�Zھ�!��'G��4���Rn���RN���U�߾���l��K�k3 �}w���z���_�w��o~D677�Y�k������{7��o���z���\ۚ���/^��i~��\}���d��޻�yq�����Ϯ�E�P*N�}�a��=������)���h�fm�� ���:�N�X�Zh@Ν�g�>��A�̜�#,��������������;�]��� q>6g9�f�zbS�g��ib1Ff!��
��o������_����߯*�_(^?�)' {�.�M'C`�r��X�m���BD��ڶm��߶����ب�ZU���www�i�:Qͻ�w��鎎� |��j�i���R�����SK@������� )Ca�&D4%ª��$��SdT�R�7�Ϧ���jcc����Ofva���ݻ\�^о_}x�Ta�������>�%qff�;����t��������?-�ݼ���/���?�~������K[�v�G���޻{�ūDr��ͷ�~��˗/**�@f�UX|��i���g���D�<��`E$,q�y�����;�gI#��ڻ�J�u%�D�&s��U��iɽM)<69 x�lPt�yr�- ����	wl�!�vF#����}�9�A���u=�WM=�XĦ"aѬ��k�T�uJT��i�������V5�}��ZX�C��/��Ƕ1'8�!�&� �<�XSyi�=������S&j��b�ijDl�vwo�6��i�a�`��pٶm�:�"2����cS��N��sJ)�j��>:��J�	���1���# ��@���Y(T�� ]�k�*!E�)!��"�X�D66�r�d��H�����R����۶=8�?��b�y=k�gﾗ:�z���^���b����?�7��w^~��v3�f�\\�}����������^Nv�����[��n|����|�=�o��D!����H�����>q�LѴ���4d�F���Ts&"ǈ2S �8�}�
fu�G��
�o��$A��)�?�&³c��s��Ե#F^ס='l�U�9��?�0[
����H���A�j�j��B�UU�Y�̈�`%���ꥋW��?��� hV3�)�=�fyJݠ��zN9>�MAG��p���(23�f�,�1�ҳd��w�ZJU3���b���~����UU-3b"̔R^.�u�# H� ��(ed�#����WF�+����p��q� 2�f3kM%  0R@C�u]U�{ޘ�f�7�&޽s�GM�moܽ�a�W���<l,BSw)������^y��?��_�P��?����^~%V�=�Q3���K�w�6~��>w幯���߿�F����/����Y���v%��n����O�J  "��Q,#��+��Q��]�=��rm��[9od�۹��Y°f`��iDJH��h����Y��"fE2"DD$ .�f�Q1b!��lf���'�M������cn`�v2�\C������f��_s�yH��HDA$T��o4�E��u�	3�����~��Qش�ͷ���'.)'St:�R+~+δ[9���)�^su4��DC4��{(�=!x�Y�ZB�S߶������RD�˭�]�x"TՁ�S�g[z���E�I�Hh8�DĈR��	DB��N @&B#�Ȥf1a��D��R �Y����� T����w�ԳyF:8j�>w���`y�/4kDo���^�t�������ν���v�����{��/_�z������ٿ�7{�o|�7fS��� c��܎!%�_��޿����Q����s�����/ݺu�m��_�2�G3�]�G����sCB3c����*t���+0[*3N�V(����!����Dry7�)M_��ړ؅��{{�ְ/���O�4Mi��������������7?��rD��im˓Fh��ُ���W�KF��Z��(,U�ne����M�wx˸ԫm6��f�o��9�0�bf�֧sI�uH��S����)[5O�BA�E��o۶�j���YC�9��H����; ���O�m볛Q���Af�%#��°���Д�i]�X��aD��M�����&"B5M�U���;;ȂI�se������wY�*���mV�J싯�r��ݫW._�t�4wW.\�U|���-�o���ѽ�_z���*��u}�m Z�U���F����US߻�'U��ݽ|��l�^�re���Su#�gퟄ!aC"r����fƀ)�Q�'�8�<�
Ч�s�۹=6��%SJ pobf`^�$�Q���W���zZV4%�e��v:�tl��!�Y��'�E}jJj���y�eك����cS�fM������TQB@&#�YŔR3k��%$3k�����?���p����N>7y��8��4"S�fb"fܤ��;�m۶_"b��Bj����}�3�|�ؾ�c���ݛ�>T�jg0�MU{�af�XV�#*��s�"�I��T ��6�c�X�� �Y�*���5u����VR������H�w��l��hms6ߞ6������k/���fc��;{����/\~��>�^a��/5L�UT����/]�5w�_�fF9j������?�dz�嗮]���{�۶��ٹv�Z��^4�����Q�oBdF&&n��,��1A?lX����Ǿ侃��vҎU}F{����w��,����Y�d�J�@N��`X�A-$k�d�,?k�t_/<�t:��/͈��G����Zh]���?:8���ؗ��{���J++0ml,�j�R����S���8S���roo� �f6�r�" �jJi�\����o��f�:��)�^�H�W��IC(�2D�3�@̂�TU�SZ�iU�Ŭ��&[����K�D�0,�:h����P�mH��bѶG[���;ۘ��E�!P˺�������+�\�����ŭ�o|��b6k���+���\���h�AUI"U��HSq]u����%տ��/�������˗���Ͼ���)�@�����=��mӒ��3�g�>��vnO�V�Mx��0�0�3=�� 8��!�3��f2=�d@$@f��@; 0J*"��a���$J�)g�:���= c{b��9K!DD�b���Y���C��Tu��xՃm��'$� U3���_����-�3���&<J�1��	��),@,�tD�����@$�X1���f`"@���U��뺶Ӭ1ƍ����v�ԇG��O�s���mS�r�+���  P5"!Z�����~�0s�I
K$,�%�q���P�(����s�{D�A3��+�Sʷ�{>����f������d9�t���+�0���HV	fE�����?�����˿��7߾�9��\��+/^�7ͬ�� ��ܺ�}i�4)�"e���A���������?��?{뭝��/|�����^����H2 +@�Y�¾����AF�p����[6�����G=U��|���~��x��=k��+��S�я`�k��򒗗���r���=C'�8H��������q (KAXZ��`)w�� �7�j�xt`��ׇ���+�@={��t�޽��D*w����u���tc��Wf�Y�ҍ7n߹�u�W����53 �9����D�^��>�� cS�ZU��e�z�9g3��a�e#	sN�K��������TQ5{�T�]	��&Օ"j��>�9WU�sa��2�|��_�ʅ��ּb90T��|cK����w��������_����'m��ls�Q�ռi�~�sv.
�����W�(@&P�L������{w�W~����wv.����M�.67%Dͪ�䧪|4j �(�9f�ڥ~��{��l۹�ۧ�d�6ph:gG��μWn�B^ �e�r��N� &fG��u+�HY�8�J�wm��\C�>��=�厫}E#����b�f6��f12��Z#3,l؈�D����������Cl�Ƕ������ �� ��}j�YU�xCf�ܶmι^lml̪��{��[o���jh�;;UUu]wtt����j����T�f�%�e��������fV�ub]��lV7 �C"�U���P#��l���]UU`�Y�� ��>9�0Q� �G��!��W����;w��ʥ�_x�;��ٌ��R`��,��~��w����?�O�߼��K/������ W�>GR[�9R��aH
�A{S#4adz��>��_��7~��ܼq[U���X�\���It�L�͌dҨv��9����eb�S��s'� ��p��۳h���~<h���{�Op�3�j����͚Y�F��%bDW>�/,w����a��}�W��S �`fĸ1��n۶�Umcc���F��� ���d0n�nww��ڋ/.���ݶm�ݻ��u]KL��\Ϊ�yy�@�ه6���yS�c�����g@Q�S�1�H�*�A)�e��j¡�pt��Y]K��w�yg�`���k�?��7�|�7/^���/�k��0WD�"�������������僃ݯ���{��k�u|�F�jf�n�ֳ��K�#�ZFUe�*��;;�B ��w����sy�|�K���k�]��"=ժ�x����n@T��5�Q��a�~��@�vnϲM�,'2#40��z�i�c��X )��7;ɐ	�lE [X~�mHA3�e{��CQ^dp�S�Aks|;�mLS#$]��GNm����^հ:*B  an�fcs>k�:p�*DAvqFD4�h �b �/����Y{Z�S#?�ǵ�p�l�d% Y�]��ͬ��0��TfД�e���I]ع�u��w�WUȚ=Q)��"�� �Д@	T�B�ޘ���y!Q@fPfn�fV�1�ż��fB��ɧt�A���1�jL)�AUU�w�������}��w�;88��_��W?w��ō���Zִ�uPs���0��[��{/��zc��͛L8:�{��CR]�6ˆ�!Pf>
"U4�}�慭�����y���˗�~�m�5��C���q]�g��`��\��J��P�̉��Pz��h(��/ĄVHzu�\]0d��J|gm���C�Gf��ms�4�#�x�R�Ǳ��3e�<9s��r>S�8.d�E�Ր��E��ߦ��������t�#-(u���kO/�|����J� M��EG������M��MSU���H����(�>߹{'%�)љ�j�
��w �)!6����s�����׶mV�9�}c\ln� ���͛7�.�S�f�,�j3�S������=#�Ѳ���h�a��	,ΎDDP����K�X$8/T0jN�cf�>�>eЦ��k׮�٭�BN/\}���^hf����s��gߧD������b#T1����X8�X55�8Y���� sp~c*��jW�\�s��o���/��y�k����K�8Ĝ��ð�c�>�Ա��<�Gl��eU�_��s;�s;i��uc�x��3�j�9K�Y�_� 1�*���9o�س�U>��Y������6�Q�D�
e @᪪�����b�����/m�f�K	��	)�x��=�)�$�p��x4l R�.k��:H �����r�Z�H%3�ݻ;|\Ex>o$89�)��msN  ����U5��SUU1���B亮 ̪z��άj  0�砣`�0���DUU��� �������S��޾�+�_�BD���Cu]�u���L�c��l6���Y�pUU$"�b�P��5aA�  d�Y��"�ط݅�m ���}����|���ϧ�ɯ@A2 ,��CHDlf)�
`f���|tΫZ�d��Y	��e�ރ�3�ϲ�#�e�s����6�ʳ�#��DE,�~�	�/	�"�!�f�ԃ�~�4=aQ��*,���Y������G4'R��JbH)/�Gmۺ3B$�?)�檪BȐrJ}�4�Q֬����f"$ !�5ĦiD����3TD��C�l��\���2Y	���}�0�dU�t7@�L�fd�B���:op޺}�̾��_X,f)���݋/��GJ�1F�5uSU� �� !w)>=cX���I0 3��uߧ����{�so��fʉ���=K��r*¦�(!2���m[0S��+!�g�&=�s{lU�u6,��IߋS�G���)� H�2�c�<d��XR�㼦�j{�$R�!�0�T&�~�!�����l�)���u]/��l&1:�]!J_\��|>t:V�3X�ى�
��S�)?��t��@�T��)���30UHd�U�QȀ�"
r����]׻���bVEDf�N
��<`a?/ZĮ=Ȉ������:�D! жC�#�������mɴ�������W�W��������z����p�ӵ߻w�����/_��\v�ﻮӬҸ��ppַ"���D���$,� @e����M}�.^���������?�����+B#�>|���O+8� ) )#2d343&��ƞ��N�A�i����Y[����㴹��LჅP��~�'i������d��~xZ�<���3��FD#tJ����f1AM�Uq���@����]bp �����u]�u�cC� }׏Epf	�2ն;j�V�E
k,�� �"�}�f����Q��~o7�'�������T�ՌJ[Z��*�u�Ա�*	��:Pc"f0�I�� AӜ3 �YffA���e�����k�}��k��� ���Ӷm�ww�ޭ�%&�1�!DWUt�8ݜ    IDAT�F"!�8
�v1x�|�%���e�]�p�o~�c/��}�Oߌٜ�PA�@�g}�������q��t9X��pڎ�"W��HĄH�
L��30m�����p�"e����VyrY�7��\gy��#pO�x�d��K�j�2_̫����>Q���t���(%��Û�@�ES��/�v ��NSC¾�f+�2��w�g�j�!���7弿�����ä��
������b��]�43�2��s�\�!��lVU3�Z��)R�u]�1_�u�B�3Wd�Q�98r��Zj9����흝��]3�r���?��[�w��6S��}�Rn�6ƊEjb&�lf95��1�9眝%��˘e(��+�'@B��nݾt�����PW˃ß��/޸q��V� ��1V����v�!8� ��FsI- @�lEQ���r���Qy�8��>��L�N����,Y	L�I�{�h�c7�����B.� �:S��-�8�͝˦i���J0Rǭ��s]ժ�����RJ"��/�Mz� 9�8�hegU5���(D���:�0}ǅ�.��=Uub&'���(�9� 3#��6m�6g�B,BI] B��j6�b��!����rEED&6�JB�p���o�;�5�.]�t�R�u�ZUU��ڶUU����X���JQ%C�>�>�BUU��Uu�ġ}�c��FD�5����h��G�ۛ[@��/���)e����$1�=<�I��fd�����8$�Zt|T�q*-��ϼM���ݔ$��>� Sdg�ݝޥ(��F`D8��"��U��k�+lr�J3S�f.�1��ӓs�#M8����?N֜��������4P��B]�ͬ��j>���+vq$�i:�4����}�����ry���쬊�N���|��YG�,}G�%H�j�~-!� ��ȒjFL�oUK�*aIC�7� ,3M���}j}�z&""d��
��f��� �gb��U$�)]�t1�p�ҥ����O 1K۶�1d���`����d���ef��T1#�0��ʼK�:� 1q�[F�ܣJ���ͭ���۷sJ$�V��Z5c�����|�g�-VWhHCI�������bf}��v�{!ab3�@{j�_�(X�zh��g��8�J�?y�~g��߇u����� �G,YO�[� ��Ӌ��s���Ye��� �L]�Q�3��$3�I����N���Z[Dp� 2	u]{�ե+(�9��V�ajSt"�03�m{��]D4�}��Wf�r �ɚ��C���p��"�R�+�����s2����Sv�O���5��Y�l���``牥��3O�bXK�lԒ��wP]7�OE,��sܜ�� "�"D
PH�]%;��� ���2�M�ȓ�������-ꍃ����,��>!�^�vm��������..�I5ᓮӛ��� Wh7��k�֋�Ĉd����]���S�?X����h˧�}.�i\�Cc\� `hYz�����FuL!"�d���,䬽� #�07�)�����H;- V�L��9%��3z�	$U��f�żi���]r$����Jtz����Σ�÷�|�������8y��=���x���Є�	6Dk��,�q��0��5�>�9%�|tt��u���	!��W#=q�� bd�㛚s�:�:H��` ��$�J0PM	��* ��/t,"9���d�=�F,�S� �7%(�j��� d����䑜�y�ʕ��o��Ô;bT�ã�#1�*��}���9wz�? �	y� !1	����(�H�U<�Y����T=��L�gZ%�4�Z��7���A��>�Y�K�ǉ�V�$�vO�U5+��z>��lUW|��j�e�p֞�|B����O������! b۶7n�0u
�������L��>��i��=9ygJN�O2����$Cv�ı!d��)'B2D՜5 87��u]���5�@eث�PƑp�e����0d{+�u����Զ�Ӊ�)�!=�ٴ�*zq�ԕM�5g%R�L��'�����"R0#�z���ｻ��W��9��������q�W"a��r������9KlgN�۹}6��ߦ��k�p_jDt��id��	0��ɀ�e 4��fYձ�j���֦�1z���T� �|�,�A C [�b\� 
��P�
ʺ䋩" �/�15��l��g���&��,B̚sV��� C8[����������}�|P��w]�3k���[��*�gL����X�R�e��;�'j����V'�����Y�� ��,����3S^TծM�jVsdDԔ5gcWQE��%L��B!0 �46$p`�)���;~���I�Zț����2+*�SJ�Q		�TrN�D�
� `	���4 ҂� Mys���׾��|?jVUb6�6"��E���h�����y��z�̌E����ң5B��	��Y��*+@��!c�gg��Q��w��M3��P�w�V��Ug���rաy��W�U8�#��5[N9�Y5�4i[�>�D� X���Y��3�'U�������1��X�*�*�)7�����z����x���i���CA�xd3P��Z��G�icfWm&L}�( �U,���,}V��oA���� c�!���}YVlPM��#�� �}f|x�Eʖ7M�ɯ��rU���|�fh7�	ٔ3*�2��lc1�ଵ��D�ã���ŋ7��>e"Y�WV�<~ꨓ��H���z#��=N"?\�A����s;��k����'�<�t;�  �V԰�4h!�A5*]N���q=��̬4,�K�% /�w�343���O9�WY�A	N�U����HD��|6�ճ��ˡ�U��9p8�򓟘�
}�3Lfv�e:M+�C}V�9�]��(�P��%�d�ß�,De������kg�B�20.^EgP"՜���㽄�Sz+! @Hf�#E ����0v�GeV�ͬ$���cJJ@���I� ��w��]D�ڵko��3�������~D�����k�E�������E�^[8��Yt���?k=��8�~��'2�Ϝ��'���)�ǟ���W���>���P����Y-|\��$�f�X4�y]�1D�%��â8Ih��� �]����<Þ�-Y�f�GG��CI�9/�E�XUU!��e��vrS��TsP#�y�ll,fuL9�;<:��޿�DZ�N�@^i�3�M=���]���'��  H���٣�� �^ͪ
Imp��6����\�u{�\�����ucYQ�O��'��G5�e�z��J��)#}���� ��U��b����ܞ[����6�cU�_�?uh��j�O���"M��` @V
�F����&>�2�&��� !�����sX�|�r��f	a6�oll6��l�*4A*��o�������5D���9��m������)�M���i�;c�Xx�m,,����5��$)!����x ��㊒��w��B!d���/9�G(3�AJ�� �F"&AT2EP�i�/����r�[MD܅O��W `@#t%N't53�!�͔�gZC;s��rY�Y�B9d.�j���RNLlY��1 ��U�,����e�)u[;[�]���w�RS��*h��!^���d@W��hz�* 1�S�RDte�2�l 9���o 4,�+KZE<�� � �3�-{�4�S�N�lks{NU0�e��K'kN��4^^;:k��H�&��Y�g�\��ϟe�5j��:QLί�]��%�#�����%����g+��w��|�<2��{�)8�oS]���>�9�uXߘU�8����f��0�Ȱ�Z�#�X�/\HN�-��9�$�����OM1 ��>��|d[��Õ��묢���JTKJ��,�P<�������x�(�s�wt�U�"�R��aGu]7�yUU,2�T�;���hf��X����I9�>���{x(��Ҥw^"r% a�f rv��4��F,�TU�\^�x���[���u��f���'�2cY|$R�T2OY��`�L#��X�����3fkؗ�5gy�&��	O�F��P�$=��(��8 ��;A=�h�A��5ʹ��ygpl����I	׳ϵ�3���H�C�D��)��:�	�+F]�]ׯ�?a�?ɲ����>o8�t���7�+ӗ���x��& �bΩ뫰kX:�t�� ��b�dE��fӾ�%
!"�8��j����@5ed3gjU�F
]{�puq26/W�F�f�J9�՜�9�X�
�F�j�΀Ϙ姡�1�͒鼞]�t�go�Y5�h>�R��zc���� D����:�q�)�Ts0�ǂ�C�ا�p
Ύ;?�Ű��j3+{�>%��e�h%����Q�j�֨)la(�d����2��>�р	4b�H�� Y�w�R��2�9ݻw��T�'���'}���<�t�-w�.]�o�9� ����Y|�f�*�*hJ)E���%��H��rv~A&��X�wd���f"�Y�S�H��ў\��(����(8�ʖr�(���`�v���f��r
M�ܽ���x_x��wڶ��d�Z�\�'h,��lp�9eU�H��㧆��A�s;�'e�,�ZِX~���es�tL�F ��/��?G0 8�" ��3�`6R����(��L�f�Х+a��0F @�xɈ?B�DA T��39�f&}�l���PprHN.������t� <�4�L(W/1�԰�A�~�(��##S0D�h��eU�_T��Wxh 4�,D�L׊��V!��eͅ�#2�0(�qd!@͖!�m�9`T����a��;�d@ C�� ���~�q���JB֔�)�I(3 �,�`lĤĀHEL� �h���z (�ydnS:�j���gg��Lk��D�dfE<	�)�����_,D�L�m��3Yf�[���	����xK>�Z�k��<_8�,�n�cE�U�aZT{bܰF�󛀢�Y��R�D�i��k�8�hx�؜�)G	�����1IAE*B�H���q�3C�g�\qRQ�#� �$ a�p2�M�ʞP����{� U�Rf"�*aB3��2�����Q:Ӎ��v�k�f�8j� 4k�wU�j�S������D� ֎�����spԌ@G�GD���تp  #��ƕ�P��R�fP�����Ν9)�l>(�d�!�(�=tF���ՔJ#y���3���۹=3v��ĉ�҃�T�V����7����Z�U��@J<��<��i���R�UR44!�:�:��I��0G�D��2X6������i��j
">`YQN~�Sa
 �pGyǰv��gh��KZ����g�9��s�"2\6����.h|0Q3 �*+�r�fgJ QUS�3�b$Ԭ���<�I;Q/ x��80�p�"&3��	�JO5�@m3�2 ��@G�
4��3��Q�!9��W!t}O.߆�ҵn޸qJ뵐ǚԠ":A$r]Ǻ����L��Զ� ���&", ̐�����_�0�f��N�Zr���i'��[��i֘�V��UG��0��}��w���*<�4?�ϝZC!A��j��CE�F�9����Y�����f@<��G��� ~,Q�n9l�"��t&w�3e��L�q2����dd���s�U�u�up���\�g�3��W�Ʋ!bOѸ@[d��\�ܷM��&:IkΉ sJ~�B��*���}?�ϑ.33"45%00"���2=&����P�@�3eO1��V�=����,��j̴��E��R� ��;�����k���.�	 �H�d��.��('��B���)����>�Y�iw����d6���36� 2����\x ��p���b!uԫ��3"hK	Y��J����d`���b	#�T��II�
D!���)f�42WT3R����6u�\�m h`Y����(�)���D�L�n�
��F͏�ȗ�H�	������\w���e�2�d~��=-��*&2"+ә��������ʅ2|A@-kj�L"F�O� ��l�gKD���&�9+g5��g��r�>�4A��f@ ��@U��Ԍ�UJSV��2fS4� @��``��S�N` Nh��[ϰ�����������9f ���}�֧���zlmzQ�Lͼ�i<L�t]gjɒs��}M4\��<:���a�x:����c���?��LٓQ����k�3�  j����;������v��8}�N̼1L'_ˑ  �|��0uM��?s���_���c��2�i��
cZ>�B|嵑��% P��cd�@�N�Nf��(7M���A64B�!�Z!�BS.m�"���c�g~�_�S D¬��~2�����FG���񚞦S)%Dt���]�m��~a�lf��@�вZ�i7T����ﻮ�c���wXUs�{BL��Hɰ�`�L���jf��HF!*?�ǎ��9�""�V�U�!�  �D��ch�=�\N��F�Ub�v��;w��O;�  �)aq����{c��!kRM �j�1k"$o"��[oK� �u;O.�������6��38�a4�P@V��>M`+�i� �9�_� 5��Ɋ��s���Ii��f#5 D4-i�� �PB����L�֌5��*i�;Pt�  4��V5�K��ry_9
�l䑧[Y�(x��Xu�i�T7�e�%�����ly���{�X� "'��m�i�6
h$@4ﮩ99,x�ՄL����ЅlRJ��I�S� ͰOmV��,������q��#3ߑ��f���biP�PR�h�x�/Acb&B�RU.l�9�52!����?��+�0%3U�Y�Q����aL'g�O�"Dd�I�  	R������-x�͙� V���{ϞlǬ� |�6̓��M����N���������v��O�g	 �j��k�L�YF բ�G ���cK�Ƹ��(�aq����:����/��#2��T
Y� h��)���]"�{�[���j&@U �����Tِ5gI�F��^�z�sޏEVM
�!��s�"LA� ~^T�u�b�Ā ��&��LfCR�#�Y�bd��̌(f�u]E&�Y?�FTvg��D(]O��bUml�-0����l�0�/欂,ȁ%��쀨 fD4��<1�YPug�S�I�_. #�#��w�۹=!;�Y���$�8��r��>��Ȅ� ����ܧ܃fȽ9�`-  V53T+x��� ��� ������pw�Zi~"�!���*K'3���B��#ٓQUcص�U�����TJ�f�s�B���� M:r�>�v�7 FP����2�V��k%˄¯F�|E % 4E3b��#t�EE�����D��Jմ7�u��P��r֩6��YR� 
d���ƀf���E���{�,�UN3�q����߉䙥��3��P0�r�x��;! �*���#0������Xܹ{� �GWDDY�WI<�LSdS4DP��c�(,)g���!!���ޛ5ٲ%�A�������x�JH����j�	a��0=
^�1���x<�Ѝ0��L< ��V�5��u5t��T��u�2Of�!"�r��WĎ��9y�[�V�[٩���w�X�|�����(J�N��U?�6���)��Go��ƕ�������h_y�H  �M��C	s[�G��Y��uNM�/�+�l�BfY�I5C���/:�
q�2�zqZ�-����z�TP���X�ʰ���A�)� ʺC�f|�􋎈�W���;w�޻�/�;�)on^B{�~����95�k:���ϥo�`*�2���s�][�V^���i��H1�#��inUR�9�U��8�몊R�_UA�v�yV�v�%x+���dV���ξa.�w�hG�h�sR5��t�����Ӝ��KuÎؗ2�°A$N���"j����v;�,���� �π���[��=�Y��=��А�r}+'���X�¨9眽U��X�Ȇh+���c�Kƀ����8;_,��D�rN�o�/@R�j_��u�O�]�Z�̫���?0C��:���^_.T�4�z�b}�cO�E�� ��r�    IDAT{��ڻ:	��B��ޙ ܥ�m)N��*@U5u�C �ک���̱��y@h�D��s!�S����j6�����X�{��['͊>h_R�ˑ��9�~��� �����>�,ϧu�lZ���¯��3v��eH�K��I�Զ����l�̶�L?��WdbF������뛿��f}�#��7>��b�?c�
6��U#ˑ6�S�R�DeBU6�2A ���P_�,�H�ע�u�D4���Ȍ\���'灹�~��������m���CSP(`W�*��w�sو�e#_�c!\	�|�ߵ!�-̃3c�z �i�UI�j�)e����%�3I3�.���P��pVm�Fr&a�(y��ϛ3e��I]���ʚ�P3V�XB
�Z��.��b14;>�DB�ҕ|5�)�
�n�:��% �Y�.L��3��ڭ����j��"�u3fl����-�eH@��j֔u[�{���
k�o2C��>��Q�9_��؈�����s�G߀��W�1�� r}>�I{M��6�v(���l˙��)1:��p�s���q���#x���z��f���s.Q�����J�㙢O�{�90x4U>f~�Q��	���o�+9�/��	Y�QXQ�ٙ���L�u�A$�4J۶�	�uI��=nD]�@���@PK]G� 9Z��$#3
.�ݓ��A�(���"�I51KNɌ`���E�X�Y:@��>M8��8�>	U�k��k�O��S�6�3.
��(n^���̲�l�/�r��J<.��1�sf��2��v)� Q� �uR)�r=/����|��et���w!c�`�[��Ɣ��W��G^j'�ᆽv�����붶��/dWJ�v1+Wg��'�w�����O����?��K�C��y\��l{c�E������_�("�+�@��4�J�Q����[kU�)�.唽������Q���c���L��+k�2�9����P"�$��0q��^�����)F"��OΟmb	݈N�3�� �M����x	ء@��]3� �pmE6D	��(�d�iZO��d �F@�$&b"PNy��x�OdU���e � ��YK����ȋ�f潻 T��u)'"fE�:)�$�f%����(g#��T�� ͺ��;_-I���[5�7`� 1�@���QN#K����k�ح��7׮�����-��f�40�k"LL��,唒��Ri��<㴳5q�1.ܰ���6{���䜃�jD�����+2�����<�0�`�k�=��p��]ꪪ2Ӈ4��d��)�k�_9?W�h�3��]�i��`��[?���
5!�B��B���1Lb$(d�Ӥ��ѾsQ5����R�bUy���^\�D$V��-�:/P21�(�M~*�9)֬��ؐr�1�V�85��O�31��	2���j��" Pe����?�O�UݶmUU�ߪ1�l���h�1�~�MM��9ԛJ'K���1���ܠ���g���Qq�筝�m����/���2:�]�.e7����#���o���$&�I-!�91����О!)a��N�c"���T�4���'�,��M�]_�~S��n�&��Y(<�*\�\�R�W�\5+�E��[I��w^5�D$ 9W 
$�j�Y@l�E�:Vu������7N9eQ�1��u]J9w]��U�
�L��N2Q3�Ts�: ��rF;�5|���҅�
WY���@F�"Ȫ��������x���y�A	?�w��O~ �m��|�^�� p�[��DD�P�,yZ4M�*]@�2�A
�b|�vk?S���%�,�oc|?���i��Y��.핶EK���z��wUe/b�Ds�.<��X����4��@�K���e3v���bv_��7���a���//~Ɋ�F��_\�SRR���/��?�gJlV�N�=��;��=�W���B�P2p�FW)}�c.M/���L���U5�2y�D& 0$P`�*C�@b�i��D�KE\AjX ��yi�þ�}��ݲ�k�$R�
Hc"m����V;M)KR+\�Ps�u��x�4CX!P ��ZVH���\؊�ϒ���_�4�R��(a���f�K��YMY��ps��R��S��{�Y�.��Iכ�z�&�,)U!29�oW̮�9]�q9��!;��w�������A���D�� �CoZ�ф���SSJ�I-�v��lw�l ��4����L�2�V�]����si���xcJ淅tV麔I~��9�0�-^���u�] {J�����\��\��T����H�"8����PU�b�C���M�E��Q�a�6&LB$��SJ�i��Z� ����-� !���w~N��}j�����!�F[�w�����@��;�q���U�|���O?�"0kz�F	F�_ 9��{���#�c�[�o��[�57G:�aQ/��P�b.WP�r���6]j,�)g��D&��nC?�2D�%�P*��j0 LNM��y�T�sG�撙CFm��mԨ[��;��BO$=J�_��a%i�V�~�7c2�nVk U �����լD�#~םHh����LҖ ���� A����b��1�NժP��CHB�(���U�����p�MY�2�"����0O�b!�u48�`۵ �_:ϾT�m[͹$x�eJ��=)q!�Ur`Z��Y�i� )e��Q���
��>�J������ ��=|��}B��C���K��TN80�$[��.���	cT��i��'��G ��}�'i?a}JŶm��p^t��i}�Et�����z��y�DYF�)5m�RJ�j2d3����-3o�N^�"����?̸Ⱥ3�3�m��d^h��.9��~����ĪXUUլ7 hWC�4�J�PwJS7�$y��f��y�$�S���3"N�����:�!����"���,Q$:ڹ�x�L��#P�Oa.m��JL�r�Y;� ��,u "yO�`-	X��5Ƞ�B��X�x�U�����&�&�*(��� a�d��M�!�����1@,i��%R"	���P�K�7w2���M�lfo��k��M��֑;�9*�v(�q�v��]d}!������q��sd*�aܷW%�%�~['�_j<�4#�)�������M��)s�ywM^���c����@;��#N�㒽8Ӯ�f�c��ֿ�[���������������̥�6=^26����ؗ���g��mX�Qq�s9����7���H�I'�%0���`��lDb�"�Cc�cU�*�������6Ќ��"�r���*�9+��g�:UdJ�%eb˪D�m��g�I��)u�K��5u��B����Y��f�� �0�*?\�����q��䭇�P�v�ZU��*uupp���G��"R�����op���;+-)s���B��d��_ж��ٰ���,���w?��Zp�"��/~�k��Gj7�ە��k�욵�E�z�Y^m�d2��otU�p<#؀<�m�gY��lg{���U} � ��s#bd�b(��8ɒ]��eK3��X��Y8ކ��z:�z�\vM����%���P�g��������w_ؓ{/�
}�7�@�e��RW�;��
��UdR��IY1����¹K�m�vE�����]Ju�̔5�cz՜S"a3���fֶ]]��){ږ�ͳ��@�D�/�I8pIя��i�����9��oP.��(R����W;�%o�)""��XFDC����H����y��w���7�vk?Mv᩾aa�")3���A�)ؘ��I������J,"���@v�A�ݓ���:�օ}�A�����GB�PS�^��YR�ϝR�R�s�L"&�A�o��o2���X��zm	��,�ҭ�k��~-��H۶�~�eD �i0 ��� 0`����I�D|�c^ ��6T!�i�&����.�e�'�j6�����ݑA��I^U3�� �BL�Q�������!De3�٘X�̲*e�P�-�1��:M�2#f�.' �A�y�m�b�q��Q��L�$�7՝�jN�5����Ii0�-z�ʪX�4o��������pМ���l�k�\Y.� ��VM@XX�m��Ĉ8�XU`&a�W�/|�lG�����^���o��F�����qv׍*V6������-�Yww�#v3~^��M�Y:d�ݔe3�f�,{��BA��H�J�9�#T��?�0����J�X�e��*�(^P�|M ����e���\(����G��_�O.��������	F+lDW��l f���1�PU��	PMI�b�u]�6��
q6�TJ�d���D��f���y����t-�Bti���P1�'!�)�#"�R�Ĕʹ�p@ A朅V	s�2\ !(QT�ʴ����>�|j=��̬�� YR03�[.��м���"m�WWL_�`u�.fP���i�N��0�vk�6�K;K#6b-�=w`�9�R�����͖u�p��Ld
HϝI d�pg�p��КK����&&��U���v�	1*����
+��=B��5SMi:��&���������"�������_�=W��:�v	�wRm�Lʺ�h,��3̝z�@����[c j�9k���B������G�9���.)H��C*���GjNG�\>��Y�'3'�b���3�^��V�"꽅�Q�&P+Aڔ�l,�i��t�>#�|!&Pi�� f� 2�0�	$(�'e��'��Je�|?�ubהSS3RM��M��|��I���=Ry�(���. r�d�d�
q���W����N����㭽]3��oxz$^5���E��������4g5�d'f��P��Q��=�{7V���j���zݒ��r��[�^�Ү53s��{�����-<xp��	ps�gW�U��[�L�DX�,�4����\r`{q��&@��Ĳ�ܵA��B`a�������2)B�ZΪ�bfK/�E����I뚃 H9��(�����edu9ka	�L�ԅ J�\7�HUONϙe�����5�g�i6S��F�Ɣ�b��y���k�J8k�� }O���H�괪S�)�N��/�����d���f�v���W,��&�YbL�(��@a�x�C��[�&Zi;s.�WH�lSq�J�Y͊���K������/����hH�|`�l�%b��<%{A{ZK��6<2����ȏ?ḀN���m�Η��O��������_|�/)|c��4*O
�Z�ɦ�8EJ�Jd���&E ο��,�JD�U�Y�UUs�/�i�ʲF	1J]����P���0�V�	��ų��C���c "U�)��QK9�����6u]փM�Z��l�QV���|�Z��S���tj�n� �Ʉa��VB�kuQ"���f�3
.�J�3R����A��e������R�����i�����&���_��? ,�u]y�B�XU�{�[���|�}{���c�g�����k�2�} ��,�R�<�8������xI����cxm;>�X-d{�H��mJc �S`_�~����NVR"-H���g¬�֫�?�a�:"����������-�&���م��������"W�S��C�>�pl�iم�&}"f����.%#�&��$V�Xb5�JES5)��=��?��S������v�5H1F"Ҍ�S�I�T3A�<�Y��#��O��>���z�vDΒP�p4@8�r^?=_�����R��8k2Ӛ�P��Ď�85c��ė�H�?QJ�
��i��b���o�M�nn#΄�N�2Ȃ�.�,|��3��6�����]�Y��7�٘	�EA�(�խ8$)s�A�Y�Q�J{��	F��� �G)ԙ� �l�R��2��XՈ�(	�	�#�=?�ę�D�D��K�eQ���<=mA��=��m�B�]��'s ��g����f����Ƶa�۾M���.UD/Z��qY4�BΙID B G�u�M��[�
tj�+
O��~�LU�'ud2fA`&�=v1˪`o�g= �vCD��#ஙw +K�YD32,�eCκi����P�ڔ��%���k��O�����N�{�u�4]�c��)�B�1��EMm���e�����8J�k!X%�E�$,���B?�{{�,�J��˕�k�Je���'0�������=x�����>?<:��:#+t|�^�i�z�PA������W'eU%��Xh�n"�(e�~����3�l-�rg[��+� �v%,���`�ױ��e3�8���Tz�a�I^[f�^��_�R)]@L�փQl3.����֣l3��.���ٮ>~wp�+E�W}�����z��
�n�i:cf:R��ۍ"��Sbf�3�pbU��9��Z8Խ����L/@�c]qI�yp��gM̠Wp5�5?��uyS[�֛�&�0�Ϙ���x��W��m�G����*�P���W� �[��4$�	�=�16)!3��A� ��'�w2�8�Y%��s
�Z��YPOb�L�Ԓ�j�
�tm۶�ڴ�S���l�ڴ
!�H$�@H8ԓ�b>�Ϊ*����j%BU�Ӫ�Φ�*���(���z�`]֛ L��|ʄ���A��l�>�?h7�i]�ZR]��c=y���q�v�ԧ�H@I��sȥ����ۻ���M+5K"d�_��u�ۯ� �"D��o�\i��,��L5�]�"?vs�yђ���gj�����������kq.\e��GGw�Sa������O�кlV$�߅5���zȳ��wh��$�8`Y�O����39y�n�! ��$"���"H��Y<3沈��eY͋����e���{�!�H۵��BR,�W����)��ؔ�i$L��@�1Fg�������.�����|uE�XM'��z2������U����^��D��l<Ŭ\!S�Φ��t�ӬTb�mJ��o����A]�����ws�¤kef|�g�Oʅ�aP+�+	�n��ڕ�˃��6ޅU���s�z��o��r1�j�qdy���zM` ����pDIQ^~��; ��ɴ�V�/������D�rֿ�
�PO%�7�7�e��7~È)P�L��^��[?>!��?�8�qe??�4�Uv�O�`8��c��?'�@����!��Ɖ�T��!��"�H�aqVA
̖� f��MP��`"w��k+v,��!DUe��5��Ѧis�5$�-���r�aD�d�M�2,'�XQ5A5s�)kVi���_|1�M۶3KK[u�KY��RV��!� ��=O��Og1ƍǗ�+MgS �j��د����yx�����??_�\O'��������L	=L�s�¶b�]�P^2���L���q�W��o�־���>Kk�����TI�ʯ�A�RJB�@0��1BLf��\��SP��o��;� ]������m�����3�w��)YH��~�DL}g���UL�JT!	m�5Mc��/~��b�n/�6��&�r�[��? =Zd�h���(�;�oJ$��+�P����^D�jdY!��CUU���L�ՇK����lZ�+��5[89����Zo, E"����^df��K�R&�.{k۠�\P�>��i�8F�m�l:9X,b=�Rg�Is&�P#uyeMR��.)؊�?z�s[U��ޢ����d2��i�=����l6��xd�������;w���:L����g?�K���.�6�aV_-�t�R-���Hp�UQ��Y]�K�6MS��T�$�fo2-�_ $�t��%�^�Oڛ^�|ވ/c���E��"F���y��r�O�7$%�^��vM������a�e���j���.�vMG������Fs�����"`�v�{��{��/?ygx�QO���$NI�[@G��Q	,�l��$,E�g��Z�,H)�r��}�:�0����	\�)��ۇX$�7b�P��30)������&aԿ���U�N��>��df]?ڦi�M��1F �10���rZ���ڦk�yUU{��M�t�ќ���"��(H8>9)[��woo��*";��l޵-Y�C׶�[2�P2���|��߿�����ɿ���1�_|��{x�z��k<�jj�LD;션͍    IDAT<=��V���׳�\��#��[���Bwy�sR8��r��ьalȦ��jW�J����d޶͎n�WWF���ЁG���Ӽl�8ZI�L��L��
�s�������}o��f�������?���{7�@Z^�Ǭ�;�Pb�@DBΚ$@!ͥy���򹁌��Ì�h֥N�� �������)�j��0���Eu���y�c�¡mΉC�1XN *�,ۄ���L-k�4e� �R�d  5#�lFTOK��w��efK��	kc�y�^w)�@xkLN|ʐlڶ�fe��p=��3��k �Ԛ��6p��h�m*�{ޑ�s��LO�NM����G}4[̹�0ב��Uef��Rd�bo������{���$��~���;���W���{��V���<?��N	˖��}j�u��1KG��PWy��b�ˀ��؛P�|u{�ٹ�	�{�=��ީ�����U�`�z���QvW3��50����e=3��9�Yi+�J_�F�I3FQ�B&�Ы58��љ��&⒣!���<���sj\�%,��F��{��y��*�`���fþ�)�`y1���[��D,2M!�e`���i���}s��Y�T�L��>N)EM.�-
��ށ@j0�G�!f�� �C�^e"U��[�Z`�oeҲf�+j�b
�����r�AmMU���,ljDD�ks�O���b�dդj��J����ͦ�)����
�������d2�6M��c�1Ɯ��.�(L"w�˵��T���i������i�����d2�L��bєSۆ:�F���O��W���>�����7���'������]�ּ���+�E3�{�.u��'����v�ĭ��ϸSs���^�G! ��倸���g*���K�̲�/��������5�lF�ˣ���FGԓ�^�m�$xw���q������#D&��>}1�P���T�ZjF��˝i?���ɳ�lN�֩1D�v��^ݍ���b	������PU�%n6f�w���)���R[���'ȁ�9�4y��k� ��?�J���e6��5��3 � ����t��3	�f2����K`fv!V�TAܥ���@�k� �fͦVU2�S.Z%f�%o<�N�Z1���u��z���zE���|�u�Ɋ����բb�-�auDĦ�Ȅ;���<�7��=�j��d:�|t��|u��ɣG��ON>���b��!ć�>���/��y==9;�)qf�i���?�O��?������������o�����Ó��f:����ŝvc+K�ל��H�kD��i�Ea$�J^�Z��^֟��3V��I�˗y���q��:��蝈m�x��6Ϗhǣ���g�9�+��U`���`��me�n�Ec�kM�!�!��E��l�����y��%(0A���^�k{�����)�b
���m���.��Xeևe ���b��>x?����u��q
�l@d�Qb��������}	�Sn�f��,�볳�irN"R��<B�A�g���^��6�4���<����mff9�D�T��'Y3)c@�(�ɴ���B@۵A�j$����31���L)^5��:�)��Ys`o�g�]�I�u]�Ȣi\KDX���!�¨}!p�!�"`R� 3K]�R�n���=j۶mۮY�*J������p��m�����=����ַ���|��g?���po�Sjכ��"�U��?����i����?���_�;<��ح6��L�zc�s�o��B.:Kt�n+��H�9D21QwY�ڭ���Ξi�^�Z:+�����^�����<GV4��b �  .5�n�r���3VRظ��1�������\A��DL�>f.�z�ƞ1�/��\�>�\�U�5�|úmf�I=���Xu�����H���(���H�O��l���'���|1�Ϗ��t�[o6���ٳ��O�={֤�PB�97��4�f+�fIe���q)a�l�g��3�Y�4!I)�u�d�s֜s��8��;�^qR��mSGb$�Xց��i �L&1��E�ۍXB` F�qU�k۬
�*�V���k���&m�uUO&LQJ_J������9�HDK�u�l��5����+�Y��Y-U�zyV��l����ij�����b6�L&16�U�m�æ�|���~��O�{��_�����_���Ւ�SN��$_��1�8���1l�r��D �2�����=P)7M�UE���A��:b�zY�D�~��1���g��+.鲞�s������h���r?��R��-�M�u�q��ヶ��v��JM⦡�9;����1���M� S~��8�|	��ؾ�Y^w�U�(��vxG���D��faH�6�ܥ�uu]��Drj�W{
a��� �A�Y������dZU!�(��e1��b��'��u�''O���|���ӧM�fJF�����;�9g8�}���:�������t,�5��>���J��Gn�z{ A��HY;w���0oR)�6������ŞW�s�f��uf6�Ln�d:�������t>�*��"�PD��!� ��U��������j�ܬY��q�to�u*���4���"k^�&��
�7��;=9Y�Ns6��O���������W�{G�����dӵLT�u��<�͘1Y�x�Ry��fU�ѳʣ����7�s�ڭ�ж[~3�B��Q�Q���S� 5�.�G��E� �w�x�`,�(�L=���ç3�V�\�<0�6�ڃZ����@�}!'���	yp�jj5c/�P���m��݊�yK��!�"��Z�H�XU�����S D�p��y��d�HyL)&�+�{tp�7��U]�Y��f�,dQ8
u]2��I��������|���㧏?�9�d�H�#1e�w>�/f��Yfr�ߝ�kQ?����}ocДHM�rs-�lC�:$|��i���KP�3�%�]@��- �ڶmJ��`iV�J� 4Mc����Mcf��4�T�z6���jS�*JI�� "R׵�c��M���t2������ =~���:g��簘:}���]��=��|�����>��'{���O�?�����h���{��:�������C��*d�T&�a�k���|��ׄw/�C̦��,�!���>�9��LB�RXHT$_X����ߺ���ϝ���ew{y��f�/_��_ֳ���������_��j��m�s� )��$� �nh�Ua���rjX�E���y\��:��G�˄sƸz��k��
�)PB��irJ]ׅY�����g�!����b +�������:� j�������~i��z�B�AD7� ܽ{�p����GG�_~����2Y`�)7�K-�3; H	H2��Vs�󇇉<��&Z�]�#Z��7D�)�ĩH�j<%��3˪YY��!�L������e "�N�V�Y%j`ܵ-��b㓓O��v�)��ԴKB���AxC5�c�ĺ�qRUq6]�u]ϦUNOO7��bV��aL��ڮ����}x��뺚�]ޛ����jup�n+��|�|t�t�Y�1G1��eq0�I(��ǔB�D�@���/l�6�:���fnA��vk,Ж��J�6 �^8ɏ�f�lԥ �����ؔ����Eܻ"F��4�,W8Η}Ww�΀�f}c\wD�y��R׵mX�����u]7���!�����!`V����Gu���
�|Z���V�e�u���9g�c��$Nꪪj�c]����x�v��.�r)9��E��h�zy��h�����וsD	B�r�?��3�"2���W��piEQ�ۺqʛ�nx���4�	 ��)�.4<�l�7��G�9�&�*H����t�^�4k`�w�p�\�2Aٔ�"K�����c�د뺮�u]O�U+��"�Mʟwˠ��f��4���r�m��{��]����Q��9"��e!/��z��t$$�)un�r��i,0r���eX�n�)a�.�4k�G�߼��k�t�G3s�s��n0�֯��J��d�mO.��[�fuǺs���e�g�.6���v��uJ9u��b�Ī��:;Ӕ��꺎14�@E��v��TM"����"DI�A�1�b1�@g���?���|���(����>�s���p2�ԳYR�p��Q%�dy���i�,g_�ᡛ���"�>l�R���-`fm�1[�:>n�!�,Ld9���@����*=KB ��RJ�%��ތ�B��i`<_̫��>Bw���f:�m6��z����U�i���ZŔ��9J��f��$�".���EG�d"N�-�=]�vM{v�,�������?z����|ֶm�6��,��Y�����?��������PO34�������}��W�*A����r�H<e9����`�����[�)�@�r��7��y��$,؉��2��d⠘^�~��XT
� z�-������\�K���DKz����Nb�V2"Vή�\�/ٕ�p��jP���?����(��_��df�׫�&���o����{���?@B��l��8��hFb�]�$0�泣���b������G�u�{��_~�e!�jV�ڮ����h�n��������d6}��޽{�T-��u=��inR�2�9�$�k�Y�Ii4�:�W������]l���R����C��5+��X�&!���U)�8�\�T��U��^�P�!���ќb�UU�U��_�Y�ͧ���|1��i��M`()�i`L�XM���z�����O)�=:��d���?��S��j:988���jy����rצgώ�*���>�����1���9I<8���ls�ރ�~4�'���d���(ݮ��li7J_�n�Fu�2'� k��Y._�R�z�P`�������C��r�<���/�؈���}�|���;u�+���~�c�Kf�p|ɮ�g����2G/�o���=w�sy��)L5?�?0ր�u���\#�@��������e�����	p�e�G��(1ĔCق�#K4O��.��4�7�a}�������9�7��je�̬��{�f2�Tu�6-�����F�'Uu����݃�=l6qy�L�ܥ��N�*��=��fY����j�n6�<_n֫��p_ �ZU�a<�'���j�^�M�5�I۶ 0gVr����;���G@/�f=_�U�� �-��cf)D�C��p��)�r�W^5[ݏI��a ]�����|Z׵v�mh��_{)����;��,1�(AΞ>��]��l����d�^V���t:�>�����Jb�
"�1Tu=�TUU1�d6m:�!���j�\w'ϖ��}�������:E�<!������"�o���V���Ȓ�H�'}k�vk@ bSS�`�HW&�\�/5� ���L�ᙙ͈��_>K;+���1Fk��7�c"�7('\��k$4M�r��}��GO�<	@���*V)���(`�$ƻGG���ۛw��������R�i�0H�����9�'��IY׫�)�mjW����f��><���PA��%Vդ�l6����@۶%z'63e(z��Y�f�ۭ���vw�P�"���F�o��Y��j�sI�2����Z�<�2��� � g�1M'�GN�����|�|�:_�	��������Ǐ����po��c4���4�z�`��PE���WU>[F��,�FG�/��*Vmۆ mۂ�%2��ã�b>�j	¡Zv��^�g��ѽ/���������F��C���5�ek2�:I�9���3��|�ۭ��O��k�׽}���Uܟ��3�On��x�K5���Y0-၊�,��2C�v1�@��0���<a�Jm����=GC P��X�ݿ����,�%�Y�R�)�}�A�0�xo>ۛ�g�I`n��5mUU�^m�{��	!T!Tu5%�.%S�1�U�V�M��a��a:�YI�"�鴊U��%K)� )���Q!ܙ6���R�9��{���x~o�N�IX:OfA� ��z�9�NU�D�,�L �33�I������Ӫ��:�u}xx���㓓��z���k��z�\-��ڛ/���_|�4H�UB8y�t2�<}rR/&]�_�ş���[M��'O�������F$2s�q��Ϧ���l�%�MB������ş���w�~���nW�0������'}D�|�?8֏!5"����mXyk����^]��c�UI���!�G��<�"DL�I�J06e(��n����9��O��_F�/� #ʽ�gr�T�.}�KJ4nǴ�:]�q�KI�k�I�z���ۯ��d�i]O������/��_[��?>.ZK��,��(���߽w��?�&L�L�Y���NU��tvtt�Z�>|x�ރ���������][�u�6 T5+V������|!!��X�����,�!pUo�'5UG��fu�|!Sc�^���O�֋Wz4Zʴe�%�ە �w>�����5"��v�7�9;��0 ο�� rհ���P9����9�{{{u]�{� ��U�?{�������ڶ�g����oR}��'�ŝXU]�����_��_QNͿ����w�����&�lY9�r���8H� ��ɤ�,����}���'����o��?~�n�~�ů�Ư�@U�k�T��o�N23!r&��X%X�w��Gg��}̺M�d�����d���.�x5o�f{+w��u>q���}StE�3U�ǿ��!}��<uo��)U״��Პ�����q>�b���B��r�@vW�ݗ�k�)��oԜ����$�h殮��|�?�ѧϞ����/��e��v���G�U�Ԥ6�.��<<:<<:<88��*��j�b溮	I�Yd2�pJPm����|R�&��8q�r6Md�Y��e�Y�pB��\�j����QS���[�!}��0�Fs2���������f�!�����嬪j�)��ru��f��rٴ��?����d2�&�_�ַNN���?�g�}�٦k���;X,�����)�����[�ֿ�g�g]����?��X=>��?���4�v2��Z�����(,"��,BR�z���W���-Ww
?;[�WXc�e�Z���"�r����m�R�m��ZFuk���+ >����������\�G^=2!b��A�ᒼV\�h��m��g`j�;~#��]�6�KZ���(uk/<����q�a�@���f�i�����7~�W�����*TӅ+}��A�Ã��?��p2��IJ��.�����l6��f�YQ������?�L�<}ʧ ��|s��ֲ�����Z��Ia��T���::M�FjC���ܱ�WV��n�q{�0�b��\��ga&���{�)	!tM�uM�4m�N&�TL7Mwt���oM&U===����gϞ}���M)qUU1���{���������7k�$9���03�8򪪮���=�Y CB(�C.�}X>R�����w9��p���q́� �FWu]Y������>��G�QWwu��T	��ʈ����T���{��o��ׯ]{��נ�?����/'����|���x�ZjӮ��z�\1��~Q��R����������p�hݭ��u��������=��.j��k� ��?k������F���#������ۋ�_�n�.��Qu����UL�PEG�3;P0�-�]ɼ<i�ïfF���o��h�N��=k2&�2�9�ˁ%Q)���6�̡̈��m��\f�I�$DTue���r�A��n^��Ӯ ��������TUTTTI�TM��:<:l�F̈���@*mj��4M΅�d^u���@�B!!܂�h�˩���JD:`Vi+)�EK�W�y�gNzX�]�"��b0��� �=��^&D�� ���q��^?:b)%
��'w9�G�<|trr�K�N���F��]���;o_���|�1�b888�>~��?�я�ݿ��������7���W�_:�s�ΪY�Z۶���&̌�aDN�i2�/چ�����.�ӟ�*ܼq��G�"��eV��;��C0S/���+"R��WG��ʮ��v&�t*�AO�ϵm�lH�`.�[����栂���W0��>�ܙ:	uH5_t��f~>g6U�q��� 62�z㹿e}����^����H��T�@h�^qQ�~����ѧ��yX��<{_�SS� � G{�:�6�TW'���� �fRb&g �O    IDAT153$�N�m���������E�LR�i:��f���0�	�)�f}�
 UL�" ��gD2cb3��C�!S�  ^��]�";��	��'#�(�����|'��] �P�T$�(��1Dw��(z6衛�ma�iU�NO}A�E�MQ�bB�Z4o2s888����՟��M����|(T��o}}��Gw�J���z�ֺ�<zt��Ƿ?��_�#~��oòY����u�6�d2۟��&�l>#"��8A�M�t]�����ә\{eCk��� �W�gK��q{f�l/΋V��g����)B
a�^�mk b�f��)� �՗$0@�>��=����/	�w��=Ͷ�L_��ҬC���K������)����s,�;_~��.������s�;��R��/��u�(`[���̛�� �CH)�����L��k�'s��B����00�oA�ū9�r��[�|��L�P�a"����E�z]���|��G�~r���sdbm�x����$R05#�*��M����څH��U: �����p�\��'�)"���[����O~|���Y==�N<�E�X��ɨ��X���ӏ%Dd#�c}���󯊨\�ۿXSjC����w��8�_��ч��NF����C5�.g5D���"j��&�Sc���7����������h� Ąj�Ʉ9�XO���M�B����~�p����'���GZ�z�z��oV��ν�@�H)�`�z6�F�p��Q�Nͬ�����7�H�ɉ^&�l'�0x;�an�sΥ�ѳ��̀���+����=�f����}��
T�*FbEB%S�bfh2�;$��{��;��s��=�عj��NP��=�R�Ϝ3S@U�ܴ����?�ۿ��?��i_�f���HF�z��Y���;9���ë�#,���jR�px�����_}�գ�Ç�>|x��dsp���]�e)�7/�8J@2+ �H����8����""�P��=k�~�%"��2V���(� ��ǵDg���<Us�E @�q�JL��S���Y
 PM����7�?����?�Y�.�R>����f����������]��v��2�N�yӬ�����U"Jg��_��?��O��?��|��ߢ�(DE�&�nZ �Z{[�];���}����S�g��2��:�����hמ������|x8��#��+�LmkR��K6B5� �����x�=\������w���.�TS�,���9Ĕb�@�h�=�I�"_tf��c�ٮ��KA����I)��N!N�շ����}��?��Sr"��	��()�13)��ȁ��9��IUr�!&b�����z�X,ڮ�4�_������tZ��kG�J��F�B`0 25�Y��6��w3!��e�w��]Oi�F}L{��3'���xef�"�
P8�s��I�o�����_Ǩ���bJ1�#w��D�jg)"*��s�bw��u�J"�N&)���0�͛7����o�z5N����믾�J��L�f��l�y睛�t�d��u�����*9�zVM�΁�=�XM��y#���۳�<��+/� �ic��*����ҷef�I�4�Q�]�a-��qj�#��)j/�6Pd1�躢s��2���`H������v;ϙϪ�@B N��`��v�!�|q�;����+,]d����ʹ���K�Bt�E��6D4�N�ӟ�����'��o�4���
;�.�3 N�ɹiZ ��b1��i/TU5�̧�iyt|����s��������ڝO��������W���S+0=���cԒs.}t��~����d`I��34%2p@��S�:w�����C�m�`�@� 9��=�K%"��D}�j/��D 6Hq����c;�(U!� �(���Ƣ�j��"�� R���ɾ���M�Y<>�s��;o�3����5R�z�f	���7����G����7����=����?��W�����͡b=�[�l�;9x砪&�����k�������o���w�����?�_}��w���o�[�݅��mG�k�/��
z�Fd`}��*���K�EDh �>*hxR�  ��ە���g�/����^��L���a_�0*� O���C����w5�؃e��l h�(h���W+�u��=8 �g��v�,wkE�����s��l~�����_�u��ዬ�@�ŪـQӴ�������������!t]׶m������� ��߿���~���������ɫG��J�a�\M���)~��q�BOI1L��� #��]0��l�x�<y������̉���;��6�Mg�U�(v�\�\N�Q��
��6�YH.�E8;pX̌(TU�7�7Mӵ톹�yӵ7n��L �5����G�6K���^Ko��Ŭk1�G������CJ�4��� r��(`�lZ�t�T�"��\?��7��郇w�O)=x�`��/���d�%f 4Gn! ������n��/%�reW��a#�gDc�� P��qB@ g�R2U�詪�r�����E��NJ�,D۵�E��C��gۿ�;�/����'����9�QrDϔ>w}��T�P����������������/��Ͳ��0'�A�lp�\,���l��˦H�,���������NOOW�Uιm�G���f�^��OO��ew}
 Pד��a`�%���
�*"��$츥�vH��~���z��1B ���.�5^��r�ph���S�!"���������>̤j�����ÈvF`D�1�ű@^a(R0gaΪjE���$�Rr��5�UUUT�]��=�l6\M��k'u�x��ã
��dE��z��j�n:����j�����1Ɯsȥ���=x�!j���Ƶ��14MS���<"r��EU�I�I)E��w3bf ���ʮ .��َFc ����՜����%���B���U�G��b!�������L��׿�
|�W���o��{��β�<2 �����z�Bl��i6f��i6�Ng��|8�R��5 �o߾}��m�6MSr�LΥ!����dRL����&����.9#ϒ"�L��۬fC�n�z7�o�L�����,�v���)G)�XKW36��!bUUU���ra�{JBD` �QE�zn<�)����OR�I�7��1����W_�L���Mޟ̒bK��{G�G��&��Ly������������ q��ܻ/Z&�I vF��Y/`d��3mX���3����6�M��.˅W�ʮ�r�Y�W@([0�A�m�{)�
`�S�����\M�`۹q�9�����y�80��y��C@D@̤/��|�CXx�g��h`H簶jf�f��5��b=W�7�_
�����tr]���d6�{���b~v�Uev[�Bh�=|�Xm^�>+�7�u&F��d2��7��\�>�͇m�f)H�9Vu5��B�'�Y�9�p�(D�UQ�l��j9�L82# F�� �s$^,�t���;{:��0Ժ u /�]T���yCg�3�N���
@gҰ fFƞ�PQ
gV<fƄ!	��As6BR���2"e`e-�y2�"�2q��E%�0�L�\�("�cd"�)̰9].�FA��7��br1����� B�A�>�%�1��-O������������M P(�ɼv~&��$��3�j��si4��y�)"0!�!�,��NO���xt"uq._D2FS"�Ɖ���x�N�Rn�s�?ɞӷ-�:̝����Z8���w��6l;?G�g<�宽�#��Y8��ۼ��8X��ซ8�uaٶq?%���'qg+h�����0�2�٩�g��޶l�F̹[���Fx�:���/�D ����R���TT�1� ��z�49g �����SL��4M,���䬪H�Z�90%Ī���n�X�.M�L&K�! �)�]�����Bf6����h�t��g({��>�h�I<������;UXU4����/Ur&Sb:� (N�j�e�X�2!"�JK1"T��bC��1QQ-�XLsׁ3�H�� B�*k6SQ1�"Ҷ�r�
S#�n��b׏�]?��������d���-��D$fn6]����W��>,O�ɕ]�W�B*F���m�d�o�܀L�@	@�a��1$�`X���s��׳�������ϳ `�N2:�iQ�L�(�W�:� /$$DfFD�*}y�IN�h� �9�m�}�_����\��̤�R`R������蓏o�ЍQ�����t1�hfh�\��L�(��r�*L�RT�)1�����ٜ��.�+DD���\P���%���8�#3 "x� �Q����P��#Zl���3��m�]��������4��|&r$�w[���(���j&]W��d�)`@4`v���* !R"�\�kV��w�b)j%k,b�C�E`bt����BD�*7@��L�r�gt���2��B\���s����=��PB�*�_��D�tw� ��,Ĕ�&��#B!0bߢs�gyeW6Z  ���ȅ�i�F/�ցz�%fj��P^�SEvy���s��Y�q=]^ ��z�����"�"�̧�7_1|.}g�D�bPV��t���rU��=�D�M����Q�"Z%�cED��T�l6��mc�M� @]�{�K.���?
��\���p�J��� ����}&�tr�~�EH� <�r�ۣ9�*o��� �T� P��"�Y���)�L�@RrP)B�;8%���WgD30�nj��MAf�}�ͦ�"�&�ص�RB�9E�1F�Uefд�)�1a�&bR� �� "2qq�բm�F�6T�Q�����7�>�{�~���S䨒�Br}dɢ���) g )�[t�.D���,���v-�|��!���,��(F�b���������Ry��� �=K/
;��om��M  � R��7�,^�C��al�-{i�O�.������1s���r����[ �?>I���UU5� 0ଞ�����1���E)��d6[lV��Ӷ=m�.�"EU!����?�Nc�o ��:3Jq��lh@�'�'�Dq�`"P%2@Ec��6�wl�)��/i;�/� ����23�peUQ�bETr�H�L�D��: ��)2��&a@5�]!��SմS�L@!ƺvgYQ`���!��������,.%���F��j��K}<�?�V�壓�7���o,_s��na��kgy�ǕD�����3��>K�z2�8��j 
�9g�!��@��Xp[�~�v���f��}Q	0�z�_���d2E�RBD����� J?'�T# {6G��M�/w��z^f��uy�X,��> B{�����0��RZ-ND@�m6��s����;�۫���B�����l���* ���s�*ަj@��* !@) `�
���]3T}VLD#���m#fd������j|j��]QF�C��F���j�y����NEā8���	0S��(N�4���K�f!��|�Y�6���J`%E'RPg�S�"BE�m��a:�=�������W����[���)/��D�>W�� ���XS0�ܶ�6B�����s�E��ʾ� ɴ���+����Fb�r��"�82�A�d��� Q�h���N�:��_� �	�k��;ѓdH�jH���d"f�b.��g����s�"��7��[	�ϳ���΅W�C|"��A 6�;~�����l6e�R$w]���r�4��4�RJu=I˘>�ǋ��jy�\���
���~�S�n[�bV���W��[��;-226RB3���	   ����-�C�՜��<��DCJ�i�L�v�,�Q�#�mV�z�{nFhfެB�.1��FUq�(b�D�C�ȁB 
�d@d��dPD������lrۙY)R��L �H� UAJidM!ƺ*M�^.����rU#��ƛ��/��K�+��zp))2�Iͦi�5�w" �Bə�E>#��>�O��m�.��?��� ��q^���K:�/K+�wӶ�3��"}۽*��p���
� �cHU�	 ���!��A����>�����\r���=��/��9�R��Tk���ٌS]��t2�NgMӘ<�R� �Z1Y��ޤf ȥ�2�7�.w1��fC�1D4F�T%S;99�{��b�(Y����$�:�C(9�Bo���ؽ����g��u�c��q:CG�έ!��IW�\���	e(_���L�*�����ޝ9��
f,��y��no�x�=�8n[6AMU�(
��S��EJ��q PQ��U�Ҧi6�E�4co�S�3��5��M����Lڮl����6wӣ# 躮�N6�MH	��)ɋ��U������A�6]k � �=�:s D�� �+��?#F�������s�:Y�Mז�ST�bTU��d��IU���h��|�D�K��9����,���C{���9�����n;��-�O߯"x�����k�9��%�����҃ڶ�v����h�=r6C�JY.���ڈ�:+"�z�X��׮�W+b�y릪���f������4MӔb!Ն�U�4�NSL�́�l�Us"41QTC����㼝0�� o�����w��{)h2`+VJ)""0ʦ���{N;4E� @jN�x������L����;�^���Uh8P�cտBb"Fl��B3S�,V��Ņ�1p=c��g.	{M�,���f�9d��kb̥�m��j�Z�J�����g��)�,��F
��x6�����-@�j��c�$ � bjjUUI) ���"���l���_v{8 ��#���BMw^���
w���]<��9�=�ץ�
�׮�����/����殿F��v��'{UC���N� ���(��cHƑ�Y�٨0�L�,#�H`>�90�)��K���ӷ��sF�s���F}�c/"r{�6�����c��J.�@������r�\LbD���M6��m۶��7n4M�Z���b�X�7��Y���6M�^w����m7Ƹ�����G1�P����|Dʸ80�n�k�Ҵ{�*�	���p��Ոiܬ��Rb 8P�:�:2�Q"b�PSp���!����R�#b��RJ�Q	�BK�7� 
��AN���XB"5��>�J� 	�L�ߔ"��UL
A��CQ�����߶m�P캖s��k�6N�o���/~�/U]=��zACU͈հ(TD2�be|�RJ�o��j�(�}/4q_ٕ}�-0����P���EJQ�8MS���$BGX�T�*�mvҰ�Ӷ�wzc`�w]��|F���IQe���V�`/ �D��-�����j�\�[o���G��)�.("!�'H�F�.��PԖ�լJ���)��EEX5��f�xk>��׋�ݘ�k׮��_n֋�����ĖU5ɽN5�)X�g*(]�u���/�lυ�����X�	inĭQd"�%A!29�LD�r!Rڝ��Q ��5�&WCSQG��ڱ g�2� bY���t-@��1ƀ!0�8!2���zr���7�p ���2V�/�G �����ySg"E2Jq��k����O~���Q���+��܏�{ ����gv�5��10s� �z~6;r}	ן�.�>}-��?��?����9�����#۹�=��S5�pD����[��4��h�0qU��$���s$kQ�N���tB���	���h��c$)eoo�ݯ}�_~�G��Ǐ� %��;]:7��t���%� R��ӞCd�"��r]�t63��jy������b��r'R��:��R��u��B�N� �H)���3y�q�X=���y�l�ZS(f�� �C�0�������kf:$=�u�l3�&�(�673U��"Q�H����Q�L��f��b��g\�������G=�Ĉ������c� ۥ����ý3QU3c@RQ˙b)��%�t��j2�޸q�i6@��m�>*�l��K4$S��VC����y��q��;�ʹ�+�-X `"����iLH���j �J��,ͦaV�HAR(�Z��?�A    IDAT�"�t� ���ϓ���z�"��aO,3 Ԇ&���@�}�8|���h�c�I�,����Pg&fS� ́S������_��'��rsz�@$frb���~���h� "YJ�RHU�,��f���{뭷�]�~zz���x>���!Ī�&�i+���j��r��:`�m�^.7��tZ�*"��� ��H)��0��3���| 6UD.Z��Q�R�� ��a�;�j={@�	*�vU����J�!�5{�̃�R2Gdա������AE:�@�V��F�s6�Y�K�9R���_2U��{���5�����Z+b��b���I��k~�EĜ�LE� w9g��R�H۶�J?��������"f�
6�K*�͋� ����x ��ђ?\}�`��2r Q-���f�୭�S�Xdv�I�]@Z�Z������EV_���h�����0�Ԉ9S CƘ8&#(��1ǔR�'�dVOf��y=�RD�K�*r�Q:��݀8�)_♜��y'���ss�RZ_u�b�F!D40��x����j��Ze{}�)�7(
�]oڃ餮'�ڶ��{�������ݼyNOO��Yb�S5�L��t�Y�6m[�k��S
�x6��x�ѕ���]�Fe�3Gғ�:�h���~J0SU�A=�hjBF��/���ԩ:���;�E";r�Į�&�fNY��("��a�!R��"�i��S�%��f�#���H�3�yaH�X��HD�k{9C�f�U���[�ǯR�����F�d㈵,&�Ub��b�ʭ[��\@�_L���9\(�)%�" �<ܧ����"�+���G8 ��	b���P@ �ce@��뺎u�*VU�'1A��&��#- Z0) H��"¶�(;ܡ����u�E�T����Y�`i��φa�25@�1@�u\U�W��l:�������M�!����ϗ-w����l6u}�`�����������7�nzg�'��y�����t�lD
V1��)��.7���R���O�g��_�5�OU��9�R�W�E�R�-�W� UGW�Hޒ7!]2��r��"�&�4�d��s�S_9wE�uf+� @��m�;Iԉ�3 x���r׵�lD5���SH�,ox�;���Q0�;3_<5�e����܋����f=Q��a�zCι��fs��ux�w~��ܥ���;ݾ2f}����9���+9K�\��!� @���w=����oWve�_ֳi�TSH!M!rH53e�f�e5�VU�RrRLUL5N m4�4��Z[�v:p�ً��2}j��}��Zζ�q�H�v`����S�4��MXryf�[��J%3�*��c����d��m��tz���{w�l6������Ǐ~�����xo� �Xl�ܫ�R"�B���r.���7=�-�W��y8��+��!"��Q
)��]A  e��)�jD"��!�K����C�qc��)�c�P�p���!�!�D�����'5�\�K�*�c_�h)���)R�F��7<3��)"`��"�Ǐ�x�������[}�Qie2��4�З�1pȝ#��q`GV �'^B���]��5HSJ'�"Ǫ��Bm��.�PO�i6�瓔�t���VUUŐ� D� 1u����r�ơ|IλmO�U��A�?2���@Df E!D!F5B����*;Q� jDdp�},n'���˝�i����k=��Μ��8Q�6A�,%�xt������O>��m�?��?*9�Ez��-;n�+2f���-y�6��j�Nt�ur�޽H��W_�N�����{��?�i]
����o�0���}o�n׋�j���
�J[�޾���?��B��mA\.tg�6빐��/T2�;6�I�>
�hL���̉� 0S��
�WA�EI�U��I5�>S�*}/��5��
��*�X�@Į�e ���j�� 
� j��B ��A�
c��c�eph�m�����e��%��J� �c �O�$;� 4�I��'����߸aR�������2�UL17��*�ꀍ��eg��6'�Sy��E�Q������OEd�Y=[��C��~��D=w 1 �0�}�'d����M	Q�@���*�ť�ӊϲ�� ��'���{���� hۏ��`��z�YY\���(��e�YQ�����ʈx��弽hZ���𓾺;����3��j�~���s�)�ScJ�9�a:�U�y=�VUcr
��R�"��US" -EU$늖n.�8P5A��� +r�̿�-<�ЛR]}��?~�޻�}�����������+׏�>��f�O����̬�]�i>��c\��w�~������舘����Y�P����ۧ���Q�u�`^�<x��bC�u}6���(�h���˧E�0���x�-	��`������A53���k �h�ar"u1c5"UAUVQ�\<#
l�������N�Dlh�=�xO8p �����HW�%�e�EK�"����{��5���"�
@֋�C�e��B4��㓒��t�����?<�v-?�|VCDR�@��4gx@D5c�CO��o����߉���o:8mB��1�c�9�"EO��SJ��S���A�d��L9�4�ג�d�ڮݘ	���F�:���^lx�3���!�#�s�N�4�9�k<;5|6���N35�vb6U=88��O��GF���w�݃Ї�����/�z/FXL��[�,�1���$UhP�-�K$bbg�],�붋!��f!������k������݇�y�Ú�Ν�UUM�4��ҙ)��<x���wv�ofb�wT��0�);���0��.�� ��^ \	�m�yЍ;nը�K�"��7�0���J|�P��]5�3�����q�e��ti{qD5�e�\ڦ)m�:!��ԯ�Q�q@d8!V��m�l�������㓷���d>��?���}2���3z,�q��r� G�\2���p���>}rW�W5�+��X�9͐�8p
!�S�>a���q33�z5G�(٦{�7��Ц*��'��m]��ЗRC("d��s)������὇�o�x��A5���K �'���Y)�P�61�����0�B(RV'��f}rr�n7u=9>~8��f��+ׯ�7�֬����\o���\���N�5��v�d6>}*��a�Kň"bD�Eg�3���{�AE��%��ޓ�����ti�RN,RD�,�У�{S5Q!���W�ϋ�턺��}�%2Ef(�@�u�� X�,Z��,�V����( �f M��D�LK"A��jY:�"��fo��W�h.Ӫz���?�s'�p61eO��;��0��� �,�΁C�NsQ�=�����C��ʮ��  D��92�X�XWU-`
Ca+&jdD�7 bc�� A�I(-W�PϪz����Q/M  O��9c��\���+��?DO`���m7?��|fC$DA3Ad`k6��k�u������g?{��7o߾�ݤ��5D¾Z��2�KwR��t����3S��$��Y��"BLUU��Z��u=���)|�[_;ܟj�~��_n6��)%�z��l6�����fE	��"�w{����ll�G�<��� ���Y����!J�s��fB�����"���b$&��g:$���l!�sĚ!�*$2�\��@� �fl�#�m_v�D=Ue��H�R�S����Q-����rY6mn[�C�)v]�^5��B`�b%֕�F��A1��X�ÒW'���߹������������|���0`ŷ	dD�]��U��dQ�Q
��Q/7#a�[�m�z ^v��s�8��?�����q�?�+	�p���t�hTCCR��Ѵ�̉c�I�̹��L�|eD�N�H���f�IUm�M��o~��ݻ9��w�� 3�9�-n�#c����N �3�{���R�������9�UU�u%�`"'�"�����7?<<:��o>����}����!�{Q�b�5QD'+�q��d�me@$d�D�Us+.M�J�M��>503�}�^��hgN/��)JA��@ܡ�s�́Q`N1��6"��������B  ̄�H	@�Q�ܩJιi��zy��V�ܶ�?t)�SQ35ʄȉ��
X0 @S'�&��r�&��ܙJ�����ƛ��}���w�����0;Ó��LDT�D�/�w/�׻�+�jZ�$S�!g��%S�])(�ۗ�<�p ��nŘ�+
�B�j�ꚮY�M6x�������h�r�z��<��&�U�Q}���@	���M�D�o��Ư?�xZM�����?���?���ON9�yO�m�!��"� ��bEs���# D2���������@�R�<�͙q�^YO��ټ~ｷ������~K�J)�2� ��"����J3�7�1�ù��Y�/� ���ٓ�O�����i�>��P�0�юw/�u]�=��=h菍�L�����Y��Ù���̬���ED��5m׶��rq�hs��\;gy�mWr)E�L�S{��7�5�l!L��R 8=Y��&�MT�Ӽ��~���ܾ��Slt{^
�)�r=��X�H�"][r�QȘ�a����B����ٽ=�b�`O�w/���6���[�*�xG��!t����#KU-R@KTuVKo��/�:�d��M�Ԋ�Z D0CD�)u!U�S�	w].���0:�Q�s�T0<��*ۅ�c�n�#���ÃG�_㵦������_�EUU��z�!b��:�J��w\ �����,Ǐ��8:<��) @J	1sH�L��@(����iJU�Ã�TU���J)�r���7�@�9`�f�� �iP�4�! @D{��!*E�h"$b����C�1���� Du�G��c��EH$56���Sb���9A �Y%, ��@H�]����"9k)����ٔ��\�M�^.K�9QN&Ӻ�a�n�mW�(X�u��ZHXD�����n۶HY.����ݽ{�����\
2|���ݲ�"�!z���FQ�]WJbtuo �aqy��=�Qu53_�W�z��_��86���j�%7m!r0��_zφO�D�BBJB�C�hI�u�v�Ev�F��&��Iy|��d����{���2"���819n�ưrX>��3D����*�=�KJ��ed
 �t-��f�IJi:�����_&U��~����O1"V�H�+�C�/���f$hM�=�w:��1b�Id$$aaU(����5#���h.b(E�,!���� $�FfЋ8"���e��*N,�s�dD$0��3����1"�!��4(��^�k�"JLd��(��L�D4�E�b�*��r�Y4&2�K0"���t���f)�P����w;��&&K���9}|��ރ�re��$�j���XOBө��Yo�jٵ]]Mg�����(�;��Z�p�M�.V���<���������]7�͇U��	yJ��V�!:vY 0���M���ڶ��.Mj(��,��	c4����1��8N��]晥��ο���WA���nw�y����~^���m�Ww���I��; �3����v?�"�i�%���K�TQ� -�)��b������ ޫF�I��Ǌ�*��m�b��[�M�Dqvv}NGZL�z���{0ۣ�-e��-�	�����.��L<��C�RĠb
1l�hH}{�!`$ �6?~�-����N���(DFc`3˹�	a����\J�e���E2t �E���8�z���p���PS�3!��`U3Q�"�1����P�#�{�GZԝg q7�Q��Ոa�;�����L��"���� �!u�Z�1&���sE�^^@� �
Xrn���tq�ӻ�?�۬7����@��Y�W������B�n۶^.O����k뜩b���
�	��9�6���t6=99�'�ȭ���� G5Br�]#4Sb"�R,����"���n�и�T����w�Wve;��5T3��9s�h^ASb
@ �K�%W&�����hL`fDh)�%��j�VK�U�]k]� ����f͒�y�/�YUg�� y犔D����$��8c#�Wͼ�$^�璢���b���V�������YY���zp�`��:U�������Wm�-j91n�P�  2DTt�N��!򽃋����R/6��॓���BY��(>�L.��?Ӭ0���V8˳�d@����Ͽ�����^������aZ鈅u� �@�������c-b%�` ��lfDL!��C�WBbf�u)� Gj$FBs�͍�Q�y`?��s�6��`�YG�Ɔ���#�Q�o�7�ų?)gS�Y<	�*
h����(�"�������f�� ���U� �,�=4��)u��� dӮ�V������^����u�7o�8Y@Ķ]�|�f�=���f1[�ճf�????�2٦nȀ�Ѐ0 ��)VM�@5�-?|pr�@M��������]�}�eb`&���̠
��b D*}0MX^�Y��0|�a _�I�N�v�i���y���n{�4r�L�3��hf(Τ��_�Ϩ(�kDLS�Y;��:k� #V��fyU�ڪ*�`���;�Ww��d�
?�a�H
���]7��d�?��??>>������k�56���T�����gT0V����u|vJDȑBL�Z��")g	�U`&��D��xUN۶U՜sl�d���m�Q�����SS���EU�<�j�.���Ww�&
�?)��E,4�M�1K���%�L�D��B�Bn.b�i�I�,���H�����KF�M���������������4�;�1�����vE
d��y�qĊ�G{�y�\�'M34F�`Eb�-#h`"B�LD�����?��~�z/��c��v�OT# 1K� 3w0"b"�?s8Ͻ���xQ�'����!��M<ӌЈ��z\'�)R�c*�*��b��dMY6�$z�m�zYG��vx�7#*�������n�ｽ��g��E �=U��e��kFL�"v]�wx���O?����e�$�z�H���4H"1�u���_W˖�Kby>��u .N����
M���Jbɖ$���yN�R���\��H�BYK$� UE�$gD��ը��~����R4��f�!��O��e�@���!%�/A�J,��@b�����E@�B����
!��h�	��"�R`�I�� ��@T�vݭ�)�U۞������v� ]Q��� ���}�S?3LYgM�Uu]�f^�����<Kπ}�'䣣#3��K�!`���U н����P������O��m���([z� L����8<E��(9�VK35�1TK����/��p���s�-���n�}_	�x��7�?^�h�P���b�S0ݘo��h�e��X|K�g�L?!D��x#I�@Ir1���cU5u�)K��� nC�zå�~�.��"o��x񉌁�U�y��f�vZ�0��ǂ�Yۮ  ��ӏ�~��g���w��j1yA�HFlvQ�S�,�����,�XΪ���`��Y��[�2���"��}��R���Ch�Ro�(�r^�蓽�T���D�#� ���]u���i(�*$D�"9%4� ��IV�,�D2"t]�jp�L��9F2��B���G�MP�XS��>w}����m�>99Y-W}J�B  &��D"#22�,�O�s���+�d>?y�@	��RUs�>Fbi�m+�����5���f��b ��<P�p`D�ү��q3GL�ټ�kP���>�t�{����Dt\"юj�y�p� Oa��%)2��XkU��QUA���N8�@�I�����%*�T�W���nz+��1[D�q�=\ą�޹e��:=/Q%郅e��O��=�����*VU��#Ī���BRJ]OI������"�\��-H������b��@Qѐ�!�����*�:����p�٘+>��zoA`4����nʇN�M��_��3���n���,,R���bJ%�dfl��QUT��#H��GD
���dpNsBA/�GSD�A�FԲ	������~�����m[I��<�X3S3�$)Q�Y�$c�R��k�vU��V�f"���r�! �����_�^�ڍ�%w��D�m������o("V�\|A    IDAT""���{'9"�|oC̤��X���J����n���S�75�\���v�_{���ۖM��K"  !2#��Y3��/��	�Xf�B���h�����:�N��;��<r7�#�s�P���P}7p��Ƶ�����+w�n�3�����9�������?z���G'/��fB�,N4Y��j��JUNOOONN���񓇏VU`Ī
9�*
aڤ�D=6؂��m�` ͙}l��]�L�ѳDd��{E���D�1��w��66x.%2U!bSK)#�d `!  FRՔ3�}��r� ��PDE�	 �h��
K��S��~�\���-��W�
L�@�r֔Ӫ]�)�P��
�!EH��e�XU��R�E�*j}�� �Y�U�u�Y�1�w�/��Y��"bBu5;�)k��[�s\�~:�z/<���d�1!B�{Q�*V!�8V!֡����@�ȁň9h�!V��:�b+���P����+XQ�Q�|ɴmj���}d��P����4`jL#��XYD/؝VJ�6KS&��0#t��#��5&�4�����O?~�������F J ����G����@C�8BBrD
�V�j��g����7M?~8���y]�1ֈ�`�z�焄����W@B�ͶW���[�)dcQ@�����q�qQb"g\G&���%D���[�?"�Ձ��L  ������QMU���P�rSDLDs��r �Y���Ȭ*J��@��1�� (��+tN�뺜E�$����v�\23��~1)	@�u]��1��!2�z)��
�k�z1C��% ��O��h�b��<��ԯ1�Ex�b��h���2�� �p��5Ƭ��{&��#���ǉ��j ����j�f�İ.۩#�/yv��Z�f|����6�� ��()?�������S�a�u�7�����x�.D�.؎�ǃ�X���w��xd>�z=�=C�#�&��0L�>��%n;�3T��䜅����UU U��
1ĺ
!�X�IB�M0FA-  db�!��沏��b�yoC��
󐝷�d�t7�Ǔ�����\*Pa&����u�������7�|��gϾ�ny~�ØH��-�"^��Ŋc  (����u����>p��s�k"����딒���6)���c�L񲊋�! ��O�%c�5�0������HUg�y�!g� h����� ��(aTcs."*�XG� ���}��HU�	�dkC^�|vIY���]h0��v�fQQ��7� �jWO�>�*^.O9X
��b�9��������v�&˧�eS��3�pr|�<�=D"Y��˓*�>�;���ltٱ8;;�������X˫*1���D�?��`��7k��d(9?�� 9�2��?�C�cU�� !1#�2�1#DYc��r'9p�c�.^cC���E9��_U/�ζ~^����rD@$bR5_�i��\`��d|;��)�GG!�Ǐ��˿�KͲn�v�FDf&&��ÏAΝ���U@D�H]4�LL
c�Ay�*��V�!�) ���!2���j�2��.33#;}�5C�����Jޗ}���j�.��e�4@U���E�+ga��E$�*U�l$gz7T�,�H�53ED5Q5UD�!�u�4���Ӯ]��f625���X���������l��U�*~��ɷϟ}���3Q]����+�l�ϛjA!	"9�����Z���<pd�BdY�yᮥ#S�û�{>pp���%���+(�8l��)�Wy>.��A#�Ѿ�1���r�7����a�V1<�,Qu�:�E��c��cd88`3�a�h�x�1�Eb��!H�e8����q�iQ��|�
�Y>n���*�m��Z�q�fΉ�X�x��ɓ'D�y�R1�e���+�9��O��R 5N� ����u��5Mq蘕���?��.���b p-�6����h�	�*2���9gU�`�pq)���2�֗FDQ�"<���uNDD��ݛ$2T3���+33#Qu�^PC5�c�4���U��:&vb#R0��헿���GO�ֳ�K=�r�����������w�>�9������/f��ɓ� �f�}�Uۥ��qU�g�l;\�g��.�83�>�8H�j�����j+����~���{�X(J\�.� ��C��D!ƪ"��<������"0 zA #d%φqL�c��3�Z� s
��
ݺ!x� MT�м����ü>�C��m򕄛�p��-[t+�B~K�,���[N1��0U��٧�;'g�RzDs�$_\Zr#P��4�����
!@@�Y��,�����k ���B� 8R�nZ0���"8d��@$j""Fb&Br�%v�
��a3��cs�]�K�8���df��,�=8K��+6���D� h��I�n]���h��s� �)*�f�DP�3�\"􄈳�l>�}���ϟ???; !Գ:�����]J_�����_���z��������������f �f�j�x�w���'k�����_>��u��	��ހ"'4��G^�+lS]��Ŵ�$t�+"������9��2p! 	N#�ۯ�]o+?+u��k����M�z��xG۝o�k���.{����--�ń� ���S�g�����_(���� |�Հ��
'�#U`����Y��ԛ�|m���̽Cf*8����z�����I���x�4~p�[)b&�9�ȄSw����	��v� �t�<��Jʓs5E�a7�t��O��ܿ����b�f�&�0�i ��B�0�ٳ�c��i��(9�	s�������;�����ˎ�@�!�S�f>C�����j�YD䊀�Ki��p>[d�����?�_/��z1�7��������Y+3[�{��p����'�~�g�l�����:1P$���х��� P2�C<)�@
D�L�j`��3��۽m[��(�y�L�v�T�@��~�������d�&�U��pr]'�K3�������/����]�Dd�h���zօWvH�JϽ�1g4�,���{GGG'''u]�/���8(/O%��ݥ��d bd�GHdٕhN bS�&�|�<=##M��L��H @L1��x(���_�w��.tm����~� @C������"��@ݎD�� �B&N�!H�(���,��ϑ���q�LБ�&�#7Mu���f	��}�,�c�C�!>~�2-���ӓu������Ⴧ����9i���G�j�)�o_~�ٟ�o?�������b�zp�&��V��wᵧ�Ю�w�����H&@%&���O��}�� 3Sp�Ɲ�p7l�}+�#����<x ���.�ٕN>�]�+V~@o�_�`���2�A��ˮ�Ƽ�����B�9(��1 :��rZA��4f�H
T
=�i X�ԋCĆ`�-m��6�rp'�1 ҡ���tNe@�4/���E�5�&`�e�$�4&�X�Fp���HCZ6+�RZ�:�5��v3�.�]�	 8��L�C��8aop�:�|��q�W �����PIjT$�r΂,�D��g6c���1t	BD��C3Q3�@��-����~��������b��e��HU��>�l?VM����ɓ'O�'��'�>z�f�٬�?x�:����cۥ�>/��i6��Z��-���{�}n"}Ί�jW�)�A�Tw(Z��t�vo?%@����LMr��%�V��$$Q͠�W�B�jD���8/�z]:9X�!3�$�� �3�T�T�]°>��:k�@hb.it㳊��-�pד�{ԑC���ks��V'儈!D� ��z����������C���ʳ}"D�%�_7�$�Ը VH�D
�Ҏr��24G��P]ic܎�Q�9�D�*�@�̆��!�K�f�Z^{� �TQ^D���"�9�uM�%����U�HMT�f'�󸮚�YPU�,�H�f�L
R,R�%*FV5���%�����'O�vծ׫���k�����'��#����b���g�H)�����?�����_��o��@�΅Oz�;kͬC �f�M[A�M��E��O�dk�lf�J�6�h?b	����gMӮ�>v���  �m�긊�D���P��m��O)n�6�.~��D9�!�4%L__���p+u�����a�,�6����6铫�7h����:l�ܠoŜh��t���Y��Z�U�%Lr��/kz��H�P|�ݘZ�4��3��MІ�*S���z�^�DA�1�L��	�!���29����mh</�@Ԍ	��� ��er��kD�umf������ӏ?��?�h� ���}��I)B�8��X�l\�A$f-�LLP�a��`��� a|AY��c#ا�����x+���aw8�#c��|�)�̶�KW�6�U�C�����,6�3�W�X�j1����w�_<8�?:l�UUUO�<Q��>���������*�$5U �`e�蝷��+`���8��nn1uhu��U��e:�wK�j�G˽�����!R����U���,2������6	�;�fHH��%���#pT�s\��k6%DO,B���6 ��$%EٜK���\m�S�( �fk��MU�m�YV���lI���ggg�HL�&��M�B������o}g��nwp
�K�1���D�ǯ6Q�R�XUc�_)�4�������9���N T�6E������!f�`&��A�(��d�R3.Qh_+���	2!򘊊�`@Ff�bh�٣���������O?�������}0*���,�d܍�!�#�����4IL �p�w UUњE5�= �"P`"�ƕr*�ya����y�zooQ���r�W�Y���]��+�'��b��S����ʉ�׈��u]�"��o�9�		h��7�0K)Iʒ3A�����8A��2�(�^��Y���ȁ�]z�n�����j%���@4"ƪ��J$��Ƣj�O=�c�!%7�U�����OSe+]x���'��'/��Sut��D}3������s
b���DʠJ����M���?]gf2C�9uw.s� "���[�����HO�cDTD� �YU%T 5peך�"�m��e�T��g�����+Է�IV�f��0��{iw���g��뺪"�$�
��M�����~2��Ƭ��i��뚦��"� �U��)� ,L�d(�N jf�����9 3 ��]��	:�b��,:"d /u��E�}���|=+9 �^M��͚I`5�X�|1�C���hAaݎ�q�)
`
2 #05[�P��!ٝ�������ʺ�$�V�,�%*06l�Q{:��+�>��OD�R�xZ�����k�HaoDdD�0QtVH)�X�����3? �����"E5��SNbj��(`0�Ȅ�}�n��loQ���~��]��ú�Yi��0V͋�?4�œ����HBQQE��Ӈ�
�{�$^e%�*��v�YV˥�Qz*>@7> ?F����vv��t��tȷl���'�7`�'�ӷ7uo��\�Y-��Rʒ	�Yŝ0Qu����������GQ�4����<�n�D��yɴh�4� S/{��eޞ���.]��ڶe�����P�1��]KD���m���5�lgƌ���\���g����YP����9�w�)ݿ$ �R��Y�Yo����F��͛�������)mP�JLf�%���}�u]��b"���t�E)�ۦ`�R�>���a�Q�-�Jq��a||� E/^%
h��}�.cQ�Ā��6KVM�SNSϒ6p?�
�ro��s�  ���. ��S��22�Y�a1SC���
!�� ��縈ȅ*��#�T�-��K ���J��ŉ����f�����A�[l����C�^��T�ٺ�1��� �
3�q�%$ %b$#ՒD4��[NY �9]2u�/���<,������l�m�0��JNWG"��t�XL2����9���E�FT��W1�������H� 

����,mۦ�ʎt%�kv�)B�2��0a�{�����;<h�����lq�>���޷d�K;/nbމ��� ��g3���b1/X\�s��qo;��79�������|��3؍�\�t���E��EJ)眳��S�I%�H.JC���:'S �Teb� �ȁ��lW��`��/�6�w1�ᙙfɮ*�/Һ���Ǆ�j6�ؾ�c����zV�G�|e��9;;":��s��d_X�E������JV��/ˇj��*>����]����,9K����1 G���TUE�j�SJ}Nb������(|�ٟc
�i��z�7�c��]�V����Qq잓�����������3���G:Խ�{ϟ�jJID�R�Ǫ2��sV��6[���,D `@��i��ȋ��Ҁ����Uy��������L�cu�0:uP���ZЃҲ_�9]�ȓ S�!�to���4��������˓��M��k���^��8��:�eD0���%�P�3�djfdf8�v`\��7))���U����	ωa���+�yns����Χrw1E�y��
 �]٤�t|�z�E$	 B�@�@�����)�`�J��&�@���_/�}�fO� ! ��4��� ,�Bi�|�d xt�@RH1��l?+ ����S�q��u/'�����4]�-����=����C����?�  0��m�o�J�Uu+��{�#G�������)��ݚ]a%o͓��ɵx�1N8�f��8�&TW��
��lz�8zl+��!��fZa$�p��k�l�4ݦ�i�v��ٵ��M� ���B���|���}�.gr�q;�6s�g	CP
2��p �t��N@�FL�۷�h2=l�ps��s�����H� Q��5ggg}�&��Eޣ*~ v9�W6L!D׍23"��"b׬�~�ԖL�>2�=A�e���h��%�.�\N��L.'�u��{r�}N)��r���O�K�`̭����/u$I������"������Q�-�K��P��.��0��R�c�UUԜ�뺮�:�0�Ϛ�	!�(ͽ�۽@0S�4�?]�3��۽(���z�DQ���(01�.�<"z���F��4:���
ܒ��v�&*��:Ɛs�"����/��hdo���n."13h����Q�
��<�heoE�4��� ���tu�r&�	R�Ȉm
B��(�@UED�9���*���z����:ԉ�7��Nc�$�4$"�J�@�^�e�� ������u�nEĉu���djD�FՎɅk3B�hK�֫�?z���5 ��'�|�ͷ�fj8�Bx.�%�>�dY��V-��Vڮ]�n��n�~T?�D�G"��d�ι����_|���'���2,�<�  )�lD��s�
/͘N��\�F�V��d;�17\VޓojJ�<�� @���KЋݛ��]ɢ�	��m67#�ȵ�w~���9�L
ڔ ")�|xE������y���Ь��h����B$Ue������
 ��[��}߻쥗�dˈ�)%���6�݌�ju)T��M3oW���K2���O֒���~�ǯqD��V��9�x�)��d�C��&V�X]�M��uͦ��o<�������F� |@d0g�2��`��(ZpVXP���RHP��M���=�(��A�2w  �Id��.�>���JBQr.	!۱d{�M��],���"�!3ͩ���� ���۪
0	��W3�-p�N��s�X*qSƣX�1��"�7���h����B殪8ȣ/�w�
�륪��ﮪ*���t,�Q
QMy({s��@��ِ4�" �7iY���Ts΁�[��պ���}N��\v�0� �P�4�H���9U��&\������/�<�OV+r���S��D����J����V����� Dfb��W��a#����.�&)�{�Ҏ���_>��N�\�S�ަm��]�3w䮮��U��|g�����P���ʵ��(�vYڵ�!��	<�o/:��鄉u�*    IDAT�c�s۲�~ c����	AS�-oX�F��?�}ռޕ|�O]1Dʦ��HH&}����v����}+��J�p��'݇�'�m`Q��`C`"b�4�
�XUi�̦�\D���?�<CC�PL�̲H	�I��ˣ�]׭Vm�2 ��ԃ7S�檊���kb8�z6����# ��n�^�}>}�}�u/OΘ��7�M�Z���լiھC��{6�B��1 ��/O�Mӯ��k��}N}ߧ��^���탴�ܖ���!���áO/�7A�Q ��(E��S��N��@Pv,�����#��!�7n�@�Nn�_3B�G��l����W1D7Dwo��Bc��R Ԕ�ԝ"S��]w�c�}�c�J�E�����L���L1F�D:�3���u�a>��Y���(��ñј�ydc7��;�fa"� �P��c�I,��� ��@�$w��T�1F5UMj�I�;=;;k�����)�Y���};[,��?yx�\��m���J��5�2^���e��QzQ]���|>_�(��b1_,�ЭW��#0�;tK��w����Oѳ�U�n�-���uǣ_o�cF�� �����k��L� 	M-�*b�]j:ҿ�����F4��s��A�Ʌ��Y|�w�6��/�n���	@�w�ݛ����Öi�`��9g389Y>}x�&��ׯm�;��9���{co#4e�0�:&1!R����qP����"¡L9�b'"0U�	 ���06����mU�LT����>1	Q0��mS�M�0"V�:�ۗ>��$)�����]-W����/�l�`A ���/~h��Һ�R�	��[�q�e#�>� ���GIA$�}Ny�^KVw]���+a9}�>L������b�#�0PcӨ��f��%TM �&ɬ2�B]��y�WhB4BKV� ;I,2!���(z�ƈ�-� ��d ��DM�q�Fy�>�����c���ٍ��!������f"J TEf�×�3�aAD���9�������L�u00-�,!�t9[��N۹�43 F`��8	�8�G�x�����E��зr��K��!F&B�02��Pe6s�'FR3�Y�̙̈́�H�d�^�)�hd��Nx�$BDY�9#F�"f�`�^� �)�勓�o_�b�����I�N���?uI�/����Ջ�/}��y��$,J,
�`�@�q�7�e����[�r�m�C�0@�<�B�����  'A��@�)��)�s׌�����d�^Ͷ�,��ǲ����7���ͻ�נ��^�z;�����F����:ׂ���j���;�_�TZ9�M]\
���gw�&w|
Oّf��Zn��!4�\7�vf�w8��u�wETTeʙnV>�I�-�saH�!����,�q>k8E�) �t��f��[=��oe����ytooNto�'(KN?n��~��u}+���ٻH8�H`�j��f&�9�c�8��MUE��q��=.��C�4}߻����S��Ɯ��@4hP% ����@TQ�c!R(DB!��n����8�ju�jOW���l}��l^7��fO�|֭�O�W�9�������!0�~����o�ʈ݄�?! @`!���Ӥ9���c B"�o���ћT�hz����ڐ�$Ñl@Pq�����9K����Ǫg2B&f"��B 
D�H\��WrB$ ӝ��7�ћ$���� �*
c$�ܧ�������.�n�e&���nV0�� ��
�y+����	 �:�s�f�*���;�9SWr���s\&�����Pɪ*d�=~��ZJ��1l@C[+��+�Y�$�����Ȑ1'9>>]�ק'竮U��bq~�ڛ/4gj8�u�V]W��������9�\��O�<}��4��z��V�;?����^�m�~�lg1�"� �����$�������z��k\���j�Z�Ar����Gl���K��ԏ���^f8w�׹ר��ޱ����G�=6���=̨���i�.�t2˹���Q�
�яw�+����څ�`�~m�RK���| ���4i&F�=��T��_~C�:��:��{h"�;3�o�l>�ID��#
���(��;\R$D-4 �"�I�  ƨ��࢘a�Gb@$��c��[,�����:�9p� �����Y�Z�xq��>%��~y~��gd�`�9:��O�Wp�^����������|��>�������(G�IQve�� ~�.��@H�D:`�  ��Ń���,q������Q�]�����NɆ ��O���瘃W.�	��8�c /!Gҫ�L�oT��®8��!e�D8j-a	�ʰ0��@�?Ӏ��vd'Z��(��EyF~�����K��Գ� _�����Gp`M��C)�ԓ�,)�U}�߬�h����L4RQ8��tں�R�����#9�Ր�	Q�L�*	T��:����Y�f.G�D�L&)C��˒ �H��3,�^
"�MU�#WUEYS�������������e�M�Y�P��G����>���Y$���ǟ>x<[��<��/�O=��_�����s5 (�,`�H�����ٷ�0U���#�!k"�.��9�����s}>��w�w�k|S����5��˽q��I٭H���ސǵM��������siB�Z�͓Õ޾���}^|˳ܠ
	I��8���I�+/ QC`�I<���)x� ^U���;�a��V���lTISs����{V�3�%����7G�^u�<)h~���ʺ��lDg(�Lь9��T����|<��*Y�� ��"�<��T%g���WXE�����ߪ�B�,��g��b_�X����������'M�,�����z��~�O>��
Ė�^�D����˓*6?}z��'�уx�߱�I9�����n����8@5g;>9^.۶]w�|vv�\���+���z���ޣ,d"��b����I���L�=�G��d-le��c24��9��,��������fV���J�/��&O;��JO�DM�*V.VML�S�������#䀔R
N�Z:�����Ά���/�J�US����{�܃]]����i��TU2�Y�u\,�w��[���1/��[�5��g\
l<�H� ���#B�b��?��IO�<y:��GG��g��կ����`������+�j��/���ng=�O��e�y���g���x�G�)�wNH�)����DR�if1���b��[�-fH�g'柳��!�{�w�m�2��}v��YNg����mN�@Xpa­bB2�q*���N8b���C����%;�����D��B+R�������P�]�D�����K������?�@��b~ff��w������qbf*�L�8`_���@����4ĳ�Px`? B5U
�3QJi�^�P1�yo�����O�Ϟ=���ਉ��l�jۯ��R�~��/�PCI�͢�{� �����'�b~p���ǟ�|����Љ��Hﾎm��Ӻ�ӳS���Bߧ�SN���}�vC���]l����RE�̵� P��АAi�� �o��36�̣Xj&`���`�l�uU(ŕ( E���F.���-�f�����E��R��*	����f�
P��f&����H��/O�c�g�t �ӝ㆔`��m�tq0ϠIXEPC d�&6����7�cS՚S��h/]_�Ӊ��� �B�(��� �j��.�輼��W��jH8��:ӄ��SN�`����o("��aD %Bլ�Y�Q��	�jD/,á��Fߤ�b��LU-�*� �����dCR $����%b(�(Z Dd��>����u�&yQW!��Z�����/�=z�X읯���������^?��_�]:=`�f B����q=�46�g+_��Z2���n�]�E2/�U5$#C"4�{�r�8���f&bfB1ؠ~�e�FhF�O�x���6��o��4�q%�øE��si̿��e�M$,
�儃���\�Pt{lz���G��;�D���o_M?!�Q֐��ꆪ�2�\��K��݂;��0��.݌��QW}϶���m% �ŀ��8BjZ�U�1*j�[[𫚅�������T�g�)������zd�.^�,A�1�\�ڡMT ���!t]Wd7(4�,�V��/��o��MR��gsD��|S��:�c@;]�/�o�D�`*�8n����e˺�XU�X��s���E�6ɠ;�XTR����Ɏ9�@�G��N��f�"����^UUU�̚ �-�9N26G�i t�-�zz�2�t��
Ro,�1�wP̛�̼��T ػ��l�0�r�[6M���WU/���٬i�"�~�^{o���(�w�C3��v��,DT߆3��F`� �H��B���A�r4�J��0	�8����P`�D�)�IkfD����ȃ��#���M�����N��i۸��R�)���P	�ǹ�r�n:q5��>[��g���˳�/���/�:�a�,HٝzSK���!Y&�X�|ǝ��k��(.��{k� 6t;��)g�Nq�3 C�]DԔ�T��"�}�R
 -gAD�����M��|o��!��(c�I ��W�,KB��̫U��%���P���Ï�2aU��r�9�Y�(��؝'4p���
�?����j�\.��U�e�\-���j	]���wo�m�O4y9΍�1H Fu�+���Q5%B3����]��#N�]s�������x_��f�n{ ��Bl������~�=Z
�������T5"�h63�W�%����D(��{g��+IN����o5�L��9����������9�B05%ED���9���Q� Y2"�s28;;_�ڪ�hX���V�;U$��_�x4��{d&l��*��9QCY#3  d�����!��|8�� �ru*������r����ͬn����^��f�*uc)^izWF�%���/ffVU�l6[��}��` �^e'��+�'/�=�{{K�.����pd���3�R� N���� UA�R�KO"\�G�b�Z2��]  �Q�f�xx��9�N�ih#I���Ҳ�e�I��=}�/?���gU�������_Ͼ?>==��YP]��}�"j�b^sOd6�w���C&����Q3r(�����)�m�ݦҥ�_3zƘM��F�K6�G��1 @6T���F�@��0 �l��DE�Q��X���2޾H�#D�J�*cl@$��*`u(`+�Y���� ,3���dS%PQɒW�}�4��#-M���EP����`��R�0W��Q�BK�o�#��'F�ex���t�`�T�o{�S텵s����� ���^a﫶rjh[2^ݍ���U����ۮ|}}��	�|.Ưᥣ]����P>�7�{2�����|�J9<-����㡯b��V�L���K"#���w2���h3��ZB��jfJ��=����������_��o��888ztxU������^̹������sa�s���㉝Ch\�ݓ��O��(�dh*:*Y:J�C��uY���f3]�kѬ*UU1�r;��TH��RN
c`���E*��GfQ1!��&�j" ��Ez5��ֲ�B�X�*u9�0c4$\����}q��; �=>߽]�uu~~޶�z�^���[����!�{��5�����۶w��%VK����o�6�D �C`"D��7Q�n�F�9dB3PB!j�j��g�M�,��;��ܛ����� ��(�"5�Ȥ$+$�2��/�P�_�?9����1�#&<�h��MI����H��8�HjH� 	� ����Zޒ�=��ù�/k���Dt^������{�9�w~?����Eb`N�I����S��]��gJ�H��Ă{i(2BVH@��Չ�K���	 �_���/�o��7��i4Uղm�W������:��6�Ԉ
�"�4 ���|��sⶏ�W;P�Np[s0���Y�4D4꒓'�{����]�ґ��ȝd�" ���$D"f� �AQ����!r,ԨN�Hb �*]�;���@	 �F#Eh5�" Њ��O�8.����e��i4�D��` IZ�T�Ҷ���77��u@��b^�Qe�eL��*�D���'SbG��;�\��y���� ��X[�eQeY��l��,���\gy��Y���k���� ���3񞾭��{4vvf|��:���67�i�v���C��A�ԺL��ns6�
���9	�e����ky��AC6��OE'��M�w�F�ǂ{^�[&]��)�P�5"�SR Hm�����W��W���o\���=�%u]-��L�ɨ�L15
�.�����=�\�Hw"�)+�
:m����h�- ����`�z���m[3�P1Ʀi�6g�S����e�hͬiaJ�L��e@]�*FĆ��D��0���M���#��M�M-
k-�
tBb͜ˢ��$6��pUG�z���#$ځ�Lmwww�\.�����r���U]ל3�C²�8��P�O��7mC��S(�;n���,�;�!�"�)[ �`v���@s4F�h��t�H? i�Y�젤"�}CC����Oݹ��h�`����v@�j���W�H��3��i�^�&��Ct���L��mc�Ϸ����O>�D��'����1峛[׷��҅�m�ڻ��ȅMY-�TET 3��,H7a����pǱ*�*Pv�� �2]�!(�����Q�\C�;�#Ď����[#��P��������8Ϛ�QBC2�d`�Y�e��mG�df��	�:ɔ�ZѤ��h;�S�����5�1 �p�5 0h �! @-�L�ь� L�b���i���Um{�j`1R][�^��4
�,���󢩘I�/Y!<�|dQ���G�f�z����Gw���RW�H>3���]
�e L$�D�������d���֣�g�_��>j�r%8��yt~��,ooF�u�`�}\�ğX��Z�J�<J4=�s��夽��?�w�>e�w ��u���o��C����p�~nO�F{�n�c},4;Iղ?u�̻���m�`����)mPv�3�	.&�J�x��e�߼�eY����Mۜ={Uo����?�������җ�<_����E
%�5u�Z.���W_o�H2�
ʁs���j�5�͊@����ֻ��*�cv�P�pԣ�� ׺T3��# � j���^��]UU��!�J�ԤB��XD���u߽�'�ǆ������REQ�F�8%QU@P3��%�e�!PR���y"�mQ!�#�rz�rq挎�@#� ��a�a���aX�	�'ہg��W��jeYnllTgSJ6�us4�eId�������ک��Yp����T�P�CZ9dϒ����r$��2��DDdt�; �o��^}&���<2��(��~�V�uE��A�t�׻�U�4cl�6ư��'Ĳ�[_�̟�ŭ���r����q\���kWo�^�߹U���"0Pkr,�p,���@��GN�������"� j7�:	���ڭ�JX]��� ��5L��g�ݒ��Y@ =��)BGz'=-�A,"2'��m��;����]���Ic�w���������t@�Կ�$�9*X!��|�"�)*������i(<���f3f�1�6.<69w��pm禊�#��
������l��q������|^UU۶"�i��bnղ��Dd�!;im~�[�{ҹ���O�zl��<���!���K�����������F�WT�ݨ��;�-�&jk����#~�� p��z.���p.�_�"���r��s�ίV���mP;��w�����ٟ���K�߹����@0��]��B��c��x};s=>��G��i� H\�j��m�344aC3AD��'�橗�*f�R&/42UI�1h�&&�jUU��r SSM�%� 2P�<Q��+1;�U=�������+i\�3���"i@F$F��#fC�kvY    IDATSU�ml�"D
#EQ�m����ř��T��/7�2/Z-��(��lc6����F�&��/<Y�vj���>%0����D�d��+�����!��5��H�6=�! �e�i�&f� E��	��IϹ���C�>5�C�N���=��#�a.���)�?O4f�1޸q��ǟ����'^~��QQ"I�D �BJuU/�R�)r4C@Tg�7p\"Z0��:�" !�9���e��TF5P$s%S��= v�n&��P�Q�EPw@Ռ�HE3�	��� &5��U��ВC2CUi��'Y��Z��o��.
�6R�1@+	�8��TR�up����P��Uuy&  dbB�"1a�P8 1Ǣ((����j�zg�\.&�MD&������Q���y){�N���Z{���~�A�1�c��qFǆñ%F��h���Psy���Va�����֟'=�w����Q�_�JKz.��N,��z��
ѱ�k���Ogf����f�*O���zѢj�,u����Z�z�׿eY�����nnn�9s����/YUb�VU%����jU��V�D�����̲����KϛD�HaȦm�K�@��4dl�g��={9��T��HL�$��Wfk[Pae��bD�4mJ���2D&�m��u�3\4E͒���#����X (�X���g���9y�KH �����"p9�P�r�О�\#
���U�� �d걙�-�� fؽ8 {{{��|�L�ż��m۶m�w��ȩ��]Y8�;�k�L�	��$x��q�Z�)��"FbW�\��=��vTeֹ�ob��OC]Y١�_X��O2�,�x��٫W���_��jU?��ͪ��۫�VR��r�mRM ʈ�FVEΔ�!���:b	���+�Ҡ��1�UPP��E(�v\h������������́쩻5�ث)ؑ>����!�
�mBPUK�]XU�UUD+�2ˤ�ˋ��D�'��i `:�p�m�Dz�|]�`��f֪qYFBUd*�Gc(&�X�(��2s��|�4mQ�cӶY��A�'�����������d:�����j<�����x"��j1��}��=��]���8&����,{;�J:.�͝�����]5�[	�9�j���to�XG��yo"��!��2_y�+����/���D̬�UUi��ZHR.c�'���w.n���u+���e�;�����)&��N\���Q�(���fx��4M��*M�h�B,�"�M]�"�$�baf^���	̰m�6M#)E�"0����� ж	�U�90�j�p�S�dE+�E,&V������r�� �H��ͪZ��q|�bԩRK��,��$�岮��jYU��yj��~�0<?0��@�!"��D6� �w�?w;�+�ݝDD4��g�S�ueڴΨ1��%5쓔C35 �^��)�� ��JW�"�pֆCҍ�՜�D0ǳ�;XtI�n�;���0��)���l<A�ׯ��onN7w���z��+o\!" mS"�Z�##1��3��":I����E����7K @1 ��r`�T�C��y�Y"��Z��QA0BHH�����H�Nt'D@"]0���!cN���9�#�&Scd�``F�����I*	�UUU�F#Y�$�Yj��&ph���� �����)2E1b
~�f��Đ�΃��C�R���k��901E�
�PAaCY�#
�F�8s1�PV���3���'`Q&�Ηǯ����;��n_�u,e�'&�K}�V�#@ ��3QF�S' #P3���>��W7�V�k|������N�������{؇��3ί(����ɿ��L�n�q47�f������[2V|l�g�����Nv�����s�S.�}�Y/������'ݩ�.�u��gu���|�5Y��ݠ�N�,=�nkv;i��Iά餻���tw�^� h#����;����cv���/=z}��җ�D�{��3���S���c�^(���v/��v�XT� d�H>:z�#�u��Ӭ6B,��$e!D��%�n�i�n���E(�8  ����Y�00�b1����X�
�Î�1��t�<�4�(���b`�XR(��_��L�������y�U˲ ��iD����[�L'�����V�zc�������Qܺq��n���.�|'S�{-�8��k���ǝ��5"�W���ډi?0����q�Y�)�Yj��� $����$��}xh�_��.E$��<ZG��p��m�iڍ��3g����\�ru<=����_Q�!2�S8�xX��5�r����.��C�h�7D���� ���=f�_}C��<��99ʼ��}3`����`
���-����.��Z7"*)�M[������TT�,�(R��ct�����ڊ$�!��R*$\�X�P�PrQb���2�B��? F�=4j�c�1J�K��'ɔ�G�=�ȱֿ��Ų��b�\,��b�\�t�3_�i&8�k�S{7�1��)�|��#�Ύ�L-&u/�p�t�>俠�X�������+ص#z�G��<<a�1���؏G�U��tA�#�0�f�ɟ��~�?��{�����4M3���Ewͱ�5t;��ib���v\ϲ��` �d0� �g^{P"f�(͙9M,��C`�L�S�5!bQUE@?�BJ�,�����H۶!{�IM	)�[�"u��2�ؗ�A$�h�&Ā�UC����|�@I�D8Py�9�C�h2�!"�kmBG$t�:�2�/fY��gQW��b`!p}6��ޝFv���ݼ���嵒���X�����=Y+e�.��C95��;U���+��@��Pv�C5 �һ\Q�R��(����T��9u���T�� :��~i��xN"R/DLI��H� Q@RQ��
E�f���������}�W_���~��KEY.WKD��f�����g�5( ��z��!�f��@��np7�i�)�N8 =g ��1� i�Z0$U殗��u��]��X3#����# ��)&SD@l��w��H �j�TA9r��]��%S3M�U�"����Ȓi� B��X5-Ţ$�f���$L	L- d PC�Lb�L¡E$Q�'�^� ��OYLQU�р ��@r$����j�RUMk��Yas]�G|~�+��)�������z=Tyy�v�A~�W{��M�!�]X�йL'z��_�s��1{��P�u�~���K�������'WI�2L	H `������:gI�0�I��C��2�%�G�!�� ��a<��j���������ߏ����	Q�ru�}�=�ٷ62s9bE4~'@������tp����7K"���N���e@�]�QA��L���X�@MD�N�dD2/�0ͻ�i��l�؃��NcQ!I�h�- ��m["*�	�]��90�p�1�"q ��0�����E���] ���{�z�6��9󇩙�������^.��j�\�V�f�z��{j���X ��Q�sfL����
Ō�G"pI�c��бU���9�G�L���� �,�u]<�=;��٫����1�������`zB�1����_��7���?��O�U���}p:�խ�mm������M���ݡ�	a?.t�R^��?�§9���CW�����L"��TՈй�  �lp��z � f��	�۬�	Mы��5 U54��%�`	�,2�)�IJ�HD��*���$))�� �vד���E��9��SM)�!c�?�?��� j�-bɁ��c�J�����}PD1Ur�N'���R�,����3[[[[[�����5�ڽ��胻�0A�9߮LG���b�L�#��~tPD�;}�i�p�W}���%��9�ɧ��S�j����Ӄ?�|������$sfp:���;�W��jL��!�)y>,�5ٛ�r��տ��g?�{�ϊX���돽����YS|���loo+�"�x}5>A���eI���`�p�"��c3G��+<ݧ����`�9�LW�*�̌����0EH)"X@SBTATkհ�Ѐ��C�Cdf2��AU[QǾ "K�$I�2w|��, ,Z���^�>�&ETQ���TU5"�\o���R#�R=^���	!���6L|������HJ-t3>���N2:�D(���PE  � ���C@�I�δ�@�d��T R��s	&!"{@R@��Б�fi�������*�1 "��B�(`���$=���/��J��Cl���z���lmm%�������~��o���s����t)��|9�8�7�l�a�C\�VӋ���2�c]�}�u��^^4����Tp@$� � %�ʉ �� 1x�$dZ�@J��3U�$b��P��L$1Z�fB�N�/��Q��eP�A�>Y��$�E�z��*#�eݐ�����Ɂ���
#� f�
���Z��Y�m"�������VU�10b&�ah@�6 .�ì� �*u
�YTm���4)U4 �v׃HĨj&Ā����[�Ly����e=y�<�=)"��d��F�$������'���6X;o��{f���<7�S"���u�*ɬ�x��3�R?���<�]9�y�=o��у�[��u�N䀽�>'�`i�^��w:,[?1ݕy�/�?�|�WA�H�"�][��_d1�iCd?0 ���e�9�[���f6�!� {�kݔ�WNIڅau7�����PS���ع��X���VU�ʲ�m�h�j�6���K���O��W�^*��r�ɒ��U��V��������3O>cmc�f����t��v����M�9��4G��eLI  �Z��TE��\o����s�ayD��D�")s$RTs"( ���*"F�@�m�2�YP�ڟ+�mf.�	].�)~�JFV���zՕ8U��[���$��s,��A)�a~8��C������N�c<KO�E1�����G����N�-� M�[F-v�X��J�����Z�б�)2���%1 qO�y^�v�/�<�%!"�w9�74 Ձo��1D �/����ŋ/����?����̀�
&#'��Ц:���s�=�ٿ���]�����4�B�{�"23Qf4ED������2�L��cD�����3 ���'�YWQ���E�X�ȡ�4����l1@���Ī�Q'5
b�� �j��I���bw։4�D��v�Ų�8!"�  �&P�H( �
��L����`"ж�T!��% '4Vj#BXýx������Y!d_�u� �i/
��H��P�2�(�qjo����Ļ���=�G��#�[�伣@úr���A���q��g�>�� V[��m�ћ�E���{�~ݝD@��G���4_�˲t���7������o��3��{�QDך���D۪n�����3O��Ƶ����.�?�lp��!��Ac�1�O��NC���ٍ�g��H-W��;�$!b N$��Hp�A�D^�����Ӗf� FH���)`�� LQ����S')-f d!Z�����4�ӵ�h!F*���LUT R��#����V�V,��� �ԶUU�#�H�-	!�!1������CP�}���ٛ�%��Poa��ڶUa�$� �i-�vj�Z;4~}�q�����Zȅ�F��%�؉u�0xB�'ND&"���3셭9��ݿ�x -����T�  s������ߠ����'�6O��NevSN��E`3T�bQJɘ��̬��-&�bS����K_�`��fy��	 `<��jj��r���]��/~���^{��_���G��o�<�Dv���i8Kݕ�i���oz_! �@=	09r���!����EfF� �i��D0eD��k�]���i��9�������֠�ur�/������f �m�GI.�I�t�S�ı�����֭��ڔ"Qm#����t�6rdf������iMx�Y��&�j>�u�  ��[ټU�˥�0�B����ئ M5�H�p�E�vZsy��{f�t�I��1I�#_���68�㼛���P�E�~U����Ξ�`���?�,ͤS.����Yff֗]�-�{ wDi��BL��B�����( ��1��wԹ'n��5
x�Zg"�8�lk+Ơ�����կ~u�ւ"0���
 ����3Ԇ�����o\�����3?�W��A���ʞ���U�f��B�g�N]t;piWi3��D̤I��c��()����=��5P@T��y  G��~K(�vA2�if*
ƈ��4�%͂�&>o�$3c6����>�跹m[3�@1� 1$�Tu4Q�"��  j�b@j&��zU�%"r�%3k��j�DB�VĹ�S�~p�&�ocլg	 ��UU��P�뀪��:2��N�a�~`|�I��d��	Q=��s�м/������f`k�B6bba�Ģ�`
L�n�͹_L.�qp��������$"�/^|���>��������lj!��F�QQ���6M*G�����Z.������{�g��?�7��[�m1{�e
_��	��-��1����p���=���A���{~@D&T&6v�͟I��G��v�����\�J��#%��"R#d�Zۮ�dx0#�W~�ڪ��
�2����V���L�����I�VLT�%1 ���"�"$m9	�9��LF��9RM�+i��L��kS�� D�̴���b�4�8Nb\k��q �k�	�Ao�6��t���6�H�E#"�ܿos�O��Zp8�kN�:�+�/̚��#�Cn�c<"��[h9�)�I����8�n ^�e��������/�گ��j� 4q̪�6- �j�
1`G=of&�VuW���ƍ�ϼ������җ��������+e�t����$<����KPp�K�^�"�1r� @�D��H̡�+��Da�&� HB䅋(`�"&S���t5沙a��i" .@$ʤr��!�:ג��)(($I�*�ĕFجm�-��bC�1j�Vf mDڪ.c1M8F$�$�JT��$���	�khAVuդv�ڙ|Kff�qF @U$TSU��C(���`�6�t�O��
C
�<ʃ(R��QW��� WBCP$���Dd&%/�CTW�Gb2 $�`�= �k�*��pt�6�%H7Si�C#BS��xn̉Ν��Il�������5�Ff052k� �ta�;��������r^�*��`'�����s�z/<���^��o���"^߽u��K���+��o����_}��m]�X�K�Ċ�� �[�xc���!������� ��536 d��h�^ϙ;��2��{F��"�+ZBu�
"Y碌�d:��k J �ɣ����O�������(V��@��"" h���j6�R��f��ڦ�9uJ[��b�j�qog@�ԟ4A�D�@To��
!�fL�IjM��`��j[1���Xpqfc�v����Yd$�d�e9��qR��8B,���W��������}��h�䘕ܽ��j6��� 0�����ѥ]�@À��jYo̠n2h�:If*�ʬ�(�'��e���؏w�u��Ƽ�u�} RTTfR�z�F]���ɨ;�/ �u��r�	�;�I��C �{�wh�=�6X�}T�{�͹Nҭt;��τb�4ޔ�gwǏ�p=���=f�f��a��:� �!��,�j�o�w#)1�<}o�-�̛6�S� 1�|1��d N�����'������߾����������eɁsJ���5IM=��+�㛻;�x��'�c������W�sa�1dLl&���;�vp�������� �_����$�0jd$*L,x�9�q�;��:�M��G_	��D�b�h X.�QbK�P��,gӍ�,���7vn��r�������F��r>1�r~�r�R��uv��7QQ%/W@C@�S�S�n��.b��c��HI���s]D�i�M�E0����7    IDAT�A"���V��I�ͭ�MiU�@��sB�;ޥw�:�{dD3�-�+��! �Sq���n���$O��]c��\̐�Q���G��C�h�\�fkl"2�t��Ybh��c������K���}� ��Q� 8{�̕�W������too�j���v ���)"��a9!��m�����o��l��K�ɟ�������B҈q,
6�6� @����8�8�.V��6�2w�b�y�Wf��DL����S�ʁ�:����h�!�z�����$1�/�L	�L�t�1E��T�������hr��G/?�X�����7n�����u]����幋������e�rfI@[1SDud�!* ��#����#���F�Ք"	Cݴ�Ҷ"2��f���|:�	d����.^�<a�5���5 b�C�+/� %d��$f�������.��9�S;�����%�k��Ke��v�����w4�	Sd..��/��F`tO�AeYV�
 F�!���˟�Կ��O~j�����3�j�Jҕv���f�U #Cp]#2������v���ˏ��O��bQ}�� CX�*�[ ��q����G: ?�X�J�\��xB"�*��C@�8b�@UQP����K�����
��N�8p��$�C�ډ!{DDU �̙�l6y�Cx���ׯ�x�ׯݸ��_R�����b�?�����s?����k�!Ui����f�����K������J-�*�)�YE�X`1�� "B�EQ��S�&D�j�E�!��t�<ޘ]�r���P�E1k -녶m�t��u@��6�I��ۘ��!�uA������꺖��$)����:�S;����k&<SS#�L�^ɦh���a�=wڲ�ͯ���0��cE�@K��h��`�<�`�>��_��2��H �\���������h\<��#W�wewwwkk���/����ݿ���Ϸ+�$#qঃ��B.%�ՓB�
^ �Z�����x����?��������_76'�i��J�D&j$��YW��P��������Ã��Rʅ7
h���+�Oy�
�:�	uRVuF@����92-�dT4M���iTƺ�sӑ�  ��e9�N˲��,76���I�4W�7߹u���W���ʲ|�������x�S��OeU�����������_޾y�X����ܚ�����u���c9/I�lw/�P�e��H{��C)�[cZ�VU�\�p����{���@�"��|�ң����U�8���IY��isKż=E�0�&�[Qa���D����� MI �d�����^V��S��|��?���[}П�VH'����1W��8�YvN�B�3{���3�1��hG=T�{��8�y� :��A[ח.]2�����x��?�����g��/���������
EHUU�eY0p۶ݥ1�xd��)��o* V�rg{Ֆ�ɍ;�[[[���'B������rQ�q��L�1�
��E�nL�e�Gm=2�t�k��誄8&bbE=���ͳ���sދ�,K5	@4E���l�`]�;��('�iY��Ν-�C��[�𵯾��o����T�lLg��� pf:�������G>��^��HY�9�/\<��3O��/�r�4���_���������d�h��o�mJ��#**$UTol33ZR3S2 �U݆��qP^4��꼩 `�ZEi���kW0\����y6đaH�H|��g��Y���|�ǌ��D������I��ک��- Ā��	��ȹ�!)���m<vP�g�N82��O2!�j.��ij^�8��Z#�M�O�w�U���������o�vE��B�l6�U�2��qs��������A�!���h��?G�"A�x���}� ����ŭG�N!Ajk,��y�<z-��G������!b�A�y�'�{ 9�"�jd�ed�"���F����s'�2�8� "��efd����b��x���&���5*��tR��h4��o��ݗ^z�����������ͽ��񩧟���|䩧��8�5��DfP��ucF�`T�X�_�����_|��ͦ��ڍu]��kҭk�.A�bJI�n�b�@��C� 84W���\���F#۱�h4jR{�K�]��u�|�0���!�	��w6�ٽAkhg��8�]��˅Cn,UԌ]�άw����ІcK�rq��]0�>�vس<dG}<�V�W_��h�#���B�7:������/� ��Aw7���U���Gs��|�eY^�zu4.�z�������?��?��+o\#&1�rШi *�eE���(�xk1�(�l�	Ю招v���q<Y6�O�����B���ߩFaB�I4�ak8~9<u}�j!��9o��k�]z�Z3b�"�#2�*��K$�[��,���$���k�2Q���M����l�c�쏳�9+�r:���x2����o��ڕ�_cU�u��X�6�e$z��|��~�'?������t�'�\����hY̗6��s���'���_��|��G'��3O���@�����.55`�{s{���[7���6��
�� Ub�J����������x\UU�a��ُ~�#�͍������q�&P359�����4u(=�p��
�� a�4.�n�5>��.�ک�������(	�ӍD�jl�����(�����b05'|C�hL�؁'�$bf�5�M:�,;�oe%r(q�1�'Qu�4��e ��K�/\ؚmloo���������o�&5B���9Ј��u0T���D��3g��d��M� ���VK�A
����Ǯ�ػt��/�7� >󧟢�<������Ԅ��e�e��͌�Դ�/z-f��H@p$Xޣ��0cqb��%s��5���P"�@&0! D
�B�l@�P�P
!�MTѶ�m^~� 0�h4�NGEQb�"DT����_�|��߽���Uk���]���{���O�����d������ysf#�������h����Ž����݋q�� �(L葧��r����G���oMf���k/|}g�ƍ�Wvo]����,"S�Og��Y�G��؅._~�(��6"M��W�JDKW�4;���wA�a�~�857�y�=a�-���KGL�����M����\�L�itÁ3�=T�����������wo_�x7��e��.y��Y:k '!b;�֍  � "&`��8@`&"���t�Y}����`�����|�TG���d���yfcsssckc�m�G��Ϋ�������Ӌ�E����Pǖ'*d�I��'��9ڞ�Q����X�Ae�\���9�٭3��������̟���7?v6߼q�,��l�H;�vy�U]U���c}"�AL�i��Y	f!��x�P����N������9Nf�h���C5E��(�X1$�E���ط�N&EQ�'eq6��mR��j������o�ve{�l%�b�ws��3�����?���n�=��Y��+ h�n�E�붮��d٤8 ��X������[�7o=v~��gf���|(,���nd����06 UM�I�$K��U��F�xs25B�T'�Pp׾��s13�n�\�YU��b�mki[/vj��i�{���ک�`Z �(��В�����:H�s�wsC�#�:5%U&����"���0:�:��6倨 f��]F�|M��.��D��[[g�E[7;��g6���dTD�{���}�s���'��s9���Q4=.��� ��J�bb�T]�ޝ�^o �� @l�X(RQ����f9{/_�P����q��͝�G/_nS��+�a���i�6շ!' �"��_�y_=�C����`T�:�:"�Ȣ�+b#�JbbD����29�A6�BQvR�h��g7��&!g�M&�m�]��헿�͗_{�;���ۥ���zYU pnk����|�G��Ǟ���cg�]��F��*M�Tp#��DT�jo^-�բZ��di����1�ج�7�z����;v�&���͍�i�bQ���j��HŖuUU�bT�e�bww�((� V�UJ�I)I�N��XX�U����yۑ2������&шь�&��t:�L���Ǔ�dR�'#���~�8�2�A!�w�ǖ���j�}�0���h���d�c`84��AB��ur��*�aW��7�X�\��R�]O+����#2@$2�dB
H�L��X,RjG�r����������g>��������/~
�MʦiT�9s� �m�:DG���JD� ��T\{�	0�&�Y,�vn�$M��Μy���Ѩ��_��Sϼ���Fh�]���y߳�����޾1�M�3� �Ԛ�n���}_"*�"ƨ�����EQ�� �ۦm[bF3����9$� %�kafԇIE_q�9��D�X�3|v�Z�����/�x卽�W�����.�oݸ5�.^:�����������x�͍3.\�J405�{jm���P����ug݅b�4[[��ٸ]�(�����^�umg�/3F��?��?�ܘ^8w�̹Yj6.B���i��[7���|��&Im�H��9�j����S�N����/�C�@�t_}[��|>���iTk�&%�3����S;�w�Q`�L��S{ �9ܥ�:�"@l*`���?ω�!"�I&�dT��0�b���f1ƥWP$d" bV�<��zV@{�{�o�e� �:� �"�̬���t:O�{{_�~�YUM������j�� ��l�Xd!�&!"C�r?9@��+���	DD�Y1(nDC�Nu�m_��b���[�	�.c;_ݾ���1��x��?�?�O��������n�m�f�e3��"�[7�ǒB$�pw�;��"5������v9��}8pfq*˒]�������CPT��(1``�v��x2��
�ݙ	��occ�/˺����/��7������˲V���Z��ш~�G>����q�¥�����d:�؄��AhWҶ1*o�2�t:��Eh�vww���,g�"���P��j�x�L<���� ~��?��+/}녯��w?���]�p���ƣ/|����ژ]�pakk+��S�:{ �N��$mۆU��A!��DSW�����5;�;=a����?��u��F�ou05W�eD��+��LuB1�LS���,��ܛ=p������jq�?�o��|[��e�Jǔg2Q���w��/Ք�@@1�0vb˾��c.Ɂʮ���y�1cbo��530F ``2B5��/��ڹr�ʕ+Wn]��\��{�r	��4*˔Z40��Q��4��L�zё��8I*2s?�3ب�jy��vUU �y��%g�N.=���?�Ͽ���O��ܸy��s[�Z����I'����0����c:.�kjj�
�����h<b��]�4�������7����ְ�9�o~=�� I�Hq0Ip%��DM,�$�� �R�JJ�(N\�T�#�?rlW���?��G��J*�˕X�UQbQ�-�RD$� $H��э�~���{w8��k�����w_w��Q�X\\�{�������3s�{S��N�lJXF&�ݪ��3;b��'�B2 {������y���w���kO>yᙧ�]�i���FG�����p<x��x��޻�{�����9���9��gTI#ˈ
�K�1d�&!��#J����h`��h 褃+�;����;W��p��7nL��&��'����ک������:?�v���FcΊ<�s��j����^w[�f�33 b�	
R������5-X���y�k��:r�� �[�>��u����!;����M�.�d*��:��P�R�()�2��t%�%�艿'ĥd���*���_�H$&����m�VWMy���׮�U�sp�����#U�(���N�a�'OD����2K~�Pb�ڈ�� ��+��ZL�\1m�
�:��ӣ�����Ϯo����������jzҦAF0Z-�Y'����>�W
ѳ7�B�9y����!�E5ƨf(�[QED�Z��:��9��9f�]�%�r��� ��y^���/]��ܵ����p���̡L&��y5����{?���~��Dy{�����`8Ș@�N��)�:$����@�Y�5M�&"�,[�_҆��ijJ����n]?��ol�Z��*����������[����4ޚ\1���?��h8���Y��[z9&֡�(����T�D33 ���¦�G�.��ک�/�u_��Sw��\������,�r>o�r^��弜ϋܿ��^9[B�^#������)����	^�ӾZ�{�*�X�b9��|�]?��Sx~r#�����酸�;�B�	��@N����Hb�@��cf$k� @m_�ʗ ���д<��5M�B7�A�`/�qMOQ�D�@���:�`1W�ȫǪ��{գ[�ą�U��Μ��=}��~�?�����W~��O�?}�"��,�ѷ6$��Eᜋ1��������HDd�L� �a�UUc2PI�itQ-+�'�311y�3���S9��{{�/^�������^�����,�U�a��G���������k������`��	t@`j�*=.;�s�ItD�#\YN�s��ET 14��h��C]�����o��޽��7��\��22F2�U��s��ߟ�G�����h���󻧶O�:�{��$'[��[�'�b����<⒘nU�;-*���L�ד�����W������d�EQ=��LzX×��x��辁#t�c�]$��U���ઈI��T�b|�;7����S���)DJ�����ě���N`"  PSL�2q�*ZR��(�v��D��$i
�#�A�Dk �sεm{tt��Yu����m������� ��4to��&K�=Y��D�]J��D@E�i���*��T��E17]g��u�i��R���M�Hct�1Ve3[�?����z˯�����}�SEQDi��AϻЖ&a4�Y����ᱚ"vĞ+l��)��Q��1�(��dhΑ��,h�h�KɄ�	#�F@M�ZBNDj����fmU]��7�N��o<{�����9nB�Zm⬬t�5�����C��׽���p��m�{���`�|�(�*��A$�&LD�
ۺ�ϧ��k��M}�;��rxx˥�J� � ,�S����uմ`
;�gw����g��A��ِĤ���A��Vhf�>{P��}�׼�<ϝ�7���ۛ�=���=Bl����T���i��53sf�&��8Iߑ��N�m��Q�{R���ut3�Fi�#ƅt�|>[�(
GLLLMaI��zbu�+��+��-i_n�ܣ�r�n�m���޿�t#�%��?޽�P��Z�O��EIz���/��xח��=_�v�l;}J_5��;.��w��x�ks�߬fz��Y�����۴A�g����L�����{5�4�f,�J@���@T�0Q ��S�J��`�1ꭃ���èbl�`f��X�t\r�f`��K5"0U! b���JL˚r�;#^H���2Q��/\qrt� 1�&h#��sw�܃����k�~��~關���z�s�`<>�������w��x�	s�"�'b  UI��{/"����H�"�
�IS	@���3��*��7���<s�ڵk��t6+gG�\�(VM�"�Cz�>��{:���Ϝ��9�}bb0B����PZ{������Dc�4F����MU(|O$�� ���TAA�@c�ad4F53�y�򖷽�捫�[��ʐƣ��{�� �{λ���RY�C���Y��~�������vvv���76��9O�8��.��� ���<�Ķm����;�HQRE ��;G̺�x9���	ܹZڶ�NgMӴm�4M�ضmX��D�D���}h�}�v�[��?�W� VG蠛�\�c�g� F��i/�e]��q�M|���&/ܘ�Zt� �]��"Q,
8S�h`Q[ R� �mcI�!fV5@\���#M[�/҈	�T�����@M-����3����,'��	y%F S�"Bl �ɑh��6Qڦ�{�����>���<��/��p����en���xm}29�~K��^w��[���N�A    IDAT�	��\V�J�P���ʎY����  �.�d�LDh%X0�N8�%ڵ�ן�x��g�nM���l*���hR�'���{�y�����>��[]V�^ok}c4�)�1;��	�$M�&�(p�9����/1�Bh(���g� �<|d�Hrw�5�y5��E�𾗟����赺n��Q$ֱ5#ψh 1jPa���UV��W��E���-oy������`���~oc�T���Z-���� �6��F����՛�L���Ő�Ơ���73�a���~PW�W�L�zn���^[�Y����Z�.��һ}eU Wvm[�,���0��?d�R�'*jl"v[�j]�htG�?��ef���&l�I�6DB&Q�(���-��V�BT�*Q-*���@**-|-fN�߲-*�aJ3�J&ޜ��ߐ`7*@�&NJ�	���� BĈ&��CTm�	!�ui"�{���w�����+����O����g��Z�����hM�dRP�������Nd�$�;B�̈�{3aR��1���;�-���u��u�!ȓO~�_�z5�z}�	�?��:�vPmm���w��'��^Q(��eY�3I3���"��Ta�T�_0&��"  @S��C�Ac�QL""�Ǭ���:mK0�	KZt�B{��H+Tͼ��x���߀���^;8��X���i�!z��B5ؠ�G`bOh�:k�IU7M���/�����pgk���S�No�r?�E>0��iE���f/,�H�J Q$��_��e����b
g��t:�������Y�[.�%V1
����4��i!! -����)me�nEݷ+~ZB��Bh�W�@�Ff	+c � D���MDn�6��6�物;�:E�� ���Ab�j�h]7!@5���T������Ӈ�b�幬�cN� N�P3B����,ɈU�)$.�k��5oYQ� 8b& "jL�<��aT KmZ���4a��@PZ������s�����}������͏Ν9}���`%3Q%@rǥdd#�ZH2#���^�Y��(
 P��7h���Ȟ��Dl<S�
�A��ܱ�(�b���y>U���˗.]�|���|��_��e*���Gդg��~�?��O||��ك�[��������z5��p�!��|�C�(R���ƀ�ؿv��W[՘.B����r�a�ϯ˞��X��G�!Z���`��i �n\�"M���4��UTB�֌��YF�����(oU/���GG�\�_����s��w�s<�?x�����F�弬���1�q��D�̴Ҙ3!�va �Dm�FB v>�_:�A�X�����^�}[��_9�z�t�����W-��Ց���wՑ%֠rO���Dt�)��n<]PO�q�W۞���eԅK٘銌��Ĩ��(��<*NfUy4��U�Жe�4�b��\hDȜp'r� _!B��3�4L��BV.DJ�A%��R�H�=9��Eol����ڜ������ 0�7j����#���G{����_�?��܏2��s��\�&&f�<��<�����gY�y�G�u]���!:�D�#d�O�1F����MӤԙ�n�_����ȗ��勗.�f��t���y)�^ݟJs�������|x��S����^����e@�<Oj��f'W� �%�M� U��.^�� h��42�����h�Q\�8v+ ��uE�r��Ӌ�lJF���\���_��y&�4V��9vΡ�(�z���v�XU5 eY��y�����j!�Y �������ƹϾ��v�6عa�(k��Q�Z��1�,]����n��P ���Q�?��FȽ�(���5�����}{Y��&\O�*O�]z��.�Ι��L;�X%�_�O₹;�> v�+0�K|wD�� �.�<e3�T���N� )�jۺjnM�7���YY�*1��8$�@I��_X�y�g$�"�ХJ�6�C�(*QU�����)�Q��T���������Y��e@�f��Ԣ��DS5@��4�ѴUb���n4M�^_ӣ���?�G�{����?��Uu��z��ج��0@�������L�$��0�#a:ۀQ$�("���3CTf��j��T5� #��م���~}�O}c^WLT7ͼ��6wn܈
o8������|�G>|���yQ�[�A�U%��hd�%a����b��AY��~BĪ!4U���烺���a��2"O�$p'�oRqQ�&`^!�N�{P��]��d�z[� �fp4�y��"�]�! *H���b�'狼H�R4�u8x�ꗿ������[ۯ{���z�c�wN����16�H� �]E䤭f6��{��n5 *�@��.�YYN�����|��.�HH��t\aZ�t�����e�4bW-��W-����_H���
�kd���fn�X�V�^�l��i�Q5�mT#�	6Y"23](u��2 �D Qb�U��# s�yƖU���k�Yy4�E1�A ������AB
 �+-a�~����,f���4H�H��"!QA�#��� ٓK���Q�BU5&�D1J���A��67����L&Y�7��>��O�������|���`f@`�������w�8˲,ϙN�i"b�Q�2�C�¥{۶��  1y�M��j�e= t�d�<Ͽ��/]�����N�e˾w���Q]?��c����}l0��[�;��H+1b�c�^��j��+�.X:X?"F3A�W�իWAЉF	U��y�*����� ff!)��,/B�@���w�b̾�w�<�=^{�d�Z'�t#@��B���U˙w.��.� m� Qm�r�|����G����'��K_}j4����=p�����(f�L�@���*u� �Y*U��f�|�r���	D�Ĭ]�ּ�m3����Eџ��{<��ȫ��rY��~���}{�AJ+���9�Bq��"���e!	SG
͎�̢#FK����SU#r�Ȝu|��L��!T1BL���N�����Z�(��V0bB4dH�3[���q�  /���i'�[	����ޡk���20 �IS�Ѣo����!F� �bN�D�!�cr@bhH�4��h��� �8�L�����ן}vm29������������w�7_��CG�y����`mm��
�3��"k��*g�Aom8(�i�������$r;f��'�E�E[ZM@ c`##�c�0��*nܸ!�VU�}��XN�M���rp�?��?��~��7�v�<�z�C�ϳ�	�0���("��03Y��P��*�CD`qV6��x���}�I��L�
�\f�z:�e�1VU� ��g�9E��� R�C�@ӌȎ�Ff����.��nݚM��y�2H$�!/h=Q%61I�1��*�c"dvu����ɨ�����>��?���=���7�ᑍ���ڀ�Ecue"�i���	�F� �`�ز�f�� ���Y\vCS۠i�,˚&�Y�� �ۀb]���q%yu�U��3�-C��˾�o�u�|V?���W;j/f
��l��x�Ճ���WO���S�/�����C�L{1|��U�.�K]ci��d�h����Z	�V�N�d����糮шOtbr�t�N阶J5u����HHL��t[s�E�m[l����DP�D�I��l/_�{�ҵ�y�0��iD�7E�R��I<_���p�H�@��+�g���Cp�fd`���b���Ef�H��D� `E&�@B����{p.F� R��Q9SF�Yڵ������~�W�o���$���u��j���u�c���쩳�����;y�'ζ�l��y���GU��<�PN����<7��Z����B�UՔ������D��[��9�u8E��7��������<���=�أ[[[y�G��W$���1Zj����.�U���Ĭ�P5��öm��w,����y��n!���gGCt�;M��� ��p>�y"J<�(f��
@*5"Db�>}�n�N㵾�Cݔ�,��{Ϥ�:��N[��@MQM�:at  K˕�"����nޚ^����ӻ�Ξ��\������@B#�R�� D�J�(1˲�h��uS6Ms��\�@�N�% �I��l6m�6JhCi�%޵�K:�E���n�b��v��r��ē�\���O�P �OiٲX!FG���,u+Q�����LDʲ�A��Q�i����3�|tp������~��=�@�k�7��<<��G39�6�G!&$.�1 �&f�κ�ԉ�y~�]��ې?��Y��4eu<���`L   �ݔL4*l&�D��������:`��X��#ǆ��Tͱ��#S�4h� �y��������?��_��O}���7������~�����:��6����|1��z|$t��d�s���s�L�F�e�T4*Rb��"Qb�1Jl�Qblb�����AՄ�ן�����E��w��G��8w~ggg49�^Q8GY���s�HY2�j��F�񕧨bh�� rXNn�u��D��Vۦ���)�l}sBے�E�B���3R ����I���^G�mHd ��Ք=�on�R�J��b>���!�)�G娔 l�18����$qf�� ��1"P4('�������s{gO�9��������>�����L��."U� ����L�y�e�:����������QBl�s����H�b'�j������f����|�_�o�_v��+�o���o|E�k�n�_A��w�- >w\�ez���ݖt��8]P)"���: P�y��	Cs6����͛�o�d��C������S��]߿y0��ܺ�?)[c���y�K̌@ە�I+��t����{�.�ݯ���焳7"S�����,%b�8���L1u��00�g  63 �ޛYºFk��iD�L���W����߸���x�[�����?��_�������-�-�-�s5��fİ��B�N�"����f�m��e���$ ��y�1�H�ڶQ���h�D�!�K��m���A$�:�";�t4onܚ �w��}?��?��Cƣ�S����� ˲�`CCL+�pQ��kpcjfAci�L����önr�L�U� �h^��ݺ�7��a ���*��}��¼���Ȳ��b��*Q����b�F��z���|sm}<Z�{��ޕ��8��/TM���T.���WD�H�L;1"QL���@)Ɩ�%R��pd�*z4)��ً�\��w7Ϟ����F�� �`� ��%�BE �Dy�t��j��L���k�賬�뭒�/��s��۷f�:�MiӪ�rv[��.Y���{Ɣ�iu�ª��23�&�a��p�����O���/]�������:�V1F���0G��D(xLݾZ}]�X��V�@�}K1-��a��t�h��l� �:��zҬ*,xwQ@T�hq*��L=��1":F�4��  ;�<3�nse]d�{��i/_�[Uձ����/����������ׯ<|�A� �6�a��u3��h4�����{UU�����sj(�hJf��D>sQŌ�(���F�(����QB��iZ��iC]�e+D4�U�m�6�c?�7~��ݛ��}�8	xQQ���^�!JZ3��j���0$302�!H]�GGG҆^����#͏&�[�<�~��C��vw�k����`�D13.�赡e@RL5S� �4�lM8���碗9�����P�m���dX��uۤq�4� $+#Qb��a>^��v�� DC� �ϲAh��pV���.\�������|��٭���g�$�Ui�)� ������VB��Hsj�� q��,�ݧޥ��W��2ayG�G/o���[֋���',ҵ%�����01��u���^o8�yU��_}�O������g/O���p���!�� ��* &ES���
���S.|g<���
a���g�8�t�d�g�#����b��&腨�D�EB�.QDq��#�"�wP �!��&�$*���7��0�T���m��|�����������}�7n��y<{j;6m��7��E5F�L&j�>J�k����@�h������hjI��![P�@�mӆ���(M��M݊4bG��&<p����؏���?�7��	�}R�bv���<�ՙX_ԽP3@�
-q�J�������CF͜=�a�ƍ��T�4a0fy�i�kb2���$F3�E�U��10"-n1����x����������<7���7Dl�ء��D� �� T��C�$���˓Ϡ���<���C�
EQ R۶&�����.]~n���]��<o����L � �0i?�~�̬c�$��A  ��33fv�!VL�<��v�� 825����$��"s��=K|Q�dʢ��3ǈBRA hB;/���|�3���?��j2��ǻ�ͪ�Ŕ� ����)ٷ멵�,�`�#��dz��HY�N�D����ԺX��TIC��cnّۚ��"�GD�� ։����	I�:�={M�6��*��1�ƅ������/����'�������:uJ�:��y_�#&�^��`RL�&Ǧ�<3�EĢ� �$Z!4MӆB��P�m���[	j���G�?��G��>�j���qR�r���A#1#������w܋��h"1�Bh�VU1[!d "βl��QC�/_n����lm�8��&�hf�<坷�������M�4Ab���/z��M�j�#bkALI�XU�A���j'q����X	�߈D`�,b�{Um�8mj�}?/���G���3�/^�������݇<sj{�˹�`�Ј�j(`DY1YG�� ιC��( ���Jt7��{�Ie��_���k�^Iz�Wa��s�/�P���ygf�����,�9�I�y�'�H�8�B&�O3�ۈH��ݖ\Vd�x��K�|����~��<��7o�ϲ�SQU��P!"��v��x�HZ�/�o�����-3˥-ݟD!63GĈb���y"63�$X�@��nz?J��c�.�!KF.M�3e��l�{�!EK��[��n޼ID޳g'`�ĝ��g��8�>�����>��~��>�g���g8uʱ��9��^AD�rVE���,�"*�މ��m�3���մ��yՄc�:��m˪�ضm1D�2yʨ��QU���7����?��;���D΋��-�@����,��/A]0��� MӤ@�i��o[�e������ݽv������������ML��<-���4!�y瓳�<%!ͧ��Ξ��O���o�66z��ޕ�L�	2`�&�"�Eє�Ĕ��\������f��ǭljl�����SLN��J��W/������왭��`��9b4S��b(���u�)R�B9�����M��u�4UU��W��z���]�-=�qN��3Q�tiQ#��0"B�E�XE[k�0��A0�<o�fcm�����>��O�S�:�yDz��Eы�pZ�#2 ���uI1Y�l�@ٔW� B��DE��D���%;v爒����9l�� �)�]��`�st��fjI�E:1 �a��h�6JYN�h
FD���-�B�Hm��1$U/�y� �9�V��riME���YL�)3�� �s~R6�67|������������>�o�ۻ�1������� �n���T�9Q�ʪj���ۦiʪn�6���І�4Mu�T�xpp3�����=8<�
G�����G�c����Yo�+
�d&�5.'�pQ�����DF+^DU:6$T3�����k����v�[��m����F>蕍 ��l����﯍�t��5�:�z�A]UT���J�,�	��Ib��6y)L�ȈEQL�&��Ӂ��c:�B��b��y����u=WJ��������9'3H�W
Sś�B�I=[c 5%D13"M����F��3
*�\���_�⣽����k�;;�@R�r 5����lʺ��O.]Fv�&���Qr��飣��ϟ�#������8Wd]�9�=�Vӈ;�������<� I�?��W���ή9�B�6A=R�!�_w�H �S4��3�tO��Ϯd(/%�|Q������K=H��u��I��{]�t�Ɏa�@Cv    IDAT���:�����G������w��#��YbSF��TT�iD��c.�"�Y����ĺgv�	hQ�]۶M���,�O?}ᩧ�����������W�g�J�MB�H�An��+�|;��:��4�   �����Q�e1ƶmEb��O����J5����LF&ddr��.=	��;�����E��r�"0'V��
��σLjY�>���|��?���/�Y��7!*4y���3� ���Mӆ6�mh;k�����mc�&���mh��?�::|����p�X����?��?��w����su]罂�[�%;��V��[і-�s;��l��w�m[��zY�'f�T�$�h4b�h4����z�Mo~���v8���4�Ȝ-ΤF,��8�i�U�TU�4M��{7�wO��v�j����Y}떙���Vb�4iT����O������옔��r���$�rPRb̈� ��#��<u���t8���5d��n����Ҡ��FM����0���Z�
IM(�2���<�Lq��v߾c�9�_  y��C&nc����{ �4M�4e8�ol�y���� `2���o��g>��~���â7hCkQ�3�3���kBv�WT$�^�{>����e��y���١6��-l	��ε�.�QZ;���> �mk��F��y�f�CK%�T�� �T ��(�(D��1�,���y����[u�)�K�]3�b%����,��b�ө��w��]�A������׏�z3�懲���(*MS�!D�Ab�%�m����M�4!6Mhۦn���[��л^Vȓ�\y��s?�~�㏿�=���b.��=!x�iڀ)����] ��Kx� y6KHSnېeY]�|^�y��l^� �����S�TuL�W�}�9�www���.^����x}�9����*m{x��a& '��`��
ҍ&��BUͽ��h���n�l����(
��3�\Z4h��i�n�/�8��2�>�~-8�@�g��X��Jh$�s^D�wyQ��m8�������<���~?[��{����0�k��3�1��Ѝ7��U�ټ�ڣéėܳ�;�v_<��}{M�K��/�P�_�ݑP�v2a;~���B�9}wa6�9�8������� ���O�e"ѓO~噧����������dnU�������kkkLBl�xt4E�<��[� �[��3����aw��e���$qo��{�vrfγ�D��#�V8�TT �5S� �6�or&GL��P�� � mH��/�%��)"���)#�i� 1*��Ҷ��B]�̦G?p�u����G����o�ɯ7�6��$&����lBW��FUm%�m�4!�mb۶mm��AY�u�:�9}��?�ß�~z}c;�g������̘Ҵ&\	!��R�������L������ڪfvH8�L�\��eE��Q�j1��l
@�Ѩ`����l�������9}j<Eqs� }���s��0�����	�s�9@U��tJL�^O�谚5U��l}}=4�|^F�ċ�u�\d���\�v�0�]	gQ�3���HMA ���y)�J� �y���Í��B�6�\��cux�b�;�_����׼a]��Ӧ荈����,�.]�@4���~f2��k]��/�:H%ֳ����f}�^��z02;�jZ�Za�\�:C\[[���<<<�|��y�����O<��׾���~�ϛ��!8Q��C��mb��\"+�&��S�-۞K[m<�p9�D@W�<�H�dG9��5]n��v�]N�mL�V�@"��%��	���q��U�M���jG��LI��S�Ą�L�R���Ŧ�g���>D��HE�� X�K�@C�õ�i�Fɴr�|��>f������O<�䗿p�h����ϸ�^�~}c{Ub+��46���j�r^�UӄT�M�e۶UU�y��v���s��������E��\�|VdY6(z"b�D
��\�� �E%������Ic5���7k���U]U�>4���^?�y9�f��ϧӍ�5����l������6����N��m����\�mh0���ׯ�
��(Um^�mh}�=S[�5���{[kI���yVm+ ��H������1~� �(�H�w�qP8ޚ�L0��P[E����.�s�=�ϣX�$�ʪ�M�`��������p䈋���y���+�>���p#�ESǙ)v��w������;��/�������n?Yd� ��{I�o�q�~�XG-f�ab	�3���{�\�]�fD�16M3�����K���O?��SeU��Ng������6�լ��w��0����DC4^h��-U���4Ž���]�c#";��49{$<v�+Y����*�l{X�N�K$r|<!��FI��T�H��L44U�&�wM]�sD�}t*�dx�^��'*jP )i5�7�'������&/o�k���}���ukO��mmn��	1TUY�ulbUUeY�u���M�R̦m۪	󪜕ջ�������{><���a]W��(��E~DJ�HL̎�RZI��.�p�L��̀�w(8�̙=9O��˒��s�b�/�s��ሜ/�3���pʦ���պ��6w�Á���JWx�w0UA�Ӵ�S�eLt�ʕ���왳�LC]UU�����Og�A�{O�r&R��4$���o�"˄D�f dd"I�΢���N����w�3Y�df�\Ū��������h���o�9������ݯ|�+�,�L�ɬm�(�;6���,h��O�e����۽���
�@���Ī�صL���6��<wΛٗ�����z�����_��z�3g�h�#mn������Yo��齯ʲ)"ʲ<�(Qc7m��usVN�Nnɻ9��G\u!x�;YP��l�|��1h:�;z�i�&J(�`<P��E�c3E��A#�â�F�Ûm]l{�޲Ԭ"*��� ,��"m�(20QY�#3{�\��*T��S@@x<jKҥ5�-���@F7's��?�+��?:�ԛ{k��ϟ�\y��=�����UY�U]�uS����U۴Ǟ�i���M��&�7>��O��O��C�[Gb���x}�@��'g��ӥe�>�*�B'�[(d!2@��gQ�d2��{μs���ss�1h� ���/�2�6�w�i9�˾��������0]���b�S��M���<��H�1�d2!е���ٳ ���^9�|��"�!;&"B"����-Z`��ce% S�4_�=΢��)��i�@� (�"��D�T��ٹ\���@��\vp��������� 	��[�4���(;43�ۥR_m���i+B��>���_u+�^��;)�zu����_��Wӡ$�� �����W3�y>Ϝ:��.]��կ>y��ů>����`��ٵ���<W����66@꺮�
��
j���˭�����/����)�	�YM3#��(��CP5#�F�:���U�7-|�%�bbJ�E��&�j�4)sr�Lи,���E��F;�c��X)�[(�9��E�,��"��(��.\��1^��ŋ�O�>��G3�/�?4�u�:�BYǲ�m�YY�u۴��a�)C�6�A��� �}���?�هy㍃[�����VY׮m{�<�<;J�)��$.�B��ջi�@B�����q)��P�,k�j^���9�9�Ĳ,+�L��G��,����xm �������~��̙3��`)�}��m�����1�d�}�Y�~[/�=={�p8C�8��H��)�Z��d�e؉md�%A@$�$Q���DR81AH�X�	�$%q���(R�Y��{�����RU��s�ǭz������,r��u���^Uݺu�=�l�_��Q�Q�,˙�Ϊ��m���	�uY�w6�P�P�9�ާ��Y
"rSX�*!@2��� @T.<����s�Q���TjbU4CR5������*T��]��>{�eM�W�\Z��{�~���a����얥xK�+���s�����p8�u{���w���׾���/�\����� ɨIa��%��9Gl�%�(3q��5C3N��ɠCl2!��P{���}���lS��J��O��:W���I�k��)9WS�js��X��GeRԓL$�#j�������r�j�7�1���!Te���dO1��Y4�=�<h �2B��#"�1��}n�Ρ�z&ED &�k'&Ǎ_]#FDfa��:��yp�`�h�/�;���>�@��~��?z�O�,-�{��A����.��|��2��O����sO=�[XG���_���3���Q��eEE�E���"��� �R�r�|���:�[˻ݝ4��!�6*�L��82P�h�9���Yסwt�����f�������	˲,���q:��v��*�T.�T�~�/��[��h8�w�DL�. u��G�ɴ;�L� ��:����zU��KK�^�t�Dv��me]����(��EfF�E!o�\�� �x��C���� �E��DĔ��d��Iq�O�U2��h�4"�s�.2I���$ׁ!A�8X����5 �����1Ĉ� A��0!9	��$Z3���m ړ��@N�k�C���<�ٚ�q����Ml��D:u��#�c���4���6�B� �������j�k픿�n:�!z��&<�W��_���fH��<���`}}�����SO=u��Wع~��rꎪ�b�� ��'�  d)(��[L�o�������,��U�	-a��=��=�$0R�~o�Jk.˲N�����BUU��(R�����Q�j
�5O'h �H.#�0��&`3$dj 
�X5!"3���  �a�n�m[ZZZ9��.m�<u�?��+�W���+W��e���tm���׎;v��՗^9w��ջ�u}�����~�#��]��,�dy���ر��v�hҠ��y� �9�_�֓l3��D����>noo3���g�"�7��+򝝝��E�hp�D4OB��w:I:�$�,�T����d��o�����`0�r�r����رc��+�_ PN�.^�v:K���m�o,�D����ҵ��׶��ɀ4J]�	jUe���H�6E��c�	N�����˲L�IED(����Ʊ�W�M��i�X�J����RZESVq"펦�bаjjZ�,�V��Ɣ 3Ԅ��2o�-�'N!MFFDU���8w�l���������s��Q�Ӳ�Nѡ�2 ���o��~-�p.su��;�_������s{��$����$DC�V�QC�g �7Nsc��"T1�,�����K?�㝲�hQd��B���.--�K������ ���,4�n�`�	���Gػ5av�.!�ΰ�&�q��.��r��U���O��_�������I�s�֮]��圫���W�.?~����>}晧�;v����?��C?�����s�qt��,#JqHMT����DH��P�����C�ӱ��p�ͮ�Ҕ�sn<��]]�R���2C !f�t;Y��ө��(x�D"N�AA�9g!F �t:�9Q���O}�����Kˋ�a����I]:��*�+�RNƓ�v0p�k[k�._p�49ґUB�g` ����DĈɩ���1�E�Y0�sr�b�X%�ڳ�`{���!R�rB�K����L�q�(&S�lc���D
�Cm���s��ˡ��o������X���.sqo�<�C��߄������?�z�g�V���]�zmm}�ꕫ�� ����tBU�P�u�e�`8M���V��ۻ�Idf���M7��I�;��ܭ�ɤ�~d~i�9�x@$�jμ/���t:W&��x��wر�I��_��Ȃ���/�$��%�$FDE@�-J��^B�*�j>�Gǈ��R���HE{ ��Ñ�mǎ�]�<�N�������+'���o�����/�T�R�o�F��嵍��y<�^�p�_�w~�S?�s�謮mt;=G���� ^S6����5�����鯭=��������㌉�"�-s���$� ��;������f��Q��t
 EQ���VWW'��)'�O�@!���`:��?���W.]*�I��]t֮�^8���ںY,D
U4D�Q��)٬�� V�s�L	������k���A��К�5l��Lo%�[�PN�9���!djmV��XD��ReИ���*��F�`&f�9��9�'��y���7���k�B��&���2����wD��TWCk"�  i�{�e9?�+9Oe�p �G��y{�1��WR&ń���Y~V��:$��=�&Y`7f�,$�S枸��[T�t׊�j�R�5"��B�eh����yg:��e�7p.wܚ�Q� IQQՐ���"R�%�"�YCJ�h:u�y�����gF�; ���i���j6�,����ĉf6�N��B�{����a���N���7?����s���ٳg�㎝ի;;;�/����~��G���{�G�e����ʑt+UUe�]�l��M&N�J"h��:�}8{:v���:����2j �e�vY����3ϰs��N�D���������q1Yյ�x����y`�5`�9�������H�Dt�,,,lnn���KΟ������B�U樮�ꕫ��N�ۻ���
ᙧ�s�¹��9z�(�c41@S�"5�cb�[C��'U3 � � �I�PG`���#���D��J����)��A	N7�'�t���+Q��j��E3���g����
����P�|������Ws�G)6vɫ۔��ΔW�����́c�"`o�������δɤf����}���|F�Q$�ZU��O��-Y�J޹a�'�V�  ����sb�=�Q�;O:��l\HPUCl\�{\|8;�A;x����Y��O���" 
����iY '�'�N5F�gY�1;��85١Mz6��,4@S�fE� 1��:!��A�����m6"�-�@Z.��;���
Fb��D���s��9z�xe��3�����\9q��W�����_���~��>�ܻ~߻~��������A��wn��[͆� ���-�>���CC�Ϯ�k��� }�
��[���"�nnH		 B�(H���F�,˽���h�\�E����p{��5�����Hc�767766�<U��t���E]\\4��}��W^zn����t�.-򬜎%！��!4���K%@s4p͐3DbF�c�/3'�<��a3z�I���Ն!R7���*����0�K�6̈ 1ƪ�!�DUEՔW�)�i��Y�lJ�y���߿V������7_��~~H!�|�gg@DhC	�w���o���&=a�F<��|LkK����N���]cm�#@���=|w~���k��]]Ƶ@YNc3Ȳ��뺎1&�n��*ֵd��>#�m�g��&���@Y������Q�{2? [��<u������֞p�U��&�ej�!F��=�����UL�`\�'��s>�v�<#@&���D� ����	�e=LGQ,�۩�*�c5J���e������݌���6j��!�cbB���p�����?{����@�mw�{�����d��/��7�ş��������y����ۏ�^Z{��y�<�"�Cj�cbkÕh��e6`�:�toC��&��j�%BR�i�n�¥+�=���b���4��tީ��h��\���;o�>ϳ<3�8���9�"�^[U��G�"@UU��DD�s�y�e��|����?��Ʋ����R�[��BLDBT#�����!4�3�ڔ��[:��d8����dAE�9$j�r��D��	�"M[DL U����&��	F	����h
`��BuU�(��������,�كp�,������_����ՠ5 �G�W����4Ux�"���4�e=�6�0/�{�oe�YTUDD$M6զ��9�R@�%�<�7[�(� {��T%  晁��IM��k����<��Ϧ�rҝN�á�����N�B �C��ɺU����qT��u��2�1�UUv��(|���N]���.ˊN�=;f����������s��������~��o����z4]Y>������Z�l���~��~����?����w���U�eiy�9BH�A3��cC���&�OJӜP�(�d��p��5ǜw��j�    IDAT���v�fb���JUU5s��uCD<!#!�s�"�!(�sN�RUC�^O�F[�!��A������k��e�������o}�[/��r��]ZȽc�,E�(�fV�5�0���j��4�&�h�Sz�^i�%�������p�0U��vf��T��2�EDC� ���Pe�4c�RT}��n�-���F�$:`"��Y��L �$��&k`_z�!�z.�Tw��V����n"�J�,PJ�Ĺj�Yb���( 5�k��n����uv,��6���C7�i]KZ 1f0��d<���i;&��2�r�e�Nosgg{g�|D��n�"�.'"! 40�$f��f���@MBP Q5Q�e����˪�dE��:�9�uz}�<�w�q��ϝ��ziy��*�Xt�^��66��ż�ˋݝ���_��^9;��x������6��p��{,Nƹ/�z���sQ��?����ӿ�[���F0ab$NC��V�ݍ"%���B��pOo����o��үH��b�DQ���+.�\�ة�CdT��hET�8�:��Qb]���3�i]�1(���'o���E�df!֞�loo1Z�K3� Ο={���,�Þԛ�!����U`6wi��5XTr��wN6300ޅ���qff�[-� �� ��4@TEUM���)��� �$(��s������㰃[��e����d ��2�enH�G
�J|�����eQ�ɟ�r����6B� mf�|.ȁ6����������[5+70kKs��2 �9޻�䛎�΃�7�S��luA�I���&<��z�g �HD4��L"3�&w�N=o����o\�z��k�ѳ���㮙��;g�4�y�����76��!H`Ȇ�Dw�woaXW7��c�UdZ�	�syy���Ԑ�9���E�R^F
�4~:@""b3H�ica�ү""Eb�uQ S��v
�,*fV��jd�a�7��Y^\D���_��K�TUO����������w�>��{���r=����_>w���\��ķ��1����ǋ�V�m=癐�Xl��c����S5�4 <<�r�%6�� (�:P@QUpe��<������i�+Q%" u�� Uʪ��J���Ȭ`./B�iL�13$23$��}ʎ%�� 1�s �B�̹^���v�)��"�kB����mL
F�NWn>K[��_����1 "bVU"�������I�'"L�����m�j��	�}:��1�DCJ�Q5SSӤ4g1�9�V;��)�6��\O�<7����\�/��n=ji f+N���<��{|}rõ�:m�9��f�I7�*�D� �g���h�a�/>�=��?��7����u�eΊ��\����b��[��̝�u+�9����dDbZ�e����ЛY*�Ny@��ڕ%  �˲�'O�=V�0�h$B��F	�����,.��c�9bDCT�"�O
R՚��Õ �T1E���<����ƨ�`�����;jL�HI�`Z�u�u�ڑ��Ņ!�}�/|��ŋ��_..�}CP���B��=w�'?���/�v����w������B��S_�ǟ_����<��<4&$N	��غ:�h~A�٠����]z�-<���8����g����d����A�N��!�du�ZU�A:���Y�w�u�<?N��k�!b�r�� ���F Ƚ+���$�)�_MD-Ej� 	3�������7�i���F�\8m'N�����IY����v�	�*q�%5S�vS�r�#��:M���셭��&#�o���{荔% 4\C��&�O��,���M���XY��*����-�?8�����{�ݷocey�K���7RY.���>��ZR��Ȍ�dw
���V���/,/�8u�UZt�J����V�2C���p��1�2#�Š��)� #d$J��q��4����&"
�����Ɠ���:�F#��
�����������g����r����`�t����ͣǏ_�|��|���p��怜��'�����ǟ~��?�S��9���g���y2�u��P��j����O�&���N��� �򌚩� q�_�r���{��kU���H~�F��4NaQ�bbY���Na�,XT�0Dk��F�5�Dd*1Ɣ�l*fF��S=?X��)H���f��0k;�ڛ2�搴�Y3J����L�^OU4Y����!�� ����)��FA&ϱ����DA3H8��N�,�4����_����{�7<��Wyc��|R��MY��lsy[(��J��Y���mn��ԭ]O��A t=�y���1�׾c���q.���@B�2w����ߵrHS�� dyQ���]eY:CS�fV�a{}˳wH#�u��N�� �g��ji�4��� 4J#��:)��ʪ�	��vk@�`20 ��*��2����9� ,V��'N����_���~��mǼϷ�7�]�Y�9�{ߙ����O}�S/�r��w�����G?��'��ޝ������h�7���y���\��ʙ3�<��s�3�{Y^MGDl֦�$��)?�]ZR�R0w'�l�9��L*�L� I�\��=����P��hs�U���DP3L mu�������t��,/��R,1���ͬ�fgE�Ą�S҇MxB5Y`��ٹ���;bF&DMu@��`�)E��]kRd͚���.�n�,gS}	��]�.b3�
���d�@ �� 3�iy53L���#��~ ��W��-�	��!�C��+��dڿ_Gğ݄���=�z�ZY��1�� 톺��,�~�C-D�:_߲��RC�����E���  ����X� 9�utR�O�㵵5�)����0����t:��J� ��!��tr0M�pO���� !��Y9Q�h&hJ� h��t���~wi���G��O~���� ���v��rj�������ħ�|�����p8|���3<������/}f}}}}}��?����7��3/>��_��~�����) �	M�<������� f�/�,t�%�M� ���!V5�'�;D"�9)��YR����g��c�UY�J;���ٞ]y�&̔�ji�iQj��X6I��DY����EN��,ĠE�����&�RSTD4������D3@p ����I�/�$���2�Wb#1K0w���[rK��rS�e�H\7��y�2���Y��d�ھ�Bܷ}�g#�uh�w��M��iR��P�\�����?�L��c
�@\bd�r<�Ub� ��'O�*�#v�s���Aet�f|!1a��M>�ѮᥔR9��1� @1J]Ku52ֱ^XZ���S�������^YY��r��s��J0X[_c�;>.��p�7X���;��կ�{�~�2$X^Z|��?������G?���A���SOJ�G~��LGE��#* XSʗ�-�nFl��n&ޮqv�l�I*�7� F��3z��W����h��U��4{Rj HQ�t2�,g��#26�⹘�R��H�BCT ���4��&	OC5J*�L�b��L"��g�'v� j)��ڔ`n�ө�?���A{g�lD""��jJ�cк��L���!#"�"�����&tSU3M���4E S���;ղ<���X�ݰo�e��u�K��Ͷ,�v��j�㛱,�e�*�}g{'Z�oR�[R*��ƚ�*˺
DN��=JDt���2S�bf�x<��+�ϼ�(�����s�9������,#IT��M�h���wl�5�����`�;��B�Z�3Θ������C��d2�ts����VUU�� +�´Ew�*gϞ���?ymmc�6>��?��������_���>�����}��?��O���?��_��gz�@:-ˢ�u��I0G�%�X�΁��ߙ���ڂ#kWE���^�� i{{4-��@���6eIfO�@S9�H ̜e��#��~4D$&0bG��14MB  CB4"$b&n��jf!�L���u���D���Y�!V1�Вx����D���y�ć��_W��bb-mOۖK�\}1��2���o�2h��j4�������d~�܌�|3$��=e�e9��υK �1�k{��A��Y9��\D��`$���dJK84��P;r߇7M
��sҡ�T�4k�`�)"�jw�>�,��UM�u�tRN�Z�D���>�󮻽��:s^t��+W�r����1eSI����D����UM~ d@R� v�7��W�=���������;6�!�<"8��幨:�Y9z|4����7�<q�[���������?z���v;��.��_���_|im�ꏿ�=���m�l#eI�%�q�d�	���d��H$�*�����
��*����) D %W���p�¥+U�餮J�u]NB�!UP��L�e9.KC���0/���o� �!( (�c@Uc@f6�(*&�$&���J�hiG���xn�V�JD���y�y��K�"��.A�'�%���n|b�2JіeJE� !Q|���R��%���� ���6�$�7�4K{k�R44�^6�l��([�3�Ll�ͅ��37��NIY�m��|�-E�_��CYn��{�d޲��9g�c��Ǳw����5�o�N4`<���5JcM��}��<���X#�&ɍ�!
( J΍�'E�������9����.�Ц����?�������u��N����/?~|��\t�,˲,��!a�2㾈��MX0 ��D�j��u�U-u��G�_~�P=����;��{����o���I�,JPj�&����q���s�����޻��6�����?��}�{���5�޹v��>�ɗ_>7�/��?�{��?*�Ӑ��`I�YbL�ĨM�j�4�2��M-Z�ƨ��*j��Zձ
���h�"Q��`<��&cS1c�����SJ�V,fYV�����4�UQ-�W�A�D4F�m��ɒ��	vA�M�8' x��!�C*���ngqqqeeeaqa0t:]�(�5���qsP>s��ҶOpf�όc0��w�Ҕ�c��3L�%�.ڤ��k�m�c�ܰ{����8�E��O6������oR�B���L'Y�%B"	22���N��&d RS��.>���N�~����eEǐ�++ݪb��d�*FE�TafAC���;̤�D<�#33�!�X=�b��*w$����{����ߺ��﹢  ���P�@��e�4\�\[������O�|��C=�ؗ�����������w��~�=�y���j=)W�y��/��-w�Ҙ�:��~���=@�� j&�<P��;s��^��&>��JP�n�Ɠ�v��y�9/�%�����g�%T�z:A�w ����$D5�b0&#Sg����`"�b����1��D�:aJ�*fh� ��	����y��3�_�N�;Eb P�Cf���X�Ց�@�
DȰK��H�	Q�ؾ���y��mᎻ%?2?{��'��G����m��\�өw�����,'�|���T�`f�"{�����?q�	 ��?���°���"wyVE�3��M-�cH!@M��m����:�a��y���d�}���cKK�w�����49>PEj�Q:Y>�NG�qQO?��C�y����DK��}�{�����뮳��r����������x4�NWN�~����l{{�5ڙu�%
ĹWT�$����帜Lʺ����U�U���uCC�B��R����!���n�v�P�
dY@
�ױ�R@1��t:���մ��? N7"��1���E�|�}�߶��-�PWUUUU����u]O�F���2?����Hd�1ʾ-�U]�c��Oi�Z � w˼�%�d^���[ۀ+n����c�У'����^�+��C�M�ʀ�qI.b%&r�2rLE�^�d��,")R�߭w����?e��}�[X�,sE'��z�A�����Y�pyF��9�Do	1Z��e`��
*k	U��hk������?w��tg'��2>��k �L4nmo����pss�ԩS�v���~c}��;�ry��<�����g �l:�������W��P�z�]7�%pSIu�`��A�ky�ai�-��EUT��:��h<�Tf��C��EDd"g����@�T#3��:֥#t�*#R"%N��HL*C��gbǌh��=#hz��jd�^�X:D-�������
�bD���{Á
��)�<�'�i��şDءc`D��|��u� �=�n:!���o���|��L�����^o_�eY���|z���ygDĄ��yt�E���ag0��=�9d��j��ʅ��������7�}g��\����_X,�^���$b�rf ��̾�F�@�]�~��j��5���u��?����'n]Y�ٳo���X�����vQt���O?}�}��ѣG����<���;.^�t���|�_x�����h��͏;��/LJ-���s�Gm㘈�8��9"���SU��1Q1!�rf2$���Ī�F�q��'m@��R���tF�����;�"˓2v	�Nw3ՑR�FU�gE��e9QQi�Z������L��7i��*iSBu=��Ӳ(����WQ"����7�9�����7�0��vX��>��-�%�pqo"��f��$U�az��-ADb�N�)1G"��	DPR���z"Ku���NG�\�ysg��ǿ}�{���G�Z͌�S!�ƌ\�@j8��F�**��-�
�#&3 Jeff� 5�1A��{�����ɴ<r��h���E�V^U����k�+�ϼ�]��֟��_����_���>*�w�q�m'n��׾���}�ʕ+?�?w��Y�����k�����F�^�*��(`��M� ��@CUU�R���,�˶�M��'�Ub���xg<����]�LFd�X��HP������w���V�vsv��f��%���*d�՗e���}��<��<�:"�(��(10�Ҭ��9!��)"))V0�L�<O-�2�2}�Lgȼ�L� O!��5#0�{5�Us%����N�g?���u��:ww�B��x���s�����	�ro�����:1��CS��w�PCr2)&Kʱ��3����^��tz��ɴ�������O����x��8Ũ�.����^��v:�^�����y�׬ڙ��'l3�!H�-f�� U�i�ϲԾ��ә�\��������lei���Y������������gΜQѵk����c�N�
1���m��;v��-|��C9OGS6��͍�Y�[����;J�!G���>s��'��H3���`"�E�2Ĳ��n�  �hIeR�I�f
0}
���Y�Q�@�sIU�h���U9����`ai��}��g��OΟ;癓�*˲<ϝ�-�v��L�<*�"M�F��:���13"�uMD]7RIY�LS��;�5Q��{p��S���M���(��@�ھ��X��J�[�z�퐭�C$�싋�W��71�6�ޅ���4�� ��(����%l�\�6�&�S�;���A�TQ�6W(�� �$�Մ�63��k�$cO����n�e3 �:R�?�����P�UBr!b$t�ˋ���r��EĲ� �xkE���9�>��m��3独;�1�n�� ��LБc�):��4q)��� �"��"@��:����O>�d��RV��:������v�w�i��lLYQ���x��{��cY������x��G>��/�y�zmu��Uml��??�N��c��Sޓ�n�22 1 #1e�;r�������PSɢQ"��I��3�j���Ab��� Rk��.E�fO��(�+�z2�so8��"+:䲄n���R3���{����vv�C9���X�  ;&"P���"H fJ�L43��,U�0"!��s��%""��׽�v���ܰ� 2iS�	� ٨H��59���3#rH�Ęj0-Ň�,%+I�:Ki����h����jjj����:�9��a��,�}�c�$%1�"X���g��^f����u �絚�s��u3=v=Iպ<۔6��%o��~�[_N-(��^�����E��x��Xw���:�=EƳgpBM+��{���\K���`���6�i!�vDJ��U������V����TO��)�)�+]7)'�=�c�P���$�    IDAT{�n�Ny��?�͵z��i�0@$�J�����CuUt
��y�e�n�ȋ^�����|�H�e� ��Q�������)���Ҋ#WWU��ͽ�CD�{��N 	�����М˘9����|��.2��! `]KVt����³�{���<<����G���ի���'�x�;���_����3g���w�=\����^ظzuRN��GyO?�e���I�
-^̈́���0�0Q" �Y����uJ��:��h\�A �hU�b����PI�CU�Ĥ,��}%d7f?�������>/�3f�" ��!��";ǄUUmnnb����^���+�uQ"8��|�jU��,#�s�l 1�T�#�\�gB@�|��[�ؘQn������V  `"M,� ��>ëݻ8�mTu��� h &h�jͷ-T�5l-2�,�v�q�n���� -1ü�L�gEz���z!�ץ,���2��h����X��cϾVW���ξo��>���@<<Z�>�ި��ze9��v�';r��`-����n��`��aoW��kh������3<��|�k��n's"%�I�r��<[>y,�u�ݞ�~qi���+�]���yc��h`��ͳL��ڝm�������I����p8��W�:-�>�``���~ ��|�nmm�nl���N#��r�,�ɴ>s�����_��_����?����[_�������k�xt���j]�s�3?�:e��1:��$����y"$�&��m�� ; 0 (�z4�V" �Ucc`J`uY�Ubc0�(��$��  R]����uC��;Q�8˲��Ќ��,�0�����`�_^Ya�ƓI��:��юĨ1��* �1�P�q7���-�F��S����w�~kss�teW�M�f�䘝�Ԥ&�1;�C"b���Q5Sk�T!�Yr�
��4�)U�ZM�REL�W�n$��瘏K�XY��������]���]�־�+�;վ�o��L��}�#��v#ђ"�:���6Ksxt���|&QY�Y�Y��(�,C%Dd�QjTCBpY��|���K�+�o?5Z�J/������~���<�l��y����$J0@�PV�:�)�!p�(+ jj.T]hH����K�/b�e�II89] ��WbW�^��+�'n��ٟ������>��~�+_}�G��?��w�s������*Ǻ,��Ņ<���竪��q�@~nBΖC ��0��Ǵ1�&���L�ɴ�j @p������ΥX ��WQ��S��h�Ab,j�ܪ����203�1�����n �O���L'�͝��d<��ʲ,AxF Ȝ���qkNǨ��Z�E J$��|b����7C.�Z�Z�Y���[vӍ �rzXz�DD$fU�jF�����)l|+~yK�����@plS���d͇�$X35�6�tނ|5�"����*�� L��&;�<�w�CFCD��# ("r����=���t���]XA���o�}���~�C��k������ۊ��P��f ��S`��)6�Q":�:�"bD�Dŗ~j �؀ �!ϼ��������u�O<�ę��p��p�������n�v}���Wο�;�q4
�g���'�~�x_d��Z?/IO�T&!�) ���Q˵����UR���D%�ܹ��jDD�:t`�,6D���5�"�Ĥ���:ABG�@�� pH*Zt���� ��l\\X�u�,˶����Tb�̬E�nn�{� ���Ȝ �C�Ti�����s�\I
�xn}'��O-1�&�K-'��!قhfHj�0Q�"�!�F5T�*j�][׊{���.lq��~��f�D��A��C������?��o�<ӹ����e9�X�����{���(�g��H�����z��#Td��jjf)�(;�e�Ȓ��<�D��/���������N�Z���by�!b��I+��$C D ��DD��%��X[� ���3@1�2D:h_�h<�Z�H�������s�p8��\[^Z���>zt�,�EQlmm!c��.w��z4ĝ����|���?�����r�(ꍹe��/�D�:�(  9�wY���T�O�D��sQ��(��Z5Ӻ������Mqj��NpHUU�̱#&v<��eYx����ѣ�aY��ɸO�zZMK�q;�8�1�2bn��1yfv�9 PC�����S
�����j��tw"����ԗk�"�i���քeh
�ں�&cT���&Qc�(&AU%�
j)�ȒI.��!����M��L��B�w��,���M`�&T""٫*�f{���7��M��N��&�����68c�='  0Ef@l܇5���{p}�^��<�5�|��_��W����ĝw�yu�rV�Db�7p.3$A�]��A	!T �> ��ڢdM�=�1c��s��9�T�\�y�Ó��D&�.�j��Ȫ�}gΜ�|���p��G>�����c[[[��W��?zte��"�!�É�T ��?����_��Π+L�t~Z��G��(��P	@	QH aⁱ��c�ET���IA��	���',Ӟ`�U4��jH"�ё��(! �!D5H��
#$W6;�籰�f�eE�N֙���$TeYnmm�u��3�T�h�R�쟓�I�GHp<Ɉ�u�If��3���S�
$�/��!}�M��4�jh>���2Y�$����4P^mPR���<L��8�6�L8�5��!��o���q>{c�ޘy�
�_��w�o?��`��NT�4��=iӻZ�(m�^O���	�f Q����v]�	�l.�����DVj7�˭<��VΟ?bi�#����V?��ϟ���S���p�|'��$v;�]� �):�(dE��~b2��ڴ,�gj�ǌ@c�����j��S3��ϋhmo�����b��K/�x��;��������Z\\���β���:uJ5Y9r�ꥪ�..�
�k���p����]������LF` �@0�� �!�:j�ed ��g�M�%��;��<��[�[{_Ѝn4v��H��2�E���Dȣ%l���?��c��v��1�|�|O�C�Z8�F��Q#�$��@� �h���{�������yn�z[�dgT4
���z�ɓ��������]AU���Uœܐ���p�P6�f��\+ ڦ!�@�&���RfIl:*R6��|S�����"
[AenlUe��U�5ӱJ(���u���� QJI��"U%UP�  Z��)1R�eK"S���#@�����  ,�F�;�0��';A5eI\��w���+��Ԡ�l�N�$����w�)�.���o���m?��)���_S�1y���"4ET5���I;�FY���N^΅����yϐ7�OX=Q�_{����07m*����M���X�5!�����x�x���4D& f(`&1���AiA��GP��?�y ��׿~�ڵC�NPU������e�*���E��u]oll9|���s��n��vbYR�T`(b�1��t�Lc,�Ą	�\�k��03�0?�����|csk����eX�y�ȑ#�y�G��W^YY�(��w������|�����CD0:y������Vn������>�)g�r��5`60R������h��
Cݾ� ���h���@@ 43A0����ɷ
 f��*�g��:��TU���2f� Ԑ�3���I���� �H)��,CQŲ���N�(�d�3���Ep&���<�P �*6Ɉx
 ��@�'_p�(3��;�I���0�PE�TTŢH� =���0�}E5eB��bW�AG
�K�k�M�$o��rGv�P��j���I;XOW�}����Z���	��5}_l��g�Sē���/���a��4bv�|@$�.N?�[�]\Ym͜�}o :���=\�YD�F$PK�z���e��pN�g�JE���B�<���O|��?��7��w�~wmc���1FU�E��v��n�ӉEDYx07{�ԩCG�Ģ�(�@���1;;������I�X8W�A���u�^�v�ı�p�����t�ȑ#+7WN�8y����������S��seY6?��#M����珟8��hkkt���׾���ó[#=v�ȕ�W������r��6�	�B ����>��"��,�U"2�&eʷ[�墕�%�4>݋�jbaI�8�ܭ���mY���  3K���Q,;1eѩ�n��������b���}�!��D)�%��3"Q���A�� �7Y��ܛ����Y�4u];�_;��7tz�%��/����!� )S�f	LP���ePeTC31Q��/������X��{�v�N����x�}{W�� D�v[��	:l�u�>�7���#" z�O��!�����I���Z��ٙɔ�mu�(|� b��)�d�RU�O<��O?���K�u�nY�@h��@�4� `f~�K��"�>}��ӡ���Bc��N՟��⋜RQĢ��(B��+k_c���z��0{s�fYK�������9{Z��/ݸ��QS���@٩�����Dt���.<����?w��Ѳ��[���_���M�%z�ٍ���ָ��V���������H�$n�ȝ�t�A3a
y"aRjm��ӫ��E��̉�}d�"̵G`����$nD 0R� �
d�8�E�<:y@��)�")�!(!U(��u��Z.����-�^K3�LO[D�EXB��(냤�*��hֽT0M�KQɫI�Lu$��iD��R�b�̒��^ѼEL�Ovˈ�.�}��w���v�g}P�;�j�y[A�]c{s�Q� �t��W=�ͥB�$��e ��D��NU�`�(77C���\�������?��tƩ�,X�����ͥ�K׮�ͨ?;���~miIs���L!PA1�Z\�y�瞛��ժ��D�S�IF��� ��ʀ��i�o��=���}�?�s?���|�̙�_���tz��}��9{���?|����<����|�ٳ��k_��?��2��)����̍��Z�M�[[�QSƪ��u�R
1`�^�8L�]'mU51�s4�;��g����e6p��ے��f"��D� �v��~5D�Y�H�"������0B���"pۉq{��s�EQ11�"�[E�%5��vC!���\����BNuh�^���EX���0�:�Օ�U�DT9K����&�,(־���c��ݳ��-�ώ��-��7����}�A@�,0����E����0�L�O������4�HdP�@@KׯS���	 "df�I^+��UX� F�1|�~�?|�+�׏]x䣟��p<n�VN[õ�^[[^��X��sk��K7������D������/}�^[�?yj��R8���Q5tB�\�p�#@=�~p���F Vo���g�}��G��׾�����k_{�����m�������ډam!T'��\^Y���~�O��܅?���c�ӉSǯ��h���ot:U(l����a��#SQi�ę6|�'�@EW��b�S�в��:����E7!pRI��:%.�j��g�*4/M��և�b� ���Tq NC)�^e~LP=��N\B8����-���P�d����S~W��� �B��u
9���S  c3u�,��S��Kf
��#E�Vi����Z)Bl���{��]i�V|�.�!c|�f���^/1	 �%�wMd��o�v��>�qyy9b�Դ]O�ɚ veM[UUE�Z^Y����\�(�����굫�OSԆ��Օ��_[]�ީ�ӧO�?��ﭬ��on�{���C���67�^z�%�z���]�Y��y�͐p}}�,ʪ(776�ݞ���^|����_�|���3 ������9���z�_��_ࡇ��O����ͺa\�-�o�\]��CB� 0�����85:�W�j�9%SiӋfm���L �y,�m�R�&�)�s�HJ)q�$S�	���-�I�X�NҰ4�,&
Y�Y���E���!VU��v��nѩB8p=�&�eS�}�`_� !�h�a��x�4���",,��񱊦����G�xå�rn�(p������]Dݳ{�Smw�����3/��/�t{N4�_S6���d�o�eN��
w}�wb ��׈ ʲ�6K���Rȴ}�[_�[2�um���~��~��k���jmmm0����K7�l��vˢ�PI4%�Ee��bY��N��=7�珟X��433�U�4^[�u��B���[7oVU5z��2Ƶ��Ë��"���nll�������nܸaj��42?���V3������Ç�p�7�7(�ןz�Xmye�?�'���pum�6 ���:��N�����qJ",`<釟������
�k���&�^U%՚XR�u��4u_��30�`J蠭X$�&IJ 
j	��!��(B��x�vؓ}Q��!�D���Z�� 331�DD�C�!F�Lb�"�x��̹ԜS͹VU'"P�	%:�j���k�.�t�����x�i��ď���)��y�侨׻��κ�կ��w,��kw��|=�>滺ox}} Xd���֝&43V��z��<��C�ϝ��/~��W_��_������-��xmu��>�)Ţ(b�  Ɋ"VUu���NYz}��!F�i�S[����n���+�'N�6��>���˯�K�.��ѣG�_��0����y������N�"fP�u���n����;333����/|�/���w����L�xxn�%��l�o����B�[..,���
�S���j�#����6���)�v����x���҈�����z{����ʜ#bcA�*�#xl**M54��RӸcJMj�&����3�B���q̈j�j^�ei���B�^����CY�e�=��0qr;t �*{"6�=�\�U6Ie�_َ;EAD�U�W7���� �����y7Θ��-����v	�M^Ӷw�w� LI���v)G�ma�
d��>+"L���Jq\)x��;)�p��>�L��{I��N�T���0�_�e6�i�!�~%�p�!"!� DJ���~�b�j�""�A��  ��`�h^2$53�N�Xd8}������+�^���MF�QYv����ϝ?wnm}}ue�Lʪ�x�G+7��)��Zp�O�XDUk�G�4Ƃ�*5̀�[CKz���n,=�ޟ��3�;����7W���k�/�jj�N,.>���Wo���"��JQ������̠���������=|�k���뫫/���`fˢ,
0h{�$��A��u�y�6�,���C� )q��fN��u���z�Ռ��x$�DM����DHH�A��db��ݞt{}3@AA"0��q�9�AYD�c  a�1�H�:�8E �tdQH�X��Y��"�3�R(c�����Rᚧ��������v:�̤k�� p�< SeUVQ !U�d**�ܨ�j��,EE����Ts��ǴS�@���
���	�wN/ퟷ�"w�
�U!�F�~׾l�I��jr<�k��.w��T�VQd�9�؄�&sY�`9WdoT�r�ދ� ��<2}UZ�&0pLTPw]��aM��6Cg�^�g�=n��u�?��N��J��^�}���+?�v`���vw�*Y�M�:l�0%Թ�Y��=�{йh|����u�) D���z#g��1l��v�� �q�x���m�}�o�d/�'��������У�:|�LU���Z&�1���=s)��R���t4^�|�(�C�[����g��~��Y^Zf�CGO;~�*�Օ�&�eY�T_�z���@!0R����a{~���(E�EQTGO�
�����Ï?����C�N�G_��z�N��To��>~��飚�ꔜt4�˪"��pkn�7�v�ݗ^z���}����8 ���nF,h (�'�I<n ��UU�PUY�<u�,)%�i�q���7��I�,��>�����@�@�Q5��n(�^`���R��Xx����~akk �HD�YBYH�aY���|��m  Dʢ���b�*%��(�B 0h)m�D&�EPͅM�	�Ȝ�Q���JML�e�S45դ"&,�Dr�$��    IDAT6�D��#NͮTDMA��w��w����;�5����A�/w�0�c"���Oډu��
�~O8��p��N����N���=N�|�Q�,a��p�݁3�~���{�}���̮����g��ũ;�w���.M*��D}���5�cӵ��ֲ��D �#��s�����:�H���~��y�B�����
����E�R�"�8q�̙3����?��k/�4�p���/���9|�hAafff03���������q8u:�n���v�E7��5��"F?0O�qJu]�F���pcs���ixan�S��{����Ë�����{G-�G[7n\���Y�y���B53�t:,5�^�JuzO>��ͥ���K �s]U�]��}����d<���dʜ8%3�M�;o���� lK��b����@yy&�c!b��Ұ'v�TZ��M�k,�!	B�$��)�X��,��2�C�!'��X�"�̓�s&'�!ĸ7U���j+�-DX��9����r���:ՁI2af�$�¢�<��[x�)l�h�{���v�� ����vP=r��f9=��l���~�;.������[hwad9�v6��\���ڳm3��oUd��vE��h ����|�[Y]��5:i>�i�1�#��X�ʀ��&�M,b���t;/����˗�?��Onl�gfO>������>fVn��A��R������iI��5��$,�M�
!" a�c�E(ʚU���\���>�3�y��z���W.�r�� �Ѓ�o���'~�!5MUTEQ4,�z|���իKf��tD���=�����cE�i���C�bE(�NG̼Ւ�F��`f,�`��a�j��RD8��R�4�x��:%�Rj�T\�:��0'}0FU�ǉ��u�N'e��ge��NS7H��Bf[�[�c�8Ea���g�@M�ɘwh�-DD����i�*��eI�Ca� �R�aj�(8.�p2Js9��7y|)�&.��ο�1%���y�Ȫ�"�3f����L�g**�3v8�q܁Y��nY����߾_{�#K�/.�Y�8�;9�]��rݭ���c���=��E��Y��������=ܡ���/���AΒ���g��,�K����s�D� 1RQb��>����� H��o�^��vV��y�!�eQ��U����ј�x��;��g���,Q��H؟�_�zm��(pj�Y�F��" �5�L7X{������k��ٹ��F���_[]����]���K�����^z��g���o=���R�ci���2�K@%֭�P�[J����:�~����3�<s���G�Ϋ��͵HT�ոi�N�YЀ�&�Z� (Pp� �� ���IRӤ���4")5)�pbNb�e0T$������La4�"F!vʢS���0t����LA5F�� ��V����3����"n�@�H@B$!"���iQD��H�� ���"aNM=63Es�/f�N�(���s�&�f`bj �M��&ʦ��,%eVaUffQN%KPQe33ˤǹ&�����'b��?)�2WwNĻ����|�8KT��®;h��=;n�ݧ:2e~Vf^� QA%��cͺ��& B33����!Do��K?���P(" 6�!�^�)4�:%.����.\|�GO����>���4B��՛���/f��tb��&� @1��7WLF	���~�v��pE'%9�0���ͯ��o�[X����x�����K�^|T����fggϟ>���3�N7ˢSU=q����xnnn<���g?���x����?����#'�f(jeY�$ �@It�ȣ�y���c,��(b�E�)�FY�4�Z�7����,c�� i�	��� 
!�X @$$Bo�P3sC?6V)cY�Qh�&�)�2u�W gi�IoC{�m
Ң�**�H����Ĳ���-8Χ��f�*ޟ*�d & lf�	�U�&Vv��)�$��Zf�1�,"ho���f����r��O��Xv_�K�̱w����(:0��� 4�.Y��4sv�\�@�P��R'��1�a��B�*#���_x`��5��1���gbD��� *P�HHN	�S��?|a�ڵ�ytc8Z���ɳ! TU�8���8M�hk�ni��4R7���˃�t��Y�-�؟�/ʲ?3���-,>|����߿p��CO�>��_����<y�:��Uop�箾��g?��3�Np��"��p���v���4M�@U�4�o��G�Q�Ѕ3���,&�n�I	� 01o��HA��h�F��=kP����cy���TYUţ'ɹ�"-) �P�������V�N����)��=Q4B4Ӏ8��t���b)����܌�#��&���ۢ�!�����0U��(���EO�6u-*����x��ǲ�m �'g !O@�z'��Ksj03I���L٘UEY\��=�b&���Mm
�=]<��b�+���A�I�,`*@��|�3
?i��LTK�������,'(�]3��'����}ebv���0ۧ��eN������P�   j�Piy�������:ع�\ˢ,�r��[���u:�N@��x���=Vo�����p����7B������+�7nܘ��]\8<�CȻv�E��T� � JD\[_ԭ��h4~�����/|��?��<u澢�9r��7�����>���=��{~�c����8zh~v�/	UT������Ng<��Ϩ����/�ҧ�z�/��#����(t'�QS7̊0�;yu�Z �>W(R,)��(CQ�e�,˲S��jb�n���VUUv���~�L� �r@C25WE��iXB�t:�n��̴i�䂗"\��p8��MӘ)"aTEQ�UUM�"�WUIN,*�"Q��\���43_%hM&)>�������S*'�Ɣ���̒4��$V���Ҵ���D>w0����d�����go�vD�^��^x��V�����]SL�<��Ld��"���t�N ?�� ���]�=�L-��gb���[@w"��t��ap��ߎh3'-��b@$$*0D#�=�У�2�����]��f��.�#(B$ 05��� ��N��^~��7n�8~b~qn4�<}�8sZZ�����H[�[�h����z4l�Z8����Q��@������2�}@����ڕ��*_���^�������s��ɧ����N���_�v�z�;���Cǎ�����1qYD7�RQ�
0��*Np03��u=~��W��칳0ճs���:��FD��8��Fm �#bw'��I���
6Ƚ�.��b�rͲ(��(b�&	��n�p�ۯ�ݪ���EQV�I�f3 �̬i
h�����E�ڧZ D�@�`ޮ�͕)����EQ  7���E`���~^oTS�p�47���*��2���FgRf�Jn���$��򤋰�rJ��uZ�|��1���������-�,���6S����a�Ƕc�S���+a��mȥ��NG�5۽�����y~˾❉,�Oxmr�_��C�'�'"�p����#۟�=���w8D�q�mg���M�v��*�wAL���0�o�Y�>����1h�`�T���������Av��|vӇ8��� ��o0k~��a1�e4�����F�����i���F#f6SfeIu��u��̍
O�-޽'�&#�n\��D�(��������'O?u�����gϞ�ۧ�6���_��/���O���+h<���|h�[�"7�����8T����Q��fj��j��&�Ѱ��:t�����6M�D(�YA����ܪy���Qe5@R�M��QQ4�����t�9���T���u��#`EQ������5���B (�*� z�E�\��9�}K�n���:�RSu*TH)��Z�4��	�9x1���`[��4@�L]�T\9�Y�M��2)�4�إ���@�������dz=�Y����s�ou�u&����6Y��8�v�{�e��������-���{����w�Yns�xk���ո-g9��u�z?Gu���l�YN��O�T� `Z�R[b�=���8K  �}� 

a�ȱ�ͭ�⓪`�wag��	�� ��S�a���eQP��wum����ث��>Eh)5�I�z(��Xa��7MS��zd"�l* J�1Q��)5��1��T���ijx4�W66�/���?�?���W��O��/���L��O���z�ѦjS ���x �a$�d�x1ӣǏ��������������ajdTצ����)�h��&�L˚�R� �L%����ڦ���CRp{
1�׮_S�Xv������e��! D��"�T���PC�L)��SC@�\������ �b�L ��=5���hל����N���b�f��=���䴽��4NV"*I9Y&xe�$��I���@���6�񏾀ێ]n]��u�	w��=g�N:���:ˌ��o{W:��݋)}]s��7����ZV�  u�byy@�� a�}���Bs�'��w��s�~����SO��p\7�1 ��!�B�1�0n�ψ(� ��xO<��|��͛+��Y3 �z�������������w���+��W~�駟f�n�S��?��������ٹ���zUUӓ��)���:t����k׮]�x���� �H23##3�"V{�����C(�"��N�Zv��C�(�N�)W?���]��6���*����&�Ц��)���,RO�ɘ5��Ksۢ/�&Ī���m�=)f�f�N7�wT�d¢�e&�Y�2G�*��(3kǾ��I�*�(��&Qvj�l�-Y��Z�w\U��ݳ��❧Ioe��ڭ�.�g�@
d�YS3B��;{D��u�;=��G��x���՝߁;��r�@T��Q7�o.��-�����m!�4M����;� C
E�f�Ï>6X\��r=������" 2SD�1��(:U=Z�@0b֔T\g�T���cb�
����x%�a����O>�������?�/����������7͙ӧ���5T�_Z��٥���D?�으�������z���Lš�����pk+%����n��S���B q�B�E�)%Q-�2�e(�X���@� ���$!� �C��D�l�+ ��^��vX���T�41`@�u�=^ 
ADLT�DE�PY��43����2���)��*���8����P��ЕԜ�N�[DT�EK�A��Y��H�Yڬl{�d ���t�4-�3]��%6䎔��������myk�������{"�B@w�����Ù���>Kk�m�lջ�G,�uc�_z��8$��s���@{�k��6ę���%�"P����[.�=>��m�c3��@��(
�,�Ԥ�x��� KW� F��TVU��t:s��Ņ�����[��[���?���~uyu���/?���~��9��ۏ>���pt����ZMHHugp�����C �����?����8q2p�C���a�]}�.b�b�� ��BQ��3����MT4���4
�I�L<i�;Y (
���Q �|B��EQD��Z���){�V� �1�9-��s���2��6M���R���(� ����@���ߟv�6k�,.��*9���)EDR�RRN�X����ݳ{v���9˃��=�}nSh+  @sn�4%��n���ՙ��<��~( 
��Q ����S� m`��I���� fE�ngss�������(V�]��4׏�N(,��q���/��H�S]�f6�'�s>�R7<f�@ask}�ȕ�+�]_���#�ȿ�����������w����z���gO]��3�\�S�n�K7���4DPD"4�fCD2$�#���F���EQ�����m�����&]��R#T��@�BQ��"1D�fEDf��Ҩ�z� �E�*�';MāC�N1T!��$*1ƔR�c���f� �{[
a{}�Ǐ��I̔Y���hb�&�`Y��A� �Цtm��0�ؔ-s�;:�Ɣ�$e�ʉؖ������w_,�Κ��Z��;��zFd��$���lg��;v2�|�����=u���ܾg��d<ȏ�}��N���;M���ԛ3\��˭�N쾳F�h	pE"�F�^wk}# Y���G��������E�����υ��F""���Q��"̢"����-0��&e<0"�ҥK�n\_��h�����ps�Ī8w���#���g~�����7�׿^<�x���K�.�_�PV�[�>auE,���Mk<AJ�]�M-���L���>����&I4RˌCY��Ŵ���F$5SNҤ���K�Oߩ���9t���=�ѷ�c613Ua�P��;UyK�hf�F�{#3sue@��,�,��%�0����sf��� �D@�&����7��b��o��"��R3����g��,����}�� D�4�n�6�"ﳯ)��MϘ�D���e��@���M��йh���DO�Ѥp��Zh˖y���d�Ͷ�=�v��h`���Y;$$�W/�""���D@cD�ՙ�g���3� ZV�������@��и*�ȢI�U(��"6�����!���' 0C2
��b�H!��*�U˂�����bE��o~+T��<��7����C���+�����K/���������_f����ø�!
N,ׯ�?y��%0��[�flf���F�1o��Bp}�\��5@��I���! �������&��I��̐�qO4�H��nZ���sVE�C� �F�Ӟf��,N#��j ��"h�d@ REo�`�1�V������$5�"�	��)?"����=Cm���l��"*�~���v�U�ET$�(�C,���vD��[Μ�����o���3$/5nk��t�����8��~m2���'�,�68a�(~�x=5C��x���1�N��m<�m�v�x,S���l�m{� �~��m�r:��q����;y"�$������M	�d�c@���-����Z���[���ɥ$D�\S�~�zgF��L};�;"K�P�(Ke�P����g��<DDk�n�yȜ��&;Z�@ʲ`e�XH��5Z&�b"��i�1��7�f��N�4�ШVJbH�hȟ��_��|�'��{��{��g/_��}�ҥ˃^�$�>����=x��ǫ��aUa�����ؚ�*�qS�*�rG o�$���!7-���P�~S(��5��Lsd��N�u�TsbI���*`AD���AXD���γ
J1REl)^=��dd��=�Ն�"0_V3c��Yh�m1c��̔9�&������$fSEs%5Q��*&`����Rˊ΍��4&:=��+X�1��߳��YN�Ч��A�Ak��}g�Q������Չ 3�y�D����V\}��cO>C$"� ����+ܦh(��'m/lrƑH)P��M'!�^��!!"+'N�oC0�W���++kE��U�WUU����.tO~���7�����O�/̿t��^{m<>��#/|�ٓ��,;�as������ͯ�,��	�E����1��)P]�h2#xn�B��9�K���!�޺9�cz��S�TsbNl�B��Bj��ʢ;+�9W�K�vBc��T��s��6Y�%�[mYX D"QI��c��0g�P�A�)^U	Bp����L>W1u�h`ae�%�������U������n��F�-���:�y��}�|o����S{������M�M�Ɣ��ǽ�����[x'+���zNw;;"K7�!��X�v�>����%o��������EQt:��i<	@SA��"���$Ӛ#��L��B����S^FJ� B���A$a����)��@���Ã���A_D�sZ^��n����m��Vw��?�'�v���}�ÿ��������ǖ���n���-���ѓ����O~�د���V�ts�UJ�eo�0 ���F��fv;�";��6���ۖ�I\g�4�$��4)q���Us���Ք�YLTTI4 �/G&O����Ԓ�,��������t���eU@F����Z��Gz    IDATE1�5�V�=ի�����,��)���"��eٸ�e���������ݳ=��:�.!���)�tژC-.��0 ��(j&�jE ��e����+�PC/tM���|"�ѡ ɡ�ÃI㦚�pM@�^��g~i�믥���[V�	�P�(�	�����g%)#��݉�t���~`����������j�+@���i��E"�b#QD�$	B8y��N�7۟��-Ν8��1�����S���/^8�@�[�Aof0�v-�腋0�����?����:���m`35����UIM�����w^��Fp�% T�VY#�Y����3۵t�"ɞ�SJ\kb׳R�AO	DˢlX�%�4�ib�`�c������"F�q�rQ�"PbF�H���A2Ru�glug�I���ꕾATLMMDK�ǒmǘQ�2s�QPTM��4�(���ݩ��	Ԁljt�ň���Ҟ�1�������������O���,'}� �4��9�z�~g�������cs��v�S5C���Nl�}���r�/Z@?��}*�E"�NO��vh��jM�� �u��(`(��6`J�H�IU]ICD1Ф�9꺮�F��N�����6?����~nu}��G���r���kW.��ҋ>�ă.���>{��S�~��>{�����o�������=���C
ᤂ6�l����m�OH�xx�j槝q��,'��x���42��d�h�u����8ML��UX8ՉkH! @ C�E���4C�+'�V�<��$s֚	����c.n��'�U�d,�ko�$Bq����`JD-���kO
�Z�eEMՔE�A�n獺���={�v�:KD����JÉ�$4%�L�I`ʧNM�'���4;��T{�N4����YAL���ƍ�h�
E��x4��,o�)�%���V��m7���P
��"��!�ت�Y�OI�I{b�����lme�B��j��7b��`~~qf�h�Щ@t����������s��X]���,�2%U��`V�bicc�����췞{�ɇ.,:2�\�UeQP]7�J�q�㮳V�4�P��fj��<̖TX$�i��d�i�=�YXG��HRVs�m�&f��H���)SdB"?3srv !�ښ(�f�)UP��A@U3�ʚY�4���EU��)����ʍǔ�b����&~���R�̉�-;x�OY�N͌3���Jc��I�ݳ{vG��Jy�����T�2����ﶻ�Y�5�[�enD0`��܁M��)O99NG4�G��T�l��t��i��v�Ks�,w�9�		M!  ���N�!E�(�P�tp�v3c�,n !D����RJ���P���PX�Ƽu庅�?������,�\y����:�87����K��ӟ��?��g�ɯ���8����c:������[Vz��z�<NV�ĬF!_a���o��s�fU��9����l
 l`f~�:U�����&b��)+5
��+$gRC�dX�wb$���DC̡-�Hj����e�/%ny �7c�� 3Mb���f��˨��rbM,��< �-Ƿ�w�.�ݺFO��EB�"p�XW�lk�8YCݳ��l�P�ٯ=I�v� of�������-�mw��`/�꭭u*�ݎMB��<  �Z��IK�G�������~oK�[����7YR�Bb�'5R3Q��<�O?�����GQ���E��(��n���2�E��OΙ��ds�U�ӱfb��T���x��"�   �$*��Df�
'�&, ������v�íN, `aa���}箭��3�y���:壏��;3��5�����K/�=w�ŋ/.��ԇ����_?5?3���b��:i�H�A�[Y(��>�V��<u ��;-��!�Qno���qMD�Sbf�I"��@��g �ل�QN,)%�u�J����^
&���� !  Q0G�zU@M�T(� �vVCQPT�Ƅ�x��bn���! �)Y;&]1� J �)gk�IU'��;��C����w�ێ�P��I�M��"���n��OAհ���x� ��A���������P��L͖a�wv�j��<{�#�7�*��ӵ�wSdyk#��ĿM&"���B�`f�IM �(���R���Ɯ�`��(��= r6;{�Mx9@�H%P��%�ve����(P!�d�BҲM����D�)�`�___/˲i�����Օ�#G���33��~��_���~y��ӛE���_��>��O��G�?u��������G���gff��������x}c8���S��m��V��i���>f `��MtI�`�� 5M�~J�������y�ᔘ��M�J��,��h�Pd`h��9%ijn��8�� BN�!P5���Љ2��Ū�?=)** &����j�=nd��%g��RL45�6��mA�X���R-��������$͈ZU˔Ϛ� �P��={�'�ܧKg��2��f�]����㝲w���m�TD ���v0B@�k�שY:
sj�{�s[c�Z�MC%�D�Ķ��r�+W.#bQ�'��V-�����\Ivvo����PXh�э�FO/��L������F�����/�"ٖh[>6}L����Ciq����}+Ԛ�^D��?�x/_VV�PU@ȯ�^�%�w��Ze���,�D�\��������ɋh
�E8�:TE@��
;�NQ��`P�e)"�Л��k����M��Y��Ϝy���߸vcY�?���ٹ��O�~����>��O~�SDߙ�y�/]�������'O=~��+7>���|�đ���E��[5�f9g'�SH�3 f��pll���B�)$&�B��1�R!c]�\پ�&�Qg�zW�P�)U>V���\�M��N�!2��1���*3����FGs���`]y�0�X��,E�E�HN��X����͒r��FN��Q;1���
 2�SN���V���m����(u��,�=����-�EwwE{t�'��A�UFѣC>EU��)�]� EQ�kH��ȴ��y�k�xŤC��i?5���u�~H�{�}�� $"Dt�Q=�U���v������R��]__�����RU���6������7_{��w��ĉ'R�n�\\X���������Ƶ+�O��t|��,=~������ݢwdy}0�pt}�_�����ԘsD@U�R�
�ՂX������l���ĉR�d��)��D!�)Km$�P��P�+��	Z��;�B�10S��SP!1F�	<[hBlYe9��>-G7��H��*-�G����/QD��	1��H隉��>��z��
�04b�SL1���Z������A��b8��R�00Xq��6���r��|s�%��y��d��ݡ�U�a]}1�a��!�Eq���իW��<xqjE#� �$^n1�l�B�YN��� �L��&��âS8��8�B�Ϭ=��P���2"0���-��92�w�NX��ٷ���'�~u����o�=1K����u�3��?:��S7o������Ͽ����_}y�g�YZ냦�����Y<3s���Z��n��9	�DD�t$_	$Q`!dP"!H�L��D)�cL�2.r�^��&Z�"J}WT1S�"
#�,-ic��#�=�t�(�>���0����(�@A�A�نg�>�D�b��3�@�T��*)�<c�	=Yv73�$�	��0<_ۧco��:�pb�I��7xǢ�u �Z���!�,��D2�����T�Ma��ܪ\���D�Ŋ/�\��E6�B=�g��E�[h������35����t
眊�M� ��������B�_t������ꊊ�YZ���/���WV�ੳO����N!J���9s�)D�ꫯ���|��+�ڙ9~�����0��� ��QU��z��D��T��H.E�A�
'�,�L�����D�8Fb��`S�h_4i�D���0aS��u'd�-f,�bN&6���$��g�\ǩ��V�E��1qJB���)p��b���|Z�HR����+s������8O1��в��o��Ъ�Ւ�w�a<��æ�̢(� ��]Ṉ��|��G����8���5'�ա;4�n�^�m�9W�G���z�Fݾ�<rrG3�:�:�.Ċ�9&aAD_8fp
�-�$��L+m K�b�wVV��գ�N�{ᥥ��kW�����X�����~��?x��o�ˍ�_y��?y�������cnvn}��wfz7oޜ�y5^K�l$$�A�{Ȋ� Ŭ b>ON��*�X�X�XU��b5���BH�2GA�r���S�E�|��LĊ䙩�,mlR�Bd:�B$�UT�YtԾ��ȣ5#(
(03Q�)������
@̪Ժ��8.6��e���#��O�d#�[�uZ:������.F�V���e�)�!f��aG�����MB��T����t�/��A��f�-�ι��bZͦ�\��[�2���;���6���?M M��8č����yf��zkkks�s��^{��+�/�Y^���WV��<yjnn�;��Π?P����3�O�=��͛7/_�|��ţ�/_~���o\����_|t��3��X�T��&N���(��)���GR�cJ�#q$�d�'J�(T� u�ϖφ��p1>�]gfN��MDI��S!�Dz�"�F���F�g��4)A��=,���aQ �1��b��2��I�lپ�l�w}��b��Ů-�H�U��G�K�*�M�p��Ǣ� ��*CM��^UDD����06�д�7��C��b�h䝞���: �" F��:�|�"�-���������v5�2�+l+�u5 xD�^�C�Vj	
�`|�*�މ�sjJm�`'b�қ7o�e��9�.�)�:t�9r�BZ8�=�2��f��(zW/_�9����/����׿�����_���������/���wgΝ�����<u\�tiq���x�ӟ��Dw~}��_/�Td�h%!��2���0��7%+�'"J�"QJ�1Q 
)E�(���D"&#�ì���k`�qE�:��c����Q�Ab�B��A�IY��%�X~�
���E��5�)���� �J���NY���r�Ԃ�,�j�B`�
(�X��������n�<[�.�������h�=�Z���Ǵ����5Qu�^���d'u�;��W��C�̾9l�E:"���g����q���Ťg���v����|�f��b�>�-���u�����f���j�Mw=����\G
 �7��U�r��(��O[��}�>�rj��k�C�=�s�=8�ʪ��0� �굫�^�F�p8��<;yQmF��)�7�'�b������9�f�Z��6�)Ò��M�Ӄ������?�я�;��G��̜:u�����s�������ϟ�嗜s_}�w�w���.]\�}���^������ju}ca�H}Кn^2W�����
�	'�HL��^���%�d�������SJ"�E�(���L�����EDY��Q�8&� �>�$���H���Y8r�.�(�aH���@�8%�d�t!U!d1�l2י�:9��=(SL�8�!�Y��y�"�<�Yx/=_��Pz��-y��w����ʲ<6?OY��rD�DD缚�r!�s^UM�IkJ��{��C��y���ښ$b6qjC���Z��p�Mcqq�={�w>�p���/����������O�>[Ez�7~��~�_����շ�8~��ܑW�՟�˧Ϝ{��CY����o����퍍A1#�N���3}.�\2�� N�O����&�2S�[�%
!TUˊBHl ������Xrvsf~���	ET�$u��1 Cr��q�Z�'#��l:�lC+�(+��*k-� �FMUEr�@4[��s�̴n�[g�0�m��c��� l͝O�i�>5\�����Y�nT[w�qXz���,w��7���e����L��%���WXD�E�S����^��)�)�_ׇ�?mW��7Y�nܲ�z�F�r�âSTU�̶���xߛ b{����۷_}��>�`i�����oN�8�G�߯����������O��fn^�A)�8q��W^����co�s�����ݥ�唒ѵS��DPE��>ҎS&fV b"���l��R1U!�`�DQ('�BͤS��)��;#a�$��)�Pr�4E��)(�cVNʄ���2)�Jd�����V�2+3��ݨdbbR�Q�L��iMDpW#���SL����n쳋mѡ������!
u���ԃ��u�������/ "~���
��,�w� ���u�}v�:�s�{燥$�Ҵ��93P�����Z�1[�����v�<xު���C�t �����%���?�O�}�鯽�?��?�������k��������+��믿~��UQ������·~x������'N��p��UQXE��B��H$��Mkb����di<�6"�� �j��JJ	���֨��6ec���HATIX(��*eJ+NQ(
�hD��UN)� \
��LlՓ�t8��
������j��*0�4(u�4���8��ab���帏�D���a�(;��Voes�`#�t{ii~~^v��� ��\���&:j�x��;+7oޤ�ԡ�II���wd-Y<����K��O��˿�K��/Ν}�w���������̳�޼y����O�<9�׮}8ؠ������?���W�D�o���/~�g�U����z MLfcفX��ea���D$Q
��@�L�$��$67�P2]h��B�8	�Z6e�E��7�(%&��*�S	B�"^��2�JX,MXTD��Hr���\�L�kE���4��U�x�M^�1��N0�F�b�)�β�Y@��U��eo�C ���w�U{��@q ��NY�{�"ƪpp�����y pE��A]7��.��EQ�Y�� �NM� wd�D1�oD��++�W�\!�N1�ejoDu�EP�b��IE�Cu���r�����s�^Y��O���|�ᇽ^�?�+U���s����}�I�gN�������333���ܹsw��:w��'�|��EьK���pbJ,�G���Ib�ak�!�5l��j2#ę�D�Dx'Se�!EM��J�Iͦ�J(1G�*I0�L�@�*-!N,s$J̉9���'a�oI�$�)i��H����$��O�)�!)�����^��@���z�=��s��<@䮸��m��j2�nݣeَiM�۫���6���{�^ؼ7�d����=0GJ�m+��O ������(n���^�Wּw��w�k�L�4g�6+�rM�9�Q=��:TVVW766
pݎ�t�P'�Ӆ�#���=yrvn��͛�ҟ����^<��s?�������o���p��7�\X\���O�3���o����#������A���/.}��>8{�))8R%Ue2Q��K%����ERl�,SJ̖"�)�K��)H
����F&b�)E�1IP�-9�KGT���E2A���OB�<(�PdV��4Q�,a&�6˒LђQLMruJC��@3[�	z:�ٌ�goޑG�!��,M����髦I4�|ѝ��u*c�!�|�p�Kn��aS@����>�`%�� �� �!Z�:�'�vo�@��O�9�j{�����-��Ͳ����ur�}�2K�&@3�u�z��#��G�ff��_����1[���QGkkr� 
��O��D�/��R �Gu ^ PP"������K��L/Q��K-R!�jw�I�"�g��H�7���ţ���ʲ�t���`p�/?�ĉ'�{�ţG����ϟ?��e����ί��m��/]���7߸u����0���/��b�DL$B�m��D��D)Q�9�R"K�!�D�c(C(S��*�!ƒCCE)�)&J1� H6�X���SP���X��|Υ�N�@��b�)Q2�D�Sd&a��H��n��H�,�%827Q�V4{�MZ2�<ZHWM	$��dv>[s���N��n�J8]������Z��peh\k�v�Ԅ&�	F�-6�ox�wIp�����T�&�h�̪�_�7Um�|쩫�Ƈu�n)���B�#�-�lu�Rp�!    IDATM��� ��3uՑ��n����������N<_ı�{c���y���]h���ܵ�청���j�^k�������I�7��U��i�J�\#�l酓|��	�1�P�����e����jY�EQ��$�s�6�>�#[��&Mv�� 3��S���1�����7]��ΥD���M��8IZ�"��_��7��X[[s�ݸ}KD��/,,����O>�$ \�����Z_Y>���QO;��_�2�p�ȱcG�}��W���o��_��/�����������.��H�(U���蕘2�D����e�:a4�c
!Ę��c��%���2G����c�V�"�aU�yD|V�J����(�����d6sMu>+���-hl0k���՝߲t�Ë��Au����"��<�	>���sP;;H�(}X7MNw�ײ'��3�����QEE�,�Ttz�qf�{�֭����'�����%��l3�: ��������  EV�"�w·P-��r\�~�έ�3�4�����9Pq��2l=���(����رŋWo�\^�H���s瞞?r��ٳW�\
!}���~����>�������N����ο�_��n������������Eo�W���[K��T�9	�(pJ��*��)�x%1%=��kCiH�*SLL!�*���2UU
U(+IA����2�)����涽��*�,��Q���,�1��}�rJ� ",D�ꆳں�4cG�߮��m��aO�=�s1#�N7��tĺ;���~C<а񈞥a����o��o?��]��AFGPW�=�^��<�2��C,��/��n������e��]�]�s�(
_���k�P�*�LU��W_0����t:��d�f�2��N����X�_H)-..���'O!�ŋ�<u������o|�?X���O���R�:ޝ={6�����������g�7?>������ҭ[���px���A���!D���@J,���@̜Li��l~�U���l���Xb��#WN"� I�c��Ҕ�jKҲ�mhh�JGQ`�D��F�U2��U��дd��i8�� �hY��#6�Q�Ƨ��`��L{�t:\ad�Ԗ��&� :�X'h9����.��q�c���6��D43e�:Uv�2���������U��Y��9���I���*:E��[�A���V�J� <�g�~����������"��ps�m`��K�E���] /���{}:��x���No�[t^~��\�������w��?�Cם��O~Ίes��ϟ;���W���<��٧~���z���p��	����-�*t��12+ XTRH�(Q̒X)gY�XU1F�1�*P�������R6�k���\(М����Tsb��X���h�0�ʀ¬,��D9�e*���z릷�O�d�8���m^2�J��}*�^��C��4�g	;0���߼�aw�:e���h�E�"�u_|{�`�D�EQ�ӹ�tGU;E��0vhS���뵽s�C��;�+�a╊#
�*ܾyc}m���2��CK�jV���Bǎ���XXX���/��t����g^��Wo�Y8r���?u���y��o���q�ﾻ֯�y���O=�対�o�C58qlqy���S8~���'f:�;��1FJ�*+�����ۭ�j��2���R\�SJ)
�cJ��8�q�)1�"�&U�I�J��� Ц;��AEF:`��V@�ZVՖ���zh��b�}��˃ϋ�;Fܪ����f.��x��ֶ��Ҷ��棰PJ�8Z8�p���DTt:*����5�UhM͡�P�9��Y�H�Tu����i=��.�`P^�|�Ν['�-,�����Y�cla�(�焠ΐ��9_U�O����ŗ_y��g�שּׁ�~��/��؉'�;���>��#J�׾�����?{�ie�����_���7�}���G���QVUD�XF`��\�ˤ̔(��Dđ�9�X�s�c�e
�bPՒ�D�����_E��򙚀�fQ3h�O�s �u��YP��1���x5��E����~��y�ڽ薾������[���ѡ*�(��z�̚�U�ݠa��pLDiqq�֭[�R�{B��㍈���Z�R�8�DwV���u���[7���#s�Z��"iRt�pnRn���B���鬯�w�nU�s��Z��ܳ��Z���/}����=w���mV<r�����+/�|�����t�������o}�?��/�~��SO���7�]��Z���̹�_|�13Ue 1��:!�`cŉ�D�a!&���Y�P�T	%�H��! %�YUYR"1����l��t����`#.�j�T��0(����׏�	�(���NM�	����!�%C��f���d��l{��Z@��;�s�5�`��˰��7б�$�L��+,W��4ڐ�E�����?�!h���g�S���X�� ����Flk����"9��?�����^��0�#v!��ќ����ہ�
�{a�QD���˫;��1�$J�wn__]]�u���
�]��ޱ�3'"N4 �9+�V���D��oܸQ��uz�"��_|��O�X\\�x��-N?y��K�������}	?��}@Q�g�9{���7n����}��S�Nu���*c�贬J!�JN��(sJє�,9V91s�ʘ��a�"'N��S0�)G{�D��4���C����[&��@=�JKX�	u橳�-���v������:�	׹=�ʄ���a���di5�N� ��$B�۟E�vg�,&�צ�kn��
Y+\� &�'�J0�j����������k��{��or�!��zL�צ\¦кJ�a��oN|��A" 9�bϳ�I��]�Ў��V|�w��.�0�H� @���y[1�v֜��0��[��B��L�cg��آ\@�X�ҥK����÷�n�X30�Ҿx@q���u�E RH�Ay�������t��f��cUU�s��#sʩ���T�Ng�ݲK�"����$"��r�֭3g���Ν��߼�T�O~����瞽p��W^{e���֝[<r�[��Ż�t:�O?y��G|��g�<YU�������(�A���B�0��Te�f���0s�DVޘBcj�E�P�Pq����@�]e{�jM����Ίw�A�C�H?���೉aS��;O
��ln��خ^�����f|c����u�"�JMh����]�N�����kϘu��ړ+��p���w��͉9�z������f}��޳�o��oW���F\�����];��r�Mj�*03S��T�έk�/^�~�J�puem~nvnv�ԩ(%����U�|�v��5* �Zڭ������W���W__<y��ů/<}��PUo���g�}z�ر�`ce��;���'��6����#Ǐ-޸q���?�0��Mﰪ�~�(��Y.n���P�bU�S(c)T)V�H��1��(VUXBl
U��~�)1+�*萓]E Uk��Mih[�#���'v�q`M9�=��ZOȤ5G������٦�#�Z�yƉ��0������aW٩e���r�6fz�K���	 ��؞�Vr����[��l~�I`}�w�H���u���y�y��熫���F�w߶����7���`�cSm~���Z�1�����m�![�	I�k1�Kt��IU@T�!��Q��\�t	��E��ޏ���><�P�ҙ`�s5�O^�{Jkkk��w�j������ޛ�Ut:�^2�d�k�g��c*�!^__���e�̩�������`c�\_���o,]��,��^_��r�ܳ�B���_=�������ү��tv��)ܹ}+Ve*��eJ�/!%��� q@��PQ+	Uee���}"�*�D!ƘX�s�c�uK�R禦r�r�ݙb�)��{Ry�W<�hTǺg�{uΤ@¦�bm�)0��PlUbH�Pc;5���Y�ǽ��WUTE<��*�Y�=�~�ڭ��^�㒈$qj���FY*�3o) "��$:@�Tb��� 1����鯭�y� �}�@fN�D���� �� ��f<�7(@MJ
" ��Q�A��t�/�������^�z�ӧ�����?���_�v��k/�������ξ��3]��������{޸ziqq�6Vn���:Us��*"
Q��LJ��zDX(�$aR�1�q�I���9*f�1aX�0"h>�%�,��mY���Lw nd�;��t:p>�RQ�� �{��	�M��׉#w�xO���G\.�zK�m����Z_<fy?;+�@T�=K��oS�PiW��m3x��,�"\t@(D�� ����_�W�M7pRJ�!�uB�-TU&N!��WW�W�x~fNEggf�&�u
�"SQ������A���|�{��Y��B����˗.������ϝ8�x��������?�����S'O�����?��z�>����
��ڝ[��)�+�o�,-*KJ�Sd"�DD�H�U-#��X�EQe&2><�)r�B�%"��������SL1E>X��_� ��0\�F����s�SQp�.�3Y�r�{�LUY�w}���ѡ����'��+�&�޻$Rd�9�SD'����d�/S��"�'�����b��������ƪ*/,�_�q#�����3��j�DB�t�����ڍ�ő�م�L���~�������;r|qqvn��_�v�ʑ#G�;���{��+W�VU�?vda~a���k��'O��z׮\���׮\Z\8��r��`c�p^$q�DA�,�'��2�h)BFЪʢ����*����<�v��;��&Y���~��Ǎ���s�:D���h\�5[x���a�	05i�{��?X��9Ipg�K\�q)���X�b8}`5^(�\.�����t�_߮��1#ԪcwSE@DaQ�q���1�z�c���v".%��)��(��`�ݒ8<�6�l���`fn��N?.�R�eU��N�s�����p�?�ϯ����۷�=�D7.]y�������G�W�9 𮷺��A��Y��N�(���3	��6��0A�$�Va�ʪ�:4��w���>�
�ܽ��N1��<v=X�HJ�֝���D���� @�uT2̐�yJ�,����w3�TplU�V:Y8DPl2H ���"@��,S�z�"
s:%�������P���i��UU��p��'�]�\�)�����tND�Rh un�L ��ֈ�X�e���=�! �t
!fD4�6��
�h��耠�29�M�C�$8���8�tm�Q�e��QѪ��.�ٳO�޹�-�PT����K�Td��m�)��D1�:@UI1�HB�l)��&��H�-1GYXE!'��V[ k��ߤ���2��ر�ˍ��:�OR�$;�Q�}N�{�e�:�(xR�lC9����]ﭝ#�ðβ͏3)�s+E��+zG��ی���ܛ�xG� 楮^��q���?��<Gp�ߗ�_�Ѫͻ�>�vK�e��\���k�f�����׃�,G�ڣ�4�Vs��C�eRA(�X�jF�D�H�(�#�X̰v��Wg�N����M/6�B�  \?��Έ��R���k+�(b��EE�<e0����\K'�9AUa���s
��9'����x�AF_A` aVU�D,�3�U3hg}*_�rJ�(��E��,B)���xK~�횠�B=���St�^��R�����)�xH!�5%|tq�����r/�P���3T�◈�WGF��*�茙�m�+�c����'�( �V�Q�8�O>��{����	 �§;��P �iS`���:t�i��\���,/�*���+���l�ؠD�yNIT=d�a�-N[u���NE����fC�A9X[_��Nѝ��cEN�!=���`:W��(�(���w�9	yF%b��c"�^6�Uaf�nyIu�ּ�y�'͍F��<l�����z��)w��s�Mq��FFN�����i?uv��7����z���)�#��c�3`� (�`� !�9u`fC��k-ʬ���E�)
_�t������o @QtB9���@�j6�m��
��L^
��cLB�__-��bY)v:����V'�g.u#U���3l��;K��)�t����" �0%r��vb-g��L� T�� ��D�Ty1�Hfh�o���ns�P�C��SL��ᮃ�^��n�xo�?EN�uV�*��q�9Q�K�۶��n3�m�-�梴��x.PAL.QD�<���*����O̅�$�N[����c�rf&BTA@4��c(Ke�eUJ���Sq
�;߄>U�=�*���Z�HD�
�)IR�-�0:�X��IUDU�\�CMª*��W���9:�s�)4QI�S�&�?��Tk����7�x�������v <bKOs���^���G�ح5��+vtv�슱��>��oo��Ds��o�#n�nֳ<�ٰ
6\���U��k�ہ�&s�� *bä*��n����#��e�(�DI�M�ֆ�FU��9%���"G��XcUU���j�R�L�C�� �Xi�^�$Ęb,gggg�zs�s��^�Vt:��s����IQVUPU��XKi���)v�r�`��㮒��U�L�)��������Y'9u7��s(2܄��n��-3�đ�Hkkkׯ_;��k+ˬ��n�1(;�YK���RJ1���j���B��$L��p;V^l��m�љ���#3�'�y횈��.]\���[�X�z� �6���in����v�F� O�ŪHs+���V��b��!
��"�	�S<x�W����D�&�ٷ���Y�AC�`���������&a�Z7�j]jǁ"(���e��MӰ���rB N�y !�=i A���PUc�1������"�eYt��W;EǙW���T-O5s�[�x��r���M��p�6SL�����Tػ����
�#�f��f=�n�Ɉ��3J�&�}�c�l�� �F��fOfiL��K�#z 7�؂Qދ�Za�%��6�a�PZ�~#NŦ��*<ph�j
�v��l#D������?�=I��7	{� �'�����*j�o��(̑(V� �˾w���s�,���L�ڬ 
��PW+*�	�����6k�9Pe&% e���T)F��)	R}kv��f5�Z�uD��y��sV\�9l=Y-�z�yk�9|zU�Q����w��Z3��2���^���v���+&M2v��خ�k����}��޲,���I�c�(��r�:4��Ϋ��M��z퉂���z�v6l~�7��h�`[C1����ʧ�˘(�Q���g��O	[��u�cS:Ү; 㡞m�g�kg��
'Q�L����3ܾz�>�e�؞��s��P{ľ8l/�����e�h� 1;�8D�l{�w����^�������rQA�T�AUH�D8%Iª���B�
#�H�� 8TQWx�Cn�H� "Q��U���󪔇�m{�&w�9����  T�%�)7��r�Z�NX�۰jB������3a+�@<{9'ǒB�RJ�����ܹz�������mV�t��XHQ-G�E�$+���J*1���BUU��FL���z�Zt
�a6�펆����@��bv�V2!+�}u��,~<,]�d  �ٛĦ���;���|�c��n�[�p_eOu�0Afa�DED8Q�*T��X[Z^�=r$
@�Y���p������UQI�Ic�D)�c�U�Q�<��]�S���<T����ډH�9�i�;��i�]A˩լ#��A��i�SL1E��� o;f2�&�q?�0W|���<�;��BDp ����Zن[������r�c�f> o�� �v�:Up�
J�T1��#%�O>��7�Pt�H���]G�I��yeP&%�DJ�)�XV�
)� 1w��ը䰟��,aHw�"ZG5T,K0�
Z,�u��)skt�.��Դ�f�;��MZsb��v7����1���u���gD=~s<ލ]����M��[��[�k7[�y^7?�*e��jBU�N������J�[��	ެ6�cšs�������Y����]zt��vGbꐀ�ho����j��^��,� (�$��J��Ua�Fߑ���S�D)%{С��C
�'���/K;�>��j����we��Q���^觎�)���1@����~�fe��b�^Dt�Pl%��  TIDAT� �Z��k��줅62�h�9�A���
"�섔I9Q�����/C�tg˪Ά_PV%�����Ce���B̉���P"�D1Q�N�(�23���r��QO��M��p\;�y[�s�>���]�(C[��r��qX��,j����Σ�Gֲ�1��o!�������6�Y�9e��0��UU�f�A�P�����scY�	��$BB�8Q�1�TŘb�)����:�@�cc�5�EU�wEZVc�u��h���l���5����+9U��;�	������V�`��[���5��g�m�l���W��eZx��fe���a��$�VTjՋ�`̧N�����Q!��q$b=r��������T�'/��$ �(��@+d`�D)�P�0(��F5؈1&" �Q(Q2Bm;`�ٍ�Oi�;\su�e��Ga�|�������U���O� '��kj��z����Y��E��i�ӝ����3���ḧ́�h�lA�f���Xmb�����E�e������:�Ɔ�>��3�:�B�64�M#�/ P�k�k�iI�Y�S\���ֆCT��	㽗����C��Ӿ?ʖ喰$�b�%��U+�xhP��;'�:	!� �9�q���833�R`&1�lU"f"f`&��(e�2��A	�
hKXE��91�9�,�F5Ne�֜b����B& �Z����>ϮP�,G��w	ulRr�n�����N��b�;�{�m��9)h� ^$�C,��u*���ښ`���U�́JL$LL��Y������r��6g�U���{���UvD�w�<ڍ�����gb����0Y��=��;�F{��ع=��9��KX����=�n�J���#�;A�n� �ե;�kǞ8�Q��������Qu"���B�,��,Jl� N�,��E�-Sr�M9�~v�Oߡ)��GL�֘�C]g9�$5�ir�L�n�(l�#�E;=Ԏ��*�8 V��BQҬ7���:f���*[�6�8n��7��v��EQ�b����.����G�G��?��T��S�@,66�
 M1�R1F��b�)��FU�k)�~T�!�������:%���mו�;�&�Wu7c�=h<Tv��;��-��mQg�����$�=�}�>r����Z�8��x�ݤ����caY�3�rtPU�� T�!�:eAD^XX�r�
����-..D�!�f�L$ ��_�ЏUY�e9T�A�*xt9�Ɩ� �&<j>j�leƎ�N�z�ާ)��b��P��ٜ�� 6q���Vm���bw���޹숵�D�],�I��ޙ��DT�Kb �N����w��rc$fRU3�	��`YUUU,���BYC�s��%�n4Fw��W�����x`�N�X�!�mc�'��h[���AM=��������@a�d{��[�(�xH|M���uSU�S�ʞ��L�ȃA�����tg����΃�FJ�H��M� ��"�B""D�R""J �P�遟�SL1ţ��V��7؊��.��mk�DtSaY�c�l/�d�l�1�1M�6&[��N�{`K�A �-'IA��zo�ݚz�\[o�v��u�ew�>q�NzT�X���@���ŋ�<} b�HX�(�HD�P4�XUUU,!�UՏ1�F%�"���:2ɬC�5_-:�阙�j�h��+�����d��Ԭq���펶ݏ[���~��̲���܋��.u���ʝGK�v�
&1���6i��{�����!�q��q#k^�\�5<J��<���r7�_�\�*Lɂ��!"�k�ϷIW'<z�Uͭ3�[��!'��v4^����!���f���P��ڵ��Z��о�w��=⌥i�{$�3�۷�z�r�߼����c�4 :Du�l,�*��l��ރ�"(�7�����<}f���(�D��$S�"&EMUY�ש*�쇲�Hʬ�̌;��Ȅ�SL1��F{j8U�9�(��fC�Ǥ���f�F�9ǜ�x�b:�;��j�m�G�)��jgA5ygf�ԝ�:T�ȑ����o��o��B�E(%!�HOL��Se���b�U?�R%9B��\�����W��ũ7�I�b;lz[ |������Гr/��6�~�!�Y��/�caYZ���T�t_͖���]U! p̾�*��L'�._�|yv~�)�$�,&i�c���*�A�C��J��\�ܪ:��:��s�z�)��b���?w4T�%+t���K��#o�	�C�<�c�f%ds�ƥ�C�d,�
�]ꘐ�*	%�AR�>���w~���d&fL���I�SU��:�*�Z��	�PEA�Ծ&b��5�x��wnz8ƞ:Ş0Όqx�c�*ɽ���G��a���w�����b�I�hX����v����bYڗF� @������ ������={��w��o�P�@aP�b���	b���ʾ�C?V
}��9B�Rf�8�Ĵϛb�)��1vfY�H�' ���{�s���{�$6�lJ|݄�rs��Tp �P�)�P�/������+��b +�!d�g��*���8T+ڿB��>�)���#�1�Z'�:h��]�s9��n+'�-��v5�C��y\,Ľ��y�[F��²�;��7�4��Ȗo�ve��OS�R�!�!ŕ[�f�#Q�6��P�(�� TQ��E�Oa�SLq@Q�60�ÙP�Hb$6���*���^�d[��-��Z����ˏ�A۳��1�O`�i�ѷ�#��؁��� �wخ>�B�JU�V �k}�v�o|���vV� <8,�L��:�A�S8~��ҍ��N$Pg�%�*�,���S�)*'��Fʻ�u���k�1��8vk�]����;}���%ku4d��dX�}_Ѯ��9� P�eb�c�jd��F��f��P�o�j��Ү_U�Goz�ͫ���QI�s�p�c�++�د�e��e���K�αwng�r����BPDd$Pr��pDC9誮�Y�8_t:��b"s$f�cJ1�T)*��a���b��i8j�  ���C���v�ں�m��ố6�s� Ġ�L��I�kՐ�P] P��j��B!����e�[tʍWt��JU�1Gf�D," z7�!��*=���x-r�?��L��67����=��>BDG�y8�Vw
��}�,j$����cgYBc\:EAU`�����s�j�8a��^C9(���wBU��Pdb U'	���̭��m�SL1��4��o�,G��>.�}FS=�9S5����ǯѠ&��Q]�d�bU��|J���H���}�+_�&����#����ۑ�5lG�'<u����K�e��ć��n�k���$~����Ȑ�[2ƾ�Ԋ1G��=�~���и�u��0?m�!� �YP9k����ٵ�,Ҽ�)��b�=b�6}��N4#���0��#":�yB^���aJQU��,4E��)4c��;�b
aֵ���n⩏s��Y]v/�9l��L5���D=����]���h���,�}��5[�y'����6���PUJ	�Des��ŔSL1����R5��F$�Z�� ������  �+[u��d�V�5s]��r|�ۆ���l8�=7@p��FO��Kn��mMtD x����@���ֵ�;	oy��>e!��su�G�=`���À��g�7�T)o�͞|綾���=�,Dm�㤌��O# uTi��d�U����w.�
� ����r�����a������a.�էd��L��� lL�8k��"�8
PC5�}0�H������H�TN9��9f��b� � ���Q�u� ���ӻ��n�� /�=K�hs��	�7������H�V�gf�5�	����W�(���C���sܑ����&'9��&��F|}����" �X�-9׼��9� �y�|_�
���;�5,�~#����>y�o`�m���h��&�3A$i����U� ~o�MU�iG�GD$��Ro��Q�@N<�r�?M�Ww��^���Vzy".��,��ie�9�Z}���m�[(�C#�4m~�%���ߡǑ�Ԫ�+�~�ė�(NB��S��y&�����It��rY?�&.��,z+��c�1 ��]�Ś����qe�)�lD
g5�B�հAA�����/���    IEND�B`�
```
---


          # app/templates/admin/applications.html,
          \${language}
{% extends "base.html" %}

{% block title %}Manage Applications - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Manage Applications</h1>

    <form method="get" action="{{ url_for('admin.applications') }}" class="mb-4">
        <div class="input-group">
            <select class="form-select" name="status" onchange="this.form.submit()">
                <option value="">All Statuses</option>
                <option value="applied" {% if status_filter == 'applied' %}selected{% endif %}>Applied</option>
                <option value="shortlisted" {% if status_filter == 'shortlisted' %}selected{% endif %}>Shortlisted</option>
                <option value="rejected" {% if status_filter == 'rejected' %}selected{% endif %}>Rejected</option>
                <option value="hired" {% if status_filter == 'hired' %}selected{% endif %}>Hired</option>
            </select>
        </div>
    </form>

    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Candidate</th>
                    <th>Job</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th>Applied</th>
                </tr>
            </thead>
            <tbody>
                {% for app in applications.items %}
                    <tr>
                        <td>{{ app.candidate.name }}</td>
                        <td>{{ app.job.title }}</td>
                        <td>{{ app.job.company.company_name }}</td>
                        <td>
                            <span class="badge bg-{% if app.status == 'hired' %}success{% elif app.status == 'shortlisted' %}info{% elif app.status == 'rejected' %}danger{% else %}secondary{% endif %}">
                                {{ app.status }}
                            </span>
                        </td>
                        <td class="text-muted small">{{ app.applied_at.strftime('%b %d, %Y') }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if applications.pages > 1 %}
        <nav aria-label="Page navigation" class="mt-4">
            <ul class="pagination justify-content-center">
                {% if applications.has_prev %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.applications', page=applications.prev_num) }}">Previous</a>
                    </li>
                {% endif %}
                {% for page_num in applications.iter_pages() %}
                    {% if page_num %}
                        <li class="page-item {% if page_num == applications.page %}active{% endif %}">
                            <a class="page-link" href="{{ url_for('admin.applications', page=page_num) }}">{{ page_num }}</a>
                        </li>
                    {% endif %}
                {% endfor %}
                {% if applications.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.applications', page=applications.next_num) }}">Next</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/admin/dashboard.html,
          \${language}
{% extends "base.html" %}

{% block title %}Admin Dashboard - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Admin Dashboard</h1>

    <div class="row g-4 mb-5">
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%); color: white;">
                <div class="card-body">
                    <h6 class="card-text opacity-75">Total Users</h6>
                    <h3 class="mb-0">{{ stats.total_users }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white;">
                <div class="card-body">
                    <h6 class="card-text opacity-75">Candidates</h6>
                    <h3 class="mb-0">{{ stats.total_candidates }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%); color: white;">
                <div class="card-body">
                    <h6 class="card-text opacity-75">Companies</h6>
                    <h3 class="mb-0">{{ stats.total_companies }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white;">
                <div class="card-body">
                    <h6 class="card-text opacity-75">Total Jobs</h6>
                    <h3 class="mb-0">{{ stats.total_jobs }}</h3>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-4 mb-5">
        <div class="col-md-4">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="card-text text-muted">Active Jobs</h6>
                    <h3 class="mb-0">{{ stats.active_jobs }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="card-text text-muted">Total Applications</h6>
                    <h3 class="mb-0">{{ stats.total_applications }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card border-0 shadow-sm">
                <div class="card-body">
                    <h6 class="card-text text-muted">Recent Activity</h6>
                    <p class="mb-0 text-success">
                        <i class="bi bi-arrow-up"></i> 12% increase this month
                    </p>
                </div>
            </div>
        </div>
    </div>

    <div class="card border-0 shadow-sm">
        <div class="card-header bg-light border-bottom">
            <h5 class="mb-0">Recent Applications</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Candidate</th>
                            <th>Job</th>
                            <th>Company</th>
                            <th>Status</th>
                            <th>Applied</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for app in recent_applications %}
                            <tr>
                                <td>{{ app.candidate.name }}</td>
                                <td>{{ app.job.title }}</td>
                                <td>{{ app.job.company.company_name }}</td>
                                <td>
                                    <span class="badge bg-{% if app.status == 'hired' %}success{% elif app.status == 'shortlisted' %}info{% elif app.status == 'rejected' %}danger{% else %}secondary{% endif %}">
                                        {{ app.status }}
                                    </span>
                                </td>
                                <td class="text-muted small">{{ app.applied_at.strftime('%b %d, %Y') }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="row g-4 mt-4">
        <div class="col-md-6">
            <a href="{{ url_for('admin.users') }}" class="btn btn-outline-primary w-100">Manage Users</a>
        </div>
        <div class="col-md-6">
            <a href="{{ url_for('admin.reports') }}" class="btn btn-outline-primary w-100">View Reports</a>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/admin/jobs.html,
          \${language}
{% extends "base.html" %}

{% block title %}Manage Jobs - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Manage Jobs</h1>

    <form method="get" action="{{ url_for('admin.jobs') }}" class="mb-4">
        <div class="input-group">
            <select class="form-select" name="status" onchange="this.form.submit()">
                <option value="">All Statuses</option>
                <option value="active" {% if status_filter == 'active' %}selected{% endif %}>Active</option>
                <option value="closed" {% if status_filter == 'closed' %}selected{% endif %}>Closed</option>
            </select>
        </div>
    </form>

    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Posted</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for job in jobs.items %}
                    <tr>
                        <td>{{ job.title }}</td>
                        <td>{{ job.company.company_name }}</td>
                        <td>{{ job.location }}</td>
                        <td>
                            <span class="badge bg-{% if job.status == 'active' %}success{% else %}secondary{% endif %}">
                                {{ job.status }}
                            </span>
                        </td>
                        <td class="text-muted small">{{ job.posted_at.strftime('%b %d, %Y') }}</td>
                        <td>
                            <form method="POST" action="{{ url_for('admin.delete_job', job_id=job.id) }}" style="display:inline;">
                                <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this job?')">Delete</button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if jobs.pages > 1 %}
        <nav aria-label="Page navigation" class="mt-4">
            <ul class="pagination justify-content-center">
                {% if jobs.has_prev %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.jobs', page=jobs.prev_num) }}">Previous</a>
                    </li>
                {% endif %}
                {% for page_num in jobs.iter_pages() %}
                    {% if page_num %}
                        <li class="page-item {% if page_num == jobs.page %}active{% endif %}">
                            <a class="page-link" href="{{ url_for('admin.jobs', page=page_num) }}">{{ page_num }}</a>
                        </li>
                    {% endif %}
                {% endfor %}
                {% if jobs.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.jobs', page=jobs.next_num) }}">Next</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/admin/reports.html,
          \${language}
{% extends "base.html" %}

{% block title %}Reports - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Platform Reports</h1>

    <div class="row g-4 mb-5">
        <div class="col-md-6">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">User Statistics</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Total Candidates</span>
                            <h4 class="mb-0 text-primary">{{ data.candidates }}</h4>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Total Companies</span>
                            <h4 class="mb-0 text-success">{{ data.companies }}</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Job Statistics</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Total Jobs Posted</span>
                            <h4 class="mb-0 text-warning">{{ data.jobs }}</h4>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Active Jobs</span>
                            <h4 class="mb-0 text-info">{{ data.active_jobs }}</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <div class="col-md-6">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Application Statistics</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Total Applications</span>
                            <h4 class="mb-0">{{ data.applications }}</h4>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Shortlisted</span>
                            <h4 class="mb-0 text-info">{{ data.shortlisted }}</h4>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Hired</span>
                            <h4 class="mb-0 text-success">{{ data.hired }}</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Success Rate</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        {% if data.applications > 0 %}
                            {% set hire_rate = (data.hired / data.applications * 100)|int %}
                            <div class="mb-2">
                                <div class="d-flex justify-content-between mb-2">
                                    <span>Hire Rate</span>
                                    <span>{{ hire_rate }}%</span>
                                </div>
                                <div class="progress">
                                    <div class="progress-bar bg-success" style="width: {{ hire_rate }}%"></div>
                                </div>
                            </div>

                            {% set shortlist_rate = (data.shortlisted / data.applications * 100)|int %}
                            <div class="mb-2">
                                <div class="d-flex justify-content-between mb-2">
                                    <span>Shortlist Rate</span>
                                    <span>{{ shortlist_rate }}%</span>
                                </div>
                                <div class="progress">
                                    <div class="progress-bar bg-info" style="width: {{ shortlist_rate }}%"></div>
                                </div>
                            </div>
                        {% else %}
                            <p class="text-muted">No applications yet</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="mt-5 text-center">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-primary">Back to Dashboard</a>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/admin/users.html,
          \${language}
{% extends "base.html" %}

{% block title %}Manage Users - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Manage Users</h1>

    <form method="get" action="{{ url_for('admin.users') }}" class="mb-4">
        <div class="input-group">
            <select class="form-select" name="role" onchange="this.form.submit()">
                <option value="">All Roles</option>
                <option value="candidate" {% if role_filter == 'candidate' %}selected{% endif %}>Candidates</option>
                <option value="company" {% if role_filter == 'company' %}selected{% endif %}>Companies</option>
                <option value="admin" {% if role_filter == 'admin' %}selected{% endif %}>Admins</option>
            </select>
        </div>
    </form>

    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="table-light">
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Joined</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users.items %}
                    <tr>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td><span class="badge bg-info">{{ user.role }}</span></td>
                        <td>
                            <span class="badge bg-{% if user.is_active %}success{% else %}danger{% endif %}">
                                {{ 'Active' if user.is_active else 'Inactive' }}
                            </span>
                        </td>
                        <td class="text-muted small">{{ user.created_at.strftime('%b %d, %Y') }}</td>
                        <td>
                            <form method="POST" action="{{ url_for('admin.toggle_user_status', user_id=user.id) }}" style="display:inline;">
                                <button type="submit" class="btn btn-sm btn-{% if user.is_active %}warning{% else %}success{% endif %}">
                                    {{ 'Deactivate' if user.is_active else 'Activate' }}
                                </button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if users.pages > 1 %}
        <nav aria-label="Page navigation" class="mt-4">
            <ul class="pagination justify-content-center">
                {% if users.has_prev %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.users', page=users.prev_num, role=role_filter) }}">Previous</a>
                    </li>
                {% endif %}
                {% for page_num in users.iter_pages() %}
                    {% if page_num %}
                        <li class="page-item {% if page_num == users.page %}active{% endif %}">
                            <a class="page-link" href="{{ url_for('admin.users', page=page_num, role=role_filter) }}">{{ page_num }}</a>
                        </li>
                    {% endif %}
                {% endfor %}
                {% if users.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('admin.users', page=users.next_num, role=role_filter) }}">Next</a>
                    </li>
                {% endif %}
            </ul>
        </nav>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/auth/login.html,
          \${language}
{% extends "base.html" %}

{% block title %}Login - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg">
                <div class="card-body p-5">
                    <h2 class="text-center mb-4">
                        <i class="bi bi-lock-fill me-2" style="color: #2563EB;"></i>Login
                    </h2>

                    <ul class="nav nav-tabs mb-4" id="loginTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="candidate-tab" data-bs-toggle="tab" data-bs-target="#candidate" type="button">Candidate</button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="company-tab" data-bs-toggle="tab" data-bs-target="#company" type="button">Company</button>
                        </li>
                    </ul>

                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}
                        <div class="mb-3">
                            {{ form.email(class="form-control form-control-lg", placeholder="Email Address") }}
                            {% if form.email.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.email.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.password(class="form-control form-control-lg", placeholder="Password") }}
                            {% if form.password.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100">Login</button>
                    </form>

                    <hr class="my-4">
                    <p class="text-center mb-0">
                        Don't have an account?
                        <a href="{{ url_for('auth.register_candidate') }}">Register as Candidate</a> or
                        <a href="{{ url_for('auth.register_company') }}">Register as Company</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/auth/register_candidate.html,
          \${language}
{% extends "base.html" %}

{% block title %}Register as Candidate - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg">
                <div class="card-body p-5">
                    <h2 class="text-center mb-2">
                        <i class="bi bi-person-plus-fill me-2" style="color: #2563EB;"></i>Register as Candidate
                    </h2>
                    <p class="text-center text-muted mb-4">Create your account to start applying for jobs</p>

                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}
                        <div class="mb-3">
                            {{ form.name(class="form-control form-control-lg", placeholder="Full Name") }}
                            {% if form.name.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.name.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.email(class="form-control form-control-lg", placeholder="Email Address") }}
                            {% if form.email.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.email.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.password(class="form-control form-control-lg", placeholder="Password") }}
                            {% if form.password.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.confirm_password(class="form-control form-control-lg", placeholder="Confirm Password") }}
                            {% if form.confirm_password.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.confirm_password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100">Register</button>
                    </form>

                    <hr class="my-4">
                    <p class="text-center mb-0">
                        Already have an account?
                        <a href="{{ url_for('auth.login') }}">Login here</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/auth/register_company.html,
          \${language}
{% extends "base.html" %}

{% block title %}Register as Company - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg">
                <div class="card-body p-5">
                    <h2 class="text-center mb-2">
                        <i class="bi bi-briefcase-fill me-2" style="color: #2563EB;"></i>Register as Company
                    </h2>
                    <p class="text-center text-muted mb-4">Post jobs and hire top talent</p>

                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}
                        <div class="mb-3">
                            {{ form.name(class="form-control form-control-lg", placeholder="Contact Person Name") }}
                            {% if form.name.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.name.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.company_name(class="form-control form-control-lg", placeholder="Company Name") }}
                            {% if form.company_name.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.company_name.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.email(class="form-control form-control-lg", placeholder="Company Email") }}
                            {% if form.email.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.email.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.password(class="form-control form-control-lg", placeholder="Password") }}
                            {% if form.password.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <div class="mb-3">
                            {{ form.confirm_password(class="form-control form-control-lg", placeholder="Confirm Password") }}
                            {% if form.confirm_password.errors %}
                                <div class="invalid-feedback d-block">
                                    {% for error in form.confirm_password.errors %}{{ error }}{% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        <button type="submit" class="btn btn-success btn-lg w-100">Register Company</button>
                    </form>

                    <hr class="my-4">
                    <p class="text-center mb-0">
                        Already have an account?
                        <a href="{{ url_for('auth.login') }}">Login here</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/base.html,
          \${language}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NextOffer - Placement Portal{% endblock %}</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

    {% block extra_css %}{% endblock %}
</head>
<body style="display: flex; flex-direction: column; min-height: 100vh;">
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container-fluid">
            <a class="navbar-brand fw-bold" href="{{ url_for('main.index') }}">
                <i class="bi bi-briefcase-fill me-2"></i>NextOffer
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        {% if current_user.role == 'candidate' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('candidate.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('candidate.profile') }}">Profile</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('main.browse_jobs') }}">Browse Jobs</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('candidate.applications') }}">Applications</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('resume.builder') }}">Resume Builder</a></li>
                        {% elif current_user.role == 'company' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.profile') }}">Company Profile</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.jobs') }}">My Jobs</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('company.post_job') }}">Post Job</a></li>
                        {% elif current_user.role == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.dashboard') }}">Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.users') }}">Users</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.jobs') }}">Jobs</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.applications') }}">Applications</a></li>
                        {% endif %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                                <i class="bi bi-person-circle me-1"></i>{{ current_user.name }}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('auth.logout') }}">Logout</a></li>
                            </ul>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('main.browse_jobs') }}">Browse Jobs</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <main style="flex: 1;">
        <div class="container-fluid">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" role="alert" style="z-index: 9999; max-width: 500px;">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="bg-dark text-white py-4 mt-5" style="margin-top: auto;">
        <div class="container text-center">
            <p class="mb-2">&copy; 2024 NextOffer. All rights reserved.</p>
            <small>Connecting talent with opportunity.</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>

    {% block extra_scripts %}{% endblock %}
</body>
</html>
```
---


          # app/templates/candidate/applications.html,
          \${language}
{% extends "base.html" %}

{% block title %}My Applications - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">My Applications</h1>

    {% if applications %}
        <div class="row g-3">
            {% for app in applications %}
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <h5 class="card-title mb-1">{{ app.job.title }}</h5>
                                    <p class="text-muted mb-2">
                                        <i class="bi bi-building me-1"></i>{{ app.job.company.company_name }}
                                    </p>
                                    <p class="text-muted small">
                                        <i class="bi bi-calendar me-1"></i>Applied: {{ app.applied_at.strftime('%B %d, %Y') }}
                                    </p>
                                </div>
                                <div class="col-md-4 text-md-end">
                                    <span class="badge bg-{% if app.status == 'hired' %}success{% elif app.status == 'shortlisted' %}info{% elif app.status == 'rejected' %}danger{% else %}secondary{% endif %} fs-6 mb-3">
                                        {{ app.status.upper() }}
                                    </span>
                                    <br>
                                    <a href="{{ url_for('main.job_detail', job_id=app.job_id) }}" class="btn btn-sm btn-outline-primary">View Job</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info text-center py-5">
            <h5>No applications yet</h5>
            <p><a href="{{ url_for('main.browse_jobs') }}">Browse and apply for jobs</a></p>
        </div>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/candidate/apply.html,
          \${language}
{% extends "base.html" %}

{% block title %}Apply for {{ job.title }} - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h4 class="mb-0">Apply for {{ job.title }}</h4>
                </div>
                <div class="card-body p-5">
                    <div class="alert alert-info mb-4">
                        <strong>{{ job.title }}</strong> at <strong>{{ job.company.company_name }}</strong>
                    </div>

                    <form method="POST">
                        <div class="mb-4">
                            <h6>Your Information</h6>
                            <p class="mb-1">Name: <strong>{{ current_user.name }}</strong></p>
                            <p>Email: <strong>{{ current_user.email }}</strong></p>
                        </div>

                        <div class="mb-4">
                            <label class="form-label">Cover Letter</label>
                            <textarea class="form-control" name="cover_letter" rows="8" placeholder="Tell the employer why you're interested in this position..."></textarea>
                            <small class="text-muted">Optional but recommended</small>
                        </div>

                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="bi bi-send me-2"></i>Submit Application
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/awards.html,
          \${language}
{% extends "base.html" %}

{% block title %}Awards - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-3">
            <div class="sidebar-nav">
                <h6 style="margin-bottom: 1.5rem;">Profile Sections</h6>
                <a href="{{ url_for('candidate.profile') }}" class="nav-link">
                    <i class="bi bi-person me-2"></i>Personal Info
                </a>
                <a href="{{ url_for('candidate.education') }}" class="nav-link">
                    <i class="bi bi-book me-2"></i>Education
                </a>
                <a href="{{ url_for('candidate.experience') }}" class="nav-link">
                    <i class="bi bi-briefcase me-2"></i>Experience
                </a>
                <a href="{{ url_for('candidate.skills') }}" class="nav-link">
                    <i class="bi bi-star me-2"></i>Skills
                </a>
                <a href="{{ url_for('candidate.projects') }}" class="nav-link">
                    <i class="bi bi-diagram-3 me-2"></i>Projects
                </a>
                <a href="{{ url_for('candidate.awards') }}" class="nav-link active">
                    <i class="bi bi-award me-2"></i>Awards
                </a>
                <a href="{{ url_for('candidate.dashboard') }}" class="nav-link" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>

        <div class="col-lg-9">
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary mb-3">
                <i class="bi bi-arrow-left me-2"></i>Back
            </a>

            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Add Award</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        <div class="mb-3">
                            <label class="form-label">Award Title</label>
                            {{ form.title(class="form-control") }}
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Issuer/Organization</label>
                                {{ form.issuer(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Date</label>
                                {{ form.date(class="form-control") }}
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            {{ form.description(class="form-control", rows="3") }}
                        </div>
                        {{ form.submit(class="btn btn-primary") }}
                    </form>
                </div>
            </div>

            {% if awards %}
                <h4 class="mb-3">Your Awards</h4>
                <div class="row g-3">
                    {% for award in awards %}
                        <div class="col-12">
                            <div class="card border-0 shadow-sm">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col">
                                            <h5 class="card-title">
                                                <i class="bi bi-award me-2" style="color: #FF9900;"></i>{{ award.title }}
                                            </h5>
                                            {% if award.issuer %}
                                                <p class="text-muted mb-1">{{ award.issuer }}</p>
                                            {% endif %}
                                            {% if award.date %}
                                                <p class="text-muted small mb-2">
                                                    <i class="bi bi-calendar-event me-1"></i>{{ award.date.strftime('%B %Y') }}
                                                </p>
                                            {% endif %}
                                            {% if award.description %}
                                                <p class="card-text">{{ award.description }}</p>
                                            {% endif %}
                                        </div>
                                        <div class="col-auto">
                                            <form method="POST" action="{{ url_for('candidate.delete_award', award_id=award.id) }}" style="display:inline;">
                                                <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this award?')">
                                                    <i class="bi bi-trash me-1"></i>Delete
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No awards added yet. Highlight your achievements and certifications.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/dashboard.html,
          \${language}
{% extends "base.html" %}

{% block title %}Candidate Dashboard - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Dashboard</h1>

    <div class="row g-4 mb-5">
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Applications Sent</p>
                            <h3 class="mb-0">{{ stats.applications_sent }}</h3>
                        </div>
                        <i class="bi bi-send" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Shortlisted</p>
                            <h3 class="mb-0">{{ stats.shortlisted }}</h3>
                        </div>
                        <i class="bi bi-check-circle" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Rejected</p>
                            <h3 class="mb-0">{{ stats.rejected }}</h3>
                        </div>
                        <i class="bi bi-x-circle" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Hired</p>
                            <h3 class="mb-0">{{ stats.hired }}</h3>
                        </div>
                        <i class="bi bi-star" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-8">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Recent Applications</h5>
                </div>
                <div class="card-body">
                    {% if recent_applications %}
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th>Job Title</th>
                                        <th>Company</th>
                                        <th>Status</th>
                                        <th>Applied</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for app in recent_applications %}
                                        <tr>
                                            <td>{{ app.job.title }}</td>
                                            <td>{{ app.job.company.company_name }}</td>
                                            <td>
                                                <span class="badge bg-{% if app.status == 'hired' %}success{% elif app.status == 'shortlisted' %}info{% elif app.status == 'rejected' %}danger{% else %}secondary{% endif %}">
                                                    {{ app.status }}
                                                </span>
                                            </td>
                                            <td class="text-muted small">{{ app.applied_at.strftime('%b %d, %Y') }}</td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted text-center py-4">No applications yet. <a href="{{ url_for('main.browse_jobs') }}">Browse jobs</a></p>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Quick Actions</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('main.browse_jobs') }}" class="btn btn-primary">
                            <i class="bi bi-search me-2"></i>Browse Jobs
                        </a>
                        <a href="{{ url_for('candidate.profile') }}" class="btn btn-outline-primary">
                            <i class="bi bi-person me-2"></i>Edit Profile
                        </a>
                        <a href="{{ url_for('candidate.skills') }}" class="btn btn-outline-primary">
                            <i class="bi bi-star me-2"></i>Manage Skills
                        </a>
                        <a href="{{ url_for('resume.builder') }}" class="btn btn-outline-primary">
                            <i class="bi bi-file-earmark-pdf me-2"></i>Resume Builder
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/education.html,
          \${language}
{% extends "base.html" %}

{% block title %}Education - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-3">
            <div class="sidebar-nav">
                <h6 style="margin-bottom: 1.5rem;">Profile Sections</h6>
                <a href="{{ url_for('candidate.profile') }}" class="nav-link">
                    <i class="bi bi-person me-2"></i>Personal Info
                </a>
                <a href="{{ url_for('candidate.education') }}" class="nav-link active">
                    <i class="bi bi-book me-2"></i>Education
                </a>
                <a href="{{ url_for('candidate.experience') }}" class="nav-link">
                    <i class="bi bi-briefcase me-2"></i>Experience
                </a>
                <a href="{{ url_for('candidate.skills') }}" class="nav-link">
                    <i class="bi bi-star me-2"></i>Skills
                </a>
                <a href="{{ url_for('candidate.projects') }}" class="nav-link">
                    <i class="bi bi-diagram-3 me-2"></i>Projects
                </a>
                <a href="{{ url_for('candidate.awards') }}" class="nav-link">
                    <i class="bi bi-award me-2"></i>Awards
                </a>
                <a href="{{ url_for('candidate.dashboard') }}" class="nav-link" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>

        <div class="col-lg-9">
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary mb-3">
                <i class="bi bi-arrow-left me-2"></i>Back
            </a>

            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Add Education</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Degree</label>
                                {{ form.degree(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Institution</label>
                                {{ form.institution(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Field of Study</label>
                                {{ form.field(class="form-control") }}
                            </div>
                            <div class="col-md-3 mb-3">
                                <label class="form-label">Start Year</label>
                                {{ form.start_year(class="form-control") }}
                            </div>
                            <div class="col-md-3 mb-3">
                                <label class="form-label">End Year</label>
                                {{ form.end_year(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Grade/GPA</label>
                                {{ form.grade(class="form-control") }}
                            </div>
                        </div>
                        {{ form.submit(class="btn btn-primary") }}
                    </form>
                </div>
            </div>

            {% if education %}
                <h4 class="mb-3">Your Education</h4>
                <div class="row g-3">
                    {% for edu in education %}
                        <div class="col-12">
                            <div class="card border-0 shadow-sm">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col">
                                            <h5 class="card-title mb-1">{{ edu.degree }}</h5>
                                            <p class="text-muted mb-2">{{ edu.institution }} {% if edu.field %}<span class="badge bg-light text-dark">{{ edu.field }}</span>{% endif %}</p>
                                            <p class="text-muted small">
                                                {% if edu.start_year %}<i class="bi bi-calendar-event me-1"></i>{{ edu.start_year }}{% endif %}
                                                {% if edu.end_year %} - {{ edu.end_year }}{% endif %}
                                                {% if edu.grade %}<span class="ms-2"><i class="bi bi-percent me-1"></i>GPA: {{ edu.grade }}</span>{% endif %}
                                            </p>
                                        </div>
                                        <div class="col-auto">
                                            <form method="POST" action="{{ url_for('candidate.delete_education', edu_id=edu.id) }}" style="display:inline;">
                                                <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this entry?')">
                                                    <i class="bi bi-trash me-1"></i>Delete
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No education entries yet. Add your educational background to build a stronger profile.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/experience.html,
          \${language}
{% extends "base.html" %}

{% block title %}Experience - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-3">
            <div class="sidebar-nav">
                <h6 style="margin-bottom: 1.5rem;">Profile Sections</h6>
                <a href="{{ url_for('candidate.profile') }}" class="nav-link">
                    <i class="bi bi-person me-2"></i>Personal Info
                </a>
                <a href="{{ url_for('candidate.education') }}" class="nav-link">
                    <i class="bi bi-book me-2"></i>Education
                </a>
                <a href="{{ url_for('candidate.experience') }}" class="nav-link active">
                    <i class="bi bi-briefcase me-2"></i>Experience
                </a>
                <a href="{{ url_for('candidate.skills') }}" class="nav-link">
                    <i class="bi bi-star me-2"></i>Skills
                </a>
                <a href="{{ url_for('candidate.projects') }}" class="nav-link">
                    <i class="bi bi-diagram-3 me-2"></i>Projects
                </a>
                <a href="{{ url_for('candidate.awards') }}" class="nav-link">
                    <i class="bi bi-award me-2"></i>Awards
                </a>
                <a href="{{ url_for('candidate.dashboard') }}" class="nav-link" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>

        <div class="col-lg-9">
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary mb-3">
                <i class="bi bi-arrow-left me-2"></i>Back
            </a>

            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Add Experience</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Company</label>
                                {{ form.company(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Job Title</label>
                                {{ form.role(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Start Date</label>
                                {{ form.start_date(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">End Date</label>
                                {{ form.end_date(class="form-control") }}
                            </div>
                            <div class="col-12 mb-3">
                                <label class="form-label">Description</label>
                                {{ form.description(class="form-control", rows="3") }}
                            </div>
                            <div class="col-12 mb-3">
                                <div class="form-check">
                                    {{ form.is_current(class="form-check-input") }}
                                    <label class="form-check-label">I currently work here</label>
                                </div>
                            </div>
                        </div>
                        {{ form.submit(class="btn btn-primary") }}
                    </form>
                </div>
            </div>

            {% if experience %}
                <h4 class="mb-3">Your Experience</h4>
                <div class="row g-3">
                    {% for exp in experience %}
                        <div class="col-12">
                            <div class="card border-0 shadow-sm">
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col">
                                            <h5 class="card-title mb-1">{{ exp.role }}</h5>
                                            <p class="text-muted mb-2">{{ exp.company }}
                                                {% if exp.is_current %}<span class="badge bg-success">Current</span>{% endif %}
                                            </p>
                                            <p class="text-muted small">
                                                <i class="bi bi-calendar-event me-1"></i>{{ exp.start_date.strftime('%b %Y') }} -
                                                {% if exp.end_date %}{{ exp.end_date.strftime('%b %Y') }}{% else %}Present{% endif %}
                                            </p>
                                            {% if exp.description %}
                                                <p class="card-text mt-2">{{ exp.description }}</p>
                                            {% endif %}
                                        </div>
                                        <div class="col-auto">
                                            <form method="POST" action="{{ url_for('candidate.delete_experience', exp_id=exp.id) }}" style="display:inline;">
                                                <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this entry?')">
                                                    <i class="bi bi-trash me-1"></i>Delete
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No experience entries yet. Add your work experience to strengthen your profile.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/profile.html,
          \${language}
{% extends "base.html" %}

{% block title %}My Profile - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">My Profile</h1>

    <div class="row g-4">
        <div class="col-lg-3">
            <div class="card border-0 shadow-sm text-center">
                <div class="card-body p-4">
                    {% if profile.profile_pic %}
                        <img src="{{ url_for('static', filename='uploads/' + profile.profile_pic) }}" alt="Profile" class="rounded-circle mb-3" style="width: 120px; height: 120px; object-fit: cover;">
                    {% else %}
                        <div class="bg-light rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center" style="width: 120px; height: 120px;">
                            <i class="bi bi-person" style="font-size: 3rem; color: #ccc;"></i>
                        </div>
                    {% endif %}
                    <h5>{{ current_user.name }}</h5>
                    <p class="text-muted small">{{ current_user.email }}</p>
                </div>
            </div>

            <div class="card border-0 shadow-sm mt-3">
                <div class="card-header bg-light">
                    <h6 class="mb-0">Profile Sections</h6>
                </div>
                <div class="list-group list-group-flush">
                    <a href="{{ url_for('candidate.profile') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-person me-2"></i>Personal Info
                    </a>
                    <a href="{{ url_for('candidate.education') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-book me-2"></i>Education
                    </a>
                    <a href="{{ url_for('candidate.experience') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-briefcase me-2"></i>Experience
                    </a>
                    <a href="{{ url_for('candidate.skills') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-star me-2"></i>Skills
                    </a>
                    <a href="{{ url_for('candidate.projects') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-diagram-3 me-2"></i>Projects
                    </a>
                    <a href="{{ url_for('candidate.awards') }}" class="list-group-item list-group-item-action">
                        <i class="bi bi-award me-2"></i>Awards
                    </a>
                </div>
            </div>
        </div>

        <div class="col-lg-9">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Personal Information</h5>
                </div>
                <div class="card-body">
                    <form method="POST" enctype="multipart/form-data">
                        {{ form.hidden_tag() }}

                        <div class="mb-3">
                            <label class="form-label">Profile Picture</label>
                            <input type="file" class="form-control" name="profile_pic" accept="image/*">
                            <small class="text-muted">PNG, JPG or GIF (Max 5MB)</small>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            {{ form.phone(class="form-control") }}
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Location</label>
                            {{ form.location(class="form-control") }}
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Bio</label>
                            {{ form.bio(class="form-control", rows="4") }}
                            <small class="text-muted">Tell us about yourself (max 1000 characters)</small>
                        </div>

                        {{ form.submit(class="btn btn-primary") }}
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/projects.html,
          \${language}
{% extends "base.html" %}

{% block title %}Projects - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-3">
            <div class="sidebar-nav">
                <h6 style="margin-bottom: 1.5rem;">Profile Sections</h6>
                <a href="{{ url_for('candidate.profile') }}" class="nav-link">
                    <i class="bi bi-person me-2"></i>Personal Info
                </a>
                <a href="{{ url_for('candidate.education') }}" class="nav-link">
                    <i class="bi bi-book me-2"></i>Education
                </a>
                <a href="{{ url_for('candidate.experience') }}" class="nav-link">
                    <i class="bi bi-briefcase me-2"></i>Experience
                </a>
                <a href="{{ url_for('candidate.skills') }}" class="nav-link">
                    <i class="bi bi-star me-2"></i>Skills
                </a>
                <a href="{{ url_for('candidate.projects') }}" class="nav-link active">
                    <i class="bi bi-diagram-3 me-2"></i>Projects
                </a>
                <a href="{{ url_for('candidate.awards') }}" class="nav-link">
                    <i class="bi bi-award me-2"></i>Awards
                </a>
                <a href="{{ url_for('candidate.dashboard') }}" class="nav-link" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>

        <div class="col-lg-9">
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary mb-3">
                <i class="bi bi-arrow-left me-2"></i>Back
            </a>

            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Add Project</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        <div class="mb-3">
                            <label class="form-label">Project Title</label>
                            {{ form.title(class="form-control") }}
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            {{ form.description(class="form-control", rows="3") }}
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Technologies Used</label>
                                {{ form.tech_used(class="form-control", placeholder="e.g., Python, Flask, React") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Project Link</label>
                                {{ form.link(class="form-control", placeholder="https://...") }}
                            </div>
                        </div>
                        {{ form.submit(class="btn btn-primary") }}
                    </form>
                </div>
            </div>

            {% if projects %}
                <h4 class="mb-3">Your Projects</h4>
                <div class="row g-3">
                    {% for project in projects %}
                        <div class="col-md-6">
                            <div class="card border-0 shadow-sm h-100">
                                <div class="card-body">
                                    <h5 class="card-title">{{ project.title }}</h5>
                                    {% if project.description %}
                                        <p class="card-text text-muted">{{ project.description }}</p>
                                    {% endif %}
                                    {% if project.tech_used %}
                                        <p class="mb-2">
                                            {% for tech in project.tech_used.split(',') %}
                                                <span class="badge bg-light text-dark me-1">{{ tech.strip() }}</span>
                                            {% endfor %}
                                        </p>
                                    {% endif %}
                                    <div class="d-flex justify-content-between align-items-center">
                                        {% if project.link %}
                                            <a href="{{ project.link }}" target="_blank" class="btn btn-sm btn-outline-primary">
                                                <i class="bi bi-link-45deg me-1"></i>View
                                            </a>
                                        {% endif %}
                                        <form method="POST" action="{{ url_for('candidate.delete_project', proj_id=project.id) }}" style="display:inline;">
                                            <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this project?')">
                                                <i class="bi bi-trash me-1"></i>Delete
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No projects added yet. Showcase your portfolio projects.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/candidate/skills.html,
          \${language}
{% extends "base.html" %}

{% block title %}Skills - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-3">
            <div class="sidebar-nav">
                <h6 style="margin-bottom: 1.5rem;">Profile Sections</h6>
                <a href="{{ url_for('candidate.profile') }}" class="nav-link">
                    <i class="bi bi-person me-2"></i>Personal Info
                </a>
                <a href="{{ url_for('candidate.education') }}" class="nav-link">
                    <i class="bi bi-book me-2"></i>Education
                </a>
                <a href="{{ url_for('candidate.experience') }}" class="nav-link">
                    <i class="bi bi-briefcase me-2"></i>Experience
                </a>
                <a href="{{ url_for('candidate.skills') }}" class="nav-link active">
                    <i class="bi bi-star me-2"></i>Skills
                </a>
                <a href="{{ url_for('candidate.projects') }}" class="nav-link">
                    <i class="bi bi-diagram-3 me-2"></i>Projects
                </a>
                <a href="{{ url_for('candidate.awards') }}" class="nav-link">
                    <i class="bi bi-award me-2"></i>Awards
                </a>
                <a href="{{ url_for('candidate.dashboard') }}" class="nav-link" style="margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem;">
                    <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>

        <div class="col-lg-9">
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary mb-3">
                <i class="bi bi-arrow-left me-2"></i>Back
            </a>

            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0">Add Skill</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        {{ form.hidden_tag() }}
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Skill</label>
                                {{ form.skill_name(class="form-control", placeholder="e.g., Python, React, AWS") }}
                            </div>
                            <div class="col-md-4 mb-3">
                                <label class="form-label">Proficiency</label>
                                {{ form.proficiency(class="form-select") }}
                            </div>
                            <div class="col-md-2 d-flex align-items-end">
                                {{ form.submit(class="btn btn-primary w-100") }}
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            {% if skills %}
                <h4 class="mb-3">Your Skills</h4>
                <div class="row g-2">
                    {% for skill in skills %}
                        <div class="col-auto">
                            <div class="card border-0 shadow-sm">
                                <div class="card-body p-2">
                                    <div class="d-flex align-items-center gap-2">
                                        <span class="badge bg-primary">{{ skill.proficiency }}</span>
                                        <span>{{ skill.skill_name }}</span>
                                        <form method="POST" action="{{ url_for('candidate.delete_skill', skill_id=skill.id) }}" style="display:inline;">
                                            <button type="submit" class="btn btn-sm btn-close" aria-label="Delete"></button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>No skills added yet. Add your technical and professional skills.
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/company/candidate_profile.html,
          \${language}
{% extends "base.html" %}

{% block title %}Candidate Profile - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <a href="{{ url_for('company.job_applications', job_id=application.job_id) }}" class="btn btn-outline-secondary mb-4">
        <i class="bi bi-arrow-left me-2"></i>Back
    </a>

    <div class="row g-4">
        <div class="col-lg-4">
            <div class="card border-0 shadow-sm text-center">
                <div class="card-body p-4">
                    {% if candidate_profile.profile_pic %}
                        <img src="{{ url_for('static', filename='uploads/' + candidate_profile.profile_pic) }}" alt="Profile" class="rounded-circle mb-3" style="width: 120px; height: 120px; object-fit: cover;">
                    {% else %}
                        <div class="bg-light rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center" style="width: 120px; height: 120px;">
                            <i class="bi bi-person" style="font-size: 3rem; color: #ccc;"></i>
                        </div>
                    {% endif %}
                    <h4>{{ candidate_user.name }}</h4>
                    <p class="text-muted mb-3">{{ candidate_user.email }}</p>
                    {% if candidate_profile.phone %}
                        <p class="mb-1"><i class="bi bi-telephone me-2"></i>{{ candidate_profile.phone }}</p>
                    {% endif %}
                    {% if candidate_profile.location %}
                        <p class="mb-3"><i class="bi bi-geo-alt me-2"></i>{{ candidate_profile.location }}</p>
                    {% endif %}

                    <form method="POST" action="{{ url_for('company.update_application_status', app_id=application.id) }}" class="d-grid gap-2">
                        <input type="hidden" name="status" value="shortlisted">
                        <button type="submit" class="btn btn-success">Shortlist Candidate</button>
                    </form>
                    <form method="POST" action="{{ url_for('company.update_application_status', app_id=application.id) }}" class="d-grid gap-2 mt-2">
                        <input type="hidden" name="status" value="rejected">
                        <button type="submit" class="btn btn-danger">Reject Candidate</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="col-lg-8">
            {% if candidate_profile.bio %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-3">About</h5>
                        <p>{{ candidate_profile.bio }}</p>
                    </div>
                </div>
            {% endif %}

            {% if candidate_profile.education %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">Education</h5>
                    </div>
                    <div class="card-body">
                        {% for edu in candidate_profile.education %}
                            <div class="mb-3 pb-3 border-bottom">
                                <h6>{{ edu.degree }}</h6>
                                <p class="text-muted mb-1">{{ edu.institution }} {% if edu.field %}• {{ edu.field }}{% endif %}</p>
                                <p class="text-muted small">
                                    {% if edu.start_year %}{{ edu.start_year }}{% endif %}
                                    {% if edu.end_year %} - {{ edu.end_year }}{% endif %}
                                </p>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}

            {% if candidate_profile.experience %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">Experience</h5>
                    </div>
                    <div class="card-body">
                        {% for exp in candidate_profile.experience %}
                            <div class="mb-3 pb-3 border-bottom">
                                <h6>{{ exp.role }} at {{ exp.company }}</h6>
                                <p class="text-muted small">
                                    {{ exp.start_date.strftime('%b %Y') }} -
                                    {% if exp.end_date %}{{ exp.end_date.strftime('%b %Y') }}{% else %}Present{% endif %}
                                </p>
                                {% if exp.description %}
                                    <p>{{ exp.description }}</p>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}

            {% if candidate_profile.skills %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">Skills</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-flex flex-wrap gap-2">
                            {% for skill in candidate_profile.skills %}
                                <span class="badge bg-light text-dark">{{ skill.skill_name }} ({{ skill.proficiency }})</span>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            {% endif %}

            {% if candidate_profile.projects %}
                <div class="card border-0 shadow-sm mb-4">
                    <div class="card-header bg-light">
                        <h5 class="mb-0">Projects</h5>
                    </div>
                    <div class="card-body">
                        {% for project in candidate_profile.projects %}
                            <div class="mb-3 pb-3 border-bottom">
                                <h6>{{ project.title }}</h6>
                                {% if project.description %}
                                    <p class="text-muted">{{ project.description }}</p>
                                {% endif %}
                                {% if project.link %}
                                    <a href="{{ project.link }}" target="_blank" class="btn btn-sm btn-outline-primary">View Project</a>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/company/dashboard.html,
          \${language}
{% extends "base.html" %}

{% block title %}Company Dashboard - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Company Dashboard</h1>

    <div class="row g-4 mb-5">
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Total Jobs</p>
                            <h3 class="mb-0">{{ stats.total_jobs }}</h3>
                        </div>
                        <i class="bi bi-briefcase" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Active Jobs</p>
                            <h3 class="mb-0">{{ stats.active_jobs }}</h3>
                        </div>
                        <i class="bi bi-lightning" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Applications</p>
                            <h3 class="mb-0">{{ stats.total_applications }}</h3>
                        </div>
                        <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card border-0 shadow-sm" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <p class="card-text opacity-75">Shortlisted</p>
                            <h3 class="mb-0">{{ stats.shortlisted }}</h3>
                        </div>
                        <i class="bi bi-star" style="font-size: 2rem;"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-8">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light border-bottom">
                    <h5 class="mb-0">Recent Job Postings</h5>
                </div>
                <div class="card-body">
                    {% if recent_jobs %}
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th>Job Title</th>
                                        <th>Status</th>
                                        <th>Posted</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for job in recent_jobs %}
                                        <tr>
                                            <td>{{ job.title }}</td>
                                            <td>
                                                <span class="badge bg-{% if job.status == 'active' %}success{% else %}secondary{% endif %}">
                                                    {{ job.status }}
                                                </span>
                                            </td>
                                            <td class="text-muted small">{{ job.posted_at.strftime('%b %d, %Y') }}</td>
                                            <td>
                                                <a href="{{ url_for('company.job_applications', job_id=job.id) }}" class="btn btn-sm btn-outline-primary">
                                                    View Apps
                                                </a>
                                            </td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted text-center py-4">No jobs posted yet. <a href="{{ url_for('company.post_job') }}">Post a job</a></p>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="card border-0 shadow-sm">
                <div class="card-header bg-light">
                    <h6 class="mb-0">Quick Actions</h6>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('company.post_job') }}" class="btn btn-primary">
                            <i class="bi bi-plus-lg me-2"></i>Post Job
                        </a>
                        <a href="{{ url_for('company.jobs') }}" class="btn btn-outline-primary">
                            <i class="bi bi-list me-2"></i>My Jobs
                        </a>
                        <a href="{{ url_for('company.profile') }}" class="btn btn-outline-primary">
                            <i class="bi bi-building me-2"></i>Company Profile
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/company/edit_job.html,
          \${language}
{% extends "base.html" %}

{% block title %}Edit Job - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Edit Job: {{ job.title }}</h1>

    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card border-0 shadow-sm">
                <div class="card-body p-5">
                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}

                        <div class="mb-3">
                            <label class="form-label">Job Title</label>
                            {{ form.title(class="form-control form-control-lg") }}
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Job Description</label>
                            {{ form.description(class="form-control", rows="6") }}
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Requirements</label>
                            {{ form.requirements(class="form-control", rows="4") }}
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Job Type</label>
                                {{ form.job_type(class="form-select") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Experience Required</label>
                                {{ form.experience_required(class="form-control") }}
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Salary Min</label>
                                {{ form.salary_min(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Salary Max</label>
                                {{ form.salary_max(class="form-control") }}
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Location</label>
                                {{ form.location(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Deadline</label>
                                {{ form.deadline(class="form-control") }}
                            </div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Required Skills</label>
                            {{ form.skills_required(class="form-control") }}
                        </div>

                        <div class="d-grid gap-2">
                            {{ form.submit(class="btn btn-primary btn-lg") }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/company/jobs.html,
          \${language}
{% extends "base.html" %}

{% block title %}My Jobs - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>My Jobs</h1>
        <a href="{{ url_for('company.post_job') }}" class="btn btn-primary">
            <i class="bi bi-plus-lg me-2"></i>Post New Job
        </a>
    </div>

    {% if jobs %}
        <div class="row g-3">
            {% for job in jobs %}
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-7">
                                    <h5 class="card-title mb-1">{{ job.title }}</h5>
                                    <p class="text-muted mb-2">
                                        <i class="bi bi-geo-alt me-1"></i>{{ job.location }}
                                    </p>
                                    <p class="text-muted small">
                                        Posted: {{ job.posted_at.strftime('%b %d, %Y') }}
                                    </p>
                                </div>
                                <div class="col-md-5">
                                    <div class="d-flex justify-content-end gap-2 align-items-center">
                                        <span class="badge bg-{% if job.status == 'active' %}success{% else %}secondary{% endif %}">
                                            {{ job.status }}
                                        </span>
                                        <span class="badge bg-info">
                                            {{ job.applications|length }} Applications
                                        </span>
                                        <div class="btn-group" role="group">
                                            <a href="{{ url_for('company.job_applications', job_id=job.id) }}" class="btn btn-sm btn-outline-primary">Applications</a>
                                            <a href="{{ url_for('company.edit_job', job_id=job.id) }}" class="btn btn-sm btn-outline-secondary">Edit</a>
                                            <form method="POST" action="{{ url_for('company.toggle_job_status', job_id=job.id) }}" style="display:inline;">
                                                <button type="submit" class="btn btn-sm btn-outline-warning">
                                                    {% if job.status == 'active' %}Close{% else %}Reopen{% endif %}
                                                </button>
                                            </form>
                                            <form method="POST" action="{{ url_for('company.delete_job', job_id=job.id) }}" style="display:inline;">
                                                <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete this job?')">Delete</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info text-center py-5">
            <h5>No jobs posted yet</h5>
            <p><a href="{{ url_for('company.post_job') }}">Post your first job</a></p>
        </div>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/company/job_applications.html,
          \${language}
{% extends "base.html" %}

{% block title %}Job Applications - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Applications for {{ job.title }}</h1>

    {% if applications %}
        <div class="row g-3">
            {% for app in applications %}
                <div class="col-12">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-7">
                                    <h5 class="card-title mb-1">{{ app.candidate.name }}</h5>
                                    <p class="text-muted mb-2">
                                        <i class="bi bi-envelope me-1"></i>{{ app.candidate.email }}
                                    </p>
                                    <p class="text-muted small">
                                        Applied: {{ app.applied_at.strftime('%B %d, %Y') }}
                                    </p>
                                </div>
                                <div class="col-md-5">
                                    <div class="d-flex justify-content-end gap-2 align-items-center">
                                        <span class="badge bg-{% if app.status == 'hired' %}success{% elif app.status == 'shortlisted' %}info{% elif app.status == 'rejected' %}danger{% else %}secondary{% endif %}">
                                            {{ app.status }}
                                        </span>
                                        <div class="btn-group" role="group">
                                            <a href="{{ url_for('company.view_candidate', app_id=app.id) }}" class="btn btn-sm btn-outline-primary">View Profile</a>
                                            <div class="btn-group dropstart" role="group">
                                                <button id="btnGroupDrop{{ app.id }}" type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                                                    Update Status
                                                </button>
                                                <ul class="dropdown-menu" aria-labelledby="btnGroupDrop{{ app.id }}">
                                                    <li>
                                                        <form method="POST" action="{{ url_for('company.update_application_status', app_id=app.id) }}" style="display:inline;">
                                                            <input type="hidden" name="status" value="shortlisted">
                                                            <button type="submit" class="dropdown-item">Shortlist</button>
                                                        </form>
                                                    </li>
                                                    <li>
                                                        <form method="POST" action="{{ url_for('company.update_application_status', app_id=app.id) }}" style="display:inline;">
                                                            <input type="hidden" name="status" value="rejected">
                                                            <button type="submit" class="dropdown-item">Reject</button>
                                                        </form>
                                                    </li>
                                                    <li>
                                                        <form method="POST" action="{{ url_for('company.update_application_status', app_id=app.id) }}" style="display:inline;">
                                                            <input type="hidden" name="status" value="hired">
                                                            <button type="submit" class="dropdown-item">Hire</button>
                                                        </form>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info text-center py-5">
            <h5>No applications yet</h5>
            <p>Applicants will appear here once they apply for this job.</p>
        </div>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/company/post_job.html,
          \${language}
{% extends "base.html" %}

{% block title %}Post a Job - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Post a New Job</h1>

    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card border-0 shadow-sm">
                <div class="card-body p-5">
                    <form method="POST" novalidate>
                        {{ form.hidden_tag() }}

                        <div class="mb-4">
                            <h5>Job Details</h5>
                            <div class="mb-3">
                                <label class="form-label">Job Title</label>
                                {{ form.title(class="form-control form-control-lg") }}
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="form-label">Job Description</label>
                            {{ form.description(class="form-control", rows="6") }}
                            <small class="text-muted">Describe the role, responsibilities, and what you're looking for.</small>
                        </div>

                        <div class="mb-4">
                            <label class="form-label">Requirements</label>
                            {{ form.requirements(class="form-control", rows="4") }}
                            <small class="text-muted">List key requirements and qualifications.</small>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Job Type</label>
                                {{ form.job_type(class="form-select form-select-lg") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Experience Required</label>
                                {{ form.experience_required(class="form-control") }}
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Salary Min</label>
                                {{ form.salary_min(class="form-control", placeholder="$") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Salary Max</label>
                                {{ form.salary_max(class="form-control", placeholder="$") }}
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Location</label>
                                {{ form.location(class="form-control") }}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Application Deadline</label>
                                {{ form.deadline(class="form-control") }}
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="form-label">Required Skills (comma-separated)</label>
                            {{ form.skills_required(class="form-control") }}
                            <small class="text-muted">e.g., Python, React, AWS, SQL</small>
                        </div>

                        <div class="d-grid gap-2">
                            {{ form.submit(class="btn btn-primary btn-lg") }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/company/profile.html,
          \${language}
{% extends "base.html" %}

{% block title %}Company Profile - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Company Profile</h1>

    <div class="card border-0 shadow-sm">
        <div class="card-header bg-light border-bottom">
            <h5 class="mb-0">Company Information</h5>
        </div>
        <div class="card-body p-5">
            <form method="POST" enctype="multipart/form-data">
                {{ form.hidden_tag() }}

                <div class="mb-4 text-center">
                    {% if company.logo %}
                        <img src="{{ url_for('static', filename='uploads/' + company.logo) }}" alt="Logo" class="img-fluid mb-3" style="max-height: 150px;">
                    {% endif %}
                    <div>
                        <label class="form-label">Company Logo</label>
                        <input type="file" class="form-control" name="logo" accept="image/*">
                        <small class="text-muted">PNG, JPG or GIF (Max 5MB)</small>
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label">Company Name</label>
                    {{ form.company_name(class="form-control") }}
                </div>

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Industry</label>
                        {{ form.industry(class="form-control") }}
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Company Size</label>
                        {{ form.size(class="form-select") }}
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Location</label>
                        {{ form.location(class="form-control") }}
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Website</label>
                        {{ form.website(class="form-control") }}
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label">Description</label>
                    {{ form.description(class="form-control", rows="5") }}
                </div>

                {{ form.submit(class="btn btn-primary btn-lg") }}
            </form>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/index.html,
          \${language}
{% extends "base.html" %}

{% block title %}NextOffer - Land Your Dream Job{% endblock %}

{% block content %}
<div class="hero-section py-5" style="background: linear-gradient(135deg, #f5f7fa 0%, #e8f0ff 100%); position: relative; overflow: hidden;">
    <!-- Decorative Elements -->
    <div style="position: absolute; top: -50px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(5, 74, 218, 0.1) 0%, transparent 70%); border-radius: 50%;"></div>
    <div style="position: absolute; bottom: -100px; left: -100px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(255, 153, 0, 0.08) 0%, transparent 70%); border-radius: 50%;"></div>

    <div class="container py-5" style="position: relative; z-index: 1;">
        <div class="row align-items-center">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <h1 class="display-4 fw-bold mb-3" style="color: #054ADA;">Land Your Dream Job</h1>
                <p class="lead mb-4" style="color: #4267B2; font-size: 1.25rem;">Discover opportunities from top companies and showcase your skills to the world.</p>
                {% if not current_user.is_authenticated %}
                    <div class="btn-group gap-3">
                        <a href="{{ url_for('main.browse_jobs') }}" class="btn btn-primary btn-lg">
                            <i class="bi bi-search me-2"></i>Find Jobs
                        </a>
                        <a href="{{ url_for('auth.register_candidate') }}" class="btn btn-success btn-lg">
                            <i class="bi bi-person-plus me-2"></i>Join Now
                        </a>
                    </div>
                {% else %}
                    <a href="{{ url_for('main.browse_jobs') }}" class="btn btn-primary btn-lg">
                        <i class="bi bi-search me-2"></i>Browse Jobs
                    </a>
                {% endif %}
            </div>
            <div class="col-lg-6">
                <form class="search-form" method="get" action="{{ url_for('main.browse_jobs') }}" class="mb-0">
                    <div class="input-group input-group-lg">
                        <input type="text" class="form-control" name="search" placeholder="Job title, keywords..." style="border: 2px solid #054ADA;">
                        <button class="btn btn-primary" type="submit">
                            <i class="bi bi-search"></i>Search
                        </button>
                    </div>
                    <small class="text-muted d-block mt-2"><i class="bi bi-info-circle me-1"></i>Search across 100+ job listings</small>
                </form>
            </div>
        </div>
    </div>
</div>

<section class="py-5">
    <div class="container">
        <h2 class="text-center mb-5">Platform Stats</h2>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card text-center border-0 shadow-sm" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%); color: white;">
                    <div class="card-body p-4">
                        <h3 class="card-title display-6">{{ total_jobs }}</h3>
                        <p class="card-text">Active Job Postings</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center border-0 shadow-sm" style="background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%); color: white;">
                    <div class="card-body p-4">
                        <h3 class="card-title display-6">{{ total_companies }}</h3>
                        <p class="card-text">Hiring Companies</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center border-0 shadow-sm" style="background: linear-gradient(135deg, #4267B2 0%, #054ADA 100%); color: white;">
                    <div class="card-body p-4">
                        <h3 class="card-title display-6">1000+</h3>
                        <p class="card-text">Success Stories</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="py-5 bg-light">
    <div class="container">
        <h2 class="text-center mb-5">Featured Job Opportunities</h2>
        <div class="row g-4">
            {% for job in featured_jobs %}
                <div class="col-lg-6">
                    <div class="card border-0 shadow-sm h-100 hover-card">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h5 class="card-title">{{ job.title }}</h5>
                                    <p class="text-muted mb-0">
                                        <i class="bi bi-building me-1"></i>{{ job.company.company_name }}
                                    </p>
                                </div>
                                <span class="badge bg-primary">{{ job.job_type }}</span>
                            </div>
                            <p class="card-text small text-muted mb-2">
                                <i class="bi bi-geo-alt me-1"></i>{{ job.location }}
                            </p>
                            <p class="card-text text-truncate">{{ job.description[:100] }}...</p>
                            <div class="d-flex justify-content-between align-items-center">
                                {% if job.salary_min and job.salary_max %}
                                    <small class="text-muted">
                                        ${{ "{:,.0f}".format(job.salary_min) }} - ${{ "{:,.0f}".format(job.salary_max) }}
                                    </small>
                                {% endif %}
                                <a href="{{ url_for('main.job_detail', job_id=job.id) }}" class="btn btn-sm btn-outline-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
        <div class="text-center mt-5">
            <a href="{{ url_for('main.browse_jobs') }}" class="btn btn-primary btn-lg">View All Jobs</a>
        </div>
    </div>
</section>

<section class="py-5">
    <div class="container">
        <h2 class="text-center mb-5">How It Works</h2>
        <div class="row g-4">
            <div class="col-lg-6 mb-4">
                <h4 class="mb-4">For Candidates</h4>
                <div class="row g-3">
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-primary rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">1</div>
                            <div>
                                <h6>Create Your Profile</h6>
                                <p class="text-muted small">Build a comprehensive profile showcasing your skills and experience.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-primary rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">2</div>
                            <div>
                                <h6>Browse & Apply</h6>
                                <p class="text-muted small">Search through thousands of job openings and apply with a single click.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-primary rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">3</div>
                            <div>
                                <h6>Get Hired</h6>
                                <p class="text-muted small">Connect with employers and land your dream job today.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <h4 class="mb-4">For Companies</h4>
                <div class="row g-3">
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-success rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">1</div>
                            <div>
                                <h6>Post a Job</h6>
                                <p class="text-muted small">Create a job posting and reach thousands of qualified candidates.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-success rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">2</div>
                            <div>
                                <h6>Review Applications</h6>
                                <p class="text-muted small">Shortlist and review applicants directly through our platform.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="d-flex gap-3">
                            <div class="badge bg-success rounded-pill" style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">3</div>
                            <div>
                                <h6>Hire Top Talent</h6>
                                <p class="text-muted small">Make offers and manage the hiring process efficiently.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="py-5 bg-light">
    <div class="container text-center">
        <h2 class="mb-4">Ready to Get Started?</h2>
        <div class="btn-group gap-3">
            {% if not current_user.is_authenticated %}
                <a href="{{ url_for('auth.register_candidate') }}" class="btn btn-primary btn-lg">
                    <i class="bi bi-person-check me-2"></i>Apply for Jobs
                </a>
                <a href="{{ url_for('auth.register_company') }}" class="btn btn-success btn-lg">
                    <i class="bi bi-briefcase me-2"></i>Post a Job
                </a>
            {% else %}
                <a href="{{ url_for('main.browse_jobs') }}" class="btn btn-primary btn-lg">
                    <i class="bi bi-search me-2"></i>Browse Jobs
                </a>
            {% endif %}
        </div>
    </div>
</section>
{% endblock %}
```
---


          # app/templates/jobs/browse.html,
          \${language}
{% extends "base.html" %}

{% block title %}Browse Jobs - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <h1 class="mb-4">Browse Job Opportunities</h1>

    <div class="row mb-4">
        <div class="col-md-12">
            <form method="get" action="{{ url_for('main.browse_jobs') }}" class="row g-3">
                <div class="col-md-4">
                    <input type="text" class="form-control" name="search" placeholder="Job title or keywords" value="{{ search }}">
                </div>
                <div class="col-md-3">
                    <input type="text" class="form-control" name="location" placeholder="Location" value="{{ location }}">
                </div>
                <div class="col-md-3">
                    <select class="form-select" name="job_type">
                        <option value="">All Types</option>
                        <option value="full-time" {% if job_type == 'full-time' %}selected{% endif %}>Full-time</option>
                        <option value="part-time" {% if job_type == 'part-time' %}selected{% endif %}>Part-time</option>
                        <option value="internship" {% if job_type == 'internship' %}selected{% endif %}>Internship</option>
                        <option value="remote" {% if job_type == 'remote' %}selected{% endif %}>Remote</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary w-100">Search</button>
                </div>
            </form>
        </div>
    </div>

    {% if jobs.items %}
        <div class="row g-4">
            {% for job in jobs.items %}
                <div class="col-12">
                    <div class="card border-0 shadow-sm hover-card">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <h5 class="card-title mb-1">{{ job.title }}</h5>
                                    <p class="text-muted mb-2">
                                        <i class="bi bi-building me-1"></i>{{ job.company.company_name }}
                                    </p>
                                    <p class="card-text mb-2">{{ job.description[:150] }}...</p>
                                    <div class="mb-2">
                                        <span class="badge bg-info">{{ job.job_type }}</span>
                                        <span class="badge bg-secondary">{{ job.experience_required or 'Not specified' }}</span>
                                    </div>
                                </div>
                                <div class="col-md-4 text-md-end">
                                    <p class="text-muted mb-2">
                                        <i class="bi bi-geo-alt me-1"></i>{{ job.location }}
                                    </p>
                                    {% if job.salary_min and job.salary_max %}
                                        <p class="fw-bold mb-3">
                                            ${{ "{:,.0f}".format(job.salary_min) }} - ${{ "{:,.0f}".format(job.salary_max) }}
                                        </p>
                                    {% endif %}
                                    <a href="{{ url_for('main.job_detail', job_id=job.id) }}" class="btn btn-primary">View Details</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>

        {% if jobs.pages > 1 %}
            <nav aria-label="Page navigation" class="mt-5">
                <ul class="pagination justify-content-center">
                    {% if jobs.has_prev %}
                        <li class="page-item">
                            <a class="page-link" href="{{ url_for('main.browse_jobs', page=jobs.prev_num, search=search, location=location, job_type=job_type) }}">Previous</a>
                        </li>
                    {% endif %}

                    {% for page_num in jobs.iter_pages() %}
                        {% if page_num %}
                            {% if page_num == jobs.page %}
                                <li class="page-item active"><span class="page-link">{{ page_num }}</span></li>
                            {% else %}
                                <li class="page-item">
                                    <a class="page-link" href="{{ url_for('main.browse_jobs', page=page_num, search=search, location=location, job_type=job_type) }}">{{ page_num }}</a>
                                </li>
                            {% endif %}
                        {% endif %}
                    {% endfor %}

                    {% if jobs.has_next %}
                        <li class="page-item">
                            <a class="page-link" href="{{ url_for('main.browse_jobs', page=jobs.next_num, search=search, location=location, job_type=job_type) }}">Next</a>
                        </li>
                    {% endif %}
                </ul>
            </nav>
        {% endif %}
    {% else %}
        <div class="alert alert-info text-center py-5">
            <h5>No jobs found</h5>
            <p>Try adjusting your search criteria.</p>
        </div>
    {% endif %}
</div>
{% endblock %}
```
---


          # app/templates/jobs/detail.html,
          \${language}
{% extends "base.html" %}

{% block title %}{{ job.title }} - NextOffer{% endblock %}

{% block content %}
<div class="container py-5">
    <div class="row">
        <div class="col-lg-8">
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-body p-5">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <div>
                            <h1 class="mb-2">{{ job.title }}</h1>
                            <p class="text-muted mb-0">
                                <i class="bi bi-building me-1"></i><strong>{{ job.company.company_name }}</strong>
                            </p>
                        </div>
                        <span class="badge bg-primary fs-6">{{ job.job_type }}</span>
                    </div>

                    <hr>

                    <div class="row mb-4">
                        <div class="col-md-6">
                            <p class="mb-3">
                                <i class="bi bi-geo-alt me-2"></i><strong>Location:</strong> {{ job.location }}
                            </p>
                            <p class="mb-3">
                                <i class="bi bi-clock me-2"></i><strong>Experience:</strong> {{ job.experience_required or 'Not specified' }}
                            </p>
                        </div>
                        <div class="col-md-6">
                            {% if job.salary_min and job.salary_max %}
                                <p class="mb-3">
                                    <i class="bi bi-cash-coin me-2"></i><strong>Salary:</strong> ${{ "{:,.0f}".format(job.salary_min) }} - ${{ "{:,.0f}".format(job.salary_max) }}
                                </p>
                            {% endif %}
                            {% if job.deadline %}
                                <p class="mb-3">
                                    <i class="bi bi-calendar me-2"></i><strong>Deadline:</strong> {{ job.deadline.strftime('%B %d, %Y') }}
                                </p>
                            {% endif %}
                        </div>
                    </div>

                    <h3 class="mb-3">Job Description</h3>
                    <p class="mb-4">{{ job.description }}</p>

                    {% if job.requirements %}
                        <h3 class="mb-3">Requirements</h3>
                        <p class="mb-4">{{ job.requirements }}</p>
                    {% endif %}

                    {% if job.skills_required %}
                        <h3 class="mb-3">Required Skills</h3>
                        <div class="mb-4">
                            {% for skill in job.skills_required.split(',') %}
                                <span class="badge bg-light text-dark me-2 mb-2">{{ skill.strip() }}</span>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="card border-0 shadow-sm sticky-top" style="top: 100px;">
                <div class="card-body">
                    <h5 class="card-title mb-4">Company Information</h5>
                    {% if job.company.logo %}
                        <img src="{{ url_for('static', filename='uploads/' + job.company.logo) }}" alt="{{ job.company.company_name }}" class="img-fluid mb-3" style="max-height: 100px;">
                    {% else %}
                        <div class="bg-light p-4 text-center mb-3 rounded">
                            <i class="bi bi-building" style="font-size: 3rem; color: #ccc;"></i>
                        </div>
                    {% endif %}

                    {% if job.company.description %}
                        <p class="text-muted small mb-3">{{ job.company.description }}</p>
                    {% endif %}

                    {% if job.company.website %}
                        <p class="mb-2">
                            <i class="bi bi-globe me-2"></i>
                            <a href="{{ job.company.website }}" target="_blank">{{ job.company.website }}</a>
                        </p>
                    {% endif %}

                    {% if job.company.location %}
                        <p class="mb-4">
                            <i class="bi bi-geo-alt me-2"></i>{{ job.company.location }}
                        </p>
                    {% endif %}

                    {% if current_user.is_authenticated and current_user.role == 'candidate' %}
                        <a href="{{ url_for('candidate.apply_job', job_id=job.id) }}" class="btn btn-primary w-100">
                            <i class="bi bi-send me-2"></i>Apply Now
                        </a>
                    {% elif current_user.is_authenticated and current_user.role == 'company' %}
                        <p class="text-muted text-center">This is your job posting</p>
                    {% else %}
                        <a href="{{ url_for('auth.login') }}" class="btn btn-primary w-100">
                            Login to Apply
                        </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/resume/builder.html,
          \${language}
{% extends "base.html" %}

{% block title %}Resume Builder - NextOffer{% endblock %}

{% block content %}
<div class="container-fluid py-5">
    <div class="container mb-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="mb-2">Resume Builder</h1>
                <p class="text-muted">Create and download your professional resume in minutes</p>
            </div>
            <a href="{{ url_for('candidate.dashboard') }}" class="btn btn-outline-primary">
                <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
            </a>
        </div>
    </div>

    <div class="container mb-5">
        <h4 class="mb-4">Select a Template</h4>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card border-0 shadow-sm cursor-pointer hover-card h-100">
                    <div class="card-body text-center p-4">
                        <div class="bg-light p-5 mb-3 rounded">
                            <i class="bi bi-file-earmark" style="font-size: 4rem; color: #054ADA;"></i>
                        </div>
                        <h5 class="card-title">Classic</h5>
                        <p class="card-text text-muted">Clean, professional, ATS-friendly</p>
                        <div class="d-grid gap-2">
                            <a href="{{ url_for('resume.preview', template='classic') }}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-eye me-1"></i>Preview
                            </a>
                            <a href="{{ url_for('resume.download', template='classic') }}" class="btn btn-success btn-sm">
                                <i class="bi bi-download me-1"></i>Download PDF
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm cursor-pointer hover-card h-100">
                    <div class="card-body text-center p-4">
                        <div class="bg-light p-5 mb-3 rounded" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%);"></div>
                        <h5 class="card-title">Modern</h5>
                        <p class="card-text text-muted">Sidebar layout with color accent</p>
                        <div class="d-grid gap-2">
                            <a href="{{ url_for('resume.preview', template='modern') }}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-eye me-1"></i>Preview
                            </a>
                            <a href="{{ url_for('resume.download', template='modern') }}" class="btn btn-success btn-sm">
                                <i class="bi bi-download me-1"></i>Download PDF
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card border-0 shadow-sm cursor-pointer hover-card h-100">
                    <div class="card-body text-center p-4">
                        <div class="bg-light p-5 mb-3 rounded" style="background: linear-gradient(135deg, #FF9900 0%, #e68a00 100%);"></div>
                        <h5 class="card-title">Creative</h5>
                        <p class="card-text text-muted">Bold header with timeline layout</p>
                        <div class="d-grid gap-2">
                            <a href="{{ url_for('resume.preview', template='creative') }}" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-eye me-1"></i>Preview
                            </a>
                            <a href="{{ url_for('resume.download', template='creative') }}" class="btn btn-success btn-sm">
                                <i class="bi bi-download me-1"></i>Download PDF
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="card border-0 shadow-sm">
            <div class="card-header" style="background: linear-gradient(135deg, #054ADA 0%, #4267B2 100%); color: white;">
                <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>Your Profile Data</h5>
            </div>
            <div class="card-body">
                <div class="row g-4">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <strong><i class="bi bi-person me-2" style="color: #054ADA;"></i>Name:</strong><br>
                            <span class="text-muted">{{ resume_data.name }}</span>
                        </div>
                        <div class="mb-3">
                            <strong><i class="bi bi-envelope me-2" style="color: #054ADA;"></i>Email:</strong><br>
                            <span class="text-muted">{{ resume_data.email }}</span>
                        </div>
                        <div class="mb-3">
                            <strong><i class="bi bi-telephone me-2" style="color: #054ADA;"></i>Phone:</strong><br>
                            <span class="text-muted">{{ resume_data.phone or 'Not provided' }}</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <strong><i class="bi bi-geo-alt me-2" style="color: #054ADA;"></i>Location:</strong><br>
                            <span class="text-muted">{{ resume_data.location or 'Not provided' }}</span>
                        </div>
                        <div class="mb-3">
                            <strong><i class="bi bi-book me-2" style="color: #054ADA;"></i>Education Entries:</strong><br>
                            <span class="text-muted">{{ resume_data.education|length }}</span>
                        </div>
                        <div class="mb-3">
                            <strong><i class="bi bi-briefcase me-2" style="color: #054ADA;"></i>Experience Entries:</strong><br>
                            <span class="text-muted">{{ resume_data.experience|length }}</span>
                        </div>
                    </div>
                </div>
                <div class="divider"></div>
                <a href="{{ url_for('candidate.profile') }}" class="btn btn-primary">
                    <i class="bi bi-pencil me-2"></i>Update Profile
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---


          # app/templates/resume/templates/classic_resume.html,
          \${language}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.5;
            color: #333;
            font-size: 11pt;
        }
        .container {
            max-width: 8.5in;
            height: 11in;
            margin: 0 auto;
            padding: 0.5in;
        }
        .header {
            text-align: center;
            border-bottom: 3px solid #0A1628;
            padding-bottom: 0.3in;
            margin-bottom: 0.3in;
        }
        .name {
            font-size: 24pt;
            font-weight: bold;
            color: #0A1628;
        }
        .contact-info {
            font-size: 10pt;
            color: #666;
        }
        .contact-info span {
            margin: 0 10px;
        }
        .section {
            margin-bottom: 0.2in;
        }
        .section-title {
            font-size: 12pt;
            font-weight: bold;
            color: #0A1628;
            border-bottom: 2px solid #0A1628;
            padding-bottom: 0.1in;
            margin-bottom: 0.15in;
            text-transform: uppercase;
        }
        .entry {
            margin-bottom: 0.15in;
        }
        .entry-title {
            font-weight: bold;
            font-size: 11pt;
        }
        .entry-subtitle {
            font-style: italic;
            color: #666;
            font-size: 10pt;
        }
        .entry-description {
            font-size: 10pt;
            margin-top: 0.05in;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        td {
            padding: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="name">{{ resume_data.name }}</div>
            <div class="contact-info">
                <span>{{ resume_data.email }}</span>
                {% if resume_data.phone %}<span>{{ resume_data.phone }}</span>{% endif %}
                {% if resume_data.location %}<span>{{ resume_data.location }}</span>{% endif %}
            </div>
        </div>

        {% if resume_data.bio %}
            <div class="section">
                <div class="section-title">Professional Summary</div>
                <div class="entry-description">{{ resume_data.bio }}</div>
            </div>
        {% endif %}

        {% if resume_data.experience %}
            <div class="section">
                <div class="section-title">Experience</div>
                {% for exp in resume_data.experience %}
                    <div class="entry">
                        <div class="entry-title">{{ exp.role }}</div>
                        <div class="entry-subtitle">{{ exp.company }} | {{ exp.start_date.strftime('%b %Y') }} - {% if exp.end_date %}{{ exp.end_date.strftime('%b %Y') }}{% else %}Present{% endif %}</div>
                        {% if exp.description %}
                            <div class="entry-description">{{ exp.description }}</div>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% if resume_data.education %}
            <div class="section">
                <div class="section-title">Education</div>
                {% for edu in resume_data.education %}
                    <div class="entry">
                        <div class="entry-title">{{ edu.degree }}{% if edu.field %} in {{ edu.field }}{% endif %}</div>
                        <div class="entry-subtitle">{{ edu.institution }}{% if edu.start_year %} | {{ edu.start_year }}{% if edu.end_year %}-{{ edu.end_year }}{% endif %}{% endif %}</div>
                        {% if edu.grade %}<div class="entry-description">GPA: {{ edu.grade }}</div>{% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% if resume_data.skills %}
            <div class="section">
                <div class="section-title">Skills</div>
                <table>
                    <tr>
                        {% for skill in resume_data.skills %}
                            {% if loop.index0 % 3 == 0 and loop.index0 != 0 %}</tr><tr>{% endif %}
                            <td>• {{ skill.skill_name }} ({{ skill.proficiency }})</td>
                        {% endfor %}
                    </tr>
                </table>
            </div>
        {% endif %}

        {% if resume_data.projects %}
            <div class="section">
                <div class="section-title">Projects</div>
                {% for project in resume_data.projects %}
                    <div class="entry">
                        <div class="entry-title">{{ project.title }}</div>
                        {% if project.description %}<div class="entry-description">{{ project.description }}</div>{% endif %}
                        {% if project.tech_used %}<div class="entry-description"><strong>Tech:</strong> {{ project.tech_used }}</div>{% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% if resume_data.awards %}
            <div class="section">
                <div class="section-title">Awards & Achievements</div>
                {% for award in resume_data.awards %}
                    <div class="entry">
                        <div class="entry-title">{{ award.title }}</div>
                        <div class="entry-subtitle">{{ award.issuer }}{% if award.date %} | {{ award.date.strftime('%b %Y') }}{% endif %}</div>
                        {% if award.description %}<div class="entry-description">{{ award.description }}</div>{% endif %}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
```
---


          # app/templates/resume/templates/creative_resume.html,
          \${language}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
        }
        .container {
            max-width: 8.5in;
            height: 11in;
            margin: 0 auto;
            padding: 0.5in;
        }
        .header {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 0.3in;
            margin-bottom: 0.3in;
            border-radius: 0.1in;
        }
        .name {
            font-size: 26pt;
            font-weight: bold;
            margin-bottom: 0.05in;
        }
        .contact-info {
            font-size: 10pt;
            opacity: 0.95;
        }
        .contact-info span {
            margin-right: 15px;
        }
        .section {
            margin-bottom: 0.25in;
        }
        .section-title {
            font-size: 12pt;
            font-weight: bold;
            color: #d97706;
            border-bottom: 3px solid #f59e0b;
            padding-bottom: 0.08in;
            margin-bottom: 0.12in;
            text-transform: uppercase;
            letter-spacing: 1pt;
        }
        .timeline-item {
            display: flex;
            margin-bottom: 0.15in;
            padding-left: 0.2in;
            border-left: 3px solid #f59e0b;
        }
        .timeline-content {
            flex: 1;
            padding-left: 0.15in;
        }
        .timeline-title {
            font-weight: bold;
            font-size: 11pt;
            color: #d97706;
        }
        .timeline-subtitle {
            font-size: 10pt;
            color: #666;
            margin-bottom: 0.03in;
        }
        .timeline-description {
            font-size: 10pt;
            margin-bottom: 0.05in;
        }
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.1in;
        }
        .skill-tag {
            background-color: #fef3c7;
            color: #92400e;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 9pt;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="name">{{ resume_data.name }}</div>
            <div class="contact-info">
                <span>{{ resume_data.email }}</span>
                {% if resume_data.phone %}<span>{{ resume_data.phone }}</span>{% endif %}
                {% if resume_data.location %}<span>{{ resume_data.location }}</span>{% endif %}
            </div>
        </div>

        {% if resume_data.bio %}
            <div class="section">
                <div class="section-title">Professional Summary</div>
                <div>{{ resume_data.bio }}</div>
            </div>
        {% endif %}

        {% if resume_data.experience %}
            <div class="section">
                <div class="section-title">Experience</div>
                {% for exp in resume_data.experience %}
                    <div class="timeline-item">
                        <div class="timeline-content">
                            <div class="timeline-title">{{ exp.role }}</div>
                            <div class="timeline-subtitle">{{ exp.company }}</div>
                            <div class="timeline-subtitle">{{ exp.start_date.strftime('%b %Y') }} - {% if exp.end_date %}{{ exp.end_date.strftime('%b %Y') }}{% else %}Present{% endif %}</div>
                            {% if exp.description %}<div class="timeline-description">{{ exp.description }}</div>{% endif %}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% if resume_data.education %}
            <div class="section">
                <div class="section-title">Education</div>
                {% for edu in resume_data.education %}
                    <div class="timeline-item">
                        <div class="timeline-content">
                            <div class="timeline-title">{{ edu.degree }}{% if edu.field %} in {{ edu.field }}{% endif %}</div>
                            <div class="timeline-subtitle">{{ edu.institution }}</div>
                            {% if edu.start_year %}<div class="timeline-subtitle">{{ edu.start_year }}{% if edu.end_year %} - {{ edu.end_year }}{% endif %}</div>{% endif %}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}

        {% if resume_data.skills %}
            <div class="section">
                <div class="section-title">Skills</div>
                <div class="skills-grid">
                    {% for skill in resume_data.skills %}
                        <span class="skill-tag">{{ skill.skill_name }}</span>
                    {% endfor %}
                </div>
            </div>
        {% endif %}

        {% if resume_data.projects %}
            <div class="section">
                <div class="section-title">Projects</div>
                {% for project in resume_data.projects %}
                    <div class="timeline-item">
                        <div class="timeline-content">
                            <div class="timeline-title">{{ project.title }}</div>
                            {% if project.description %}<div class="timeline-description">{{ project.description }}</div>{% endif %}
                            {% if project.tech_used %}<div class="timeline-description"><strong>Tech:</strong> {{ project.tech_used }}</div>{% endif %}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
```
---


          # app/templates/resume/templates/modern_resume.html,
          \${language}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'Arial', sans-serif;
            line-height: 1.5;
            color: #333;
            font-size: 11pt;
        }
        .page {
            max-width: 8.5in;
            height: 11in;
            margin: 0 auto;
            display: flex;
        }
        .sidebar {
            width: 2.5in;
            background-color: #0A1628;
            color: white;
            padding: 0.4in;
            font-size: 10pt;
        }
        .content {
            flex: 1;
            padding: 0.4in;
            padding-left: 0.3in;
        }
        .sidebar-section-title {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            border-bottom: 2px solid #2563EB;
            padding-bottom: 0.05in;
        }
        .sidebar-item {
            margin-bottom: 0.1in;
        }
        .sidebar-item-title {
            font-weight: bold;
            font-size: 10pt;
        }
        .header {
            margin-bottom: 0.3in;
            border-bottom: 3px solid #2563EB;
            padding-bottom: 0.2in;
        }
        .name {
            font-size: 22pt;
            font-weight: bold;
            color: #0A1628;
        }
        .contact {
            font-size: 9pt;
            color: #666;
        }
        .section-title {
            font-size: 12pt;
            font-weight: bold;
            color: #0A1628;
            border-bottom: 2px solid #2563EB;
            padding-bottom: 0.08in;
            margin-bottom: 0.12in;
            margin-top: 0.15in;
        }
        .entry {
            margin-bottom: 0.12in;
        }
        .entry-title {
            font-weight: bold;
            font-size: 11pt;
        }
        .entry-subtitle {
            font-size: 10pt;
            color: #666;
        }
        .entry-description {
            font-size: 10pt;
            margin-top: 0.03in;
        }
    </style>
</head>
<body>
    <div class="page">
        <div class="sidebar">
            <div style="text-align: center; margin-bottom: 0.2in;">
                <div style="font-size: 18pt; font-weight: bold;">{{ resume_data.name[0] }}</div>
            </div>

            {% if resume_data.phone or resume_data.email or resume_data.location %}
                <div class="sidebar-section-title">✉ Contact</div>
                {% if resume_data.email %}<div class="sidebar-item">{{ resume_data.email }}</div>{% endif %}
                {% if resume_data.phone %}<div class="sidebar-item">{{ resume_data.phone }}</div>{% endif %}
                {% if resume_data.location %}<div class="sidebar-item">{{ resume_data.location }}</div>{% endif %}
            {% endif %}

            {% if resume_data.skills %}
                <div class="sidebar-section-title">⭐ Skills</div>
                {% for skill in resume_data.skills %}
                    <div class="sidebar-item">
                        <div class="sidebar-item-title">{{ skill.skill_name }}</div>
                        <div style="font-size: 9pt; color: #bbb;">{{ skill.proficiency }}</div>
                    </div>
                {% endfor %}
            {% endif %}
        </div>

        <div class="content">
            <div class="header">
                <div class="name">{{ resume_data.name }}</div>
                <div class="contact">{{ resume_data.email }} | {% if resume_data.location %}{{ resume_data.location }}{% endif %}</div>
            </div>

            {% if resume_data.bio %}
                <div>
                    <div class="section-title">About</div>
                    <div class="entry-description">{{ resume_data.bio }}</div>
                </div>
            {% endif %}

            {% if resume_data.experience %}
                <div>
                    <div class="section-title">Experience</div>
                    {% for exp in resume_data.experience %}
                        <div class="entry">
                            <div class="entry-title">{{ exp.role }}</div>
                            <div class="entry-subtitle">{{ exp.company }} | {{ exp.start_date.strftime('%b %Y') }} - {% if exp.end_date %}{{ exp.end_date.strftime('%b %Y') }}{% else %}Present{% endif %}</div>
                            {% if exp.description %}<div class="entry-description">{{ exp.description }}</div>{% endif %}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            {% if resume_data.education %}
                <div>
                    <div class="section-title">Education</div>
                    {% for edu in resume_data.education %}
                        <div class="entry">
                            <div class="entry-title">{{ edu.degree }}{% if edu.field %} in {{ edu.field }}{% endif %}</div>
                            <div class="entry-subtitle">{{ edu.institution }}</div>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            {% if resume_data.projects %}
                <div>
                    <div class="section-title">Projects</div>
                    {% for project in resume_data.projects %}
                        <div class="entry">
                            <div class="entry-title">{{ project.title }}</div>
                            {% if project.description %}<div class="entry-description">{{ project.description }}</div>{% endif %}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
```
---


          # app/utils.py,
          \${language}
import os
import uuid
from werkzeug.utils import secure_filename
from app.models import db, User, Company, Job, CandidateProfile
from datetime import datetime, timedelta


ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4()}_{filename}"
        file.save(os.path.join(upload_folder, unique_name))
        return unique_name
    return None


def seed_database():
    if User.query.filter_by(email='admin@nf.com').first():
        return

    # Create admin user
    admin = User(
        name='Admin User',
        email='admin@nf.com',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # Create sample companies
    company1_user = User(
        name='Tech Innovations Inc',
        email='company1@nextoffer.com',
        role='company'
    )
    company1_user.set_password('company123')
    db.session.add(company1_user)
    db.session.flush()

    company1 = Company(
        user_id=company1_user.id,
        company_name='Tech Innovations Inc',
        industry='Information Technology',
        website='https://techinnovations.com',
        description='Leading tech company focusing on cloud solutions and AI',
        location='San Francisco, CA',
        size='500-1000'
    )
    db.session.add(company1)

    company2_user = User(
        name='Global Finance Corp',
        email='company2@nextoffer.com',
        role='company'
    )
    company2_user.set_password('company123')
    db.session.add(company2_user)
    db.session.flush()

    company2 = Company(
        user_id=company2_user.id,
        company_name='Global Finance Corp',
        industry='Financial Services',
        website='https://globalfinance.com',
        description='Premier financial services and investment firm',
        location='New York, NY',
        size='1000+'
    )
    db.session.add(company2)
    db.session.flush()

    # Create sample jobs
    job1 = Job(
        company_id=company1.id,
        title='Senior Python Developer',
        description='We are looking for an experienced Python developer to join our team and work on cutting-edge cloud solutions.',
        requirements='5+ years Python experience, AWS knowledge, REST APIs',
        salary_min=120000,
        salary_max=160000,
        location='San Francisco, CA',
        job_type='full-time',
        experience_required='5+ years',
        deadline=datetime.utcnow().date() + timedelta(days=30),
        skills_required='Python, AWS, Django, REST APIs',
        status='active'
    )
    db.session.add(job1)

    job2 = Job(
        company_id=company1.id,
        title='Frontend Developer',
        description='Join our frontend team to build responsive web applications using React and modern JavaScript.',
        requirements='3+ years frontend experience, React, TypeScript',
        salary_min=90000,
        salary_max=130000,
        location='San Francisco, CA',
        job_type='full-time',
        experience_required='3+ years',
        deadline=datetime.utcnow().date() + timedelta(days=25),
        skills_required='React, TypeScript, CSS, JavaScript',
        status='active'
    )
    db.session.add(job2)

    job3 = Job(
        company_id=company1.id,
        title='DevOps Engineer',
        description='Help us scale our infrastructure and improve deployment processes.',
        requirements='4+ years DevOps experience, Kubernetes, Docker',
        salary_min=110000,
        salary_max=150000,
        location='Remote',
        job_type='full-time',
        experience_required='4+ years',
        deadline=datetime.utcnow().date() + timedelta(days=20),
        skills_required='Kubernetes, Docker, AWS, CI/CD',
        status='active'
    )
    db.session.add(job3)

    job4 = Job(
        company_id=company2.id,
        title='Financial Analyst',
        description='Analyze financial data and provide insights for investment decisions.',
        requirements='3+ years finance experience, Excel, SQL',
        salary_min=80000,
        salary_max=120000,
        location='New York, NY',
        job_type='full-time',
        experience_required='3+ years',
        deadline=datetime.utcnow().date() + timedelta(days=35),
        skills_required='Financial Analysis, Excel, SQL, Python',
        status='active'
    )
    db.session.add(job4)

    job5 = Job(
        company_id=company2.id,
        title='Risk Management Specialist',
        description='Develop and implement risk management strategies for our firm.',
        requirements='5+ years risk management experience',
        salary_min=100000,
        salary_max=140000,
        location='New York, NY',
        job_type='full-time',
        experience_required='5+ years',
        deadline=datetime.utcnow().date() + timedelta(days=28),
        skills_required='Risk Analysis, Compliance, Data Analysis',
        status='active'
    )
    db.session.add(job5)

    job6 = Job(
        company_id=company2.id,
        title='Data Scientist Intern',
        description='Gain hands-on experience in data science and machine learning.',
        requirements='Python, Statistics, Machine Learning basics',
        salary_min=15000,
        salary_max=20000,
        location='New York, NY',
        job_type='internship',
        experience_required='0 years',
        deadline=datetime.utcnow().date() + timedelta(days=15),
        skills_required='Python, Statistics, SQL',
        status='active'
    )
    db.session.add(job6)

    db.session.commit()
```
---


          # app/__init__.py,
          \${language}
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

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(main_bp)

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        from app.utils import seed_database
        seed_database()

    return app
```
---


          # app/__pycache__/models.cpython-314.pyc,
          \${language}
+
    X��i�  �                   ��  � ^ RI Ht ^ RIHt ^ RIHtHt ^ RIHt ]! 4       t ! R R]]P                  4      t
 ! R R]P                  4      t ! R	 R
]P                  4      t ! R R]P                  4      t ! R R]P                  4      t ! R R]P                  4      t ! R R]P                  4      t ! R R]P                  4      t ! R R]P                  4      t ! R R]P                  4      tR# )�    )�
SQLAlchemy)�	UserMixin)�generate_password_hash�check_password_hash)�datetimec                   �  a � ] tR t^	t o ]P                  ]P                  RR7      t]P                  ]P                  ^x4      RR7      t	]P                  ]P                  ^x4      RRRR7      t
]P                  ]P                  ^�4      RR7      t]P                  ]P                  ^4      RR7      t]P                  ]P                  RR7      t]P                  ]P                  ]P"                  R7      t]P'                  RRRR	7      t]P'                  R
RRR	7      t]P'                  RRRR7      tR tR tR tRtV tR# )�UserT��primary_keyF��nullable)�uniquer   �index��default�CandidateProfile�user)�backref�uselist�Company�Application�	candidatezApplication.candidate_id)r   �foreign_keysc                �&   � \        V4      V n        R # �N)r   �password_hash��self�passwords   &&�*C:\Coding\Projects\NextOffer\app\models.py�set_password�User.set_password   s   � �3�H�=���    c                �.   � \        V P                  V4      # r   )r   r   r   s   &&r    �check_password�User.check_password   s   � �"�4�#5�#5�x�@�@r#   c                �"   � R V P                    R2# )z<User �>)�email�r   s   &r    �__repr__�User.__repr__   s   � ���
�
�|�1�%�%r#   )r   N)�__name__�
__module__�__qualname__�__firstlineno__�db�Column�Integer�id�String�namer)   r   �role�Boolean�	is_active�DateTimer   �utcnow�
created_at�relationship�candidate_profile�company_profile�applicationsr!   r%   r+   �__static_attributes__�__classdictcell__��__classdict__s   @r    r	   r	   	   s  �� � �	���2�:�:�4��	0�B��9�9�R�Y�Y�s�^�e�9�4�D��I�I�b�i�i��n�T�E��I�N�E��I�I�b�i�i��n�u�I�=�M��9�9�R�Y�Y�r�]�U�9�3�D��	�	�"�*�*�d�	�3�I����2�;�;�����@�J����(:�F�TY��Z���o�o�i���o�O�O��?�?�=�+�Tn�?�o�L�>�A�&� &r#   r	   c                   ��  a � ] tR t^ t o ]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RRR7      t	]P                  ]P                  ^4      4      t]P                  ]P                  4      t]P                  ]P                  ^4      4      t]P                  ]P                  ^x4      4      t]P                  ]P                   4      t]P                  ]P                  ^�4      4      t]P                  ]P                  ^�4      4      t]P                  ]P(                  ]P,                  R7      t]P                  ]P(                  ]P,                  ]P,                  R7      t]P3                  RR	R
R7      t]P3                  RR	R
R7      t]P3                  RR	R
R7      t]P3                  RR	R
R7      t]P3                  RR	R
R7      tR tRt V t!R# )r   Tr
   �user.idF�r   r   r   �r   �onupdate�	Educationr   �all, delete-orphan�r   �cascade�
Experience�Skill�Project�Awardc                �6   � R V P                   P                   R2# )z<CandidateProfile r(   )r   r)   r*   s   &r    r+   �CandidateProfile.__repr__3   s   � �#�D�I�I�O�O�#4�A�6�6r#   � N)"r-   r.   r/   r0   r1   r2   r3   r4   �
ForeignKey�user_idr5   �phone�Date�dob�gender�location�Text�bio�profile_pic�resume_filer:   r   r;   r<   �
updated_atr=   �	education�
experience�skills�projects�awardsr+   rA   rB   rC   s   @r    r   r       s~  �� � �	���2�:�:�4��	0�B��i�i��
�
�B�M�M�)�$<�u�UY�i�Z�G��I�I�b�i�i��m�$�E�
�)�)�B�G�G�
�C��Y�Y�r�y�y��}�%�F��y�y����3��(�H�
�)�)�B�G�G�
�C��)�)�B�I�I�c�N�+�K��)�)�B�I�I�c�N�+�K����2�;�;�����@�J����2�;�;����(�/�/��Z�J�����[�J^��_�I�����{�L`��a�J��_�_�W�k�CW�_�X�F����y�+�G[��\�H��_�_�W�k�CW�_�X�F�7� 7r#   r   c                   �l  � ] tR t^7t]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^x4      4      t]P                  ]P                  4      t]P                  ]P                  4      t]P                  ]P                  ^
4      4      t]P                  ]P"                  ]P&                  R7      tRtR# )	rJ   Tr
   �candidate_profile.idFr   r   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   �candidate_idr5   �degree�institution�field�
start_year�end_year�grader:   r   r;   r<   rA   rT   r#   r    rJ   rJ   7   s�   � �	���2�:�:�4��	0�B��9�9�R�Z�Z����7M�)N�Y^�9�_�L��Y�Y�r�y�y��~��Y�6�F��)�)�B�I�I�c�N�U�)�;�K��I�I�b�i�i��n�%�E����2�:�:�&�J��y�y����$�H��I�I�b�i�i��m�$�E����2�;�;�����@�Jr#   rJ   c                   �`  � ] tR t^Ct]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^x4      RR7      t]P                  ]P                  RR7      t]P                  ]P                  4      t]P                  ]P                   4      t]P                  ]P$                  RR7      t]P                  ]P(                  ]P,                  R7      tRtR# )	rN   Tr
   rg   Fr   r   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rh   r5   �companyr7   rX   �
start_date�end_dater\   �descriptionr8   �
is_currentr:   r   r;   r<   rA   rT   r#   r    rN   rN   C   s�   � �	���2�:�:�4��	0�B��9�9�R�Z�Z����7M�)N�Y^�9�_�L��i�i��	�	�#���i�7�G��9�9�R�Y�Y�s�^�e�9�4�D����2�7�7�U��3�J��y�y����!�H��)�)�B�G�G�$�K����2�:�:�u��5�J����2�;�;�����@�Jr#   rN   c                   �2  � ] tR t^Ot]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^4      RR7      tRtR	# )
rO   Tr
   rg   Fr   �intermediater   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rh   r5   �
skill_name�proficiencyrA   rT   r#   r    rO   rO   O   so   � �	���2�:�:�4��	0�B��9�9�R�Z�Z����7M�)N�Y^�9�_�L����2�9�9�S�>�E��:�J��)�)�B�I�I�b�M�>�)�B�Kr#   rO   c                   ��  � ] tR t^Vt]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  4      t]P                  ]P                  ^�4      4      t]P                  ]P                  ^�4      4      t]P                  ]P                   ]P$                  R7      tRtR# )	rP   Tr
   rg   Fr   r   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rh   r5   �titler\   rs   �	tech_used�linkr:   r   r;   r<   rA   rT   r#   r    rP   rP   V   s�   � �	���2�:�:�4��	0�B��9�9�R�Z�Z����7M�)N�Y^�9�_�L��I�I�b�i�i��n�u�I�5�E��)�)�B�G�G�$�K��	�	�"�)�)�C�.�)�I��9�9�R�Y�Y�s�^�$�D����2�;�;�����@�Jr#   rP   c                   ��  � ] tR t^`t]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^x4      4      t]P                  ]P                  4      t]P                  ]P                  4      t]P                  ]P"                  ]P&                  R7      tRtR# )	rQ   Tr
   rg   Fr   r   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rh   r5   rz   �issuerrX   �dater\   rs   r:   r   r;   r<   rA   rT   r#   r    rQ   rQ   `   s�   � �	���2�:�:�4��	0�B��9�9�R�Z�Z����7M�)N�Y^�9�_�L��I�I�b�i�i��n�u�I�5�E��Y�Y�r�y�y��~�&�F��9�9�R�W�W��D��)�)�B�G�G�$�K����2�;�;�����@�Jr#   rQ   c                   �P  a � ] tR t^jt o ]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RRR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  ^x4      4      t]P                  ]P                  ^�4      4      t]P                  ]P                  ^�4      4      t]P                  ]P                  4      t]P                  ]P                  ^x4      4      t]P                  ]P                  ^24      4      t]P                  ]P&                  ]P*                  R7      t]P                  ]P&                  ]P*                  ]P*                  R7      t]P1                  R	R
RR7      tR tRtV tR# )r   Tr
   rF   FrG   r   r   rH   �Jobrp   rK   rL   c                �"   � R V P                    R2# )z	<Company r(   )�company_namer*   s   &r    r+   �Company.__repr__y   s   � ��4�,�,�-�Q�/�/r#   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rV   r5   r�   �industry�website�logor\   rs   r[   �sizer:   r   r;   r<   r`   r=   �jobsr+   rA   rB   rC   s   @r    r   r   j   s2  �� � �	���2�:�:�4��	0�B��i�i��
�
�B�M�M�)�$<�u�UY�i�Z�G��9�9�R�Y�Y�s�^�e�9�<�L��y�y����3��(�H��i�i��	�	�#��'�G��9�9�R�Y�Y�s�^�$�D��)�)�B�G�G�$�K��y�y����3��(�H��9�9�R�Y�Y�r�]�#�D����2�;�;�����@�J����2�;�;����(�/�/��Z�J��?�?�5�)�=Q�?�R�D�0� 0r#   r   c                   �.  a � ] tR t^}t o ]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ^x4      RR7      t]P                  ]P                  RR7      t]P                  ]P                  4      t]P                  ]P                  4      t]P                  ]P                  4      t]P                  ]P                  ^x4      4      t]P                  ]P                  ^24      4      t]P                  ]P                  ^24      4      t]P                  ]P*                  4      t]P                  ]P                  ^�4      4      t]P                  ]P                  ^4      RR7      t]P                  ]P2                  ]P6                  R7      t]P                  ]P2                  ]P6                  ]P6                  R7      t]P=                  R	R
RR7      tR t Rt!V t"R# )r�   Tr
   z
company.idFr   �activer   rH   r   �jobrK   rL   c                �"   � R V P                    R2# )z<Job r(   )rz   r*   s   &r    r+   �Job.__repr__�   s   � ��t�z�z�l�!�$�$r#   rT   N)#r-   r.   r/   r0   r1   r2   r3   r4   rU   �
company_idr5   rz   r\   rs   �requirements�Float�
salary_min�
salary_maxr[   �job_type�experience_requiredrX   �deadline�skills_required�statusr:   r   r;   �	posted_atr`   r=   r@   r+   rA   rB   rC   s   @r    r�   r�   }   s�  �� � �	���2�:�:�4��	0�B����2�:�:�r�}�}�\�'B�U��S�J��I�I�b�i�i��n�u�I�5�E��)�)�B�G�G�e�)�4�K��9�9�R�W�W�%�L����2�8�8�$�J����2�8�8�$�J��y�y����3��(�H��y�y����2��'�H��)�)�B�I�I�b�M�2���y�y����!�H��i�i��	�	�#��/�O��Y�Y�r�y�y��}�h�Y�7�F��	�	�"�+�+�x���	�?�I����2�;�;����(�/�/��Z�J��?�?�=�%�I]�?�^�L�%� %r#   r�   c                   �j  a � ] tR t^�t o ]P                  ]P                  RR7      t]P                  ]P                  ]P                  R4      RR7      t	]P                  ]P                  ]P                  R4      RR7      t
]P                  ]P                  ^4      RR7      t]P                  ]P                  4      t]P                  ]P                  ]P"                  R7      t]P                  ]P                  ]P"                  ]P"                  R	7      t]P)                  R
RRR7      3tR tRtV tR# )r   Tr
   rF   Fr   zjob.id�appliedr   rH   rh   �job_id�unique_application)r6   c                �<   � R V P                    RV P                   R2# )z<Application z - r(   )rh   r�   r*   s   &r    r+   �Application.__repr__�   s"   � ��t�0�0�1��T�[�[�M��C�Cr#   rT   N)r-   r.   r/   r0   r1   r2   r3   r4   rU   rh   r�   r5   r�   r\   �cover_letterr:   r   r;   �
applied_atr`   �UniqueConstraint�__table_args__r+   rA   rB   rC   s   @r    r   r   �   s�   �� � �	���2�:�:�4��	0�B��9�9�R�Z�Z����y�)A�E�9�R�L��Y�Y�r�z�z�2�=�=��#:�U�Y�K�F��Y�Y�r�y�y��}�i�Y�8�F��9�9�R�W�W�%�L����2�;�;�����@�J����2�;�;����(�/�/��Z�J��)�)�.�(�I]�)�^�`�N�D� Dr#   r   N)�flask_sqlalchemyr   �flask_loginr   �werkzeug.securityr   r   r   r1   �Modelr	   r   rJ   rN   rO   rP   rQ   r   r�   r   rT   r#   r    �<module>r�      s�   �� '� !� I� ��\��&�9�b�h�h� &�.7�r�x�x� 7�.	A���� 	A�	A���� 	A�C�B�H�H� C�A�b�h�h� A�A�B�H�H� A�0�b�h�h� 0�&%�"�(�(� %�.D�"�(�(� Dr#   
```
---


          # app/__pycache__/utils.cpython-314.pyc,
          \${language}
+
    ���i�  �                   �h   � ^ RI t ^ RIt^ RIHt ^ RIHtHtHtHtH	t	 ^ RI
H
t
Ht 0 RmtR tR tR tR# )	�    N)�secure_filename)�db�User�Company�Job�CandidateProfile)�datetime�	timedeltac                 �x   � R V 9   ;'       d/    V P                  R ^4      ^,          P                  4       \        9   # )�.)�rsplit�lower�ALLOWED_EXTENSIONS)�filenames   &�)C:\Coding\Projects\NextOffer\app\utils.py�allowed_filer      s3   � ��(�?�W�W�x���s�A�6�q�9�?�?�A�EW�W�W�    c                 �
  � V '       d{   \        V P                  4      '       d`   \        V P                  4      p\        P                  ! 4        R V 2pV P                  \        P                  P                  W4      4       V# R# )�_N)	r   r   r   �uuid�uuid4�save�os�path�join)�file�upload_folderr   �unique_names   &&  r   �save_upload_filer      sY   � ���T�]�]�+�+�"�4�=�=�1�������a��z�2���	�	�"�'�'�,�,�}�:�;���r   c                  �	  � \         P                  P                  R R7      P                  4       '       d   R# \        RR RR7      p V P	                  R4       \
        P                  P                  V 4       \        RRR	R7      pVP	                  R
4       \
        P                  P                  V4       \
        P                  P                  4        \        VP                  RRRRRRR7      p\
        P                  P                  V4       \        RRR	R7      pVP	                  R
4       \
        P                  P                  V4       \
        P                  P                  4        \        VP                  RRRRRRR7      p\
        P                  P                  V4       \
        P                  P                  4        \        VP                  RRRRRRRR\        P                  ! 4       P                  4       \        ^R7      ,           R R!R"7      p\
        P                  P                  V4       \        VP                  R#R$R%R&R'RRR(\        P                  ! 4       P                  4       \        ^R7      ,           R)R!R"7      p\
        P                  P                  V4       \        VP                  R*R+R,R-R.R/RR0\        P                  ! 4       P                  4       \        ^R7      ,           R1R!R"7      p\
        P                  P                  V4       \        VP                  R2R3R4R5RRRR(\        P                  ! 4       P                  4       \        ^#R7      ,           R6R!R"7      p\
        P                  P                  V4       \        VP                  R7R8R9R:R;RRR\        P                  ! 4       P                  4       \        ^R7      ,           R<R!R"7      p	\
        P                  P                  V	4       \        VP                  R=R>R?R@RARRBRC\        P                  ! 4       P                  4       \        ^R7      ,           RDR!R"7      p
\
        P                  P                  V
4       \
        P                  P!                  4        R# )Ezadmin@nf.com)�emailNz
Admin User�admin)�namer!   �role�admin123zTech Innovations Inczcompany1@nextoffer.com�company�
company123zInformation Technologyzhttps://techinnovations.comz7Leading tech company focusing on cloud solutions and AIzSan Francisco, CAz500-1000)�user_id�company_name�industry�website�description�location�sizezGlobal Finance Corpzcompany2@nextoffer.comzFinancial Serviceszhttps://globalfinance.comz.Premier financial services and investment firmzNew York, NYz1000+zSenior Python DeveloperzmWe are looking for an experienced Python developer to join our team and work on cutting-edge cloud solutions.z45+ years Python experience, AWS knowledge, REST APIsi�� i q z	full-timez5+ years)�dayszPython, AWS, Django, REST APIs�active)�
company_id�titler,   �requirements�
salary_min�
salary_maxr-   �job_type�experience_required�deadline�skills_required�statuszFrontend Developerz^Join our frontend team to build responsive web applications using React and modern JavaScript.z/3+ years frontend experience, React, TypeScripti�_ i�� z3+ yearsz"React, TypeScript, CSS, JavaScriptzDevOps EngineerzBHelp us scale our infrastructure and improve deployment processes.z.4+ years DevOps experience, Kubernetes, Dockeri�� i�I �Remotez4+ yearszKubernetes, Docker, AWS, CI/CDzFinancial AnalystzEAnalyze financial data and provide insights for investment decisions.z'3+ years finance experience, Excel, SQLi�8 z&Financial Analysis, Excel, SQL, PythonzRisk Management Specialistz>Develop and implement risk management strategies for our firm.z#5+ years risk management experiencei�� i�" z(Risk Analysis, Compliance, Data AnalysiszData Scientist Internz>Gain hands-on experience in data science and machine learning.z+Python, Statistics, Machine Learning basicsi�:  i N  �
internshipz0 yearszPython, Statistics, SQL)r   �query�	filter_by�first�set_passwordr   �session�add�flushr   �idr   r	   �utcnow�dater
   �commit)r"   �company1_user�company1�company2_user�company2�job1�job2�job3�job4�job5�job6s              r   �seed_databaserR      s�  � ��z�z���.��1�7�7�9�9�� �����E�
 
���z�"��J�J�N�N�5�� �#�&���M�
 ���|�,��J�J�N�N�=�!��J�J������ � �+�)�-�M�$���H� �J�J�N�N�8���"�&���M�
 ���|�,��J�J�N�N�=�!��J�J������ � �*�%�+�D����H� �J�J�N�N�8���J�J���� ��;�;�'� D�K���$��&����"�'�'�)�I�2�,>�>�8���D� �J�J�N�N�4����;�;�"�t�F���$��&����"�'�'�)�I�2�,>�>�<���D� �J�J�N�N�4����;�;��X�E�����&����"�'�'�)�I�2�,>�>�8���D� �J�J�N�N�4����;�;�!�[�>�����&����"�'�'�)�I�2�,>�>�@���D� �J�J�N�N�4����;�;�*�T�:�����&����"�'�'�)�I�2�,>�>�B���D� �J�J�N�N�4����;�;�%�T�B�����%����"�'�'�)�I�2�,>�>�1���D� �J�J�N�N�4���J�J���r   >   �gif�jpg�pdf�png�jpeg)r   r   �werkzeug.utilsr   �
app.modelsr   r   r   r   r   r	   r
   r   r   r   rR   � r   r   �<module>r[      s0   �� 	� � *� ?� ?� (� :� �X��Xr   
```
---


          # app/__pycache__/__init__.cpython-314.pyc,
          \${language}
+
    X��i�  �                   �Z   � ^ RI t ^ RIHt ^ RIHt ^ RIHt ^ RIHtHt ]! 4       t	RR lt
R# )�    N)�Flask)�LoginManager)�config)�db�Userc                 �z  � V f!   \         P                  P                  RR4      p \        \        4      pVP
                  P                  \
        V ,          4       \         P                  ! VP
                  R,          RR7       \        P                  ! V4       \        P                  V4       R\        n        R\        n        \        P                  R 4       p^ R	IHp ^ R
IHp ^ RIHp ^ RIHp ^ RIHp ^ RIHp VP5                  V4       VP5                  V4       VP5                  V4       VP5                  V4       VP5                  V4       VP5                  V4       VP7                  4       ;_uu_ 4        \        P8                  ! 4        ^ RIHp	 V	! 4        R R R 4       V#   + '       g   i     T# ; i)N�	FLASK_ENV�development�UPLOAD_FOLDERT)�exist_okz
auth.loginz"Please log in to access this page.c                 �R   � \         P                  P                  \        V 4      4      # �N)r   �query�get�int)�user_ids   &�,C:\Coding\Projects\NextOffer\app\__init__.py�	load_user�create_app.<locals>.load_user   s   � ��z�z�~�~�c�'�l�+�+�    )�auth_bp)�candidate_bp)�
company_bp)�admin_bp)�	resume_bp)�main_bp)�seed_database)�os�environr   r   �__name__r   �from_object�makedirsr   �init_app�login_manager�
login_view�login_message�user_loader�app.routes.authr   �app.routes.candidater   �app.routes.companyr   �app.routes.adminr   �app.routes.resumer   �app.routes.mainr   �register_blueprint�app_context�
create_all�	app.utilsr   )
�config_name�appr   r   r   r   r   r   r   r   s
   &         r   �
create_appr4   
   s=  � ����j�j�n�n�[�-�@��
��/�C��J�J���6�+�.�/� �K�K��
�
�?�+�d�;� �K�K������3��+�M��"F�M�����,� �,� (�1�-�)�+�'����7�#����<�(����:�&����8�$����9�%����7�#� 
���	�	�
����+��� 
�
 �J� 
�	�
 �J�s   �<#F)�)F:	r   )r   �flaskr   �flask_loginr   r   �
app.modelsr   r   r$   r4   � r   r   �<module>r9      s    �� 	� � $� � ����)r   
```
---


          # CLAUDE.md,
          \${language}
# NextOffer - Placement Portal

## Project Overview

NextOffer is a full-stack job placement portal web application built with Flask, Bootstrap, and SQLite. It connects job seekers (candidates) with employers (companies) and provides admins with platform management tools.

## Tech Stack

- **Backend**: Python 3.9+ with Flask 3.0
- **Frontend**: Bootstrap 5 (CDN), vanilla JavaScript, custom CSS
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Generation**: WeasyPrint
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Forms**: Flask-WTF with client/server validation

## Architecture

### Directory Structure
```
app/
  ├── __init__.py          # App factory with blueprints registration
  ├── models.py            # SQLAlchemy models (11 tables)
  ├── utils.py             # Seed data and file upload utilities
  ├── routes/              # Blueprint modules
  │   ├── auth.py          # Login/register/logout
  │   ├── main.py          # Homepage, job browse/detail
  │   ├── candidate.py     # Candidate CRUD operations
  │   ├── company.py       # Company/job management
  │   ├── admin.py         # Admin dashboard & management
  │   └── resume.py        # Resume builder & PDF download
  ├── templates/           # Jinja2 templates
  │   ├── base.html        # Navigation, layout
  │   ├── index.html       # Homepage with hero section
  │   └── [sections]/      # Auth, candidate, company, admin, jobs, resume
  └── static/
      ├── css/style.css    # Custom styles, animations
      ├── js/main.js       # Form validation, alerts, utility functions
      └── uploads/         # User-generated files (auto-created)

config.py                  # Flask configuration (dev/prod)
run.py                     # Application entry point
requirements.txt          # Python dependencies
```

## Database Design

### Core Models
- **User**: role='candidate'|'company'|'admin', is_active flag
- **CandidateProfile**: Extended user data (phone, location, bio, profile_pic, resume_file)
- **Education**: Multiple entries per candidate (degree, institution, field, year, grade)
- **Experience**: Multiple work history entries (company, role, dates, description, is_current)
- **Skill**: Skills with proficiency levels (beginner/intermediate/expert)
- **Project**: Portfolio projects (title, description, tech_used, link)
- **Award**: Achievements (title, issuer, date, description)
- **Company**: Company profile (company_name, industry, website, logo, description, size, location)
- **Job**: Job postings (title, description, requirements, salary_min/max, location, job_type, skills_required, status, deadline)
- **Application**: Job applications (candidate_id, job_id, status, cover_letter, timestamps)

## Key Features

### Authentication
- Dual login form with candidate/company tabs
- Separate registration flows with input validation
- Flask-Login session management with `login_required` decorator
- Password hashing with Werkzeug
- Role-based access control (RBAC) via decorators (`@candidate_required`, `@company_required`, `@admin_required`)

### Candidate Features
1. **Profile Building**: Personal info, education, experience, skills, projects, awards
2. **Job Search**: Browse, filter (by title/location/type), paginate (10 per page)
3. **Applications**: Apply with optional cover letter, track status
4. **Resume Builder**: 3 templates (classic/modern/creative) with WeasyPrint PDF download
5. **Dashboard**: Stats (applications sent, shortlisted, rejected, hired), recent applications

### Company Features
1. **Profile**: Company info, logo upload, size/industry/description
2. **Job Posting**: Full form with salary range, deadline, skills required
3. **Applications Management**: View applicants, review profiles, update status (shortlist/reject/hire)
4. **Job Management**: Edit, toggle status (active/closed), delete
5. **Dashboard**: Stats (total/active jobs, applications, shortlisted)

### Admin Features
1. **Dashboard**: Platform stats (users, jobs, applications), recent activity
2. **User Management**: List all users, toggle active/inactive status (role filter)
3. **Job Management**: View all jobs, filter by status, delete postings
4. **Application Monitoring**: List all applications, filter by status
5. **Reports**: Success rates, platform analytics

## Critical Files & Functions

### app/__init__.py
- `create_app(config_name)`: App factory that initializes Flask, extensions, blueprints
- Automatically creates tables and seeds data on first run

### app/models.py
- User model with `check_password()` and `set_password()` methods
- Relationships defined with cascade delete where appropriate
- UniqueConstraint on Application(candidate_id, job_id) to prevent duplicate applies

### app/utils.py
- `seed_database()`: Creates admin + 2 sample companies with 6 jobs (only runs once)
- `save_upload_file()`: Stores files with UUID prefix to avoid collisions
- `allowed_file()`: Validates file extensions

### app/routes/auth.py
- WTForms validation with email_validator integration
- `check_password()` for authentication
- Redirect to role-appropriate dashboard on login

### app/routes/candidate.py
- `@candidate_required`: Restricts access to candidates only
- CRUD for education/experience/skills/projects/awards
- Apply job creates Application record (prevents duplicates via unique constraint)

### app/routes/company.py
- Job status toggle (active/closed) via POST
- Application status update (applied/shortlisted/rejected/hired)
- Candidate profile view (company can see full profile + download resume)

### app/routes/resume.py
- Three Jinja2 templates rendered to HTML then WeasyPrint converts to PDF
- `resume_data` dict passed to templates with all candidate info
- `download()` returns PDF with timestamp in filename

## CSS & UI

### Custom Styles (app/static/css/style.css)
- Color scheme: Navy (#0A1628), Blue (#2563EB), Green (#10b981), Amber (#f59e0b)
- Hover effects on cards (translateY -5px)
- Bootstrap 5 overrides (border-radius, shadows, transitions)
- Responsive breakpoints for mobile

### Key CSS Classes
- `.hover-card`: Lifts on hover with shadow
- `.glass-effect`: Glassmorphism (backdrop blur + semi-transparent)
- Smooth animations (fade-in, transitions)
- Custom scrollbar styling

### JavaScript (app/static/js/main.js)
- Flash message auto-dismiss after 5 seconds
- Form validation with disabled submit button
- Loading spinner on form submit
- Search functionality
- Bootstrap tooltip/popover initialization

## API Endpoint Organization

| Module | Pattern | Auth |
|--------|---------|------|
| Auth | `/auth/login`, `/auth/register/*`, `/auth/logout` | Public/Required |
| Main | `/`, `/jobs`, `/job/<id>` | Public |
| Candidate | `/candidate/*` | @login_required + @candidate_required |
| Company | `/company/*` | @login_required + @company_required |
| Admin | `/admin/*` | @login_required + @admin_required |
| Resume | `/resume/*` | @login_required + @candidate_required |

## Form Validation

All forms use Flask-WTF:
- **Client-side**: HTML5 attributes (required, minlength, pattern)
- **Server-side**: WTForms validators (DataRequired, Email, Length, EqualTo, URL, etc.)
- Flash messages for submission results

## File Upload Handling

- Files stored in `app/static/uploads/` with UUID prefix
- Extensions validated against ALLOWED_EXTENSIONS (pdf, png, jpg, jpeg, gif)
- Werkzeug's `secure_filename()` prevents path traversal
- Max file size: 16MB (configured in config.py)

## Database Initialization

- `db.create_all()` called in app context on startup
- `seed_database()` checks if admin exists (prevents re-seeding)
- Seed creates admin user + 2 companies with 3 jobs each (6 total)

## Resume PDF Generation

**Flow**: 
1. User selects template
2. Resume builder fetches candidate data
3. `resume/download/<template>` renders Jinja2 HTML template
4. WeasyPrint converts HTML string to PDF bytes
5. Flask returns file as attachment with timestamp in filename

**Templates**:
- Classic: Single-column ATS-friendly layout
- Modern: Sidebar (navy bg) + main content with icons
- Creative: Bold header + timeline layout for experience

## Deployment Considerations

- Set `SECRET_KEY` to random string in production
- Set `SESSION_COOKIE_SECURE = True` for HTTPS only
- Use PostgreSQL instead of SQLite for production
- Consider adding Gunicorn WSGI server
- Enable CSRF protection (enabled by default with Flask-WTF)
- Add rate limiting for login/registration
- Set up error logging

## Common Issues & Solutions

**Issue**: WeasyPrint fails to render HTML
- Solution: Use base_url=request.host_url in HTML() constructor

**Issue**: Duplicate applications
- Solution: UniqueConstraint on Application table prevents database-level duplicates

**Issue**: File uploads fail
- Solution: Ensure `app/static/uploads/` directory exists (created in __init__.py)

**Issue**: Seed data not appearing
- Solution: Delete nextoffer.db and restart app

## Performance Optimizations

- Pagination (10 jobs per page) to reduce database load
- Indexes on frequently queried columns (email, job_id, candidate_id)
- Lazy loading relationships where appropriate
- CSS and JS minified via CDN

## Security

- Password hashing with Werkzeug (pbkdf2:sha256)
- CSRF protection via Flask-WTF tokens
- SQL injection prevention via SQLAlchemy parameterized queries
- XSS prevention via Jinja2 autoescaping
- File upload validation (extension + secure_filename)
- Role-based access control via decorators
- Session timeout: 7 days
- HTTPOnly cookies for sessions

## Future Enhancements

- Email notifications (job alerts, status updates)
- Real-time notifications via WebSocket
- Advanced job matching algorithm
- Interview scheduling system
- Video call integration
- Candidate assessment tests
- Social features (messaging, endorsements)
- Mobile app (React Native)
- Batch job posting via CSV
- Integration with LinkedIn/Indeed

## Testing (Manual)

1. Register candidate → Fill full profile → Browse jobs → Apply → Check status
2. Register company → Post job → View applicants → Update status
3. Login as admin → View stats → Manage users/jobs
4. Generate resume PDF in all 3 templates
5. Test search/filter on job listings
6. Test role-based redirects (candidate can't access /company/*)

## Notes for Future Development

- All forms use Flask-WTF (CSRF protection enabled)
- Blueprints use `url_prefix` for clean route organization
- Templates extend base.html for consistent header/footer
- Upload folder auto-created with UUID filenames
- No hardcoded URLs (all use url_for)
- Seed data includes realistic sample data for testing
```
---


          # config.py,
          \${language}
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nextoffer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    JOBS_PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```
---


          # instance/nextoffer.db,
          \${language}
SQLite format 3   @                                                                     .��  ���b �	�����                                                                                                                             �##�ytableapplicationapplicationCREATE TABLE application (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	job_id INTEGER NOT NULL, 
	status VARCHAR(20), 
	cover_letter TEXT, 
	applied_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	CONSTRAINT unique_application UNIQUE (candidate_id, job_id), 
	FOREIGN KEY(candidate_id) REFERENCES user (id), 
	FOREIGN KEY(job_id) REFERENCES job (id)
)5I# indexsqlite_autoindex_application_1application�c�-tablejobjobCREATE TABLE job (
	id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	title VARCHAR(120) NOT NULL, 
	description TEXT NOT NULL, 
	requirements TEXT, 
	salary_min FLOAT, 
	salary_max FLOAT, 
	location VARCHAR(120), 
	job_type VARCHAR(50), 
	experience_required VARCHAR(50), 
	deadline DATE, 
	skills_required VARCHAR(255), 
	status VARCHAR(20), 
	posted_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company (id)
)�$�'tableawardawardCREATE TABLE award (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	title VARCHAR(120) NOT NULL, 
	issuer VARCHAR(120), 
	date DATE, 
	description TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidate_profile (id)
)�5
�AtableprojectprojectCREATE TABLE project (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	title VARCHAR(120) NOT NULL, 
	description TEXT, 
	tech_used VARCHAR(255), 
	link VARCHAR(255), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidate_profile (id)
)�u	�Itableskillskill
CREATE TABLE skill (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	skill_name VARCHAR(120) NOT NULL, 
	proficiency VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidate_profile (id)
)�r!!�/tableexperienceexperience	CREATE TABLE experience (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	company VARCHAR(120) NOT NULL, 
	role VARCHAR(120) NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE, 
	description TEXT, 
	is_current BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidate_profile (id)
)�s�5tableeducationeducationCREATE TABLE education (
	id INTEGER NOT NULL, 
	candidate_id INTEGER NOT NULL, 
	degree VARCHAR(120) NOT NULL, 
	institution VARCHAR(120) NOT NULL, 
	field VARCHAR(120), 
	start_year INTEGER, 
	end_year INTEGER, 
	grade VARCHAR(10), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidate_profile (id)
)��tablecompanycompanyCREATE TABLE company (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	company_name VARCHAR(120) NOT NULL, 
	industry VARCHAR(120), 
	website VARCHAR(255), 
	logo VARCHAR(255), 
	description TEXT, 
	location VARCHAR(120), 
	size VARCHAR(50), 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
)-A indexsqlite_autoindex_company_1company�//�atablecandidate_profilecandidate_profileCREATE TABLE candidate_profile (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	phone VARCHAR(20), 
	dob DATE, 
	gender VARCHAR(20), 
	location VARCHAR(120), 
	bio TEXT, 
	profile_pic VARCHAR(255), 
	resume_file VARCHAR(255), 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
)AU/ indexsqlite_autoindex_candidate_profile_1candidate_profile       N'oindexix_user_emailuserCREATE UNIQUE INDEX ix_user_email ON user (email)� �ctableuseruserCREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	is_active BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id)
)   E $,E                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     �d	 -�Q	AKushalkushal@gmail.comscrypt:32768:8:1$pUW9uL86kZm4SUDC$685dba60415a4f287226aa404e77cf28bf75ddac82e455330afb2dd4f961b2b80d9ce6192c3093c7103edefc12759a4133e2c9b4268b1271480e43e81652784ecandidate2026-05-07 03:00:49.788248�u	 39�Q	AGlobal Finance Corpcompany2@nextoffer.comscrypt:32768:8:1$xnzJDnPUUoequSRR$f64e11bfb73c3cc9b4236fe1e8013f797385c0f1af8b12c87dde22c39d7c54603ac960cc86ec083d72c8538c061438802e72b6d0a73bffd336efdde36194a929company2026-05-07 02:55:09.484524�v	 59�Q	ATech Innovations Inccompany1@nextoffer.comscrypt:32768:8:1$0q8vluHHcjOTcgub$1dac8b948ed723d3c56933f9fe90f50a4789622ad34f070815d99147b137b33b0e0fd5f00dbd28581e64ac1c90d7afc8ba0b901a40205487f5b177ce5fa5fc96company2026-05-07 02:55:09.310929�`	 !%�Q	AAdmin Useradmin@nf.comscrypt:32768:8:1$AYrlP4sGEklkzMqa$0580bb86e1ce2a5189fc4b4103503dea6f1ffb56ef34c036ec8e179a7884470d9d1af6aa1a5ce25d971d9bca1eeee76de7e6c3942c0bf502bad28deb0d9215eeadmin2026-05-07 02:55:09.310924
   � ����                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     -kushal@gmail.com9company2@nextoffer.com9company1@nextoffer.com%	admin@nf.com   u u                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           � )  'e AA+91 8235888246Mumbai, india28ae14de-4cf7-416f-819e-927a1ee9ff61_men.jpg2026-05-07 03:00:49.7928062026-05-07 04:41:54.541554
   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 	   f 'f                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          �> 31? i%AAGlobal Finance CorpFinancial Serviceshttps://globalfinance.comPremier financial services and investment firmNew York, NY1000+2026-05-07 02:55:09.4860932026-05-07 02:55:09.486095�V 59C {/AATech Innovations IncInformation Technologyhttps://techinnovations.comLeading tech company focusing on cloud solutions and AISan Francisco, CA500-10002026-05-07 02:55:09.4854092026-05-07 02:55:09.485411
   � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         	
 �iW8
	
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      � 7�	c%!!;AAData Scientist InternGain hands-on experience in data science and machine learning.Python, Statistics, Machine Learning basics:�N New York, NYinternship0 years2026-05-22Python, Statistics, SQLactive2026-05-07 02:55:09.4873602026-05-07 02:55:09.487361� A�	S%!]AARisk Management SpecialistDevelop and implement risk management strategies for our firm.5+ years risk management experience��"�New York, NYfull-time5+ years2026-06-04Risk Analysis, Compliance, Data Analysisactive2026-05-07 02:55:09.4873582026-05-07 02:55:09.487359� /�[%!YAAFinancial AnalystAnalyze financial data and provide insights for investment decisions.3+ years finance experience, Excel, SQL8���New York, NYfull-time3+ years2026-06-11Financial Analysis, Excel, SQL, Pythonactive2026-05-07 02:55:09.4873572026-05-07 02:55:09.487358� 	+�i!IAADevOps EngineerHelp us scale our infrastructure and improve deployment processes.4+ years DevOps experience, Kubernetes, Docker��I�Remotefull-time4+ years2026-05-27Kubernetes, Docker, AWS, CI/CDactive2026-05-07 02:55:09.4873552026-05-07 02:55:09.487356�> 	1�Ik/!QAAFrontend DeveloperJoin our frontend team to build responsive web applications using React and modern JavaScript.3+ years frontend experience, React, TypeScript_���San Francisco, CAfull-time3+ years2026-06-01React, TypeScript, CSS, JavaScriptactive2026-05-07 02:55:09.4873532026-05-07 02:55:09.487354�S 	;�gu/!IAASenior Python DeveloperWe are looking for an experienced Python developer to join our team and work on cutting-edge cloud solutions.5+ years Python experience, AWS knowledge, REST APIs��q San Francisco, CAfull-time5+ years2026-06-06Python, AWS, Django, REST APIsactive2026-05-07 02:55:09.4873502026-05-07 02:55:09.487352   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               E AAapplied2026-05-07 04:42:44.1104752026-05-07 04:42:44.110480
   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               	
```
---


          # README.md,
          \${language}
# NextOffer - Placement Portal

A full-stack web application for connecting job candidates with hiring companies.

## Features

### 🔐 Authentication
- Separate login for candidates, companies, and admins
- Session-based authentication with Flask-Login
- Password hashing with Werkzeug

### 👤 Candidate Features
- Complete profile management (personal info, education, experience, skills, projects, awards)
- Browse and filter job listings
- Apply for jobs with cover letters
- Track application status
- Resume builder with 3 templates
- PDF resume download

### 🏢 Company Features
- Create and manage company profile
- Post job listings with full details
- View applications for each job
- Review candidate profiles
- Update application status (shortlist, reject, hire)

### 🛡️ Admin Panel
- Dashboard with platform statistics
- Manage users (activate/deactivate)
- View and delete job postings
- Monitor all applications
- Generate reports

## Tech Stack

- **Backend**: Python Flask with Jinja2 templating
- **Frontend**: Bootstrap 5 (CDN), custom CSS, vanilla JavaScript
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Generation**: WeasyPrint
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

1. Clone the repository:
```bash
cd NextOffer
```

2. Create a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000`

## Default Credentials

On first run, the following default accounts are created:

**Admin Account:**
- Email: `admin@nextoffer.com`
- Password: `admin123`

**Sample Companies:**
- Tech Innovations Inc: `company1@nextoffer.com` / `company123`
- Global Finance Corp: `company2@nextoffer.com` / `company123`

## Project Structure

```
NextOffer/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models
│   ├── utils.py             # Utility functions & seed data
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── candidate.py     # Candidate routes
│   │   ├── company.py       # Company routes
│   │   ├── admin.py         # Admin routes
│   │   ├── resume.py        # Resume builder routes
│   │   └── main.py          # Main routes (homepage, jobs)
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Homepage
│   │   ├── auth/            # Auth templates
│   │   ├── candidate/       # Candidate templates
│   │   ├── company/         # Company templates
│   │   ├── admin/           # Admin templates
│   │   ├── jobs/            # Job templates
│   │   └── resume/          # Resume templates
│   └── static/              # Static files
│       ├── css/             # Stylesheets
│       ├── js/              # JavaScript files
│       └── uploads/         # User uploads (auto-created)
├── config.py                # Configuration
├── run.py                   # Entry point
└── requirements.txt         # Dependencies
```

## Database Models

- **User**: Core user model with role-based access
- **CandidateProfile**: Extended candidate data
- **Education**: Candidate education history
- **Experience**: Candidate work experience
- **Skill**: Candidate skills with proficiency levels
- **Project**: Candidate projects portfolio
- **Award**: Candidate awards and achievements
- **Company**: Company profile information
- **Job**: Job postings
- **Application**: Job applications with status tracking

## Usage

### For Candidates
1. Register as a candidate
2. Build your complete profile (education, experience, skills, projects)
3. Browse available job listings
4. Apply for jobs with optional cover letters
5. Track application status
6. Use the resume builder to create professional PDFs

### For Companies
1. Register your company
2. Complete company profile
3. Post job listings
4. Review applications
5. View full candidate profiles
6. Update application statuses

### For Admins
1. Login with admin credentials
2. View platform statistics
3. Manage users and accounts
4. Monitor job postings and applications
5. View system reports

## Resume Templates

Three professional resume templates are available:

1. **Classic**: Traditional black & white ATS-friendly layout
2. **Modern**: Sidebar design with color accent and icons
3. **Creative**: Bold header with timeline layout

All templates generate print-ready PDFs using WeasyPrint.

## API Endpoints

### Authentication
- `GET/POST /auth/login` - Login
- `GET/POST /auth/register/candidate` - Candidate registration
- `GET/POST /auth/register/company` - Company registration
- `GET /auth/logout` - Logout

### Jobs
- `GET /` - Homepage
- `GET /jobs` - Browse jobs with search/filter
- `GET /job/<id>` - View job details

### Candidate
- `GET /candidate/dashboard` - Candidate dashboard
- `GET/POST /candidate/profile` - Profile management
- `GET/POST /candidate/education` - Education management
- `GET/POST /candidate/experience` - Experience management
- `GET/POST /candidate/skills` - Skills management
- `GET/POST /candidate/projects` - Projects management
- `GET/POST /candidate/awards` - Awards management
- `GET /candidate/applications` - View applications
- `GET/POST /candidate/apply/<job_id>` - Apply for job

### Company
- `GET /company/dashboard` - Company dashboard
- `GET/POST /company/profile` - Company profile
- `GET /company/jobs` - View posted jobs
- `GET/POST /company/post-job` - Post new job
- `GET /company/job/<id>/applications` - View applications for job
- `GET /company/application/<id>/candidate` - View candidate profile
- `POST /company/application/<id>/update-status` - Update application status

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - Manage users
- `GET /admin/jobs` - Manage jobs
- `GET /admin/applications` - View applications
- `GET /admin/reports` - View reports

### Resume
- `GET /resume/builder` - Resume builder
- `GET /resume/preview/<template>` - Preview resume
- `GET /resume/download/<template>` - Download PDF resume

## Configuration

Update `config.py` for production:

```python
SECRET_KEY = 'your-production-secret-key'
SESSION_COOKIE_SECURE = True
DATABASE_URL = 'your-production-database-url'
```

## Features Highlights

✅ Role-based access control (Candidate/Company/Admin)
✅ Responsive design - works on all devices
✅ Search and filter jobs by title, location, type
✅ Complete candidate profile with all professional details
✅ File uploads (profile pictures, logos)
✅ Pagination for large datasets
✅ Flash messages for user feedback
✅ Professional resume builder with PDF generation
✅ Admin analytics and user management
✅ Seed data on first run

## Future Enhancements

- Email notifications for applications and status updates
- Advanced search with AI-powered job matching
- Skills assessment tests
- Video interview integration
- Salary negotiation tools
- Analytics dashboard for companies
- Mobile app
- Social media integration

## Support

For issues or questions, please check the code or reach out through the application.

## License

This project is open source and available for educational purposes.
```
---


          # requirements.txt,
          \${language}
Flask==3.1.0
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-SQLAlchemy==3.2.1
Werkzeug==3.1.2
ReportLab
WTForms==3.1.1
email-validator==2.2.0
SQLAlchemy==2.1.5
Jinja2==3.1.4
```
---


          # run.py,
          \${language}
import os
from app import create_app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='127.0.0.1', port=5000)
```
---


          # __pycache__/config.cpython-314.pyc,
          \${language}
+
    X��ig  �                   �j   � ^ RI t ^ RIHt  ! R R4      t ! R R]4      t ! R R]4      tR	]R
]R]/tR# )�    N)�	timedeltac                   �  � ] tR t^t]P
                  P                  R4      ;'       g    RtRtRt	]P                  P                  ]P                  P                  ]4      RRR4      tRt0 Rmt]! ^R7      tRtR	tR
t^
tRtR# )�Config�
SECRET_KEYz#dev-secret-key-change-in-productionzsqlite:///nextoffer.dbF�app�static�uploads)�daysT�Lax� Ni   >   �gif�jpg�pdf�png�jpeg)�__name__�
__module__�__qualname__�__firstlineno__�os�environ�getr   �SQLALCHEMY_DATABASE_URI�SQLALCHEMY_TRACK_MODIFICATIONS�path�join�dirname�__file__�UPLOAD_FOLDER�MAX_CONTENT_LENGTH�ALLOWED_EXTENSIONSr   �PERMANENT_SESSION_LIFETIME�SESSION_COOKIE_SECURE�SESSION_COOKIE_HTTPONLY�SESSION_COOKIE_SAMESITE�JOBS_PER_PAGE�__static_attributes__r   �    �&C:\Coding\Projects\NextOffer\config.pyr   r      s|   � �������-�V�V�1V�J�6��%*�"��G�G�L�L�������!:�E�8�Y�W�M�)��=��!*��!2��!��"��#���Mr(   r   c                   �   � ] tR t^tRtRtR# )�DevelopmentConfigTr   N)r   r   r   r   �DEBUGr'   r   r(   r)   r+   r+      s   � ��Er(   r+   c                   �   � ] tR t^tRtRtRtR# )�ProductionConfigFTr   N)r   r   r   r   r,   r#   r'   r   r(   r)   r.   r.      s   � ��E� �r(   r.   �development�
production�default)r   �datetimer   r   r+   r.   �configr   r(   r)   �<module>r4      sH   �� 	� �� � �� �!�v� !�
 �$��"�� �
�r(   
```
---