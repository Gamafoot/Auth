from flask import Flask
from config import *
from Modules.Functions import *

from Blueprints.home import bp_home
from Blueprints.auth import bp_auth

#============================================================================
#========================== Default settings ================================
#============================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_SIZE

#============================================================================
#========================== Blueprint register ==============================
#============================================================================
app.register_blueprint(bp_home, url_prefix='/')
app.register_blueprint(bp_auth, url_prefix='/')

#============================================================================
#=============================== Run app ====================================
#============================================================================
if __name__ == '__main__':
    app.run(debug=True)