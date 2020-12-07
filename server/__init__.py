import os
import sys
from flask import Flask

def create_app(test_config=None):
    sys.path.append(os.getcwd())
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 's.sqlite'),
        UPLOAD_DIR=os.path.join(app.instance_path, 'uploaded')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/instance_path')
    def instance_path():
        return 'instance_path: ' + app.instance_path
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import nachos
    app.register_blueprint(nachos.bp)
    app.add_url_rule('/', endpoint='index')

    return app

