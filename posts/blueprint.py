from flask import Blueprint, flash
from flask import render_template
from flask import request

from flask import redirect
from flask import url_for

from flask_security import login_required

from models import Post
from posts.templates.forms import PostForm
from app import db

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/<slug>/edit_post', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form, title='Редактирование вакансии')


@posts.route('/<slug>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост был удален')
        return redirect(url_for('posts.index'))


@posts.route('/')
def index():
    query = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if query:
        post = Post.query.filter(Post.title.contains(query))
    else:
        post = Post.query.order_by(Post.created.desc())

    pages = post.paginate(page=page, per_page=5)

    return render_template('posts/index.html', title="Вакансии", pages=pages)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        city = request.form['city']
        country = request.form['country']
        schedule = request.form['schedule']
        salary = request.form['salary']
        contacts = request.form['contacts']

        try:
            post = Post(title=title, body=body, city=city, country=country, schedule=schedule, salary=salary,
                        contacts=contacts)
            db.session.add(post)
            db.session.commit()
        except:
            flash('Что-то пошло не так, попробуйте снова', 'danger')

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form, title='Создание вакансии')


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post, title=post.title)
