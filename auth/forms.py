from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from models import Users


class RegistrationForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Логин'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Пароль'})

    submit = SubmitField('Регистрация')

    def validate_username(self, login):
        existing_user_username = Users.query.filter_by(
            username=login.data).first()
        if existing_user_username:
            raise ValidationError(
                'Это имя пользователя уже занято, попробуйте другое.')


class LoginForm(FlaskForm):
    login = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Логин'})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={'placeholder': 'Пароль'})

    submit = SubmitField('Логин')
