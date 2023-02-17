from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo

from models import Users


class RegistrationForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={'placeholder': 'Почта'})

    login = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Логин'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=140)], render_kw={'placeholder': 'Пароль'})

    password_confirm = PasswordField(validators=[InputRequired(),EqualTo('password'), Length(
        min=4, max=140)], render_kw={'placeholder': 'Повторите пароль'})

    submit = SubmitField('Регистрация')

    # def validate_username(self, login):
    #     existing_user_username = Users.query.filter_by(
    #         username=login.data).first()
    #     if existing_user_username:
    #         raise ValidationError(
    #             'Это имя пользователя уже занято, попробуйте другое.')
    #
    # def validate_email(self, email):
    #     existing_email = Users.query.filter_by(
    #         email=email.data).first()
    #     if existing_email:
    #         raise ValidationError(
    #             'Эта почта уже используется, попробуйте другое.')


class LoginForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Логин'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Пароль'})

    submit = SubmitField('Войти')


class ResetPasswordRequest(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={'placeholder': 'Почта'})
    submit = SubmitField('Сбросить пароль')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)])
    password_1 = PasswordField(validators=[InputRequired(), EqualTo('password'), Length(
        min=4, max=20)])
    submit = SubmitField('Сохранить пароль')
