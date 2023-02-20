import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.path.join(os.path.dirname(__file__), 'lv_site1.db')
db_uri = 'sqlite:///{}'.format(db_path)
sender = os.getenv('SENDER')
sender_password = os.getenv('SENDER_PASSWORD')


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLAlCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = True
    LANGUAGES = ['en', 'ru', 'pl']