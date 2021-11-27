from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask_migrate import Migrate, migrate, upgrade, merge
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


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

    # DATABASE API route initialization.
    from apis import bp as api
    app.register_blueprint(api)

    # DATABASE MANAGE API route initialization.
    from task_managements import manage
    app.register_blueprint(manage.bp)

    # App context initialization
    app.app_context().push()

    # Database initialization
    """
    cve_db.init_app(app)
    cve_db.app = app

    task_db.init_app(app)
    task_db.app = app
    """

    db.init_app(app)
    migrate.init_app(app, db)

    from models.BWASP import (
        packets,
        domain,
        job,
        ports,
        systeminfo,
        CSPEvaluator
    )
    from models.CVE import cve
    from models.TASK import task

    @app.before_request
    def before_request():
        # g object session initialization
        g.bwasp_db_obj = db.session
        g.cve_db_obj = db.session
        g.task_db_obj = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'bwasp_db_obj'):
            g.bwasp_db_obj.close()

        """
        if hasattr(g, 'cve_db_obj'):
            g.cve_db_obj.close()

        if hasattr(g, 'task_db_obj'):
            g.task_db_obj.close()
        """

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20102, debug=True)
