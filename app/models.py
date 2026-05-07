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
