import os


db_path = os.path.join(os.path.dirname(__file__), 'lv_site1.db')
db_uri = 'sqlite:///{}'.format(db_path)


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLAlCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'DSLKNGFDSGGOE2113dSDAQW!@#!4sadcvcv;lalqtrewqdspkfmaswdf'
    SQLALCHEMY_ECHO = True
