from flask import Blueprint, flash
from flask import render_template
from flask import request

from flask import redirect
from flask import url_for

from flask_login import login_required

from models import Post
from posts.forms import PostForm
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
    query = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    count_items = db.session.query(Post).count()
    if query:
        post = Post.query.filter(Post.title.contains(query))
    else:
        post = Post.query.order_by(Post.created.desc())

    pages = post.paginate(page=page, per_page=5)

    return render_template('posts/index.html', title="Вакансии", pages=pages, count_items=count_items)


@posts.context_processor
def url_params():
    """
    Добавляет параметры поиска к ссылкам на другие страницы пагинации.
    """
    args = request.args.copy()
    args.pop('page', None)
    return dict(url_params=args)


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
            flash('Вы успешно доабвили новую запись', 'success')
        except:
            flash('Что-то пошло не так, попробуйте снова', 'danger')

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form, title='Создание вакансии')


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post, title=post.title)
