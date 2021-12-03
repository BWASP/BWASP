from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models.model_returnObj import bwasp_db
from models.model_returnObj import cve_db
from models.model_returnObj import task_db

print(bwasp_db)


def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

    # Config initialization
    from configs import Developments_config, Production_config
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    app.config.from_object(config)

    # Register routing for blueprint
    from apis import bp as api
    # from task_managements import manage
    app.register_blueprint(api)
    # app.register_blueprint(manage.bp)

    # App context initialization
    app.app_context().push()

    # DB initialize and migrate
    cve_db.init_app(app)
    cve_db.app = app

    task_db.init_app(app)
    task_db.app = app

    bwasp_db.init_app(app)
    bwasp_db.app = app

    print(bwasp_db)

    task_db.create_all(bind='TASK_MANAGER')

    @app.before_request
    def before_request():
        g.bwasp_db_obj = bwasp_db.session
        g.cve_db_obj = cve_db.session
        g.task_db_obj = task_db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'bwasp_db_obj'):
            g.bwasp_db_obj.close()

        if hasattr(g, 'cve_db_obj'):
            g.cve_db_obj.close()

        if hasattr(g, 'task_db_obj'):
            g.task_db_obj.close()

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20102, debug=True)
