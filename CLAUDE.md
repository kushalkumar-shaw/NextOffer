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
