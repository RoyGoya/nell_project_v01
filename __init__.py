from flask import Flask

from flask_login import LoginManager, login_required

from .database import db_session
from .views.index_view import IndexView
from .views.users_view import RegisterView, ProfileView, LoginView, LogoutView
from .views.admin_view import AdminContentsView
from .models.users_model import User


app = Flask(__name__)

# http://flask.pocoo.org/docs/0.12/config/
app.config.from_object('taberu.config.DevelopmentConfig')
app.config.from_pyfile('settings.cfg')

# https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_email):
    user = User.query.filter_by(email=user_email).first()
    return user


# http://flask-sqlalchemy.pocoo.org/2.3/
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# http://flask.pocoo.org/docs/0.12/views/
logout_view = login_required(LogoutView.as_view(
    'logout_action', next_url='index_page'))
profile_view = login_required(ProfileView.as_view(
    'profile_page', template_name='users/profile.html'))

app.add_url_rule('/', view_func=IndexView.as_view(
    'index_page', template_name='index.html'))
app.add_url_rule('/register', view_func=RegisterView.as_view(
    'register_page', template_name='users/register.html'))
app.add_url_rule('/login', view_func=LoginView.as_view(
    'login_page', template_name='users/login.html'))
app.add_url_rule('/logout', view_func=logout_view)
app.add_url_rule('/profile', view_func=profile_view)

app.add_url_rule('/admin/contents', view_func=AdminContentsView.as_view(
    'admin_contents_page', template_name='admin/contents.html'))

if __name__ == '__main__':
    app.run()
