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
