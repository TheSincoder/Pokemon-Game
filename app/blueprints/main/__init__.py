from flask import Blueprint

bp = Blueprint('main',__name__,url_prefix='')
# now have to go around and change url_for's

from .import routes