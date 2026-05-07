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
