import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # we can add production configurations here...

class TestingConfig(Config):
    TESTING = True
    # we caan add testing configurations here...