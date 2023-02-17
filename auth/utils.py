import smtplib
from email.mime.text import MIMEText
import jwt
import datetime

from flask import url_for

import config
from app import app
from models import Users


def generate_password_reset_token(user_id):
    # Задаем параметры токена
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    # Генерируем токен с секретным ключом
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def verify_password_token(token):
    try:
        id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
    except:
        return
    return Users.query.get(id)


# Отправка письма пользователю на почту с персональной ссылкой

def send_message(decoded_token, user_email):
    sender = config.sender
    sender_password = config.sender_password
    reset_password_url = url_for('auth.reset_password_page', token=decoded_token, _external=True)

    try:
        smtp_server = "smtp.yandex.ru"
        smtp_port = 587

        email_subject = "Ссылка для сброса пароля"
        email_body = f"Если вы не делали запрос на сброс пароля своего аккаунта, просто проигнорируйте это пиьсмо. \nЧтобы сбросить пароль перейдите по ссылке: {reset_password_url}"
        msg = MIMEText(str(email_body))
        msg['Subject'] = email_subject
        msg['From'] = sender
        msg['To'] = user_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(sender, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)
