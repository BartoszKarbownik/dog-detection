from flask import Flask
from detection_app.extensions import db
from flasgger import Swagger
from flask_cors import CORS
import json
from detection_app.cleanup import start_cleanup_scheduler

swagger = Swagger()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    with open('detection_app/config.json') as config_file:
        config = json.load(config_file)
        app.config.update(config)

    db.init_app(app)
    swagger.init_app(app)
    
    with app.app_context():
        db.create_all()
        start_cleanup_scheduler()

    from detection_app.routes.auth_routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from detection_app.routes.main_routes import main_blueprint
    app.register_blueprint(main_blueprint)
    
    from detection_app.routes.camera_routes import camera_blueprint
    app.register_blueprint(camera_blueprint, url_prefix='/camera')
    
    @app.before_request
    def initialize():
        start_cleanup_scheduler()
    
    return app
