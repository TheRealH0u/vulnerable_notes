from flask import Flask, render_template
from application.models import db
from application.util import getUsername

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_url_path='',
        static_folder='static'
    )
    app.config.from_object('application.config.Config')

    db.init_app(app)

    #* Create error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error='404 Not Found', message='The page you are looking for does not exist.'), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', error='403 Forbidden', message='You do not have permission to access this page.'), 403

    @app.errorhandler(400)
    def bad_request(error):
        return render_template('error.html', error='400 Bad Request', message='The request could not be understood or was missing required parameters.'), 400

    @app.errorhandler(Exception)
    def handle_error(error):
        message = error.description if hasattr(error, 'description') else ', '.join([str(x) for x in error.args])
        error_code = error.code if hasattr(error, 'code') else 500
        return render_template('error.html', error=f"{error_code} {error.__class__.__name__}", message=message), error_code

    
    #* Create context processors
    @app.context_processor
    def inject_username():
        return {'username': getUsername()}

    from application.blueprints.routes import web
    app.register_blueprint(web, url_prefix='/')

    return app
