from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.owner_routes import owner_bp
    from app.routes.land_routes import land_bp
    from app.routes.crop_routes import crop_bp
    from app.routes.advanced_routes import advanced_bp
    from app.routes.mongo_log_routes import mongo_bp

    app.register_blueprint(owner_bp)
    app.register_blueprint(land_bp)
    app.register_blueprint(crop_bp)
    app.register_blueprint(advanced_bp)
    app.register_blueprint(mongo_bp)

    with app.app_context():
        db.create_all()

    return app
