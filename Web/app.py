# Flask version 2.0.1
# Flask-SQLAlchemy version 2.5.1

from models.models import db
from flask import (
    Flask, render_template, g
)
from sqlalchemy.orm import sessionmaker


def create_app(config=None):
    app = Flask(__name__)

    from configs import DevelopmentsConfig
    config = DevelopmentsConfig()
    app.config.from_object(config)

    # route initialize
    from routes import result_route, automation_route, common_route, api_route
    app.register_blueprint(result_route.bp)
    app.register_blueprint(automation_route.bp)
    app.register_blueprint(common_route.bp)
    app.register_blueprint(api_route.bp)

    @app.before_first_request
    def before_first_request():
        db.init_app(app)
        db.app = app
        db.create_all()

    @app.before_request
    def before_request():
        db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

    @app.errorhandler(404)
    def NotFound(error):
        return render_template('404.html'), 404

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
