# flask --app __init__ run --debug
# export FLASK_APP=__init__.py
# flask run
import os
from flask import Flask


def create_app(test_config=None):
    """Create and configure the application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    
    @app.route('/hello')
    def hello():
        """Return a friendly HTTP greeting"""
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/auth/login', endpoint='login')
    app.add_url_rule('/auth/logout', endpoint='logout')
    app.add_url_rule('/auth/register', endpoint='register')
    
    return app

