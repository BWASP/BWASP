from flask import (
    Flask, render_template
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Crawling.scouter import start


def create_app(config=None):
    app = Flask(__name__)

    from configs import DevelopmentsConfig, ProductionConfig
    if app.config['DEBUG']:
        config = DevelopmentsConfig()
    else:
        config = ProductionConfig()

    # config type
    app.config.from_object(config)

    # route initialization
    from routes import index_route, automation_route, common_route
    app.register_blueprint(index_route.bp)
    app.register_blueprint(automation_route.bp)
    app.register_blueprint(common_route.bp)

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('404.html'), 404

    return app


def AutomatedAnalysis(url, depth, options):
    start(url, int(depth), options)


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)