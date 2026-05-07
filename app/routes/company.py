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
