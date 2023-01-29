from app import app
from app import db
import view

from posts.blueprint import posts
from auth.blueprint import auth

app.register_blueprint(posts, url_prefix='/posts')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == "__main__":
    app.run()
