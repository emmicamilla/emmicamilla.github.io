import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-default-key")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ihc.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False