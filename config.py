import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hn9LxldvTWbNNDE2cloOY7CX5on1UdW2Xed4QFaZmns'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost/auto_reply'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
