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
