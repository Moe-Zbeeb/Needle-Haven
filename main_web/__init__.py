import os
from flask import Flask
from flask_mail import Mail
from . import db
from . import auth

mail = Mail()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='12345678910',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        # Email configurations
        MAIL_SERVER='smtp.your-email-provider.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='your-email@example.com',
        MAIL_PASSWORD='your-email-password'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


    db.init_app(app)
    mail.init_app(app)  # Initialize Flask-Mail
    app.register_blueprint(auth.bp) 

    from . import blog
    app.register_blueprint(blog.bp)
    

    return app
