from flask import (
    Flask, Blueprint, g
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def create_app(config=None):
    app = Flask(__name__)

    from configs import DevelopmentsConfig, ProductionConfig
    if app.config['DEBUG']:
        config = DevelopmentsConfig()
    else:
        config = ProductionConfig()

    # config type
    app.config.from_object(config)

    # routes initialization
    from routes import manual, crx
    app.register_blueprint(manual.bp)
    app.register_blueprint(crx.bp)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20202, debug=True)