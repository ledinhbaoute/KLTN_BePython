import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:szHQAXGnGXZJEOBaJQmFKxuEbSxEgFYm@monorail.proxy.rlwy.net:27074/railway')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
