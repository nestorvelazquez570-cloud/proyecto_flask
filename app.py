from flask import Flask
from config import Config
from models.user import db
from routes.auth import auth_bp
from routes.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp)

    # Crear tablas si no existen (solo una vez)
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)