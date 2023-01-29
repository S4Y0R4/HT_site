import posts.blueprint
from app import app
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from models import Users

@app.route("/my-contacts")
def my_contacts():
    return render_template('my_contacts.html', title="Мои контакты")
