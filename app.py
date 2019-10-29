#################
#### imports ####
#################

from flask import Flask
from flask_cors import CORS
from config import Config
import os

################
#### config ####
################

# Change jinja variable notation to support Vue app
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__, static_folder="./static", template_folder="./templates")  # This replaces your existing "app = Flask(__name__)"

with app.app_context():
    from logger import logger

# set environment variable
app.config['ENV'] = os.environ.get('DEPLOY_ENV')

####################
#### blueprints ####
####################

from dat_core.views import dat_core_blueprint
from map_core.views import map_core_blueprint
from sim_core.views import sim_core_blueprint
from shared.views import shared_blueprint
from home.views import home_blueprint
from api.api import api_blueprint


# register the blueprints
app.register_blueprint(map_core_blueprint)
app.register_blueprint(dat_core_blueprint)
app.register_blueprint(sim_core_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(shared_blueprint)


# don't cache static assets in jinja templates
if (os.environ.get('FLASK_ENV') == 'development'):
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.context_processor
def inject_osparc_url():
    return dict(osparc_url = Config.OSPARC_HOST)
