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
