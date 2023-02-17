from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from auth.utils import send_message, generate_password_reset_token, verify_password_token
from models import Users
from flask_bcrypt import Bcrypt
from app import app, db, login_manager
from auth.forms import RegistrationForm, LoginForm, ResetPasswordRequest, ResetPasswordForm

auth = Blueprint('auth', __name__, template_folder='templates')
bcrypt = Bcrypt(app)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли в аккаунт')
            return redirect(url_for('posts.index'))
        else:
            flash('Введенные данные некорректны, попробуйте снова')
    return render_template('auth/login.html', form=form, title='Страница входа')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not Users.query.filter_by(login=form.login.data).first() and not Users.query.filter_by(
                email=form.email.data).first():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            new_user = Users(login=form.login.data, password=hashed_password, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('auth.login'))
        else:
            flash('Такая почта или указанный логин уже заняты')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form, title='Страница регистрации')


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = ResetPasswordRequest()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_message(generate_password_reset_token(user.id), user.email)
            flash('На эту почту было отправлено письмо с инструкцией по сбросу пароля')
            return redirect(url_for('auth.login'))
        else:
            flash('Пользователя с такой почтой нет')
            return render_template('auth/reset_password_request.html', form=form,
                                   title='Страница восстановления пароля')

    return render_template('auth/reset_password_request.html', form=form, title='Страница восстановления пароля')


@auth.route('/reset_password_page/<token>', methods=['GET', 'POST'])
def reset_password_page(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    user = verify_password_token(token)
    if not user:
        return redirect(url_for('posts.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль обновлен')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_page.html', form=form, title='Страница смены пароля')
