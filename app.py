from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from flask_migrate import Migrate

from flask_admin import Admin
from flask_login import LoginManager

from admin import MyModelView, MyAdminIndexView
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

babel = Babel(app)

from models import *

migrate = Migrate(app, db)

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Post, db.session))