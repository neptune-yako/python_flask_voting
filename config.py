import os  # <-- 确保添加了这一行！
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+pymysql://root:123456@localhost:3306/voting_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False