from flask import Flask
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_debug import Debug

from app.frontend import frontend, INPUT_FOLDER, OUTPUT_FOLDER
# from app import forms
# from app.nav import nav

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

AppConfig(app)

# Install our Bootstrap extension
Bootstrap(app)

# For debugging (there will be errors without it)
Debug(app)

# Our application uses blueprints as well; these go well with the
# application factory. We already imported the blueprint, now we just need
# to register it:
app.register_blueprint(frontend)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.secret_key = 'try_to_guess'

# We initialize the navigation as well
# nav.init_app(app)

