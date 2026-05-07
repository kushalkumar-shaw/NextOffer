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
