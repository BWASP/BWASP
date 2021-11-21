from flask import (
    Flask
)
import sys, os
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def create_app(config=None):
    app = Flask(__name__)
    CORS(app, resource={r'/': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/': {"Access-Control-Allow-Credentials": True}})
    from configs import Developments_config, Production_config
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    # config type
    app.config.from_object(config)

    # route initialization
    from routes import manual
    app.register_blueprint(manual.bp)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20202, debug=True)
