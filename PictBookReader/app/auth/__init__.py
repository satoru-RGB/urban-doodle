from flask import Blueprint

bp = Blueprint('auth', __name__) # [cite: 10]

from app.auth import routes
