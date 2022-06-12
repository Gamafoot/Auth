from flask import Blueprint

bp_home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

from . import routes