from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from flask_mail import Mail, Message
# from config import mail_username, mail_password

# mail = Mail()
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():  # important when creating a flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "HelloThere"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USE_SSL'] = False
    # app.config['MAIL_USERNAME'] = mail_username
    # app.config['MAIL_PASSWORD'] = mail_password
    db.init_app(app)

    from .views import views
    from .authe import authe

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(authe, url_prefix="/")

    from .models import User, Post, Comment, Like

    login_manager = LoginManager()
    login_manager.login_view = "authe.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app


def create_database(app):
    if not path.exists("BLogSite/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

