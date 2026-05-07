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
