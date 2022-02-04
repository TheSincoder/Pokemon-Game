from flask import Blueprint

bp = Blueprint('auth',__name__,url_prefix='/auth')
# now have to go around and change url_for's

from .import routes