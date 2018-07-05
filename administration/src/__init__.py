import os
from . import config
from flask import Flask, session

app = Flask(__name__)
app.debug = config.DEBUG_MODE
app.secret_key = config.SECRET_KEY

from models import models
# from views import views
import views
