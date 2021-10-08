# Flask version 2.0.1
# Flask-SQLAlchemy version 2.5.1

from flask import (
    Flask, render_template, g
)
from .models.BWASP import db


def create_app(config=None):
    app = Flask(__name__)

    from .configs import DevelopmentsConfig, ProductionConfig
    config = DevelopmentsConfig()
    """
    if app.config['DEBUG']:
        config = DevelopmentsConfig()
    else:
        config = ProductionConfig()
    """

    # config type
    app.config.from_object(config)

    # route initialize
    from .routes import result_route, automation_route, common_route, api_route, test_route
    app.register_blueprint(result_route.bp)
    app.register_blueprint(automation_route.bp)
    app.register_blueprint(common_route.bp)
    app.register_blueprint(api_route.bp)
    app.register_blueprint(test_route.bp)

    db.init_app(app)

    @app.before_first_request
    def before_first_request():
        db.app = app
        db.create_all()

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('404.html'), 404

    @app.before_request
    def before_request():
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    return app
