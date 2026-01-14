from flask import Flask, jsonify
from application.models import db
from flask_cors import CORS
import os

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

    # For SQLite, ensure tables exist at startup
    try:
        if str(app.config.get('SQLALCHEMY_DATABASE_URI', '')).startswith('sqlite'):
            with app.app_context():
                db.create_all()
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
    # Allow both localhost and deployment URLs; prefer env override in production.
    env_origins = os.getenv('ALLOWED_ORIGINS')  # Comma-separated list for production
    if env_origins:
        allowed_origins = [o.strip() for o in env_origins.split(',') if o.strip()]
    else:
        allowed_origins = [
            # Local dev (Vite) and common localhost variants
            "http://localhost",
            "http://localhost:80",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1",
            "http://127.0.0.1:80",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            # Render (or other) frontend default/sample
            "https://vulnerable-notes-frontend.onrender.com",
            # Custom single override via env (legacy)
            os.getenv('FRONTEND_URL', 'http://localhost')
        ]
    
    CORS(app, 
         resources={r"/api/*": {"origins": allowed_origins}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    return app
