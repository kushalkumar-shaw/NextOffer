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
