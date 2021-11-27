from flask import (
    Flask, render_template
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Crawling.scouter import start


def create_app(config=None):
    app = Flask(__name__)

    from configs import Developments_config, Production_config
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    # config type
    app.config.from_object(config)

    # route initialization
    from routes import index_route, common_route, automation_route, manual_route
    app.register_blueprint(index_route.bp)
    app.register_blueprint(common_route.bp)
    app.register_blueprint(automation_route.bp)
    app.register_blueprint(manual_route.bp)

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('404.html'), 404

    return app


def AutomatedAnalysis(url, depth, options):
    start(url, int(depth), options)


def ManualAnalysis(url, depth, options):
    pass


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20002, debug=True)

