from app import app
from app import db
import view

from posts.posts import posts
from auth.auth import auth
from contacts.contacts import contacts

app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(contacts, url_prefix='/contacts')

if __name__ == "__main__":
    app.run()
