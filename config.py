# app/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/db'
    # Other configuration settings...

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost/test_db'
    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://prod_user:prod_password@localhost/prod_db'
