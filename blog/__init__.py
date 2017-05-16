import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig") 
# is this specifying a directory the blog part?
app.config.from_object(config_path)

from . import views
from . import filters

