from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from models import Users
from flask_bcrypt import Bcrypt
from app import app, db, login_manager
from auth.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__, template_folder='templates')
bcrypt = Bcrypt(app)

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли в аккаунт')
            return redirect(url_for('posts.index'))
        else:
            flash('Введенные данные некорректны, попробуйте снова')
    return render_template('login.html', form=form, title='Страница входа')


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
        if not Users.query.filter_by(login=form.login.data).first():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
            new_user = Users(login=form.login.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('auth.login'))

    return render_template('register.html', form=form, title='Страница регистрации')
