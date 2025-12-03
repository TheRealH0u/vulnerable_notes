from flask import Flask, jsonify
from application.models import db
from flask_cors import CORS

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_url_path='',
        static_folder='static'
    )
    app.config.from_object('application.config.Config')


    db.init_app(app)

    # API-only: register API blueprint
    try:
        from application.blueprints.api import api
        app.register_blueprint(api)
    except Exception:
        pass

    # JSON error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'not_found', 'message': 'The requested resource was not found.'}), 404

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'forbidden', 'message': 'You do not have permission to access this resource.'}), 403

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'bad_request', 'message': 'Bad request.'}), 400

    @app.errorhandler(Exception)
    def handle_error(error):
        message = error.description if hasattr(error, 'description') else ', '.join([str(x) for x in error.args])
        error_code = error.code if hasattr(error, 'code') else 500
        return jsonify({'error': 'server_error', 'message': message}), error_code

    # Enable Flask-CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
