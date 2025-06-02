from flask import Blueprint

bp = Blueprint('polls', __name__)
 
from app.polls import routes 