from app import db
import re
from datetime import datetime
from flask_login import UserMixin


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    city = db.Column(db.String(140), nullable=False)
    country = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text)
    schedule = db.Column(db.String(140), nullable=False)
    salary = db.Column(db.String(40), nullable=False)
    contacts = db.Column(db.String(40), nullable=False)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(140))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_creator = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User id: {}, login: {}>'.format(self.id, self.login)
