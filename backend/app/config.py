import os

class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-fallback-key')
   SQLALCHEMY_DATABASE_URI = 'sqlite:///./database.db'
   
