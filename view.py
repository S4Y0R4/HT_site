import posts.posts
from app import app
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from models import Users


@app.route("/")
def home():
    return redirect(url_for("posts.index"))
