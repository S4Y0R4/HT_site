from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo


class ContactsEditForm(FlaskForm):
    name_surname = StringField(validators=[InputRequired(), Length(
        min=1, max=30)], render_kw={'placeholder': 'Имя и фамилия'})
    phone = StringField(validators=[InputRequired(), Length(
        min=1, max=30)], render_kw={'placeholder': 'Телефон'})
    email = EmailField(validators=[InputRequired(), Length(
        min=1, max=30)], render_kw={'placeholder': 'Почта'})
    telegram = BooleanField(render_kw={'placeholder': 'Telegram'})
    viber = BooleanField(render_kw={'placeholder': 'Viber'})
    whatsapp = BooleanField(render_kw={'placeholder': "What'sApp"})
