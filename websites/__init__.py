from flask import Flask

app = Flask(__name__)

def create_app():
    app.config['SECRET_KEY'] = 'ASDASDAW'
    app.config['IMAGE_UPLOADS'] = "websites/static/img/uploads/"

    from .public_views import public_views
    from .admin_views import admin_views
    from .auth import auth

    app.register_blueprint(admin_views, url_prefix = '/')
    app.register_blueprint(public_views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    return app
