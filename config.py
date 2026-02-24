import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-muy-segura'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/proyecto_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False