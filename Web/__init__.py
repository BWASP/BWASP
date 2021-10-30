# Flask version 2.0.1
# Flask-SQLAlchemy version 2.5.1

from flask import (
    Flask, render_template, g
)
from Crawling.scouter import start


def create_app(config=None):
    app = Flask(__name__)

    from .configs import DevelopmentsConfig, ProductionConfig
    if app.config['DEBUG']:
        config = DevelopmentsConfig()
    else:
        config = ProductionConfig()

    # config type
    app.config.from_object(config)

    # route initialization
    from .routes import index_route, automation_route, common_route
    app.register_blueprint(index_route.bp)
    app.register_blueprint(automation_route.bp)
    app.register_blueprint(common_route.bp)

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('404.html'), 404

    return app


def AutomatedAnalysis(url, depth, options):
    start(url, int(depth), options)
